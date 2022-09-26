from django.shortcuts import render
import logging
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.core.cache import cache
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from apps.seller.utils import Send_sms
# from .tasks import send_sms
from apps.seller.models import Transfer

from apps.accounts.models import CustomUser

# Create your views here.
def go_to_gateway_view(request):
    print(request.path) 
    if request.path == '/t-go-to-gateway/':
        # خواندن مبلغ از هر جایی که مد نظر است
        amount = 11000
    else:
        amount = 12000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = cache.get('phone')  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create(bank_models.BankType.ZARINPAL) # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        if request.path == '/t-go-to-gateway/':
            bank.set_client_callback_url('/t-callback-gateway/')
        else:
            # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
            bank.set_client_callback_url('/callback-gateway/')
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e
    
def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    
    user = CustomUser.objects.all().last()
    # user = cache.get('user')
    obj = Transfer.objects.create(
        user = user,
        tracking_code = tracking_code  
    )
    obj.save()
        
    if not tracking_code:
        # logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        # logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        if request.path == '/t-callback-gateway/':
            # phone_number = CustomUser.objects.all().last().phone_number
            phone_number = cache.get('phone')
            print('phone_number',phone_number)
            opt = "event"
            Send_sms(phone_number,opt)
            #send_sms.delay(phone_number,opt)
            print('اطلاعات به شما پیامک می شود')
            return render(request, 'agent/index.html')
        opt = "agent"
        Send_sms(phone_number,opt)
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return render(request, 'agent/index.html')

            

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
