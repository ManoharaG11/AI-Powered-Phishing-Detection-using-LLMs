# utils/model_utils.py
import os
import pickle
from typing import Dict
from utils.preprocess import clean_text
from utils.url_features import url_to_text_features, url_score_heuristic

def load_model_and_vectorizer(model_dir: str):
    model_path = os.path.join(model_dir, "phishing_model.pkl")
    vec_path = os.path.join(model_dir, "vectorizer.pkl")
    if not (os.path.exists(model_path) and os.path.exists(vec_path)):
        raise FileNotFoundError("Model or vectorizer not found in model/ — run train.py first.")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(vec_path, "rb") as f:
        vec = pickle.load(f)
    return model, vec


def predict_combined(model, vectorizer, email_text: str = "", url: str = "") -> Dict:
    """
    Predict using the vectorized text (email_text + url token features),
    then combine with URL heuristic score for final probability.
    Returns dict with label, probability, and details.
    """
    cleaned = clean_text(email_text)
    url_text_feats = url_to_text_features(url)
    combined_text = f"{cleaned} {url_text_feats}".strip()
    X = vectorizer.transform([combined_text])
    proba = 0.0
    try:
        proba = float(model.predict_proba(X)[:, 1][0])
    except Exception:
        # fallback to decision function if no predict_proba
        try:
            proba = (model.decision_function(X) - model.decision_function(X).min()) / (
                model.decision_function(X).ptp() + 1e-7)
            proba = float(proba[0])
        except Exception:
            proba = 0.5

    # combine with url heuristic
    url_score = url_score_heuristic(url)
    # weight: model 0.75, url heuristic 0.25
    final_score = 0.75 * proba + 0.25 * url_score
    label = "PHISHING" if final_score >= 0.5 else "SAFE"

    details = {
        "model_proba": proba,
        "url_heuristic": url_score,
        "final_score": final_score
    }

    return {"label": label, "probability": final_score, "details": details}
