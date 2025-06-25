import multiprocessing
import multiprocessing.pool
from threading import Thread, Lock, Event
from threading import Thread, Lock
import serial.tools.list_ports
import serial
import time
import requests
import json
from threading import Thread, Event, Lock

ALLOWED_DEVICES = [
    ('1a86', '7523')
]


def connect_to_rfid():
    ports = serial.tools.list_ports.comports()

    for port in ports:
        vid = format(port.vid, '04x') if port.vid else ''
        pid = format(port.pid, '04x') if port.pid else ''

        if (vid, pid) in ALLOWED_DEVICES:
            try:
                ser = serial.Serial(port.device, 9600, timeout=1)
                print(f"✅ connected to RFID: {port.device}")
                return ser
            except serial.SerialException:
                print(f"❌ error in connections : {port.device}: ")
    return None


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


ser = connect_to_rfid()
last_frame = None


def rfid(data):
    global last_frame

    print(data)
    cmd_scan = make_cmd(data, 0x03, 0x80, 0x01)
    cmd_uid = make_cmd(data, 0x03, 0x40, 0x01)
    cmd_clear = make_cmd(data, 0x02, 0x44)

    try:
        # print(74)
        ser.write(cmd_scan)
        # print(75)
        time.sleep(0.3)
        resp = ser.read(64)
        # print(77)
        # if resp and resp.hex() != last_frame:
        # last_frame = resp.hex()
        # print(80)
        # time.sleep(0.03)

        ser.write(cmd_uid)
        # print(85)
        # time.sleep(0.3)
        uid_resp = ser.read(64)
        # print(87)
        uid_hex = uid_resp.hex()[12:28]
        # print(89)

        if uid_hex:
            print(f' {data:} uid : ', uid_hex)

        ser.write(cmd_clear)
        # time.sleep(0.1)

    except Exception as e:
        print(f'error is:  {e}')


if __name__ == '__main__':
    data_item = [210, 211]

    while True:

        with multiprocessing.Pool() as pool:
            pool.map(rfid, data_item)
        # time.sleep(0.1)

    # print(results)
