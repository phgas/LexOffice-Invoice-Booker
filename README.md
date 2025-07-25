# LexWare Invoice Booker

This Python script helps you to manage your invoices on the LexWare platform by leveraging the LexWare API.

## Prerequisites

- Python 3.8
- pip

## Installation

1. Clone this repository:

    ```
    git clone https://github.com/phgas/LexWare-Invoice-Booker.git
    ```

2. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```

## Configuration

1. Download the [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) extension for your web browser.

2. Go to settings and change the preferred export format for cookies to be JSON.

3. Log in to your LexWare account via your web browser.

4. Use EditThisCookie to export cookies for the `app.lexware.de` domain. 

5. Paste the exported cookies into a new file in the project directory, and name it `cookies.json`.

## Usage

Run the Python script:

```bash
python lexware_FP.py
```
or 
```bash
python lexware_OOP.py
```
