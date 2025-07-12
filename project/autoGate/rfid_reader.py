# from threading import Thread, Lock, Event
# from threading import Thread, Lock
# import serial.tools.list_ports
# import serial
# import time
# import requests
# import json
# from threading import Thread, Event, Lock
# # from dotenv import load_dotenv
# import os
# import re

# # SERVER_IP = os.getenv("SERVER_IP")
# # SERVER_PORT = os.getenv("SERVER_PORT")

# # list IDs of Arfid device
# ALLOWED_DEVICES = [
#     ('1a86', '7523')
# ]


# def connect_to_rfid():
#     print('✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ man shoroo be kar kadam')
#     ports = serial.tools.list_ports.comports()

#     for port in ports:
#         vid = format(port.vid, '04x') if port.vid else ''
#         pid = format(port.pid, '04x') if port.pid else ''
#         # print('vid : ', vid, '  /  pid : ', pid)

#         if (vid, pid) in ALLOWED_DEVICES:
#             try:
#                 ser = serial.Serial(port.device, 9600, timeout=1)
#                 print(f"✅ connected to RFID: {port.device}")
#                 return ser
#             except serial.SerialException:
#                 print(f"❌ error in connections : {port.device}: ")
#     return None


# # connect to rfid
# ser = connect_to_rfid()

# print('serisal  :       ser :', ser)


# def checksum(*bs):
#     cmd = []
#     for num in bs:
#         cmd.append(int(num, 16))
#     total = sum(cmd)
#     return hex((4095 - (total - 1)) & 0xFF)


# def make_cmd(addr, *args):
#     cmd = ['0x0A', hex(addr)]
#     cmd_str = ''
#     for arg in args:
#         cmd.append(hex(int(arg)))
#     for hexnum in cmd:
#         car = hexnum[2:]

#         if len(car) == 1:
#             car = int(car)
#         cmd_str += '{:02}'.format(car) + ' '
#     cmd = cmd_str[:-1].split(' ')
#     check_sum = checksum(*cmd)

#     cmd_str += check_sum[2:]
#     # print(cmd_str)
#     return bytes.fromhex(cmd_str)


# class RfidThread(Thread):
#     def __init__(self, ser: serial.Serial, lock: Lock, stop_evt: Event, info_reader: dict):
#         super().__init__(daemon=True)

#         self.ser = ser
#         self.lock = lock
#         self.info_reader = info_reader
#         self.stop_evt = stop_evt
#         self.last_frame = None
#         self.status_rfid = dict()

#     def run(self):

#         while not self.stop_evt.is_set():
#             try:
#                 with self.lock:
#                     # print('self.info_reader : ', self.info_reader)
#                     print('start new forrrrrrrrrrrrrrrrrrrrrrrr')
#                     for info in self.info_reader:
#                         print(
#                             '==========================================================')
#                         if self.stop_evt.is_set():
#                             break

#                         cmd_scan = make_cmd(
#                             info['addr'], 0x03, 0x80, 0x01)
#                         cmd_uid = make_cmd(
#                             info['addr'], 0x03, 0x40, 0x01)
#                         cmd_clear = make_cmd(info['addr'], 0x02, 0x44)
#                         cmd_active_rellay = make_cmd(
#                             info['addr'], 0x04, 0x2d, 0x02, 0x01)
#                         cmd_deactive_rellay = make_cmd(
#                             info['addr'], 0x04, 0x2d, 0x02, 0x00)

#                         self.ser.write(cmd_scan)

#                         resp = self.ser.read(64)
#                         print(0)
#                         print('😁 respons : ', resp.hex())
#                         print(1)
#                         data = str(resp.hex())
#                         print(2)
#                         addr = format(int(info['addr']), '02x')
#                         print(3)
#                         print('addr : ', addr)
#                         print(4)
#                         pattern = f"0b{addr}03[a-f0-9]{{6}}"
#                         print(5)
#                         frames = re.findall(pattern, data)
#                         print(6)
#                         print("frames : ", frames)
#                         print(7)
#                         print('info  :', info)

#                         # status = 'Online' if len(resp) >= 6 and len(
#                         #     resp) != 9 else 'Offline'

