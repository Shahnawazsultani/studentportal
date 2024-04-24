from datetime import datetime, timedelta
import requests

def REGISTER_NEW_INVOICE(amount, due_date, invoice_type, student_id):
    data = {
        "amount": amount,
        "dueDate": due_date,
        "type": invoice_type,
        "account": {
            "studentId": student_id
        }
    }

    url = "http://localhost:8081/invoices/"

    headers = {
        "Content-Type": "application/json",
        "Host": "localhost:8081",
        "User-Agent": "PostmanRuntime/7.37.3",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            invoice_data = response.json()
            return {
                "is_created": True,
                "reference": invoice_data.get('reference', None) 
            }
        elif response.status_code == 422:
            return {
                "is_created": False,
                "reference": None,
                "invalid_student":True
            }
        else:
            return {
                "is_created": False,
                "reference": None
            }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "is_created": False,
            "reference": None
        }


def DELETE_INVOICE_BY_REFERENCE(invoice_reference):
    url = f"http://localhost:8081/invoices/{invoice_reference}/cancel"
    
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            return {'status':200,'message':'"Invoice Cancelled"'}
        elif response.status_code == 405:
            return {'status':405,'message':"You can't Cancel and Invoice that is Already Paid."}
        elif response.status_code == 404:
            return {'status':404,"message":"Invoice not found"}
        else:
            return None
    except Exception as e:
        return {'status':400,"message":"Something Went Wrong. Please Ensure that Finance Module is Running."}


def PAY_INVOICE_BY_REFERENCE(invoice_reference):
    url = f"http://localhost:8081/invoices/{invoice_reference}/pay"
    
    try:
        response = requests.put(url)
        if response.status_code == 200:
            # Payment successful
            return response.json()  # Return the response content
        elif response.status_code == 405:
            # Invoice is already paid
            return {"message": "Invoice is already paid"}
        elif response.status_code == 404:
            # Invoice not found
            return {"message": "Invoice not found"}
        else:
            # Payment failed for some other reason
            return {"message": "Payment failed for unknown reason"}
    except Exception as e:
        print(f"An message occurred: {e}")
        return {"message": "Payment failed due to an error"}
    
    
def GET_NEXT_THREE_DAYS_DATE(daysToLeft):
    today_date = datetime.now().date()
    next_three_days_date = today_date + timedelta(days=daysToLeft)
    formatted_date = next_three_days_date.strftime("%Y-%m-%d")
    return formatted_date