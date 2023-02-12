from django.urls import path
from authentification.views import *

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', log_out, name='logout'),
    path('register', Register.as_view(), name='register'),
    path('forgot-password', ForgotPassword.as_view(), name='forgot-password'),
    path('recovery-password/<str:token>', RecoveryPassword.as_view(), name='recovery-password'),
]
