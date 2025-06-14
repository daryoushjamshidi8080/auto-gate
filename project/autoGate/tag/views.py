from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Tag
from django.template.loader import render_to_string
from .forms import TagForm


# Create your views here.


class TagView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, "tag/index.html")


class ListTagView(LoginRequiredMixin,View):
    def get(self, request):
        tags = Tag.objects.all()
        html = render_to_string("tag/partials/list_tag.html", {"tags": tags}, request=request)
        return JsonResponse({"html": html})
        
        
class AddTagView(LoginRequiredMixin,View):
    def get(self, request):
        form = TagForm()
        print('=========================================================')
        html = render_to_string("tag/partials/add_tag.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
        
        