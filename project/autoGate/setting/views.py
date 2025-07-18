from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import antennas
from .forms import AntennaForm, CusstomUserCreationForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'), name='dispatch')
class SettingView(LoginRequiredMixin, View):
    model_class = antennas

    def get(self, request):
        antennas = self.model_class.objects.all()
        users = User.objects.all()
        return render(request, "setting/setting.html", {"antennas": antennas, 'users': {users}})


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'), name='dispatch')
class AntennaListPartialView(LoginRequiredMixin, View):
    def get(self, request):
        antenna_list = antennas.objects.all()
        html = render_to_string("setting/partials/antenna_list.html", {
            "antennas": antenna_list
        }, request=request)
        return JsonResponse({"html": html})


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'), name='dispatch')
class CreateAntennaView(LoginRequiredMixin, View):

    def get(self, request):
        form = AntennaForm()
        html = render_to_string(
            "setting/partials/antenna_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    def post(self, request):
        form = AntennaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        html = render_to_string(
            "setting/partials/antenna_form.html", {"form": form}, request=request)
        return JsonResponse({"success": False, "form_html": html})


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class DeleteAntennaView(LoginRequiredMixin, View):
    def post(self, request, antenna_id):
        antenna = get_object_or_404(antennas, pk=antenna_id)
        antenna.delete()
        return JsonResponse({"success": True})


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'), name='dispatch')
class UpdateAntennaView(View):
    form_class = AntennaForm

    def get(self, request, antenna_id):
        try:
            antenna = get_object_or_404(antennas, pk=antenna_id)
            form = self.form_class(instance=antenna)
            html = render_to_string(
                "setting/partials/antenna_form.html", {"form": form}, request=request)
            return JsonResponse({"form_html": html, 'status': 200}, status=200)
        except Exception as e:
            return JsonResponse({'status': 500, 'error': e}, status=500)

    def post(self, request, antenna_id):
        try:
            antenna = get_object_or_404(antennas, pk=antenna_id)
            form = self.form_class(request.POST, instance=antenna)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True, 'status': 200}, status=200)

            return JsonResponse({"success": False, "errors": form.errors, 'status': 500})
        except Exception as e:
            return JsonResponse({'status': 500, 'error': e}, status=500)


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'), name='dispatch')
class UserListPartialView(View):
    def get(self, request):
        users = User.objects.all()
        html = render_to_string(
            "setting/partials/user_list.html", {"users": users}, request=request)
        return JsonResponse({"html": html})


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'), name='dispatch')
class CreateUserView(View):
    def get(self, request):
        form = CusstomUserCreationForm()
        html = render_to_string(
            "setting/partials/user_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    def post(self, request):
        form = CusstomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        html = render_to_string(
            "setting/partials/user_form.html", {"form": form}, request=request)
        return JsonResponse({"success": False, "form_html": html})


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'), name='dispatch')
class DeleteUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return JsonResponse({"success": True})
