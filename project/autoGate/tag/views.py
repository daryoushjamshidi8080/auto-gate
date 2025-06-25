from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Tag
from django.template.loader import render_to_string
from .forms import TagForm
from rfid.models import AnonymousTag

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
        anonymous_tag = AnonymousTag.objects.all()
        tags = Tag.objects.all()
        tag_list = []
        for tag in tags:
            tag_list.append(tag.uid)

        print(tag_list)

        html = render_to_string('tag/partials/list_anonymous_tag.html',
                                {'tagAnonymous': anonymous_tag, 'tag_list': tag_list}, request=request)

        return JsonResponse({"html": html})

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
        print('=================================================================================== ')
        print('tags :', tags)
        html = render_to_string('tag/partials/list_tag.html',
                                {'tags': tags}, request=request)
        return JsonResponse({'html': html, 'status': 200}, status=200)
