from django.http import HttpResponse
from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse

from apps.accounts.models import CustomUser

from .forms import (AgentRegisterForm, UserRegisterForm, RuleForm, PhoneRegisterForm)
from .models import AgentUser, Rule
from .utils import Send_sms
from django.contrib.auth import authenticate, login, logout
from django.views import View
import random
import logging
from azbankintro import iban_validate, IBANValidationException

class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'agent/index.html')
    
#============================PhoneRegister========================================================
# def codeGenerate():
#     return random.randint(1000,9999)
# from django_otp.oath import totp

# secret_key = b'12345678901234567890'
# code = totp(key=secret_key, step=30, digits=4)

# def phone_register(request):
#     form = PhoneRegisterForm(request.GET)
#     if form.is_valid():
#         opt = "reg"
#         register_phone = form.cleaned_data['phone_number']
#         #Send_sms(register_phone,opt,code)
#         cache.set(register_phone,code,180)
        
#         print(type(int(register_phone)), ": " ,code)
#         return redirect(reverse('seller:phone_verify',kwargs={'register_phone':int('0'+ register_phone)}))
#     else:
#         return render(request, 'seller/phone_register.html', {'form':form})
    # else:
    #     return render(request, 'seller/phone_register.html', {'form':form})

#============================PhoneVerify========================================================

# def phone_verify(request, register_phone):
#     # print("code", code)
#     register_phone = '0'+str(register_phone)
#     # print('register_phone',register_phone)
#     c_phone=cache.get(register_phone)
#     # print('c_phone',type(c_phone))
#     # if request.method =='POST':
#     verify_code = request.GET.get('phone_verify')
#     # print('verify_code',type(verify_code))
#     if verify_code == str(c_phone):
#         print(verify_code, "You send to the next page")
#         return redirect('seller:register')
#     return render(request, 'seller/phone_verify.html',{'code':code})


#===================================================================================

class AgentRegisterView(View):
        
    def get(self,request, *args, **kwargs):
        user_form = UserRegisterForm()
        agent_form = AgentRegisterForm()
        return render(request, 'agent/representation.html', {'user_form': user_form, 'agent_form':agent_form})

    def post(self,request,*args, **kwargs):
        user_form = UserRegisterForm()
        agent_form = AgentRegisterForm()
        if request.method == "POST":
            user_form = UserRegisterForm(request.POST)
            agent_form = AgentRegisterForm(request.POST, request.FILES or None)
            if user_form.is_valid() and agent_form.is_valid():
                custom_user = user_form.save()
                agent_user = agent_form.save(commit=False)
                agent_user.user = custom_user
                agent_user.save()
                # name = user_form.cleaned_data.get('name')
                # family = user_form.cleaned_data.get('family')
                # phone_number = user_form.cleaned_data.get('phone_number')
                # national_code = user_form.cleaned_data.get('national_code')
                # email = user_form.cleaned_data.get('email')
                
                # phone = agent_form.cleaned_data.get('phone')
                # birth_year = agent_form.cleaned_data.get('birth_year')
                # residence_city = agent_form.cleaned_data.get('residence_city')
                # agency_city = agent_form.cleaned_data.get('agency_city')
                # job_history = agent_form.cleaned_data.get('job_history')
                # last_collab = agent_form.cleaned_data.get('last_collab')
                # schooling = agent_form.cleaned_data.get('famischoolingly')
                # social_media_skills = agent_form.cleaned_data.get('social_media_skills')
                # job_space = agent_form.cleaned_data.get('job_space')
                # reagent = agent_form.cleaned_data.get('reagent')
                # plunge_case = agent_form.cleaned_data.get('plunge_case')
                # profational_skills = agent_form.cleaned_data.get('profational_skills')
                # languages = agent_form.cleaned_data.get('languages')
                # favorites = agent_form.cleaned_data.get('favorites')
                # familiarity_with_us = agent_form.cleaned_data.get('familiarity_with_us')
                # cv = agent_form.cleaned_data.get('cv')

                # custom_obj = CustomUser.objects.create(
                #     name = name,
                #     family = family,
                #     phone_number = phone_number,
                #     national_code = national_code,
                #     email = email
                # )
                # custom_user = custom_obj.save()
                
                # agent_obj = AgentUser.objects.create(
                #     user = custom_user,
                #     phone = phone,
                #     birth_year = birth_year,
                #     residence_city = residence_city,
                #     agency_city = agency_city,
                #     job_history = job_history,
                #     last_collab = last_collab,
                #     schooling = schooling,
                #     social_media_skills = social_media_skills,
                #     job_space = job_space,
                #     reagent = reagent,
                #     plunge_case = plunge_case,
                #     profational_skills = profational_skills,
                #     languages = languages,
                #     favorites = favorites,
                #     familiarity_with_us = familiarity_with_us,
                #     cv = cv    
                # )
                
                # agent_obj.save()
                messages.success(request,'ثبت اطلاعات با موفقیت انجام شد')
                return redirect('seller:contract')
            else:
                messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد')
                return render(request, 'agent/representation.html', {'user_form': user_form, 'agent_form': agent_form})
        
