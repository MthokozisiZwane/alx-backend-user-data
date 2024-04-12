import requests

url = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2019/11/a2e00974ce6b41460425.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240412%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240412T005328Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=c0275ebeccef4ecf06078810d6993667fffe9588dbdd8ca0f7705711dcada871"
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
