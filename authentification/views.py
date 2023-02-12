import json
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from user.models import User
from .models import AuthToken
from user.utils import get_dashboard_link


class Home(View):

    def get(self, request):
        return redirect(reverse('login'))


class RecoveryPassword(View):

    def get(self, request, token):
        try:
            AuthToken.objects.get(token=token)
            return render(request, 'auth/recovery_password.html', {"info": "Enter your new password."})
        except AuthToken.DoesNotExist:
            return render(request, 'auth/recovery_password.html', {"error": "Inivalid token."})

    def post(self, request, token):
        try:
            token = AuthToken.objects.get(token=token)
            user = User.objects.get(pk=int(json.loads(token.meta).get('user')))

            if request.POST.get('password') != request.POST.get('password2'):
                return render(request, 'auth/recovery_password.html', {"error_pass": "Passwords is not same", "info": "Enter your new password."})
            
            user.set_password(request.POST.get('password'))
            user.save()
            token.delete()
            return render(request, 'auth/recovery_password.html', {"success": "Congratulation, you changed password."})
        except (AuthToken.DoesNotExist, User.DoesNotExist):
            return render(request, 'auth/recovery_password.html', {"error": "Inivalid token."})


class ForgotPassword(View):

    def get(self, request):
        return render(request, 'auth/forgot_password.html', {})

    def post(self, request):
        user = User.objects.filter(email=request.POST.get('email'))
        if user.exists():
            # send email
            token = AuthToken.objects.create(
                name="forgot_password",
                meta=json.dumps({"user": user.first().pk})
            )
            print(token.token)
            return render(request, 'auth/forgot_password.html', {"success": "Success, check your email"})
        return render(request, 'auth/forgot_password.html', {"error": "User with this email not found"})


class Register(View):

    def validation(self, query):
        if User.objects.filter(email=query.get('email')).exists():
            return False, "User with this email already exist"
        if User.objects.filter(phone=query.get('phone')).exists():
            return False, "User with this phone already exist"
        
        if query.get('password') != query.get('password2'):
            return False, "Passwords is not same"

        return True, "Success"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(get_dashboard_link(request.user.role))
                
        return render(request, 'auth/register.html', {"title": "Register"})

    def post(self, request):
        data = request.POST
        valid = self.validation(data)
        if valid[0]:
            user = User.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                role=data.get('role'),
                username=data.get('email'),
                phone=data.get('phone'),
                is_active=False
            )
            user.set_password(data.get('password'))
            user.save()
            return render(request, 'auth/success_register.html', {"title": "Success"})
        return render(request, 'auth/register.html', {"title": "Register", "error": valid[1]})


class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(get_dashboard_link(request.user.role))

        return render(request, 'auth/login.html', {"title": "Login"})

    def post(self, request):
        logout(request)
        username = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # <-- Here if the remember me is False, that is why expiry is set to 0 seconds. So it will automatically close the session after the browser is closed.
                next = request.POST.get('next')
                if next:
                    return redirect(next)
                return redirect(get_dashboard_link(user.role))
        return render(request, 'auth/login.html', {"title": "Login", "error": "Incorrect credentials"})


def log_out(request):
    logout(request)
    return redirect(reverse('login'))