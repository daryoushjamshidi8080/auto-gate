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
from logs.models import Logs
from datetime import datetime, timedelta
import os


@method_decorator(csrf_exempt, name='dispatch')
class StopThread(View):
    def post(self, request):
        try:
            # print('Stop Thread ================================================')

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


tag_access_times = {}


def check_tag_access(uid,  dellay=30):
    now = datetime.now()
    last_access = tag_access_times.get(uid)

    if last_access:
        diff = (now - last_access).total_seconds()
        if diff < dellay:
            tag_access_times[uid] = now
            return False

        else:
            tag_access_times[uid] = now
            return True
    else:
        tag_access_times[uid] = now
        return True


BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)


@method_decorator(csrf_exempt, name='dispatch')
class ReadTag(View):
    def get(self, request):
        return JsonResponse({'success': False, 'error': 'Only POST allowed', 'status': 405})

    def post(self, request):
        try:
            payload = json.loads(request.body.decode())
            uid = payload.get('uid')
            reader_id = payload.get('reader_id')
            # print('reader_id : ', reader_id)
            # print('---------------------------------------------------------')
            antenna = antennas.objects.get(name=reader_id)
            print('antenna : ', antenna)
            # print('---------------------------------------------------------')
            # print('antenna : ', antenna)
            # name_antenna = antenna

            open_time = check_tag_access(uid, antenna.open_time)

            print('open_time : ', open_time)

            # last_acc
            if not uid:
                raise ValueError('uid field is required')

            try:
                # print(80)
                tag = Tag.objects.filter(uid=uid).first()
                # print(81)
                permission = tag.rule
                # print(82)
                found = tag is not None
                # print(83)
                permission_ok = False
                # print(84)
                status = 'successful'
                if open_time:
                    permission = TagPermission.objects.filter(
                        is_active=True,
                        permission_name=permission
                    ).first()

                    list_antennas = []

                    for i in permission.antenna.all():
                        list_antennas.append(int(i.number))

                    if antenna.number in list_antennas:
                        permission_ok = True
                    else:
                        status = 'traffic'

                    print('antenna.is_active : ', antenna.is_active)
                    if tag.is_active == False or antenna.is_active == False:
                        status = 'noactive'
                        permission_ok = False

                    Logs.objects.create(
                        tag_number=tag.tag_number,
                        uid=uid,
                        status=status,
                        rule=permission,
                        door=antenna.name,
                        unit_number=tag.pelicula,
                        car_name=tag.car_name,
                        owner_name=tag.owner_name
                    )

                logss = Logs.objects.all().order_by('create_at')
                log_filename = os.path.join(
                    BACKUP_DIR, 'backup_deleted_logs.txt')

                if logss.count() > 30000:
                    extra = logss.count() - 30000
                    for log in logss[:extra]:
                        with open(log_filename, 'a', encoding='utf-8') as f:
                            f.write(
                                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                                f"Deleted Log - Owner: {log.owner_name} | Car: {log.car_name} | "
                                f"Unit: {log.unit_number} | Tag: {log.tag_number} | Status: {log.status}\n"
                                f"UID: {log.uid} | Rule: {log.rule} | Door: {log.door}\n"
                                f" log time : {log.create_at}\n"
                            )
                        log.delete()
            except Exception as e:
                print('⛓️‍💥 ⛓️‍💥not found tag ')
                permission_ok = False

            if open_time:
                print('---------------------------------------------------------')
                print('antenna=antenna.name : ', reader_id)
                AnonymousTag.objects.create(
                    uid_anonymousTag=uid, antenna=reader_id)
                tags_anonymous = AnonymousTag.objects.all()
                if tags_anonymous.count() > 400:
                    extra = tags_anonymous.count() - 400
                    for i in tags_anonymous[:extra]:
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
            print('zarttttttttttttttttttttttttttttttttttttttttttttttttttt')
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
