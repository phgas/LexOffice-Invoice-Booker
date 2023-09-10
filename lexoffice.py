import json
import requests
import time

with open("cookies.json", "r") as file:
    cookies = json.load(file)

session = requests.Session()
for cookie in cookies:
    session.cookies.set(
        cookie['name'], cookie['value'], domain=cookie['domain'])

response = session.get(
    "https://app.lexoffice.de/grld-rest/voucherservice/1/v200/vouchers?ascending=true&deletedIds=&firstRow=0&numRows=9999&orderBy=computedDueDate&status=open&voucherType=SalesInvoice")
invoices = response.json()['content']

for invoice in invoices:
    url = f"https://app.lexoffice.de/grld-rest/personalsalesinvoiceservice/1/v100/payment/{invoice['entityId']}"
    body = json.dumps({
        "amount": float(invoice['amount']),
        "postingDate": invoice['voucherDate'].split("T")[0],  # "2023-07-31"
        "method": "personal",
        "balanceReferenceType": "PartPayment"
    })

    headers = {
        'Content-Type': 'application/json'
        }

    response = session.put(url, data=body, headers=headers)
    print(f"[{invoice['identificationNumber']}] Status {response.status_code}: Successfully submitted invoice!")