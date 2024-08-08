from django.urls import path
from .views import SendCodeView, VerifyCodeView, CompleteRegistrationView, LoginView
app_name = 'account.v1'
urlpatterns = [
    path('send-code/', SendCodeView.as_view(), name='send_code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('complete-registration/', CompleteRegistrationView.as_view(),
         name='complete_registration'),
    path('login/', LoginView.as_view(), name='login'),

]
