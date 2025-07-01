from threading import Thread, Lock, Event
from threading import Thread, Lock
import serial.tools.list_ports
import serial
import time
import requests
import json
from threading import Thread, Event, Lock


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
        self.last_frame = None
        self.status_rfid = dict()

    def run(self):

        while not self.stop_evt.is_set():
            try:
                with self.lock:
                    print(self.info_reader)
                    for info in self.info_reader:
                        if self.stop_evt.is_set():
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

                        self.ser.write(cmd_scan)

                        resp = self.ser.read(16)
                        # print(
                        #     f'name : {info["reader_id"]},,,,,,, reponse ::::::::::::: ',  len(resp))
                        status = 'Online' if len(resp) >= 6 and len(
                            resp) != 9 else 'Offline'
                        # print(
                        #     f'reader name : {info["reader_id"]} """""""""""  { status } ')

                        if self.status_rfid.get(info['reader_id']) is None or self.status_rfid.get(info['reader_id']) != status:
                            self.status_rfid[info['reader_id']] = status
                            print('ok')

                            requests.post('http://127.0.0.1:8000/rfid/update_status/',
                                          json={
                                              "reader_id": info['reader_id'],
                                              "status": status
                                          }
                                          )

                        if resp and resp.hex() != self.last_frame:
                            self.last_frame = resp.hex()

                            self.ser.write(cmd_uid)

                            uid_resp = self.ser.read(16)

                            uid_hex_full = uid_resp.hex()
                            if len(uid_hex_full) >= 28:
                                uid_hex = uid_hex_full[12:28]
                                if uid_hex:
                                    respons_reque = requests.post(
                                        "http://127.0.0.1:8000/rfid/read_tag/",
                                        json={
                                            'uid': uid_hex,
                                            "reader_id": info['reader_id']
                                        },
                                        timeout=3
                                    )
                                    data = respons_reque.json()
                                    print('data response tag :', data)
                                    print(data.get('allowed'))
                                    if data.get('allowed'):
                                        self.ser.write(cmd_active_rellay)
                                        self.ser.write(
                                            cmd_deactive_rellay)

                                    print(
                                        f"✅ [{info['reader_id']}] UID:", uid_hex)

                            self.ser.write(cmd_clear)
                            time.sleep(0.03)

                    time.sleep(0.03)
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

                print('⚠️ Connection lost. Trying to reconnect... error is :', e)
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
                    time.sleep(1)

                print(
                    f"⚠️ [reconnecting !!! is error : {e}")
                time.sleep(1)


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
