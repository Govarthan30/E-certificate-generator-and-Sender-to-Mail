from flask import Flask, request, send_file, render_template_string, jsonify
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

TEMPLATE_PATH = "certificate_template.pdf"  # Ensure this file exists

# Register additional fonts
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))
pdfmetrics.registerFont(TTFont('Courier', 'cour.ttf'))
pdfmetrics.registerFont(TTFont('Verdana', 'verdana.ttf'))

def generate_certificate(name, x, y, font_size, font_style):
    """Generates a certificate and returns a PDF stream."""
    try:
        reader = PdfReader(TEMPLATE_PATH)
        writer = PdfWriter()
        packet = io.BytesIO()

        pdf_canvas = canvas.Canvas(packet, pagesize=letter)
        pdf_canvas.setFont(font_style, font_size)
        pdf_canvas.drawString(int(x), int(y), name)
        pdf_canvas.save()

        packet.seek(0)
        overlay = PdfReader(packet).pages[0]
        base_page = reader.pages[0]
        base_page.merge_page(overlay)
        writer.add_page(base_page)

        output_stream = io.BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)

        return output_stream
    except FileNotFoundError:
        return None

def send_email(receiver_email, pdf_stream):
    """Send the generated certificate via email."""
    sender_email = "noreplyotpgova@gmail.com"  # Change this
    sender_password = "cvvjgllllyouffhw"  # Change this (use app password if needed)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your Certificate"

    part = MIMEBase("application", "octet-stream")
    part.set_payload(pdf_stream.getvalue())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename=certificate.pdf")
    msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print("Email Error:", e)
        return False

@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Certificate Preview</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #121212;
                color: #fff;
                margin: 0;
                padding: 20px;
            }
            .container {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 20px;
            }
            .preview-container {
                width: 60%;
                height: 80vh;
                border: 1px solid #ccc;
                background-color: #222;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            iframe {
                width: 100%;
                height: 100%;
                border: none;
                background-color: white;
            }
            .input-container {
                width: 35%;
                display: flex;
                flex-direction: column;
                gap: 10px;
                background: #333;
                padding: 20px;
                border-radius: 8px;
            }
            label {
                font-weight: bold;
                margin-top: 10px;
            }
            input, select {
                padding: 10px;
                font-size: 16px;
                width: 100%;
                border: none;
                border-radius: 5px;
                background: #444;
                color: #fff;
            }
            input:focus, select:focus {
                outline: 2px solid #1db954;
            }
            button {
                background: #1db954;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background: #17a844;
            }
        </style>
    </head>
    <body>
        <h1>Live Certificate Generator</h1>
        <div class="container">
            <div class="preview-container">
                <iframe id="preview-frame"></iframe>
            </div>
            <div class="input-container">
                <label>Name:</label>
                <input type="text" id="name" placeholder="Enter Name">

                <label>X Position:</label>
                <input type="number" id="x" placeholder="200">

                <label>Y Position:</label>
                <input type="number" id="y" placeholder="300">

                <label>Font Size:</label>
                <input type="number" id="font_size" placeholder="30">

                <label>Font Style:</label>
                <select id="font_style">
                    <option value="Helvetica-Bold">Bold</option>
                    <option value="Helvetica">Regular</option>
                    <option value="Times-Roman">Times New Roman</option>
                    <option value="Courier">Courier</option>
                    <option value="Verdana">Verdana</option>
                </select>

                <label>Email:</label>
                <input type="email" id="email" placeholder="Enter recipient email">

                <button onclick="sendCertificate()">Send Certificate</button>
                <button id="download-button">Download Certificate</button>
            </div>
        </div>

        <script>
            function updatePreview() {
                let name = document.getElementById("name").value || "Sample Name";
                let x = document.getElementById("x").value || 200;
                let y = document.getElementById("y").value || 300;
                let fontSize = document.getElementById("font_size").value || 30;
                let fontStyle = document.getElementById("font_style").value || "Helvetica-Bold";

                let url = `/preview?name=${encodeURIComponent(name)}&x=${x}&y=${y}&font_size=${fontSize}&font_style=${fontStyle}`;
                document.getElementById("preview-frame").src = url;
                document.getElementById("download-button").onclick = () => window.open(url, "_blank");
            }

            function sendCertificate() {
                let name = document.getElementById("name").value;
                let email = document.getElementById("email").value;
                if (!email) {
                    alert("Please enter an email!");
                    return;
                }
                fetch(`/send_certificate?name=${encodeURIComponent(name)}&email=${email}`)
                    .then(response => response.text())
                    .then(data => alert(data));
            }

            document.querySelectorAll("input, select").forEach(input => input.addEventListener("input", updatePreview));
            updatePreview();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/preview")
def preview_certificate():
    pdf_stream = generate_certificate(request.args.get("name", "Sample Name"), int(request.args.get("x", 200)), int(request.args.get("y", 300)), float(request.args.get("font_size", 30)), request.args.get("font_style", "Helvetica-Bold"))
    return send_file(pdf_stream, mimetype="application/pdf") if pdf_stream else ("Template not found!", 404)

@app.route("/send_certificate")
def send_certificate():
    return jsonify({"message": "Certificate sent successfully!"} if send_email(request.args.get("email"), generate_certificate(request.args.get("name", "Sample Name"), 200, 300, 30, "Helvetica-Bold")) else {"error": "Failed to send email!"})

if __name__ == "__main__":
    app.run(debug=True)
