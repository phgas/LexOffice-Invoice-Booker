# Standard library imports
import time
from typing import Any
import json

# Third-party imports
import requests


class Lexoffice:
    def __init__(self) -> None:
        self.session = self._read_cookies_into_session()

    def _read_cookies_into_session(self) -> requests.Session:
        session = requests.Session()
        with open("cookies.json", "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                session.cookies.set(
                    cookie["name"], cookie["value"], domain=cookie["domain"]
                )
        return session

    def _get_invoices(self) -> list[dict[str, Any]]:
        response = self.session.get(
            "https://app.lexoffice.de/grld-rest/voucherservice/1/v200/vouchers?ascending=true&deletedIds=&firstRow=0&numRows=9999&orderBy=computedDueDate&status=open&voucherType=SalesInvoice"
        )
        invoices = response.json()["content"]
        return invoices

    def book_invoices(self) -> None:
        for invoice in self._get_invoices():
            url = f"https://app.lexoffice.de/grld-rest/personalsalesinvoiceservice/1/v100/payment/{invoice['entityId']}"
            body = json.dumps(
                {
                    "amount": float(invoice["amount"]),
                    "postingDate": invoice["voucherDate"].split("T")[0],
                    "method": "personal",
                    "balanceReferenceType": "PartPayment",
                }
            )

            response = self.session.put(
                url, data=body, headers={"Content-Type": "application/json"}
            )
            print(
                f"[{invoice['identificationNumber']}] Status {response.status_code}: Successfully submitted invoice!"
            )

            time.sleep(0.1)


def main() -> None:
    lexoffice = Lexoffice()
    lexoffice.book_invoices()


if __name__ == "__main__":
    main()