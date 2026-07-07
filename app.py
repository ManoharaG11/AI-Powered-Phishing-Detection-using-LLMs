# app.py
"""
Main Flask app for AI-Phishing-Detection
Run: python app.py
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash

from dotenv import load_dotenv

# utils
from utils.model_utils import load_model_and_vectorizer, predict_combined
from utils.sender_check import analyze_sender
from utils.ip_lookup import lookup_ip_info

load_dotenv()

APP = Flask(__name__)
APP.secret_key = os.getenv("FLASK_SECRET", "supersecretkey")

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")

# Load model files lazily/robustly so the server can still start even if training wasn't run yet.
try:
    MODEL, VECT = load_model_and_vectorizer(MODEL_DIR)
except FileNotFoundError:
    MODEL, VECT = None, None



@APP.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@APP.route("/fake-email", methods=["GET"])
def fake_email():
    return render_template("fake_email.html")


@APP.route("/fake-website", methods=["GET"])
def fake_website():
    return render_template("fake_website.html")



@APP.route("/analyze", methods=["POST"])
def analyze():
    try:

        email_text = request.form.get("email_text", "").strip()
        url = request.form.get("url", "").strip()
        sender = request.form.get("sender", "").strip()
        raw_header = request.form.get("raw_header", "").strip()

        if MODEL is None or VECT is None:
            flash("Model not found. Please run train.py first.", "danger")
            return redirect(url_for("index"))

        # get model prediction
        result = predict_combined(MODEL, VECT, email_text=email_text, url=url)


        # sender analysis (checks blacklist, mx, and extracts IPs from header)
        sender_report = analyze_sender(sender, raw_header)

        # if we have an IP extracted, try to get geolocation
        ip_info = None
        if sender_report.get("extracted_ip"):
            ip_info = lookup_ip_info(sender_report["extracted_ip"])

        # combine response
        response = {
            "classification": result["label"],
            "probability": result["probability"],
            "details": result["details"],
            "sender_report": sender_report,
            "ip_info": ip_info,
        }

        return render_template("results.html", response=response, email_text=email_text, url=url, sender=sender)


    except Exception as e:
        flash(f"Error during analysis: {e}", "danger")
        return redirect(url_for("index"))


if __name__ == "__main__":
    APP.run(debug=True)
