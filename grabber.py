import requests
import smtplib
import socket
import sys

receiver_email = 'example@gmail.com'
sender_email = 'example@gmail.com'
app_password = 'app password goes here'

def get_public_ip():
    try:
        public_ip = requests.get('https://api64.ipify.org?format=json').json()['ip']
        return public_ip
    except Exception as e:
        print("Error retrieving public IP address:", str(e))
        return None

def get_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        location = data.get('city', '') + ', ' + data.get('region', '') + ', ' + data.get('country', '')
        return data, location
    except Exception as e:
        print("Error:", str(e))
        return None, None

def send_ip_email(public_ip, private_ip, location_data, location):
    subject = 'IP Addresses and Location'
    message = f'Public IP: {public_ip}\nPrivate IP: {private_ip}\nLocation Data: {location_data}\nLocation: {location}'
    email_text = f'Subject: {subject}\n\n{message}'

    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, app_password)
        smtp_server.sendmail(sender_email, receiver_email, email_text)
        smtp_server.quit()
    except Exception as e:
        print("Error sending email:", str(e))

if __name__ == "__main__":
    public_ip = get_public_ip()
    private_ip = socket.gethostbyname(socket.gethostname())
    location_data, location = get_location()

    if public_ip and private_ip:
        send_ip_email(public_ip, private_ip, location_data, location)
