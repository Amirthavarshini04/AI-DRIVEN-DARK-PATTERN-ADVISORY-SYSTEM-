import logging
from typing import Tuple, List, Dict, Any, Optional
from app.core.ssrf import validate_url_security, normalize_url

logger = logging.getLogger(__name__)

# Check Playwright availability
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

def is_playwright_available() -> bool:
    return PLAYWRIGHT_AVAILABLE

def fetch_page_with_browser(
    url: str,
    timeout_ms: int = 15000,
    wait_time_ms: int = 4000
) -> Tuple[bool, str, str, str, List[Dict[str, Any]], List[str]]:
    """
    Renders dynamic e-commerce page using headless Chromium.
    Enforces strict SSRF protection on all outgoing browser requests/subresources.
    
    Returns:
        (success: bool, status_msg: str, page_title: str, rendered_html: str, element_data: List[Dict], warnings: List[str])
    """
    if not PLAYWRIGHT_AVAILABLE:
        return False, "Playwright is not installed or available.", "", "", [], ["Headless browser not available; falling back to HTTP client."]

    normalized_url = normalize_url(url)
    is_safe, msg = validate_url_security(normalized_url)
    if not is_safe:
        return False, f"SSRF Security Violation: {msg}", "", "", [], []

    warnings: List[str] = []
    element_data: List[Dict[str, Any]] = []
    rendered_html = ""
    page_title = ""

    playwright = None
    browser = None
    context = None
    page = None

    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-IN",
            ignore_https_errors=False
        )
        page = context.new_page()

        # SSRF Protection: Intercept every browser request and validate target destination
        def handle_route(route):
            req_url = route.request.url
            # Allow data: and blob: URLs
            if req_url.startswith("data:") or req_url.startswith("blob:"):
                route.continue_()
                return

            safe, _ = validate_url_security(req_url)
            if not safe:
                warnings.append(f"Blocked SSRF-restricted subresource navigation: {req_url[:80]}")
                route.abort("accessdenied")
            else:
                route.continue_()

        page.route("**/*", handle_route)

        # Navigate with strict timeout
        response = page.goto(
            normalized_url,
            wait_until="domcontentloaded",
            timeout=timeout_ms
        )

        if response and response.status >= 400:
            status_code = response.status
            if status_code in (401, 403):
                warnings.append(f"HTTP {status_code} received: site may have bot challenge or access controls.")
            elif status_code == 404:
                return False, f"Target page not found (HTTP 404).", "", "", [], warnings

        # Wait briefly for client-side JavaScript (countdowns, timers, banners) to mount
        try:
            page.wait_for_timeout(wait_time_ms)
        except Exception:
            pass

        page_title = page.title() or ""
        rendered_html = page.content() or ""

        # Extract structured visible elements directly from live DOM
        try:
            elements_script = """
            () => {
                const results = [];
                const selectors = [
                    'h1', 'h2', 'h3', 'h4', 'p', 'span', 'button', 'a', 
                    '[role="button"]', '.banner', '.modal', '.popup', '.alert',
                    '.countdown', '.timer', '.badge', '.price', '.urgency',
                    'input[type="checkbox"]'
                ];
                
                document.querySelectorAll(selectors.join(', ')).forEach((el, index) => {
                    if (results.length > 200) return;
                    const rect = el.getBoundingClientRect();
                    const isVisible = rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none';
                    if (!isVisible && el.tagName !== 'INPUT') return;
                    
                    const text = (el.innerText || el.textContent || '').trim();
                    let selector = el.tagName.toLowerCase();
                    if (el.id) {
                        selector += '#' + el.id;
                    } else if (el.className && typeof el.className === 'string') {
                        const firstClass = el.className.trim().split(/\s+/)[0];
                        if (firstClass && !firstClass.includes(':')) selector += '.' + firstClass;
                    }
                    
                    const isChecked = el.tagName === 'INPUT' && el.type === 'checkbox' ? el.checked : false;
                    
                    if (text.length >= 3 || el.tagName === 'INPUT') {
                        results.push({
                            tag: el.tagName.toLowerCase(),
                            selector: selector,
                            text: text,
                            is_checked: isChecked,
                            classes: typeof el.className === 'string' ? el.className : ''
                        });
                    }
                });
                return results;
            }
            """
            element_data = page.evaluate(elements_script)
        except Exception as e:
            warnings.append(f"DOM element extraction warning: {str(e)}")

        return True, "Rendered successfully via headless browser.", page_title, rendered_html, element_data, warnings

    except PlaywrightTimeoutError:
        return False, f"Page load timed out after {timeout_ms // 1000} seconds.", "", "", [], warnings
    except Exception as e:
        err_msg = str(e)
        logger.warning(f"Headless browser error on {normalized_url}: {err_msg}")
        return False, f"Browser rendering failed: {err_msg}", "", "", [], warnings
    finally:
        if page:
            try:
                page.close()
            except Exception:
                pass
        if context:
            try:
                context.close()
            except Exception:
                pass
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        if playwright:
            try:
                playwright.stop()
            except Exception:
                pass
