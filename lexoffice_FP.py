# Standard library imports
import time
from typing import Any
import json

# Third-party imports
import requests


def read_cookies_into_session() -> requests.Session:
    session = requests.Session()
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            session.cookies.set(
                cookie["name"], cookie["value"], domain=cookie["domain"]
            )
    return session


def get_invoices(session: requests.Session) -> list[dict[str, Any]]:
    response = session.get(
        "https://app.lexware.de/grld-rest/voucherservice/1/v200/vouchers?ascending=true&deletedIds=&firstRow=0&numRows=9999&orderBy=computedDueDate&status=open&voucherType=SalesInvoice"
    )
    invoices = response.json()["content"]
    return invoices


def book_invoices(session: requests.Session, invoices: list[dict[str, Any]]) -> None:
    for invoice in invoices:
        url = f"https://app.lexware.de/grld-rest/personalsalesinvoiceservice/1/v100/payment/{invoice['entityId']}"
        body = json.dumps(
            {
                "amount": float(invoice["amount"]),
                "postingDate": invoice["voucherDate"].split("T")[0],
                "method": "personal",
                "balanceReferenceType": "PartPayment",
            }
        )

        response = session.put(
            url, data=body, headers={"Content-Type": "application/json"}
        )
        print(
            f"[{invoice['identificationNumber']}] Status {response.status_code}: Successfully submitted invoice!"
        )

        time.sleep(0.1)


def main() -> None:
    session = read_cookies_into_session()
    invoices = get_invoices(session)
    book_invoices(session, invoices)


if __name__ == "__main__":
    main()
