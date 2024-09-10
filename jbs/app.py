from flask import Flask, render_template, request, redirect, flash, url_for
import smtplib
from bs4 import BeautifulSoup
import requests
import pyttsx3
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import geocoder
import pywhatkit as pwk
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'e4ddd3bxxxxxxxxxxxxxx3d7716495c'

# Email sending function
@app.route('/send_email', methods=['POST'])
def send_email():
    to_email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        from_email = "ajaysadh15@gmail.com"
        password = "vhmxxxxxxxxxcgxbzhu"

        email_message = f'Subject: {subject}\n\n{message}'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, email_message)

        return render_template('success.html')
    except Exception as e:
        return f"Failed to send email: {e}"

@app.route('/send_email', methods=['GET'])
def send_email_page():
    return render_template('send_email.html')

# Google scraping functionality
@app.route('/scrape_google', methods=['POST'])
def scrape_google():
    query = request.form['query']
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = soup.find_all('h3', limit=5)
        results_list = [result.text for result in results]

        return render_template('scrape_google_success.html', results=results_list)
    except Exception as e:
        print(f"Failed to scrape Google search results: {e}")
        return "An error occurred while scraping."

@app.route('/scrape_google', methods=['GET'])
def scrape_google_page():
    return render_template('scrape_google.html')

# Text to Speech functionality
@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    try:
        text = request.form['text']
        if not text.strip():
            flash("Please enter some text to convert to speech.")
            return redirect(url_for('text_to_speech_page'))

        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

        flash("Successfully converted text to speech!")
        return redirect(url_for('text_to_speech_page'))
    except Exception as e:
        flash(f"Failed to convert text to speech: {e}")
        return redirect(url_for('text_to_speech_page'))

@app.route('/text_to_speech', methods=['GET'])
def text_to_speech_page():
    return render_template('text_to_speech.html')

# Volume control functionality
@app.route('/control_volume', methods=['POST'])
def control_volume():
    try:
        volume_level = int(request.form['volume'])
        if 0 <= volume_level <= 100:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            level_normalized = volume_level / 100.0
            volume.SetMasterVolumeLevelScalar(level_normalized, None)
            flash(f"Volume successfully set to {volume_level}%.")
            return render_template('control_volume.html', volume_level=volume_level)
        else:
            flash("Volume must be between 0 and 100.")
    except ValueError:
        flash("Invalid input. Please enter a number between 0 and 100.")
    except Exception as e:
        flash(f"Error: {e}")

    return redirect(url_for('control_volume_page'))

@app.route('/control_volume', methods=['GET'])
def control_volume_page():
    return render_template('control_volume.html')

# Geo-location functionality
@app.route('/find_geo_location', methods=['POST'])
def find_geo_location():
    try:
        g = geocoder.ip('me')
        location_info = f"Your current location: {g.city}, {g.state}, {g.country}. Coordinates: {g.latlng}"
        return render_template('find_geo_location_success.html', location_info=location_info)
    except Exception as e:
        flash(f"Failed to get geo coordinates: {e}")
        return render_template('find_geo_location.html')

@app.route('/find_geo_location', methods=['GET'])
def find_geo_location_page():
    return render_template('find_geo_location.html')

# Bulk email functionality
@app.route('/send_bulk_email', methods=['POST'])
def send_bulk_email():
    email_addresses = request.form['email_addresses']
    email_subject = request.form['email_subject']
    email_message = request.form['email_message']

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        from_email = "jatin.sharma7281@gmail.com"
        password = "vhmqxxxxxxxzhu"

        email_message = f'Subject: {email_subject}\n\n{email_message}'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            email_list = email_addresses.split(',')
            server.sendmail(from_email, email_list, email_message)

        return render_template('success.html')
    except Exception as e:
        return f"Failed to send email: {e}"

@app.route('/send_bulk_email', methods=['GET'])
def send_bulk_email_page():
    return render_template('send_bulk_email.html')

# SMS functionality using pywhatkit
@app.route('/send_sms', methods=['POST'])
def send_sms():
    phone_number = request.form['phone']
    message = request.form['message']
    
    try:
        pwk.sendwhatmsg_instantly(phone_number, message)
        return render_template('success.html')
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return f"Failed to send SMS: {e}"

@app.route('/send_sms', methods=['GET'])
def send_sms_page():
    return render_template('send_sms.html')

# SMS functionality using Twilio
account_sid = 'ACbd2cdc6xxxxxxxxxxxxxxxxfd2d7e410d'
auth_token = 'e1163f37xxxxxxxxxxxxxxxxxxxa9763b7'
twilio_phone_number = '+1631xxxxx712'

client = Client(account_sid, auth_token)

@app.route('/send_sms_from_mobile', methods=['POST'])
def send_sms_from_mobile():
    phone_number = request.form['phone_number']
    message = request.form['message']
    
    try:
        client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=phone_number
        )
        return render_template('success.html')
    except Exception as e:
        return f"Failed to send message: {str(e)}"

@app.route('/send_sms_from_mobile', methods=['GET'])
def send_sms_from_mobile_page():
    return render_template('send_sms_from_mobile.html')

# Form submission handling
@app.route('/submit', methods=['POST'])
def submit():
    full_name = request.form['full_name']
    email = request.form['email']
    mobile_number = request.form['mobile_number']
    email_subject = request.form['email_subject']
    message = request.form['message']

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        from_email = "jatin.sharma7281@gmail.com"
        password = "vhmqaxxxxxxxxxxbzhu"

        email_message = f"Subject: {email_subject}\n\nFrom: {full_name}\nMobile: {mobile_number}\n\n{message}"

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, email, email_message.encode('utf-8'))

        return render_template('success.html')
    except Exception as e:
        return f"Failed to send email: {e}"

if __name__ == '__main__':
    app.run(debug=True)