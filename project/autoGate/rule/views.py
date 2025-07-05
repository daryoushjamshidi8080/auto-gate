from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from tag.models import TagPermission
import json
from .forms import TagPermissionFrom
# Create your views here.


class RuleView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "rule/index.html")


class ListRuleView(LoginRequiredMixin, View):
    def get(self, request):
        rules = TagPermission.objects.all()
        print('=====================================================================')

        html = render_to_string("rule/partials/list_rule.html",
                                {'rules': rules}, request=request)
        return JsonResponse({'html': html, 'status': 200}, status=200)


class DeleteRuelView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            rule_id = data['id']
            print('rule id : ', rule_id)
            permission = TagPermission.objects.get(pk=rule_id)
            permission.delete()

            return JsonResponse({'status': 200}, status=200)
        except Exception as e:
            return JsonResponse({'status': 500, 'error': e}, status=500)


class CreateRuleView(LoginRequiredMixin, View):
    def get(self, request):
        form = TagPermissionFrom()
        html = render_to_string(
            'rule/partials/add_rule.html', {'form': form}, request=request)
        return JsonResponse({'html': html, 'status': 200}, status=200)

    def post(self, request):
        form = TagPermissionFrom(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, 'status': 200}, status=200)

        return JsonResponse({"success": False, "errors": form.errors, 'status': 500})


class UpdateRuleView(LoginRequiredMixin, View):
    def get(self, request, rule_id):
        try:
            # print('rule id : ', rule_id)
            rule = TagPermission.objects.get(pk=rule_id)

            form = TagPermissionFrom(instance=rule)
            html = render_to_string(
                'rule/partials/add_rule.html', {'form': form}, request=request)
            return JsonResponse({'status': 200, 'html': html}, status=200)
        except Exception as e:
            return JsonResponse({'status': 500, 'error': e}, status=500)

    def post(self, request, rule_id):
        try:
            rule = TagPermission.objects.get(pk=rule_id)
            form = TagPermissionFrom(request.POST, instance=rule)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True, 'status': 200}, status=200)

            return JsonResponse({"success": False, "errors": form.errors, 'status': 500})
        except Exception as e:
            return JsonResponse({'status': 500, 'error': e}, status=500)
