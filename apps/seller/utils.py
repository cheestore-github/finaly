from melipayamak import Api
from rest_framework.response import Response
from rest_framework import status
import os

import requests
import json
from rest_framework import generics,status


#------------------------------------send sms activation code--------------------------------

def Send_sms(phone,opt,code=None):

    try:
        #username =os.environ.get("SMS_HOST_USERNAME","")
        username = '09923515167'
        #password =os.environ.get("SMS_HOST_PASSWORD","")
        password = 'H8MC7'
        api = Api(username,password)
        sms = api.sms()
        to = phone
        # _from = os.environ.get("SMS_HOST_SENDER","")
        _from = '50004001515167'
        if opt=="reg":   
            text = 'کد تاییدیه شما از طرف چی استور'+': '+ str(code)
        if opt=="event":
            text = 'پرداخت شما با موفقیت انجام شد. زمان برگزاری و اطلاعات مربوطه متعاقبا اعلام می گردد.'
        if opt=="agent":
        #     date = uid.date_in
            text = 'پرداخت شما با موفقیت انجام شد. پس از بررسی رزومه نتیجه متعاقبا اعلام می گردد.'
        print(text)
        response = sms.send(to,_from,text)
        print(response)
        #return Response(status=status.HTTP_200_OK)
    except:
        print("sms dont send.................................")
        #return Response(status=status.HTTP_403_FORBIDDEN)




#------------------send notification-----------------------------
        
def Notification(request):
    YOUR_TOKEN = 'put your token here ...'
    YOUR_APP_ID = 'put your app id here ...'

    url = f'https://api.pushe.co/v2/messaging/notifications/'

    headers = {
        'Authorization': f'Token {YOUR_TOKEN}',
        'Content-Type': 'application/json'
    }
    phone=request.user.phone
    payload = json.dumps({
        'app_ids': YOUR_APP_ID,
        'data': {
            'title': 'عنوان اعلان',
            'content': 'متن اعلان'
        },
        'filters': {
            'phone_number': [
                phone, 
                'phone_num2'
            ]
        }
    })

    r = requests.post(url, data=payload, headers=headers)

    print(r.status_code)




#---------------------- create invite link----------------------------
