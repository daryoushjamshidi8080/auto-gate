from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .models import Logs


# Create your views here.


class LogsView(View):
    def get(self, request):
        return render(request, 'logs/index.html')


class ShowLogsView(View):
    def get(self, request):
        try:
            page_number = request.GET.get('page', 1)
            logs = Logs.objects.order_by('-create_at')
            paginator = Paginator(logs, 25)
            page_obj = paginator.get_page(page_number)

            html = render_to_string(
                'logs/partials/logs_list.html',
                {
                    'logs': page_obj,
                    'page_obj': page_obj
                },
                request=request
            )
            return JsonResponse({'html': html, 'status': 200}, status=200)
        except Exception as e:
            return JsonResponse({'error': e, 'status': 500}, status=500)
