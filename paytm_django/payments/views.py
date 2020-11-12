# Create your views here.
from . import Checksum
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from payments.utils import VerifyPaytmResponse
import requests


def home(request):
    return HttpResponse("<html><a href='http://localhost:8000/payment'>PayNow</html>")


def payment(request):
    order_id = Checksum.__id_generator__()
    bill_amount = "100"
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': '7405505665',
        'EMAIL': 'dhaval.savalia6@gmail.com',
        'CUST_ID': '123123',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': bill_amount,
    } # This data should ideally come from database
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'payment.html', context)


@csrf_exempt
def response(request):
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        # save success details to db; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Successful</h1><center>", status=200)
    else:
        # check what happened; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)