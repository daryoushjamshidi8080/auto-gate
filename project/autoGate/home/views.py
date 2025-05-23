from django.shortcuts import render
from django.views import View
# Create your views here.



class home(View):
    def get(self, request):
        return render(request, "home/index.html")
    def post(self, request):
        pass
