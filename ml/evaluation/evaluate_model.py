import json
from app.detection.classifier import analyze_text_content

def run_evaluation_suite():
    print("=========================================================")
    print(" MULTILINGUAL DARK PATTERN DETECTION EVALUATION BENCHMARK")
    print("=========================================================")

    test_cases = [
        {"lang": "en", "text": "Hurry! Only 2 items left in stock - Offer expires in 03m 12s!", "expected": "False Urgency"},
        {"lang": "en", "text": "Convenience fee ₹49 added automatically at final checkout", "expected": "Drip Pricing"},
        {"lang": "en", "text": "No thanks, I prefer paying full price and losing savings", "expected": "Confirm Shaming"},
        {"lang": "hi", "text": "केवल 3 स्टॉक में बचे हैं! तुरंत खरीदें!", "expected": "False Urgency"},
        {"lang": "hi", "text": "नहीं, मुझे पैसे बचाना पसंद नहीं है", "expected": "Confirm Shaming"},
        {"lang": "ta", "text": "மின்னல் விற்பனை! இன்னும் 2 நிமிடங்கள் மட்டுமே!", "expected": "False Urgency"},
        {"lang": "ta", "text": "இல்லை, எனக்கு தள்ளுபடி தேவையில்லை", "expected": "Confirm Shaming"}
    ]

    passed = 0
    total = len(test_cases)

    for idx, tc in enumerate(test_cases, 1):
        findings = analyze_text_content(tc["text"], target_language=tc["lang"])
        cat = findings[0]["category"] if findings else "None"
        is_pass = cat == tc["expected"]
        if is_pass:
            passed += 1
        status_str = "PASS [✓]" if is_pass else f"FAIL [✗] (Got: {cat})"
        print(f"Test {idx}/{total} [{tc['lang'].upper()}]: {status_str} - Text: \"{tc['text'][:40]}...\"")

    accuracy = (passed / total) * 100
    print("\n---------------------------------------------------------")
    print(f"Overall Benchmark Accuracy: {accuracy:.1f}% ({passed}/{total} Passed)")
    print("---------------------------------------------------------")

if __name__ == "__main__":
    run_evaluation_suite()