#                         # if self.status_rfid.get(info['reader_id']) is None or self.status_rfid.get(info['reader_id']) != status:
#                         #     self.status_rfid[info['reader_id']] = status
#                         #     print('ok')

#                         #     requests.post('http://127.0.0.1:8000/rfid/update_status/',
#                         #                   json={
#                         #                       "reader_id": info['reader_id'],
#                         #                       "status": status
#                         #                   }
#                         #                   )

#                         # if resp and resp.hex() != self.last_frame:
#                         if frames:
#                             if str(frames[0][8:10]) != '00':
#                                 print('👌🏻ok')
#                                 # time.sleep(2)
#                                 # self.last_frame = resp.hex()

#                                 self.ser.write(cmd_uid)
#                                 print(8)
#                                 uid_resp = self.ser.read(64)
#                                 print(9)
#                                 print('uid_resp : ', uid_resp.hex())
#                                 print(10)
#                                 self.ser.write(cmd_clear)
#                                 print(11)

#                                 uid_hex_full = uid_resp.hex()
#                                 print(11)

#                                 if len(uid_hex_full) >= 28:
#                                     uid_hex = uid_hex_full[12:28]

#                                     if uid_hex:
#                                         pass
#                                         try:
#                                             print('readdd')
#                                             respons_reque = requests.post(
#                                                 "http://127.0.0.1:8000/rfid/read_tag/",
#                                                 json={
#                                                     'uid': uid_hex,
#                                                     "reader_id": info['reader_id']
#                                                 },
#                                                 timeout=3
#                                             )

#                                             data = respons_reque.json()
#                                         except:
#                                             pass
#                                         print('data response tag :', data)
#                                         print(data.get('allowed'))
#                                         if data.get('allowed'):
#                                             self.ser.write(cmd_active_rellay)
#                                             self.ser.write(
#                                                 cmd_deactive_rellay)

#                                         print(
#                                             f"✅ [{info['reader_id']}] UID:", uid_hex)
#                             else:
#                                 print('🫠 not ok')
#                                 self.ser.write(cmd_clear)
#                             time.sleep(0.03)

#                     time.sleep(0.03)
#             except Exception as e:
#                 status = 'Offline'
#                 for info in self.info_reader:
#                     if self.status_rfid.get(info['reader_id']) is None or self.status_rfid.get(info['reader_id']) != status:
#                         self.status_rfid[info['reader_id']] = 'Offline'
#                         print('ok')

#                         requests.post('http://127.0.0.1:8000/rfid/update_status/',
#                                       json={
#                                           "reader_id": info['reader_id'],
#                                           "status": 'Offline'
#                                       }
#                                       )

#                 print('⚠️⚠️ Connection lost. Trying to reconnect... error is :', e)
#                 self.ser.close()
#                 self.ser = None
#                 while not self.ser:
#                     if not self.ser:
#                         try:
#                             print('hey')
#                             ser = connect_to_rfid()
#                             self.ser = serial.Serial(
#                                 ser.port, 9600, timeout=0.09)
#                         except:
#                             # self.ser = ser.port
#                             print('⏳ Reconnecting in 5 seconds...')
#                     time.sleep(0.03)

#                     print(
#                         f"⚠️ [reconnecting !!! is error : {e}")
#                 time.sleep(0.03)


# # فرض بر این است که
# # ایجاد قفل و رویداد توقف


# # if __name__ == '__main__':
# #     print('🏁 start ')

# #     reader_info = [
# #         {'addr': 210, 'reader_id': 'D2', 'port': '/dev/ttyUSB0'},
# #         {'addr': 211, 'reader_id': 'D3', 'port': '/dev/ttyUSB0'},
# #     ]

# #     rfid_handler = RfidThread(
# #         ser=serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1),
# #         lock=Lock(), stop_evt=Event(), info_reader=reader_info)

# #     rfid_handler.start()

# #     rfid_handler.join()

#     # lock = Lock()
#     # stop_event = Event()
#     # # ایجاد و شروع دو ترد
#     # reader1 = RfidThread(ser=serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1),
#     #                      lock=lock, addr=210, reader_id='D2', stop_evt=stop_event)
#     # reader2 = RfidThread(ser=serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1), lock=lock,
#     #                      addr=211, reader_id='D3', stop_evt=stop_event)

