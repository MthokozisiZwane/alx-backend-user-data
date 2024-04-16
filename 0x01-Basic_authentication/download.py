#!/usr/bin/env python3


import requests

url = 'https://intranet.alxswe.com/rltoken/2o4gAozNufil_KjoxKI5bA'
username = 'mthokozisi.zwane1999@gmail.com'  # Replace with your actual username
password = 'Mthokozisi#*@747'  # Replace with your actual password

# Perform authentication
login_url = 'https://intranet.alxswe.com/auth/sign_in'
session = requests.Session()
login_data = {'username': username, 'password': password}
response = session.post(login_url, data=login_data)

# Check if login was successful
if response.status_code == 200:
    # Download the file after authentication
    file_response = session.get(url)

    # Check if file was downloaded successfully
    if file_response.status_code == 200:
        # Save the file to your working directory
        with open('archive.zip', 'wb') as f:
            f.write(file_response.content)
        print("File downloaded successfully!")
    else:
        print("Failed to download the file.")
else:
    print("Failed to login. Check your credentials.")
