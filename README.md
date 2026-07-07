# 🧠 AI-Powered Phishing Detection (Flask + ML)

A hybrid cybersecurity system that detects:
- **Phishing emails** (email body text)
- **Malicious/fake websites** (URL features)
- **Suspicious senders** (basic sender checks + blacklist)
- **IP extraction** from email headers (optional)

This project provides a simple web UI (Flask) with a **risk score** and **human-readable explanations**.

---

## ✅ What the app does

### 1) Fake Email Detection
Input: **email text** (+ optional sender + raw headers)
- ML model analyzes the email text.
- Sender checks can flag suspicious sender format and blacklist.
- If you provide raw headers, the app may extract an IP and show a geolocation lookup.

### 2) Fake Website Detection
Input: **a suspicious URL**
- ML model analyzes the URL/URL patterns.
- The UI shows **website-focused** explanations (not email/sender-focused).

---

## 📁 Project structure

```
PhishingProject/
│
├── app.py
├── train.py
├── requirements.txt
│
├── data/
│   ├── phishing_dataset.csv
│   ├── sender_list.csv
│   └── phishing_dataset.csv
│
├── model/
│   ├── phishing_model.pkl
│   └── vectorizer.pkl
│
├── results/
│   └── (evaluation outputs: metrics.json, confusion matrix, etc.)
│
├── utils/
│   ├── model_utils.py
│   ├── preprocess.py
│   ├── url_features.py
│   ├── sender_check.py
│   └── ip_lookup.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── fake_email.html
│   ├── fake_website.html
│   ├── results.html
│   └── error.html
│
└── static/
    └── css/style.css
```

---

## ▶️ Run the project

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Train the model (first time)
```bash
python train.py
```

### 3) Start the Flask app
```bash
python app.py
```

Open:
- **http://127.0.0.1:5000**

---

## 🧾 How results are shown

On the results page:
- **Risk score** is shown as a percentage.
- The UI provides a **simple explanation**:
  - **Email mode** → sender-focused explanation
  - **Website mode** → URL/website-focused explanation
- **Advanced details** are still available (JSON) for debugging/testing.

---

## 📌 Notes
- Some sender/IP checks depend on whether you provide optional inputs (like raw headers).
- This tool is for educational/demo use and should not be the only security decision in real systems.

---

## 👨‍💻 Developed By
- G Manohara

