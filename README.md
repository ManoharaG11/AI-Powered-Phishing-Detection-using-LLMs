# 🛡️ AI-Powered Phishing Detection Using Machine Learning

## 🚀 Overview

AI-Powered Phishing Detection is a web-based cybersecurity application developed using **Python**, **Flask**, and **Machine Learning**. The system helps users identify phishing emails and malicious websites by analyzing email content, URL characteristics, sender information, and optional email headers. It generates a **risk score** along with human-readable explanations, enabling users to better understand potential security threats.

This project demonstrates the practical application of Machine Learning in cybersecurity and provides an intuitive web interface for real-time phishing analysis.

---

## ✨ Features

### 📧 Phishing Email Detection
- Detects phishing emails using Machine Learning.
- Analyzes email content for suspicious patterns.
- Calculates a phishing risk score.
- Provides easy-to-understand security explanations.

### 🌐 Malicious Website Detection
- Detects fake or malicious websites using URL analysis.
- Extracts URL-based features for prediction.
- Displays website-specific threat analysis.

### 👤 Sender Verification
- Performs basic sender validation.
- Supports sender blacklist checking.
- Detects suspicious sender formats.

### 🌍 IP Address Analysis
- Extracts sender IP from email headers (optional).
- Supports IP geolocation lookup.
- Displays location information when available.

### 📊 Interactive Dashboard
- Clean and responsive Flask web interface.
- Risk score visualization.
- User-friendly result pages.

---

## 🛠️ Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- HTML
- CSS
- JavaScript
- Machine Learning
- Pickle

---

## 📁 Project Structure

```text
PhishingProject/
│
├── app.py
├── train.py
├── requirements.txt
│
├── data/
│   ├── phishing_dataset.csv
│   └── sender_list.csv
│
├── model/
│   ├── phishing_model.pkl
│   └── vectorizer.pkl
│
├── results/
│   └── evaluation outputs
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
    └── css/
        └── style.css
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Powered-Phishing-Detection.git
```

### 2. Navigate to the Project Folder

```bash
cd AI-Powered-Phishing-Detection
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the Machine Learning Model

```bash
python train.py
```

### 5. Run the Application

```bash
python app.py
```

The application will start at:

```
http://127.0.0.1:5000
```

---

## 🖥️ How It Works

### 📧 Email Analysis

The application accepts:

- Email body
- Sender email (optional)
- Raw email headers (optional)

The system:

- Preprocesses the email text
- Predicts phishing probability
- Validates sender information
- Extracts sender IP (if available)
- Displays the overall risk score

---

### 🌐 Website Analysis

The application accepts a website URL.

The system:

- Extracts URL features
- Uses the trained ML model for prediction
- Calculates phishing probability
- Displays website-specific security explanations

---

## 📊 Output

The application provides:

- ✅ Risk Score (%)
- ✅ Prediction (Safe / Phishing)
- ✅ Human-readable Explanation
- ✅ Sender Validation Results
- ✅ Website Analysis Results
- ✅ IP Location Information (Optional)

---

## 📌 Future Enhancements

- Real-time email scanning
- Browser extension integration
- Deep Learning (LSTM/BERT) models
- Live threat intelligence feeds
- Multi-language phishing detection
- User authentication
- Detection history dashboard
- Email attachment scanning

---

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only**. It should not be used as the sole security solution for protecting production systems or making critical security decisions.

---

## 📄 License

This project is licensed under the **Apache 2.0 License**.

---

## 👨‍💻 Developed By

**G Manohara**

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!
