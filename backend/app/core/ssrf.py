import os
import socket
import ipaddress
import re
from urllib.parse import urlparse, urlunparse, urljoin
from typing import Tuple, List, Optional
import requests

# Inject OS trust store so Windows Root CAs are recognized without SSLError
try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

BLOCKED_IP_NETWORKS = [
    ipaddress.ip_network('127.0.0.0/8'),        # Loopback
    ipaddress.ip_network('10.0.0.0/8'),         # Private class A
    ipaddress.ip_network('172.16.0.0/12'),      # Private class B
    ipaddress.ip_network('192.168.0.0/16'),     # Private class C
    ipaddress.ip_network('169.254.0.0/16'),     # Link-local / AWS & cloud metadata
    ipaddress.ip_network('0.0.0.0/8'),          # Current network
    ipaddress.ip_network('::1/128'),            # IPv6 Loopback
    ipaddress.ip_network('fc00::/7'),           # IPv6 Unique Local
    ipaddress.ip_network('fe80::/10'),          # IPv6 Link-local
]

BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "metadata",
    "instance-data",
    "169.254.169.254"
}

MAX_CONTENT_BYTES = 5 * 1024 * 1024  # 5 MB
DEFAULT_TIMEOUT_SEC = 12
MAX_REDIRECTS = 5

DEFAULT_BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8,ta;q=0.7',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
}

def normalize_url(raw_url: str) -> str:
    """Safely normalizes input URL, adding https:// if protocol is omitted."""
    raw = (raw_url or "").strip()
    if not raw:
        return ""
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', raw):
        raw = f"https://{raw}"
    parsed = urlparse(raw)
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return normalized

def is_ip_allowed(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        for net in BLOCKED_IP_NETWORKS:
            if ip in net:
                return False
        return True
    except ValueError:
        return False

AUTHORIZED_DEMO_PATHS = {"/demo/high-risk-store"}

def _allow_localhost() -> bool:
    """Returns True when ALLOW_LOCALHOST env var is set (test environments only)."""
    return os.environ.get("ALLOW_LOCALHOST", "").strip() not in ("", "0", "false", "no")

def is_authorized_demo_url(url: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.hostname in ("127.0.0.1", "localhost") and
        parsed.port in (8000, None) and
        parsed.path in AUTHORIZED_DEMO_PATHS
    )

def validate_url_security(url: str) -> Tuple[bool, str]:
    if not url:
        return False, "URL is empty."

    if is_authorized_demo_url(url):
        return True, "Authorized project demo benchmark URL."

    # Allow localhost/loopback if ALLOW_LOCALHOST env flag is set (test environments only)
    if _allow_localhost():
        parsed_tmp = urlparse(url)
        if parsed_tmp.hostname in ("127.0.0.1", "localhost", "::1"):
            if parsed_tmp.scheme in ('http', 'https'):
                return True, "Localhost allowed via ALLOW_LOCALHOST env flag (test mode)."

    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False, f"Disallowed URL scheme: '{parsed.scheme}'. Only HTTP and HTTPS are permitted."

    hostname = parsed.hostname
    if not hostname:
        return False, "Invalid URL structure (missing hostname)."

    if hostname.lower() in BLOCKED_HOSTNAMES:
        return False, f"Blocked target hostname: '{hostname}' (SSRF protection)."

    # Reject numerical IP patterns that could resolve to local addresses
    try:
        addresses = socket.getaddrinfo(hostname, None)
        if not addresses:
            return False, f"Could not resolve hostname '{hostname}'."
        for addr in addresses:
            ip_str = addr[4][0]
            if not is_ip_allowed(ip_str):
                return False, f"SSRF Protection: Hostname '{hostname}' resolved to private/restricted IP ({ip_str})."
    except socket.gaierror:
        return False, f"Could not resolve hostname '{hostname}' (DNS failure)."
    except Exception as e:
        return False, f"Network security validation error: {str(e)}"

    return True, "URL validated successfully."

def safe_fetch_url(
    url: str,
    timeout: int = DEFAULT_TIMEOUT_SEC
) -> Tuple[bool, str, str, List[str]]:
    """
    Safely fetches URL content with SSRF checks on initial URL and all redirect hops.
    Returns: (success: bool, status_or_error_msg: str, html_content: str, warnings: List[str])
    """
    normalized_url = normalize_url(url)
    is_safe, msg = validate_url_security(normalized_url)
    if not is_safe:
        return False, msg, "", []

    warnings: List[str] = []
    current_url = normalized_url
    session = requests.Session()

    for redirect_idx in range(MAX_REDIRECTS + 1):
        try:
            response = session.get(
                current_url,
                headers=DEFAULT_BROWSER_HEADERS,
                timeout=timeout,
                allow_redirects=False,
                stream=True
            )

            # Check for redirect status
            if response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get('Location')
                if not location:
                    return False, f"HTTP {response.status_code} redirect missing Location header.", "", warnings
                
                next_url = urljoin(current_url, location)
                next_safe, next_msg = validate_url_security(next_url)
                if not next_safe:
                    return False, f"SSRF Protection: Redirect target blocked ({next_msg})", "", warnings
                
                warnings.append(f"Redirected from {current_url} to {next_url}")
                current_url = next_url
                continue

            # Check HTTP Status Code
            if response.status_code == 403:
                return False, "HTTP 403 Forbidden: Target server rejected the request or requires bot verification/login.", "", warnings
            if response.status_code == 429:
                return False, "HTTP 429 Rate Limited: Target server rate limit encountered.", "", warnings
            if response.status_code >= 400:
                return False, f"HTTP Error {response.status_code} while fetching target URL.", "", warnings

            content_type = response.headers.get('Content-Type', '').lower()
            if content_type and not any(ct in content_type for ct in ['text/html', 'application/xhtml+xml', 'text/plain']):
                warnings.append(f"Non-HTML content type: {content_type}")

            # Read content with strict size cap
            chunks = []
            total_bytes = 0
            for chunk in response.iter_content(chunk_size=16384):
                total_bytes += len(chunk)
                if total_bytes > MAX_CONTENT_BYTES:
                    warnings.append(f"Response truncated at {MAX_CONTENT_BYTES // (1024 * 1024)} MB limit")
                    break
                chunks.append(chunk)

            raw_bytes = b"".join(chunks)
            encoding = response.encoding or response.apparent_encoding or 'utf-8'
            try:
                html_text = raw_bytes.decode(encoding, errors='replace')
            except Exception:
                html_text = raw_bytes.decode('utf-8', errors='replace')

            # Detect Bot Challenge / Cloudflare / CAPTCHA blocks
            if "Just a moment..." in html_text and "Cloudflare" in html_text:
                warnings.append("Cloudflare verification challenge detected in page response.")
            if "captcha" in html_text.lower() and len(html_text) < 5000:
                warnings.append("Potential automated CAPTCHA gate detected on target site.")

            return True, "Fetched successfully.", html_text, warnings

        except requests.Timeout:
            return False, f"Request timed out after {timeout} seconds.", "", warnings
        except requests.RequestException as e:
            return False, f"Network request error: {str(e)}", "", warnings
        except Exception as e:
            return False, f"Unexpected fetch error: {str(e)}", "", warnings

    return False, f"Exceeded maximum redirect limit ({MAX_REDIRECTS}).", "", warnings
