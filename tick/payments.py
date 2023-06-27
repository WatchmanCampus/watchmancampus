from django.conf import settings
import json
import requests


def initiate_rave_url(name, email, transaction_ref, amount, callback_url):
    url = " https://api.flutterwave.com/v3/payments"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.RAVE_SECRET_KEY}",
    }
    data = {
        "tx_ref": transaction_ref,
        "amount": amount,
        "currency": "NGN",
        "redirect_url": callback_url,
        "payment_options": "card",
        # "meta": {"consumer_id": 23, "consumer_mac": "92a3-912ba-1192a"},
        "customer": {
            "email": email,
            # "phonenumber": phone,
            # "name": name,
        },
        "customizations": {
            "title": "Watchman Campus",
            "description": "Best store in town",
            "logo": "https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg",
        },
    }
    response = requests.post(url, json=data, headers=headers)
    return json.loads(response.content)
    # response = response.json()
    # link = response["data"]["link"]
    # return link


def initiate_paystack_url(email, amount, transaction_ref, currency, callback_url):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    payload = json.dumps(
        {
            "email": email,
            "amount": amount,
            "currency": currency,
            "reference": transaction_ref,
            "callback_url": callback_url,
        }
    )
    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print("this is first", response.content)
    return json.loads(response.content)
    # context = {"response" : response['data']['authorization_url']}


def verify_transaction(transaction_ref):
    url = f"https://api.paystack.co/transaction/verify/{transaction_ref}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    print("this is second", response.content)
    return json.loads(response.content)
