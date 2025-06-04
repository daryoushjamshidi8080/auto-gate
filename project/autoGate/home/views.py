from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class home(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/index.html")
    def post(self, request):
        pass
