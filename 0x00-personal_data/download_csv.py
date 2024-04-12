import requests

url = "https://intranet.alxswe.com/rltoken/cVQXXtttuAobcFjYFKZTow"
local_filename = "user_data.csv"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Open the local file in binary write mode and write the content of the response to it
    with open(local_filename, "wb") as f:
        f.write(response.content)
    print("File downloaded successfully!")
else:
    print("Failed to download file. Status code:", response.status_code)
