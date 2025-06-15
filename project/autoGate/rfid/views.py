from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from setting.models import antennas
from tag.models import Tag, TagPermission
import json
from django.views import View
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class ReadTag(View):
    def get(self, request):
        return JsonResponse({'success': False, 'error': 'Only POST allowed', 'status': 405})

    def post(self, request):
        try:
            payload = json.loads(request.body.decode())
            uid = payload.get('uid')
            reader_id = payload.get('reader_id', '')

            if not uid:
                raise ValueError('uid field is required')

            print('uid :', uid)
            tag = Tag.objects.filter(uid=uid).first()
            found = tag is not None

            permission_ok = False
            if found:
                print('tag found', tag.rule)

            return JsonResponse(
                {
                    'success': True,
                    'found': found,
                    'allowed': permission_ok,
                    'status': 200
                }
            )
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e), 'status': 400})
