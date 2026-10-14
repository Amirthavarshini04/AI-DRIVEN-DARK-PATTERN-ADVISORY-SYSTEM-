from app.detection.classifier import analyze_text_content, detect_language

def test_language_detection():
    assert detect_language("Hurry! Only 2 items left") == "en"
    assert detect_language("மின்னல் விற்பனை! இன்னும் 2 நிமிடங்கள் மட்டுமே!") == "ta"
    assert detect_language("केवल 3 स्टॉक में बचे हैं! तुरंत खरीदें!") == "hi"

def test_false_urgency_english():
    text = "Hurry! Only 2 items left in stock - Offer expires in 03m 12s!"
    findings = analyze_text_content(text, "en")
    assert len(findings) > 0
    assert findings[0]["category"] == "False Urgency"
    assert findings[0]["severity"] == "High"

def test_confirm_shaming_hindi():
    text = "नहीं, मुझे पैसे बचाना पसंद नहीं है"
    findings = analyze_text_content(text, "hi")
    assert len(findings) > 0
    assert findings[0]["category"] == "Confirm Shaming"

def test_false_urgency_tamil():
    text = "மின்னல் விற்பனை! இன்னும் 2 நிமிடங்கள் மட்டுமே!"
    findings = analyze_text_content(text, "ta")
    assert len(findings) > 0
    assert findings[0]["category"] == "False Urgency"
