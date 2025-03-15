# 🏆 E-Certificate Generator

A web-based **E-Certificate Generator** built with **Flask, PyPDF2, and ReportLab**. Users can dynamically generate certificates, preview them in real-time, and download or send them via email.

---

## 🚀 Features
✅ **Live Certificate Preview** - See updates in real time before downloading.
✅ **Dynamic Text Positioning** - Customize name position, font size, and font style.
✅ **Email Integration** - Send certificates via email with SMTP.
✅ **Secure and Scalable** - Uses a predefined PDF template for generating certificates.

---

## 📌 Tech Stack
- **Backend**: Flask (Python)
- **PDF Processing**: PyPDF2, ReportLab
- **Frontend**: HTML, JavaScript, CSS
- **Email Service**: SMTP with Python

---

## 🔧 Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Govarthan30/e-certificate-generator.git
cd e-certificate-generator
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Email Credentials (Recommended)
Create a `.env` file and add your email credentials:
```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

Alternatively, modify `send_email()` in `app.py` to use your email credentials directly.

### 4️⃣ Run the Flask App
```bash
python app.py
```

The app will be available at: **http://127.0.0.1:5000/**

---

## 🎯 Usage
### 1️⃣ Open the Web UI
- Visit **http://127.0.0.1:5000/** in your browser.
- Enter your name, adjust text positioning, and choose a font.
- Preview the certificate live.

### 2️⃣ Download or Email the Certificate
- Click **Download Certificate** to get a PDF.
- Enter an email and click **Send Certificate** to receive it via email.

---

## 📜 Environment Variables (Optional)
| Variable      | Description                |
|--------------|----------------------------|
| `EMAIL_USER` | Sender email address       |
| `EMAIL_PASS` | SMTP email password (app password recommended) |

---

## 🤝 Contributing
1. **Fork** the repo.
2. **Create** a new branch (`feature-xyz`).
3. **Commit** your changes.
4. **Push** to your branch.
5. **Submit** a PR for review!

---

## 📄 License
This project is open-source and available under the **MIT License**.

---

## 📞 Contact
**Developer:** [Govarthan V](https://www.linkedin.com/in/govarthan-v)

Feel free to ⭐ star this repo if you find it useful! 🚀

