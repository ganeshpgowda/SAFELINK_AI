"""SafeLink AI - Machine Learning Model Trainer.

Trains a Scikit-Learn RandomForestClassifier on extracted URL features,
evaluates precision, recall, F1, and ROC-AUC, and serializes the trained model artifact.
"""

import sys
from pathlib import Path
from datetime import datetime
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.config import DATASET_PATH, MODEL_PATH, MODELS_DIR
from backend.feature_extractor import FEATURE_COLUMNS
from backend.training.dataset_generator import build_dataset


def train_model():
    """Builds/loads the dataset, trains the Random Forest classifier,
    evaluates performance, and saves the serialized model package.
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Check if dataset CSV exists, else generate it
    if not DATASET_PATH.exists():
        print(f"Dataset not found at {DATASET_PATH}. Generating synthetic & curated dataset...")
        df = build_dataset()
        df.to_csv(DATASET_PATH, index=False)
    else:
        print(f"Loading existing dataset from {DATASET_PATH}...")
        df = pd.read_csv(DATASET_PATH)

    print(f"Dataset Shape: {df.shape}")
    print(f"Class Distribution:\n{df['is_fraud'].value_counts(normalize=True)}")

    # Extract feature matrix X and label vector y
    X = df[FEATURE_COLUMNS]
    y = df["is_fraud"]

    # Stratified Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Training set: {X_train.shape[0]} samples | Test set: {X_test.shape[0]} samples")

    # Initialize Random Forest Classifier
    rf = RandomForestClassifier(
        n_estimators=150,
        max_depth=16,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    print("Training Random Forest Classifier...")
    rf.fit(X_train, y_train)

    # Cross-validation
    print("Running 5-fold cross-validation...")
    cv_scores = cross_val_score(rf, X_train, y_train, cv=5, scoring="roc_auc")
    print(f"5-Fold CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # Evaluation on Held-Out Test Set
    y_pred = rf.predict(X_test)
    y_pred_proba = rf.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    conf_mat = confusion_matrix(y_test, y_pred).tolist()

    print("\n" + "="*50)
    print("      SAFELINK AI - MODEL EVALUATION RESULTS      ")
    print("="*50)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print("\nConfusion Matrix:")
    print(f"[[TN={conf_mat[0][0]}, FP={conf_mat[0][1]}], [FN={conf_mat[1][0]}, TP={conf_mat[1][1]}]]")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate (0)", "Fraudulent (1)"]))

    # Feature Importances
    importances = rf.feature_importances_
    feature_importance_dict = {
        col: round(float(imp), 4)
        for col, imp in sorted(zip(FEATURE_COLUMNS, importances), key=lambda x: x[1], reverse=True)
    }

    print("\nTop 10 Most Predictive URL Features:")
    for i, (col, imp) in enumerate(list(feature_importance_dict.items())[:10], start=1):
        print(f"  {i}. {col:<26}: {imp*100:.2f}%")

    # Package Artifact
    artifact = {
        "model": rf,
        "feature_columns": FEATURE_COLUMNS,
        "metrics": {
            "accuracy": round(float(accuracy), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(roc_auc), 4),
            "cv_roc_auc_mean": round(float(cv_scores.mean()), 4),
            "confusion_matrix": conf_mat,
        },
        "feature_importances": feature_importance_dict,
        "trained_at": datetime.now().isoformat(),
        "model_type": "RandomForestClassifier",
        "dataset_size": len(df),
        "version": "1.0.0"
    }

    joblib.dump(artifact, MODEL_PATH)
    print(f"\nModel artifact successfully saved to: {MODEL_PATH}")
    return artifact


if __name__ == "__main__":
    train_model()

