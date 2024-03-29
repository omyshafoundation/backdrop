from flask import Flask, render_template, request
import os
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    try:
        name = request.form['name']
        email = request.form['email']

        text_color = (255, 255, 255)
    # Load the image

        # Debug statement to check image path
        image = Image.open('/opt/Bgdrop-automation/backdrop.jpg')

    # Define text to be added
        text = f"{name.upper()}"

    # Calculate text position
        if len(name)<=4:
            font_size = 120
            x = 1200
            y = 350
        elif len(name)>4 and len(name)<=5:
            font_size = 120
            x = 1150
            y = 350
        elif len(name)>5 and len(name)<=6:
            font_size = 120
            x = 1100
            y = 350
        elif len(name)>6 and len(name)<=7:
            font_size = 110
            x = 1050
            y = 360
        elif len(name)>7 and len(name)<=8:
            font_size = 100
            x = 1000
            y = 360
        elif len(name)>8 and len(name)<=9:
            font_size = 90
            x = 990
            y = 370
        else:
            font_size = 75
            x = 990
            y = 390
      # Y-coordinate

    # Add text to image
        draw = ImageDraw.Draw(image)
        font_path = '/opt/Bgdrop-automation/poppins.ttf'
        font = ImageFont.truetype(font_path, font_size)
        draw.text((x, y), text, fill=text_color, font=font)

    # Save modified image
        image.save('/opt/Bgdrop-automation/modified_image.jpg')

    # Send email with the modified image attached
        subject = "Modified Image"
        message = f"Hello {name},\n\nPlease find the modified image attached."
        sender_email = "ash@vong.in"
        recipient_email = email

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        with open('/opt/Bgdrop-automation/modified_image.jpg', 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename('/opt/Bgdrop-automation/modified_image.jpg')}",
        )

        msg.attach(part)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Use 465 for SSL
        smtp_username = 'vong.meetings2@gmail.com'  # Your Gmail email address
        smtp_password = 'ufnm shia fhnm kyxl'
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return "Hoorrayyy ,check your mail......"
    except Exception as e:
        return (f"OOPSS error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
