import os
import json
import numpy as np
from sklearn.linear_model import Ridge
import joblib

def train_learned_risk_model():
    """
    Trains a learned linear regression model to predict page-level compliance risk score
    from category presence vectors and severity counts.
    """
    # Synthetic page-level feature matrices for baseline training
    # Features: [num_critical, num_high, num_medium, num_low, has_false_urgency, has_drip_pricing, co_occurrence_flag]
    X_train = np.array([
        [0, 0, 0, 0, 0, 0, 0], # clean page -> risk 0
        [1, 0, 0, 0, 0, 1, 0], # drip pricing -> risk 40
        [0, 1, 0, 0, 1, 0, 0], # false urgency -> risk 30
        [1, 1, 0, 0, 1, 1, 1], # urgency + drip pricing co-occurrence -> risk 75
        [2, 1, 1, 0, 1, 1, 1], # critical multi-pattern -> risk 90
    ])
    
    y_train = np.array([0.0, 40.0, 30.0, 75.0, 90.0])

    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    checkpoint_path = os.path.join(os.path.dirname(__file__), "../checkpoints/learned_risk_model.joblib")
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    joblib.dump(model, checkpoint_path)
    print(f"Learned Combined-Risk Model saved successfully to: {checkpoint_path}")

if __name__ == "__main__":
    train_learned_risk_model()
