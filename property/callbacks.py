import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from liqpay.liqpay3 import LiqPay
from property.models import Contract, Transaction, PaymentToken


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC, settings.LIQPAY_SECRET)
        data = request.POST.get('data', None)
        signature = request.POST.get('signature', None)
        sign = liqpay.str_to_sign(settings.LIQPAY_SECRET + data + settings.LIQPAY_SECRET)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        print('callback data', response)

        token = PaymentToken.objects.get(token=response['order_id'])
        transaction = Transaction.objects.get(key=json.loads(token.meta)['key'])
        return HttpResponse("OK")
