from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .models import Logs
from .forms import LogsSearchForm

# Create your views here.


class LogsView(View):
    def get(self, request):
        return render(request, 'logs/index.html')


class ShowLogsView(View):
    form_class = LogsSearchForm

    def get(self, request):
        form = self.form_class
        print('request >>>>>>', request.GET.get('search'))

        if request.GET.get('search'):
            try:
                logs = Logs.objects.filter(
                    tag_number=request.GET.get('search'))
            except:
                logs = Logs.objects.all()
        else:
            logs = Logs.objects.all()

        page_number = request.GET.get('page', 1)

        paginator = Paginator(logs, 10)
        page_obj = paginator.get_page(page_number)

        html = render_to_string(
            'logs/partials/logs_list.html',
            {
                'logs': page_obj,
                'page_obj': page_obj,
                'form': form
            },
            request=request
        )

        return JsonResponse(
            {
                "html": html,
                'status': 200,
            },
            status=200
        )
