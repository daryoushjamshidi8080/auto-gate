from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Tag
from django.template.loader import render_to_string
from .forms import TagForm
from rfid.models import AnonymousTag
from django.core.paginator import Paginator


# Create your views here.


class TagView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "tag/index.html")


class ListTagView(LoginRequiredMixin, View):
    def get(self, request):
        tags = Tag.objects.all()
        html = render_to_string(
            "tag/partials/list_tag.html", {"tags": tags}, request=request)
        return JsonResponse({"html": html})


class AddTagView(LoginRequiredMixin, View):
    def get(self, request):
        form = TagForm()
        html = render_to_string(
            "tag/partials/add_tag.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html, 'status': 200}, status=200)

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, 'status': 200}, status=200)
        else:
            return JsonResponse({"success": False, "errors": form.errors, 'status': 500})


class TagAnonymous(LoginRequiredMixin, View):
    def get(self, request):
        page_number = request.GET.get('page', 1)
        anonymous_tag_all = AnonymousTag.objects.all().order_by('-create_at')

        paginator = Paginator(anonymous_tag_all, 10)
        page_obj = paginator.get_page(page_number)

        tags = Tag.objects.all()
        tag_list = [tag.uid for tag in tags]

        html = render_to_string(
            'tag/partials/list_anonymous_tag.html',
            {
                'tagAnonymous': page_obj,
                'tag_list': tag_list,
                'page_obj': page_obj
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

    def post(self, request):
        pass


class DeleteTagView(LoginRequiredMixin, View):
    def post(self, request, tag_id):
        print('tag id : ', tag_id)
        try:
            tag = Tag.objects.get(pk=tag_id)
            print('tag >>>>>>> : ', tag)
        except Tag.DoesNotExist:
            return JsonResponse({'status': 404, 'message': 'تگ پیدا نشد'}, status=404)

        tag.delete()
        tags = Tag.objects.all()
        print('tags :', tags)
        html = render_to_string(
            'tag/partials/list_tag.html', {'tags': tags}, request=request)
        return JsonResponse({'html': html, 'status': 200}, status=200)
