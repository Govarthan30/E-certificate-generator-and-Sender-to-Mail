# E-Certificate Generator and Email Sender

This is a Flask-based web application that dynamically generates e-certificates for participants, allows customization of text position and font, and automatically sends the certificate to the recipient via email.

## Features
- User-friendly web interface with Tailwind CSS and Bootstrap.
- Allows input for participant name, text position (X, Y), font size, and font style.
- Generates PDF certificates dynamically.
- Sends the generated certificate to the recipient's email.
- Displays an alert after successful generation and email delivery.

## Installation

### Prerequisites
- Python 3.x installed
- A Gmail account for SMTP (or another email provider)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/Govarthan30/E-certificate-generator-and-Sender-to-Mail.git
   cd E-certificate-generator-and-Sender-to-Mail
   ```
2. Install dependencies:
   ```sh
   pip install flask reportlab PyPDF2
   ```
3. Update email credentials in `app.py`:
   ```python
   EMAIL_ADDRESS = "your-email@gmail.com"
   EMAIL_PASSWORD = "your-app-password"
   ```
   **Note:** If using Gmail, enable "Less secure apps" or generate an app password.

## Usage

1. Start the Flask server:
   ```sh
   python app.py
   ```
2. Open a browser and go to:
   ```
   http://127.0.0.1:5000/
   ```
3. Fill in the form with participant details and submit.
4. The certificate will be generated and sent to the provided email.
5. An alert will confirm successful generation and email delivery.

## File Structure
```
E-certificate-generator-and-Sender-to-Mail/
│── app.py              # Main Flask application
│── certificate_template.pdf  # Certificate template (add your own template)
│── generated_certificate.pdf # Generated certificate (output file)
│── README.md           # Project documentation
```

## License
This project is open-source and available under the MIT License.

## Author
Developed by [Govarthan V](https://github.com/Govarthan30)

## Contributing
Contributions are welcome! Feel free to fork this repository and submit a pull request.

