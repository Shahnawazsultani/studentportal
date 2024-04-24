import requests
import json

def REGISTER_LIBRARY_ACCOUNT(student_id):
    url = "http://localhost:80/api/register"
    payload = {
        "studentId": student_id
    }
    json_payload = json.dumps(payload)
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, data=json_payload, headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to create library account. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False