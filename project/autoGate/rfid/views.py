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
from tag.models import TagPermission


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

            # print('uid :', uid)

            # print('**/****************************************************************')

            try:

                tag = Tag.objects.filter(uid=uid).first()
                antenna = antennas.objects.get(name=reader_id)

                permission = tag.rule

                found = tag is not None

                permission_ok = None

                # print('0000000000000000000000000000000000000000000000')
                # print('permission :', permission.antenna.all())
                # for i in permission.antenna.all():
                #     print(i)

                # # print()
                if tag and tag.is_active:
                    if permission.antenna.filter(id=antenna.id).exists():
                        permission_ok = True
                    else:
                        permission_ok = False

            except Exception as e:
                print('⛓️‍💥 ⛓️‍💥not found tag -> Exception:', str(e))
                permission_ok = False

            print('**/****************************************************************')
            print(
                '======================================================================')

            # if permission.antenna.exists() and antenna in permission.antenna.all():
            #     permission_ok = True
            # elif not permission.antenna.exists():
            #     permission_ok = False
            # else:
            #     permission_ok = False

            # if found:
            #     # permission_ok = True
            #     print('tag found', tag.rule)

            AnonymousTag.objects.create(
                uid_anonymousTag=uid, antenna=reader_id)
            tags_anonymous = AnonymousTag.objects.all()
            if tags_anonymous.count() > 400:
                extra = tags_anonymous.count() - 400
                for i in tags_anonymous[:extra]:
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


@method_decorator(csrf_exempt, name='dispatch')
class UpdateStatus(View):
    def post(self, request):
        try:
            print('hi')
            payload = json.loads(request.body.decode('utf-8'))
            print(payload)
            reader_id = payload.get('reader_id')
            status = payload.get('status')

            antenna = antennas.objects.get(name=reader_id)
            antenna.status = status
            antenna.save()

            return JsonResponse({'success': True, 'status': 200}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e), 'status': 400})
