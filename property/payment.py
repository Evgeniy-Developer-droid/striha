import json
from django.conf import settings
from liqpay.liqpay3 import LiqPay
from django.urls import reverse
import secrets

from property.models import Transaction


def payment_data_generate(contract):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC, settings.LIQPAY_SECRET)
    token_order = secrets.token_hex(16)
    params = {
        'action': 'pay',
        'currency': 'UAH',
        'order_id': token_order,
        'version': '3',
        'amount': 12,
        'description': "s",
        'sandbox': 0, # sandbox mode, set to 1 to enable it
        'server_url':  settings.SITE_URL + reverse("callback-contract-pay-steps")
    }

    Transaction.objects.create(
        tenant=contract.tenant,
        landlord=contract.landlord,
        amount=params['amount'],
        order_id=token_order,
        name=params['description'],
        meta=json.dumps({
            "contract": contract.pk,
            "mode": contract.status
        })
    )
    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)
    return {"signature": signature, "data": data}