#     # reader1.start()
#     # reader2.start()
#     # reader1.join()
#     # reader2.join()

#     # برای متوقف کردن تردها، می‌توانید از stop_event استفاده کنید
# # به عنوان مثال:
# # time.sleep(10)  # بعد از 10 ثانیه
# # stop_event.set()  # توقف تردها
from threading import Thread, Lock, Event
from threading import Thread, Lock
import serial.tools.list_ports
import serial
import time
import requests
import json
from threading import Thread, Event, Lock
import re
# from dotenv import load_dotenv
import os

# SERVER_IP = os.getenv("SERVER_IP")
# SERVER_PORT = os.getenv("SERVER_PORT")

# list IDs of Arfid device
ALLOWED_DEVICES = [
    ('1a86', '7523')
]


def connect_to_rfid():
    print('✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ man shoroo be kar kadam')
    ports = serial.tools.list_ports.comports()

    for port in ports:
        vid = format(port.vid, '04x') if port.vid else ''
        pid = format(port.pid, '04x') if port.pid else ''
        # print('vid : ', vid, '  /  pid : ', pid)

        if (vid, pid) in ALLOWED_DEVICES:
            try:
                ser = serial.Serial(port.device, 9600, timeout=1)
                print(f"✅ connected to RFID: {port.device}")
                return ser
            except serial.SerialException:
                print(f"❌ error in connections : {port.device}: ")
    return None


# connect to rfid
ser = connect_to_rfid()

print('serisal  :       ser :', ser)


def checksum(*bs):
    cmd = []
    for num in bs:
        cmd.append(int(num, 16))
    total = sum(cmd)
    return hex((4095 - (total - 1)) & 0xFF)


def make_cmd(addr, *args):
    cmd = ['0x0A', hex(addr)]
    cmd_str = ''
    for arg in args:
        cmd.append(hex(int(arg)))
    for hexnum in cmd:
        car = hexnum[2:]

        if len(car) == 1:
            car = int(car)
        cmd_str += '{:02}'.format(car) + ' '
    cmd = cmd_str[:-1].split(' ')
    check_sum = checksum(*cmd)

    cmd_str += check_sum[2:]
    # print(cmd_str)
    return bytes.fromhex(cmd_str)


