from django.urls import path
from . import views


app_name='seller'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    # path('register/phone_register/', views.phone_register, name='phone_register'),
    # path('register/phone_verify/<int:register_phone>/', views.phone_verify, name='phone_verify'),
    path('representation/', views.AgentRegisterView.as_view(), name='representation'),
    path('trainingcourse/', views.AgentTrainView.as_view(), name='trainingcourse'),
    path('contract/', views.AgentProfileView.as_view(), name='contract'),
    path('tcontract/', views.AgentProfileView.as_view(), name='tcontract'),
]
