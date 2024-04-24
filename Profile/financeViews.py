import requests

def REGISTER_FINANCE_ACCOUNT(studentFinance):
    account_created = False
    if studentFinance is not None:
        try:
            data = { "studentId": studentFinance.student_id }
            url = 'http://localhost:8081/accounts/'
            requests.post(url, json=data)
            account_created = True
            studentFinance.is_student = True
            studentFinance.save()
            return account_created    
        except:
            account_created = False
            return account_created
    else:
        account_created = False
        return account_created


def STUDENT_INFO(student_id):
    url = f"http://localhost:8081/accounts/student/{student_id}"
    try:
        try:
            response = requests.get(url)
        except Exception as e:
            print('*'*100)
            return None
        if response.status_code == 200:
            account_info = response.json()
            has_account = True
            has_outstanding_balance = account_info.get('hasOutstandingBalance', False)
            return {'hasAccount':has_account,'hasOutStandingBalance':has_outstanding_balance, 'error':False}
        elif response.status_code == 404:
            has_account = False
            return {'hasAccount':has_account, 'error':False}
        else:
            return {'error':"Something Went Wrong!"}
    except Exception as e:
        return {'error':"Unable to Sent Request. Please ensure Finance Module is Running"}


def STUDENT_INVOICES(student_id):
    url = f"http://localhost:8081/invoices"
    apiError = False
    try:
        response = requests.get(url)
    except Exception as e:
        apiError = True
        return apiError
    if response.status_code == 200:
        all_invoices = response.json()
        student_invoices = [invoice for invoice in all_invoices["_embedded"]["invoiceList"] if invoice["studentId"] == student_id]
  
        return student_invoices
    else:
        print(f"Failed to retrieve invoices. Status code: {response.status_code}")
        return None
    
