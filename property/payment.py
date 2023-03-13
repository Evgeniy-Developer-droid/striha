import json
from django.conf import settings
from liqpay.liqpay3 import LiqPay
from django.urls import reverse
import secrets

from property.models import Transaction, PaymentToken


def pay_link_generate(transaction):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC, settings.LIQPAY_SECRET)
    token = secrets.token_hex(20)
    params = {
        'action': 'pay',
        'currency': 'UAH',
        'order_id': token,
        'version': '3',
        'amount': transaction.amount,
        'description': transaction.description,
        'sandbox': 0, # sandbox mode, set to 1 to enable it
        'server_url':  settings.SITE_URL + reverse("pay_callback")
    }
    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)
    PaymentToken.objects.create(
        token=token,
        meta=json.dumps({
            "action": "transaction_pay",
            "key": str(transaction.key)
        })
    )
    link = f"https://www.liqpay.ua/api/3/checkout?data={data}&signature={signature}"
    return link