class RfidThread(Thread):
    def __init__(self, ser: serial.Serial, lock: Lock, stop_evt: Event, info_reader: dict):
        super().__init__(daemon=True)

        self.ser = ser
        self.lock = lock
        self.info_reader = info_reader
        self.stop_evt = stop_evt
        # self.last_frame = None
        self.status_rfid = dict()

    def run(self):

        while not self.stop_evt.is_set():
            try:
                with self.lock:
                    # print('self.info_reader : ', self.info_reader)
                    # time.sleep(0.01)
                    print('=====================================')
                    x = 0
                    for info in self.info_reader:
                        x += 1
                        print('🥲🥲🥲🥲🥲🥲🥲🥲🥲🥲 rund : ', x)
                        print('for : info: ', info)
                        if self.stop_evt.is_set():
                            # print('🥲🥲🥲🥲🥲🥲🥲🥲🥲🥲🥲')
                            break

                        cmd_scan = make_cmd(
                            info['addr'], 0x03, 0x80, 0x01)
                        cmd_uid = make_cmd(
                            info['addr'], 0x03, 0x40, 0x01)
                        cmd_clear = make_cmd(info['addr'], 0x02, 0x44)
                        cmd_active_rellay = make_cmd(
                            info['addr'], 0x04, 0x2d, 0x02, 0x01)
                        cmd_deactive_rellay = make_cmd(
                            info['addr'], 0x04, 0x2d, 0x02, 0x00)
                        self.ser.write(cmd_clear)
                        time.sleep(0.03)
                        self.ser.write(cmd_scan)
                        time.sleep(0.03)
                        resp = self.ser.read(32)
                        # print(-1)
                        # self.ser.write(cmd_clear)

                        # print(0)
                        #
                        print('😁 respons : ', resp.hex())
                        # print(1)
                        data = str(resp.hex())
                        # print(2)
                        addr = format(int(info['addr']), '02x')
                        # print(3)
                        print('addr : ', addr)
                        # print(4)
                        pattern = f"0b{addr}03[a-f0-9]{{6}}"
                        # print(5)
                        frames = re.findall(pattern, data)
                        # print(6)
                        print("frames : ", frames)
                        # print(7)
                        # print('info  :', info)
                        print('resp  read : ', resp)

                        if frames:
                            if addr == frames[0][2:4]:
                                status = 'online'
                            else:
                                status = 'offline'
                        else:
                            status = 'offline'

                        print(status)

                        if self.status_rfid.get(info['reader_id']) is None or self.status_rfid.get(info['reader_id']) != status:
                            self.status_rfid[info['reader_id']] = status
                            # print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                            requests.post('http://127.0.0.1:8000/rfid/update_status/',
                                          json={
                                              "reader_id": info['reader_id'],
                                              "status": status
                                          }
                                          )
                            # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                        if frames:
                            print('par :   ', frames[0][9:10])
                            if str(frames[0][9:10]) != '0':
                                print('hi')
                                # self.ser.write(cmd_clear)
                                time.sleep(0.03)
                                self.ser.write(cmd_uid)
                                respost = self.ser.read(64)

                                print('🍆🍆🍆🍆🍆repost:', respost.hex()[12:28])
                                self.ser.write(cmd_clear)
                                uid_hex = respost.hex()[12:28]
                                if uid_hex:
                                    try:
                                        respons_reque = requests.post(
                                            "http://127.0.0.1:8000/rfid/read_tag/",
                                            json={
                                                'uid': uid_hex,
                                                "reader_id": info['reader_id']
                                            },
                                            timeout=3
                                        )

                                        data = respons_reque.json()
                                        # print('🥲🥲🥲🥲🥲🥲🥲🥲🥲🥲🥲')
                                    except:
                                        pass
                                    print('data response tag :', data)
                                    print(data.get('allowed'))
                                    if data.get('allowed'):
                                        self.ser.write(cmd_active_rellay)
                                        # self.ser.write()
                                        self.ser.write(
                                            cmd_deactive_rellay)
            except Exception as e:
                status = 'Offline'
                for info in self.info_reader:
                    if self.status_rfid.get(info['reader_id']) is None or self.status_rfid.get(info['reader_id']) != status:
                        self.status_rfid[info['reader_id']] = 'Offline'
                        print('ok')

                        requests.post('http://127.0.0.1:8000/rfid/update_status/',
                                      json={
                                          "reader_id": info['reader_id'],
                                          "status": 'Offline'
                                      }
                                      )

                print('⚠️⚠️ Connection lost. Trying to reconnect... error is :', e)
                self.ser.close()
                self.ser = None
                while not self.ser:
                    if not self.ser:
                        try:
                            print('hey')
                            ser = connect_to_rfid()
                            self.ser = serial.Serial(
                                ser.port, 9600, timeout=0.1)
                        except:
                            # self.ser = ser.port
                            print('⏳ Reconnecting in 5 seconds...')
                    time.sleep(0.03)

                    print(
                        f"⚠️ [reconnecting !!! is error : {e}")
                time.sleep(0.03)


# فرض بر این است که
# ایجاد قفل و رویداد توقف


if __name__ == '__main__':
    print('🏁 start ')

    reader_info = [
        {'addr': 210, 'reader_id': 'D2', 'port': '/dev/ttyUSB0'},
        {'addr': 211, 'reader_id': 'D3', 'port': '/dev/ttyUSB0'},
    ]

    rfid_handler = RfidThread(
        ser=serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1),
        lock=Lock(), stop_evt=Event(), info_reader=reader_info)

    rfid_handler.start()

    rfid_handler.join()

    # lock = Lock()
    # stop_event = Event()
    # # ایجاد و شروع دو ترد
    # reader1 = RfidThread(ser=serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1),
    #                      lock=lock, addr=210, reader_id='D2', stop_evt=stop_event)
    # reader2 = RfidThread(ser=serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1), lock=lock,
    #                      addr=211, reader_id='D3', stop_evt=stop_event)

    # reader1.start()
    # reader2.start()
    # reader1.join()
    # reader2.join()

    # برای متوقف کردن تردها، می‌توانید از stop_event استفاده کنید
# به عنوان مثال:
# time.sleep(10)  # بعد از 10 ثانیه
# stop_event.set()  # توقف تردها
