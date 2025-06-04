from django.shortcuts import render, redirect
from django.views import View   
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout

class UserLoginView(View):
    def get(self, request):
        forms = LoginForm()
        return render(request, "account/login.html", {"forms": forms})

    def post(self, request):
        forms = LoginForm(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            user = authenticate(request,username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                return redirect("home:home")
        return render(request, "account/login.html", {"forms": forms})
    

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("account:account-login")
