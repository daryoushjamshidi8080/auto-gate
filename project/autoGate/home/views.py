from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from logs.models import Logs


class home(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/index.html")


class ShowLogsHomeView(View):
    def get(self, request):
        try:
            logs = Logs.objects.all().order_by('-create_at')[:15]

            html = render_to_string(
                'home/partials/logs_list.html',
                {
                    'logs': logs,
                },
                request=request
            )
            return JsonResponse({'html': html, 'status': 200}, status=200)
        except Exception as e:
            return JsonResponse({'error': e, 'status': 500}, status=500)
