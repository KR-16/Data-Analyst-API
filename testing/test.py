import requests

url = "http://127.0.0.1:8000/analyze"
files = {
    "file":open("data\customers-1000.csv","rb")
}
response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Analysis Results: ", response.json())