from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import antennas
from .forms import AntennaForm
from django.http import JsonResponse
from django.template.loader import render_to_string



class SettingView(LoginRequiredMixin, View):
    model_class = antennas
    def get(self, request):
        antennas = self.model_class.objects.all()
        return render(request, "setting/setting.html", {"antennas": antennas})
    

class CreateAntennaView(LoginRequiredMixin, View):
    def get(self, request):
        form = AntennaForm()
        html = render_to_string("setting/partials/antenna_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    def post(self, request):
        form = AntennaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        html = render_to_string("setting/partials/antenna_form.html", {"form": form}, request=request)
        return JsonResponse({"success": False, "form_html": html})

