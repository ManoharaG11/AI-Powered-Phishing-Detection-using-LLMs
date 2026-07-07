# train.py
"""
Train script for AI-Phishing-Detection
Outputs:
 - model/phishing_model.pkl
 - model/vectorizer.pkl
 - results/* (accuracy_report.txt, confusion_matrix.png, roc_curve.png, metrics.json)
"""
import os
import json
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, roc_curve, auc

from utils.preprocess import clean_text
from utils.url_features import url_to_text_features

ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT, "data")
MODEL_DIR = os.path.join(ROOT, "model")
RESULTS_DIR = os.path.join(ROOT, "results")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_dataset(path):
    df = pd.read_csv(path)
    # Ensure columns: 'email_text', 'url', 'label'
    df = df.fillna("")
    return df


def prepare_features(df):
    # Combine email_text and url-based textual features into a single string for TF-IDF
    texts = []
    for _, row in df.iterrows():
        email = clean_text(str(row.get("email_text", "")))
        url = str(row.get("url", ""))
        url_text_feats = url_to_text_features(url)
        combined = email + " " + url + " " + url_text_feats
        texts.append(combined)
    return texts


def main():
    csv_path = os.path.join(DATA_DIR, "phishing_dataset.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found. Place your CSV dataset in data/")

    df = load_dataset(csv_path)
    texts = prepare_features(df)
    labels = df["label"].apply(lambda x: 1 if str(x).lower() in ["phishing", "phish", "malicious", "spam"] else 0).values

    # Split data. For tiny/imbalanced datasets, sklearn stratify can fail.
    # We only stratify if both classes have enough samples for a split.
    unique, counts = np.unique(labels, return_counts=True)
    class_counts = dict(zip(unique.tolist(), counts.tolist()))

    can_stratify = (len(class_counts) == 2 and min(class_counts.values()) >= 2)

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            texts,
            labels,
            test_size=0.2,
            random_state=42,
            stratify=labels if can_stratify else None,
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            texts,
            labels,
            test_size=0.2,
            random_state=42,
            stratify=None,
        )


    # If still too small, train_test_split may produce empty splits.
    if len(X_train) == 0 or len(X_test) == 0:
        # last resort: train on all, create dummy test for metrics
        X_train, X_test = texts, texts
        y_train, y_test = labels, labels



    # Vectorize
    vec = TfidfVectorizer(max_features=20000, ngram_range=(1,2))
    X_train_vec = vec.fit_transform(X_train)
    X_test_vec = vec.transform(X_test)

    # Model training (Logistic Regression)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    # Predictions & metrics
    y_pred = model.predict(X_test_vec)
    y_prob = model.predict_proba(X_test_vec)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="binary")
    cm = confusion_matrix(y_test, y_pred)

    # Save model & vectorizer
    with open(os.path.join(MODEL_DIR, "phishing_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vec, f)

    metadata = {
        "accuracy": float(acc),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
    }
    with open(os.path.join(MODEL_DIR, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    # Save metrics to results
    with open(os.path.join(RESULTS_DIR, "accuracy_report.txt"), "w") as f:
        f.write(f"Accuracy: {acc:.4f}\nPrecision: {precision:.4f}\nRecall: {recall:.4f}\nF1: {f1:.4f}\n")

    with open(os.path.join(RESULTS_DIR, "metrics.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    # Confusion matrix plot
    plt.figure(figsize=(5,5))
    plt.imshow(cm, interpolation="nearest")
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    for (i, j), z in np.ndenumerate(cm):
        plt.text(j, i, str(z), ha='center', va='center', color='white')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "confusion_matrix.png"))
    plt.close()

    # ROC curve (only if both classes exist in y_test)
    if len(np.unique(y_test)) == 2:
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        plt.figure()
        plt.plot(fpr, tpr, lw=2)
        plt.plot([0, 1], [0, 1], linestyle='--')
        plt.title(f"ROC Curve (AUC = {roc_auc:.3f})")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.savefig(os.path.join(RESULTS_DIR, "roc_curve.png"))
        plt.close()
    else:
        # Avoid crashing on degenerate splits
        with open(os.path.join(RESULTS_DIR, "metrics.json"), "w", encoding="utf-8") as f:
            json.dump({**metadata, "roc": None, "note": "ROC skipped (y_test has a single class)"}, f, indent=2)


    print("Training complete. Results saved in results/ and model/.")


if __name__ == "__main__":
    main()
