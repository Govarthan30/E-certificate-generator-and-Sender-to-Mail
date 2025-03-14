from flask import Flask, request, send_file, render_template_string, redirect, url_for
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
import io
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Path to the certificate template
TEMPLATE_PATH = "certificate_template.pdf"
OUTPUT_PATH = "generated_certificate.pdf"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "noreplyotpgova@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "cvvjgllllyouffhw"  # Replace with your email password

def get_default_text_position_and_font(name, x, y, font_size, font_style):
    """
    Returns the user-defined X, Y position, font size, and font style for the participant's name.
    """
    return x, y, font_size, font_style

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>E-Certificate Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" 
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-gray-900 text-white flex items-center justify-center h-screen">
    <div class="bg-gray-800 p-10 rounded-xl shadow-2xl">
        <h2 class="text-2xl mb-4 font-bold text-center">E-Certificate Generator</h2>
        <form method="post">
            <div class="mb-3">
                <label class="block text-sm font-medium">Participant's Name</label>
                <input type="text" name="name" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="block text-sm font-medium">X Position</label>
                <input type="number" name="x" class="form-control" required value="200">
            </div>
            <div class="mb-3">
                <label class="block text-sm font-medium">Y Position</label>
                <input type="number" name="y" class="form-control" required value="300">
            </div>
            <div class="mb-3">
                <label class="block text-sm font-medium">Font Size</label>
                <input type="number" name="font_size" class="form-control" required value="30">
            </div>
            <div class="mb-3">
                <label class="block text-sm font-medium">Font Style</label>
                <select name="font_style" class="form-control">
                    <option value="Helvetica-Bold">Helvetica-Bold</option>
                    <option value="Times-Bold">Times-Bold</option>
                    <option value="Courier-Bold">Courier-Bold</option>
                </select>
            </div>
            <div class="mb-3">
                <label class="block text-sm font-medium">Recipient Email</label>
                <input type="email" name="email" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary w-full">Generate & Send Certificate</button>
        </form>
    </div>
    <script>
        function showAlert() {
            setTimeout(function() {
                alert("Certificate Generated & Sent Successfully!");
                window.location.href = "/";
            }, 500);
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        x = int(request.form['x'])
        y = int(request.form['y'])
        font_size = int(request.form['font_size'])
        font_style = request.form['font_style']
        email = request.form['email']
        
        generate_certificate(name, x, y, font_size, font_style)
        send_certificate(email)
        return render_template_string(HTML_FORM + '<script>showAlert();</script>')
    return render_template_string(HTML_FORM)

def generate_certificate(name, x, y, font_size, font_style):
    """
    Generates a certificate with the participant's name at the specified position and font style.
    """
    reader = PdfReader(TEMPLATE_PATH)
    writer = PdfWriter()
    packet = io.BytesIO()
    
    pdf_canvas = canvas.Canvas(packet, pagesize=letter)
    pdf_canvas.setFont(font_style, font_size)
    pdf_canvas.drawString(x, y, name)
    pdf_canvas.save()
    packet.seek(0)
    
    new_pdf = PdfReader(packet)
    page = reader.pages[0]
    page.merge_page(new_pdf.pages[0])
    writer.add_page(page)
    
    with open(OUTPUT_PATH, "wb") as output_pdf:
        writer.write(output_pdf)

def send_certificate(email):
    """
    Sends the generated certificate to the recipient's email.
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = "Your E-Certificate"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg.set_content("Dear Participant,\n\nAttached is your e-certificate.\n\nBest Regards,\nEvent Team")
        
        with open(OUTPUT_PATH, "rb") as f:
            msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=OUTPUT_PATH)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("Email sent successfully to", email)
    except Exception as e:
        print("Error sending email:", e)

if __name__ == '__main__':
    app.run(debug=True)
