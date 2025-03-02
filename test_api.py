import requests

url = "http://127.0.0.1:5000/report_stolen"
data = {
    "phone_number": "+26662914238",
    "device_name": "Samsung Galaxy A04S"
}

response = requests.post(url, json=data)
print(response.json())  # Should print: {"message": "Device reported as stolen"}
