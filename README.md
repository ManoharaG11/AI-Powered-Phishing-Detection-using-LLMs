# 🧠 AI-Powered Phishing Detection using Machine Learning

A web-based cybersecurity application that leverages **Machine Learning (ML)** and **Natural Language Processing (NLP)** to detect phishing attempts through suspicious emails and website URLs. The system analyzes user inputs, predicts potential phishing attacks, and provides a risk score with clear explanations to help users make informed security decisions.

---

## 🚀 Features

- 📧 Detect phishing emails using Machine Learning
- 🌐 Identify malicious or fake website URLs
- 👤 Perform basic sender verification and blacklist checking
- 🌍 Extract IP addresses from email headers (optional)
- 📊 Display risk score with prediction results
- 💡 Provide human-readable explanations for every prediction
- ⚡ Fast and responsive Flask-based web interface

---

## 🛠️ Tech Stack

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- HTML
- CSS
- JavaScript
- Pickle (Model Serialization)

---

## 📁 Project Structure

```text
AI-Powered-Phishing-Detection/
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
│   ├── metrics.json
│   └── confusion_matrix.png
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
├── static/
│   └── css/
│       └── style.css
│
└── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/AI-Powered-Phishing-Detection.git
```

### Navigate to the Project Folder

```bash
cd AI-Powered-Phishing-Detection
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Train the Machine Learning Model

```bash
python train.py
```

### Start the Flask Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🔍 Detection Modules

### 📧 Email Phishing Detection

- Analyzes email content using a trained Machine Learning model.
- Detects suspicious text patterns commonly found in phishing emails.
- Performs sender verification and blacklist checking.
- Supports optional IP extraction from email headers.

### 🌐 Website Phishing Detection

- Accepts suspicious website URLs.
- Extracts URL-based features.
- Predicts whether the website is legitimate or malicious.
- Provides website-specific explanations for the prediction.

---

## 📊 Prediction Output

The application displays:

- ✅ Prediction Result
- 📈 Risk Score
- 📧 Email or 🌐 Website Analysis
- 💡 Explanation of the prediction
- 🔍 Additional debugging information (optional)

---

## 📌 Notes

- Some features such as IP lookup require optional email headers.
- This project is intended for educational and research purposes.
- Machine Learning predictions should be used as an assistance tool and not as the sole basis for cybersecurity decisions.

---

## 🔮 Future Enhancements

- Browser Extension for Real-Time Phishing Detection
- Deep Learning-based Email Classification
- QR Code Phishing Detection
- Multi-language Email Analysis
- Live Threat Intelligence Integration
- Dashboard for Security Analytics

---

## 📄 License

This project is licensed under the **Apache License 2.0**.

---

## 👨‍💻 Developed By

**G Manohara**

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!
