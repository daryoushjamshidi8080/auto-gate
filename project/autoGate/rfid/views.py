from rfid_manager import RfidManager
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from setting.models import antennas
from tag.models import Tag, TagPermission
import json
from django.views import View
from django.utils.decorators import method_decorator
from .models import AnonymousTag
from rfid_manager import rfid_manager
from setting.models import antennas


@method_decorator(csrf_exempt, name='dispatch')
class StopThread(View):
    def post(self, request):
        try:
            print('Stop Thread ================================================')

            data = json.loads(request.body)

            reader_id = data.get('antennaName')
            adder = data.get('antennaAdder')

            rfid_manager.stop_tread(reader_id, adder)
            return JsonResponse({'success': True, 'status': 200}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e), 'status': 500}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StartThread(View):
    def post(self, request):
        try:
            antenna = antennas.objects.all()

            info_reader = []
            for info in antenna:
                info_dict = dict()
                info_dict['addr'] = info.number
                info_dict['reader_id'] = info.name

                info_reader.append(info_dict)

            rfid_manager.start_readers(info_reader)
            return JsonResponse(
                {
                    'success': True,
                    'status': 200,
                    'readers': info_reader,
                    'count': len(info_reader)
                },
                status=200
            )
        except Exception as e:
            return JsonResponse(
                {
                    'success': False,
                    'error': str(e),
                    'status': 500
                },
                status=500
            )


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
                permission_ok = True
                print('tag found', tag.rule)

            AnonymousTag.objects.create(uid_anonymousTag=uid)
            tags = AnonymousTag.objects.all()
            if tags.count() > 10:
                extra = tags.count() - 10
                for i in tags[:extra]:
                    print(i.id)
                    i.delete()

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