class AgentTrainView(View):
    def get(self, request, *args, **kwargs):
        user_form = UserRegisterForm()
        return render(request, 'agent/trainingcourse.html', {'user_form': user_form})
    
    def post(self, request, *args, **kwargs):
        
        user_form = UserRegisterForm()
        if request.method=='POST':
            user_form = UserRegisterForm(request.POST)
            if user_form.is_valid():
                name = user_form.cleaned_data.get('name')
                family = user_form.cleaned_data.get('family')
                phone_number = user_form.cleaned_data.get('phone_number')
                # cache.set('phone',phone_number,500)
                # a = cache.get('phone')
                national_code = user_form.cleaned_data.get('national_code')
                email = user_form.cleaned_data.get('email')
                obj = CustomUser.objects.create(
                    name = name,
                    family = family,
                    phone_number = phone_number,
                    national_code = national_code,
                    email = email
                )
                obj.save()
                messages.success(request, 'ثبت اطلاعات با موفقیت انجام شد.')
                return redirect('seller:tcontract') 
            else:
                messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد')
                return render(request, 'agent/trainingcourse.html', {'user_form': user_form}) 
        else:
            return render(request, 'agent/trainingcourse.html', {'user_form': user_form})  
        
class AgentProfileView(View):
    def get(self,request,*args, **kwargs):
        rule_form = RuleForm()
        return render(request, 'agent/contract.html',{'rule_form': rule_form})
    
    def post(self, request, *args, **kwargs):
        rule_form = RuleForm()
        if request.method == 'POST':
            rule_form = RuleForm(request.POST)
            if rule_form.is_valid():
                rule_accept = rule_form.cleaned_data.get('rule_accept')
                # rule_deny = rule_form.cleaned_data.get('rule_deny')
                # later_read = rule_form.cleaned_data.get('later_read')
                user = CustomUser.objects.all().last()
                obj = Rule.objects.create(
                    user = user,
                    rule_accept = rule_accept,
                    # rule_deny = rule_deny,
                    # later_read = later_read
                )
                obj.save()
                print(request.get_full_path)
                if rule_accept == True:
                    if request.path == "/contract/":
                        # print('aaaaaaaaaaaaaaaaaaaaaa',request.get_full_path)
                        return redirect('go-to-gateway') 
                    else:
                        return redirect('t-go-to-gateway')
                else:
                    messages.error(request, 'شما قادر به ادامه روند نمی باشید.')
                    return render(request, 'agent/contract.html', {'rule_form': rule_form}) 
        else:
            return render(request, 'agent/contract.html', {'rule_form': rule_form}) 
                
                       

    # def post(self,request,*args, **kwargs):
    #     return redirect('seller:login')




