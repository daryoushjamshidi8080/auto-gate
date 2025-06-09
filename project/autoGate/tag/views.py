from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Tag
from django.template.loader import render_to_string


# Create your views here.


class TagView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, "tag/index.html")


class ListTagView(LoginRequiredMixin,View):
    def get(self, request):
        print('hi reza')
        tags = Tag.objects.all()
        html = render_to_string("tag/partials/list_tag.html", {"tags": tags}, request=request)
        return JsonResponse({"html": html})
        
        
        