import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from app.core.ssrf import validate_url_security, normalize_url, safe_fetch_url
from app.detection.content_extractor import extract_structured_page_content
from app.detection.classifier import analyze_text_content, analyze_structured_elements
from app.risk_scoring.combined_risk_model import calculate_combined_risk_score

client = TestClient(app)

# ==============================================================================
# 1. Page with urgency messages
# ==============================================================================
def test_1_page_with_urgency_messages():
    urgency_html = """
    <!DOCTYPE html>
    <html>
      <head><title>Urgent Sale - Quick Shop</title></head>
      <body>
        <h1>Special Electronics Store</h1>
        <div class="banner-urgency">
          <span>Hurry! Offer expires in 04m 12s!</span>
        </div>
        <div class="stock-badge">Only 2 left in stock</div>
        <button class="btn-buy">Buy Now</button>
      </body>
    </html>
    """
    with patch("app.api.v1.scans.validate_url_security", return_value=(True, "Validated")), \
         patch("app.api.v1.scans.is_playwright_available", return_value=False), \
         patch("app.api.v1.scans.safe_fetch_url", return_value=(True, "Fetched successfully.", urgency_html, [])):
        response = client.post("/api/v1/scans/url", json={"url": "https://example-shop.com/product/1"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("completed", "partially_scanned")
        assert data["risk_score"] > 0
        assert data["findings_count"] >= 1
        categories = [f["category"] for f in data["findings"]]
        assert "False Urgency" in categories
        for f in data["findings"]:
            if f["category"] == "False Urgency":
                assert "CCPA" in f["ccpa_clause"] or "Clause" in f["ccpa_clause"] or "Annexure" in f["ccpa_clause"]

# ==============================================================================
# 2. Page with scarcity claims
# ==============================================================================
def test_2_page_with_scarcity_claims():
    scarcity_html = """
    <html>
      <head><title>Fashion Hub</title></head>
      <body>
        <h2>Designer Shoes</h2>
        <p class="scarcity-text">Limited stock available - fast selling item!</p>
        <div class="social-proof">45 people are looking at this right now</div>
      </body>
    </html>
    """
    with patch("app.api.v1.scans.validate_url_security", return_value=(True, "Validated")), \
         patch("app.api.v1.scans.is_playwright_available", return_value=False), \
         patch("app.api.v1.scans.safe_fetch_url", return_value=(True, "Fetched successfully.", scarcity_html, [])):
        response = client.post("/api/v1/scans/url", json={"url": "https://example-fashion.com/shoes"})
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] > 0
        categories = [f["category"] for f in data["findings"]]
        assert any(c in ("False Urgency", "Deceptive Counting") for c in categories)

# ==============================================================================
# 3. Page containing subscription-related manipulation
# ==============================================================================
def test_3_page_with_subscription_manipulation():
    sub_html = """
    <html>
      <head><title>Cloud Streaming VIP</title></head>
      <body>
        <h1>Subscription Checkout</h1>
        <p>Enrol now for premium digital access.</p>
        <div class="terms-obscured">
          Cancellation policy: cancel subscription requires phone call to customer service. Cannot cancel online.
        </div>
      </body>
    </html>
    """
    with patch("app.api.v1.scans.validate_url_security", return_value=(True, "Validated")), \
         patch("app.api.v1.scans.is_playwright_available", return_value=False), \
         patch("app.api.v1.scans.safe_fetch_url", return_value=(True, "Fetched successfully.", sub_html, [])):
        response = client.post("/api/v1/scans/url", json={"url": "https://streaming-service.com/checkout"})
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] > 0
        categories = [f["category"] for f in data["findings"]]
        assert "Subscription Trap" in categories

