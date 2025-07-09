from django.apps import AppConfig
from threading import Thread
from time import sleep


class RfidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rfid"

    def ready(self):

        # return super().ready()

        def delayed_start():
            from rfid_manager import rfid_manager
            from setting.models import antennas

            sleep(2)

            antennas = antennas.objects.all()

            info_reader = []
            for info in antennas:
                info_dict = dict()
                info_dict['addr'] = info.number
                info_dict['reader_id'] = info.name

                info_reader.append(info_dict)

            rfid_manager.start_readers(info_reader)

        Thread(target=delayed_start, daemon=True).start()
