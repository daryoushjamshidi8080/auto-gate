from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Tag
from django.template.loader import render_to_string
from .forms import TagForm, SearchTagForm, SearchTagAnonymousForm
from rfid.models import AnonymousTag
from django.core.paginator import Paginator


# Create your views here.


class TagView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "tag/index.html")


class ListTagView(LoginRequiredMixin, View):
    form_class = SearchTagForm

    def get(self, request):
        form = self.form_class()
        tags = Tag.objects.all().order_by('-create_at')

        if request.GET.get('search_tag'):
            try:
                tags = Tag.objects.filter(
                    tag_number=request.GET.get('search_tag')).order_by('-create_at')
            except:
                tags = Tag.objects.all().order_by('-create_at')

        page_number = request.GET.get('page', 1)

        paginator = Paginator(tags, 10)
        page_obj = paginator.get_page(page_number)

        html = render_to_string(
            "tag/partials/list_tag.html",
            {
                "tags": page_obj,
                'page_obj': page_obj,
                'form': form
            },
            request=request
        )
        return JsonResponse(
            {
                "html": html,
                'status': 200
            },
            status=200
        )


class AddTagView(LoginRequiredMixin, View):
    def get(self, request):

        form = TagForm()
        html = render_to_string(
            "tag/partials/add_tag.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html, 'status': 200}, status=200)

    def post(self, request):
        number_tag = []
        number = None

        tags = Tag.objects.all()
        for number in tags:
            number_tag.append(number.tag_number)

        if len(number_tag) == 0:
            number = 1
        else:
            for i in range(len(number_tag)+1):
                if not ((i + 1) in number_tag):
                    number = i + 1
                    break

        form = TagForm(request.POST)
        if form.is_valid():
            tag_instance = form.save(commit=False)
            tag_instance.tag_number = number
            tag_instance.save()

            return JsonResponse({"success": True, 'status': 200}, status=200)
        else:
            return JsonResponse({"success": False, "errors": form.errors, 'status': 500})


class TagAnonymous(LoginRequiredMixin, View):
    form_class = SearchTagAnonymousForm

    def get(self, request):
        form = self.form_class
        print(request.GET)
        if request.GET.get('search_tag_anonymous'):
            anonymous_tag_all = AnonymousTag.objects.filter(
                uid_anonymousTag=request.GET.get('search_tag_anonymous')).order_by('-create_at')

        else:
            anonymous_tag_all = AnonymousTag.objects.all().order_by('-create_at')

        page_number = request.GET.get('page', 1)

        paginator = Paginator(anonymous_tag_all, 10)
        page_obj = paginator.get_page(page_number)

        tags = Tag.objects.all()
        tag_list = [tag.uid for tag in tags]

        html = render_to_string(
            'tag/partials/list_anonymous_tag.html',
            {
                'tagAnonymous': page_obj,
                'tag_list': tag_list,
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


class UpdateTagView(LoginRequiredMixin, View):
    def get(self, request, tag_id):
        try:
            tag = Tag.objects.get(pk=tag_id)
            form = TagForm(instance=tag)
            html = render_to_string(
                'tag/partials/add_tag.html', {'form': form}, request=request)
            return JsonResponse({'status': 200, 'html': html}, status=200)
        except Exception as e:
            return JsonResponse({'status': 500, 'error': e}, status=500)

    def post(self, request, tag_id):
        try:
            tag = Tag.objects.get(pk=tag_id)
            number = tag.tag_number
            form = TagForm(request.POST, instance=tag)
            if form.is_valid():
                tag_instance = form.save(commit=False)
                tag_instance.tag_number = number
                form.save()
                return JsonResponse({"success": True, 'status': 200}, status=200)

            return JsonResponse({"success": False, "errors": form.errors, 'status': 500})
        except Exception as e:
            return JsonResponse({'status': 500, 'error': e}, status=500)