# ==============================================================================
# 4. Normal page without obvious dark pattern indicators
# ==============================================================================
def test_4_normal_page_without_dark_patterns():
    normal_html = """
    <html>
      <head><title>Organic Cotton Apparel</title></head>
      <body>
        <h1>100% Organic Cotton T-Shirt</h1>
        <p>Manufactured using sustainable natural dyes and fair trade cotton practices.</p>
        <p>Available sizes: Small, Medium, Large, Extra Large.</p>
        <div class="specifications">Machine wash warm with similar colours. Tumble dry medium.</div>
        <div class="price">Price: ₹899 inclusive of all taxes. Free standard delivery on all orders.</div>
        <button class="add-to-cart">Add to Cart</button>
      </body>
    </html>
    """
    with patch("app.api.v1.scans.validate_url_security", return_value=(True, "Validated")), \
         patch("app.api.v1.scans.is_playwright_available", return_value=False), \
         patch("app.api.v1.scans.safe_fetch_url", return_value=(True, "Fetched successfully.", normal_html, [])):
        response = client.post("/api/v1/scans/url", json={"url": "https://fairtrade-cotton.in/tshirt"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["risk_score"] <= 15.0
        assert data["findings_count"] == 0
        assert data["content_length_analyzed"] > 100

# ==============================================================================
# 5. Empty page (Insufficient content handling)
# ==============================================================================
def test_5_empty_page_insufficient_content():
    empty_html = "<html><head></head><body>    </body></html>"
    with patch("app.api.v1.scans.validate_url_security", return_value=(True, "Validated")), \
         patch("app.api.v1.scans.is_playwright_available", return_value=False), \
         patch("app.api.v1.scans.safe_fetch_url", return_value=(True, "Fetched successfully.", empty_html, [])):
        response = client.post("/api/v1/scans/url", json={"url": "https://empty-shell-store.com/"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "insufficient_content"
        assert len(data["warnings"]) > 0

# ==============================================================================
# 6. Malformed URL
# ==============================================================================
def test_6_malformed_url_rejection():
    # Disallowed scheme
    res1 = client.post("/api/v1/scans/url", json={"url": "ftp://files.example.com/item"})
    assert res1.status_code == 400
    assert "Disallowed URL scheme" in res1.json()["detail"]

    # Non-resolvable or invalid scheme string
    res2 = client.post("/api/v1/scans/url", json={"url": "javascript:alert(1)"})
    assert res2.status_code == 400

# ==============================================================================
# 7. Unreachable website
# ==============================================================================
def test_7_unreachable_website():
    # Domain that cannot be resolved
    response = client.post("/api/v1/scans/url", json={"url": "https://this-domain-does-not-exist-at-all-xyz98765.com"})
    assert response.status_code == 400
    assert "DNS failure" in response.json()["detail"] or "Could not resolve" in response.json()["detail"]

# ==============================================================================
# 8. HTTP error response
# ==============================================================================
def test_8_http_error_response():
    with patch("app.api.v1.scans.validate_url_security", return_value=(True, "Validated")), \
         patch("app.api.v1.scans.is_playwright_available", return_value=False), \
         patch("app.api.v1.scans.safe_fetch_url", return_value=(False, "HTTP Error 404 while fetching target URL.", "", [])):
        response = client.post("/api/v1/scans/url", json={"url": "https://example.com/non-existent-page"})
        assert response.status_code == 400
        assert "HTTP Error 404" in response.json()["detail"]

# ==============================================================================
# 9. Page with JavaScript-rendered text (Headless Browser)
# ==============================================================================
def test_9_javascript_rendered_page():
    js_rendered_html = """
    <html>
      <head><title>Dynamic React Store</title></head>
      <body>
        <div id="root">
          <div class="flash-sale-badge">Hurry! Ends in 02m 45s</div>
          <p>Product: Wireless Earbuds Pro</p>
          <div class="cart-sneak">Insurance added to cart automatically</div>
        </div>
      </body>
    </html>
    """
    element_data = [
        {"tag": "div", "selector": ".flash-sale-badge", "text": "Hurry! Ends in 02m 45s", "is_checked": False},
        {"tag": "div", "selector": ".cart-sneak", "text": "Insurance added to cart automatically", "is_checked": False}
    ]
    with patch("app.api.v1.scans.validate_url_security", return_value=(True, "Validated")), \
         patch("app.api.v1.scans.is_playwright_available", return_value=True), \
         patch("app.api.v1.scans.fetch_page_with_browser", return_value=(True, "Rendered successfully via headless browser.", "Dynamic React Store", js_rendered_html, element_data, [])):
        response = client.post("/api/v1/scans/url", json={"url": "https://dynamic-react-shop.in/cart"})
        assert response.status_code == 200
        data = response.json()
        assert data["fetch_method"] == "browser_headless"
        assert data["risk_score"] > 0
        categories = [f["category"] for f in data["findings"]]
        assert "False Urgency" in categories or "Basket Sneaking" in categories

# ==============================================================================
# 10. Page that redirects to a restricted address (SSRF Protection)
# ==============================================================================
def test_10_redirect_to_restricted_address_ssrf():
    # Direct access to loopback / AWS metadata is blocked
    is_safe, msg = validate_url_security("http://127.0.0.1:8000/api/v1/health")
    assert not is_safe
    assert "SSRF" in msg or "private" in msg or "restricted" in msg

    is_safe_aws, aws_msg = validate_url_security("http://169.254.169.254/latest/meta-data/")
    assert not is_safe_aws

    # Testing API endpoint directly with SSRF target
    response = client.post("/api/v1/scans/url", json={"url": "http://127.0.0.1:8000/api/v1/health"})
    assert response.status_code == 400
    assert "SSRF" in response.json()["detail"] or "private" in response.json()["detail"] or "restricted" in response.json()["detail"]
