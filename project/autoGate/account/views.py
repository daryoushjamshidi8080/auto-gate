from django.shortcuts import render
from django.views import View   
from .forms import LoginForm
from django.contrib.auth import authenticate, login

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
                return render(request, "home/index.html")
        return render(request, "account/login.html", {"forms": forms})