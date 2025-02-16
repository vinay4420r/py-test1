from flask import Flask, request, render_template, redirect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

app = Flask(__name__)

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'kvinay00912@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'jdsv jfus tnwz asyn'  # Replace with your email password
RECIPIENT_EMAIL = 'kvinay00912@gmail.com'  # Replace with recipient email

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def send_email(subject, body, to_email, attachment_path=None):
    """
    Helper function to send an email.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file if provided
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
            msg.attach(attach)

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML form

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    pdf_file = request.files['pdf']

    # Save the uploaded PDF file
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)

    # Email to the recipient (you)
    recipient_subject = f"New Form Submission from {name}"
    recipient_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    send_email(recipient_subject, recipient_body, RECIPIENT_EMAIL, pdf_path)

    # Thank-you email to the user
    user_subject = "Thank You for Contacting Us"
    user_body = f"Dear {name},\n\nThank you for reaching out to us. We have received your message and will get back to you soon.\n\nBest regards,\nYour Company"
    send_email(user_subject, user_body, email)

    # Clean up: Delete the uploaded file after sending the email
    os.remove(pdf_path)

    return "Form submitted successfully! We will get back to you soon."

if __name__ == '__main__':
    app.run(debug=True)