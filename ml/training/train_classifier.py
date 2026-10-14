import json
import os
import glob
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def load_all_dataset_samples():
    samples = []
    base_dir = os.path.join(os.path.dirname(__file__), "../../dataset/samples")
    for filepath in glob.glob(os.path.join(base_dir, "*.json")):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            samples.extend(data)
    return samples

def train_and_save_classifier():
    samples = load_all_dataset_samples()
    if not samples:
        print("No dataset samples found to train classifier.")
        return

    X = [s["text_snippet"] for s in samples]
    y = [s["dark_pattern_category"] for s in samples]

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ('clf', LogisticRegression(random_state=42))
    ])

    pipeline.fit(X, y)
    preds = pipeline.predict(X)
    
    print("=== Multilingual Classifier Training Evaluation ===")
    print(classification_report(y, preds, zero_division=0))

    checkpoint_path = os.path.join(os.path.dirname(__file__), "../checkpoints/multilingual_classifier.joblib")
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    joblib.dump(pipeline, checkpoint_path)
    print(f"Model successfully trained and saved to: {checkpoint_path}")

if __name__ == "__main__":
    train_and_save_classifier()
