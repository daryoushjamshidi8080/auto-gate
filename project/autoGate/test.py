# import port serial.tools.list_ports
# import serial
# import time
# import requests
# import json
# from threading import Thread, Event, Lock


# # def checksum(*bs):
# #     total = sum(bs)
# #     return (4095 - (total - 1)) & 0xFF


# API_URL = "http://127.0.0.1:8000/rfid/read_tag/"


# def send_uid_to_server(uid, reader='gate-1'):
#     try:
#         payload = {"uid": uid, "reader_id": reader}
#         res = requests.post(API_URL, json=payload, timeout=3)
#         print("🔗 Server response:", res.json())

#     except Exception as e:
#         print("⚠️  Could not reach server:", e)


# # list IDs of Arfid device
# ALLOWED_DEVICES = [
#     ('1a86', '7523')
# ]


# def connect_to_rfid():
#     ports = serial.tools.list_ports.comports()

#     for port in ports:
#         vid = format(port.vid, '04x') if port.vid else ''
#         pid = format(port.pid, '04x') if port.pid else ''

#         if (vid, pid) in ALLOWED_DEVICES:
#             try:
#                 ser = serial.Serial(port.device, 9600, timeout=1)
#                 print(f"✅ connected to RFID: {port.device}")
#                 return ser
#             except serial.SerialException:
#                 print(f"❌ error in connections : {port.device}: {e}")
#     return None


# # connect to rfid
# ser = connect_to_rfid()


# def ceachar(*args):
#     data = 0
#     for number in args:
#         number_des = int(number, 16)
#         data += number_des
#     data = 4095-(data - 1)
#     return hex(data & 255)


# # فرمان خواندن تگ (بسته به مدل دستگاه ممکنه فرق کنه)
# ceach_sum = ceachar('0A', 'D2', '03', '80', '01')[-2:]
# get_tag = bytes.fromhex(f'0A D2 03 80 01 {ceach_sum}')


# last_uid = None  # برای جلوگیری از تکرار پشت‌سر‌هم

# print("🎯 lisining to read tag!")

# while True:
#     try:
#         # ارسال دستور برای دریافت UID
#         ser.write(get_tag)
#         # time.sleep(0.03)

#         # خواندن پاسخ
#         response = ser.read(64)
#         if response:
#             uid = response.hex()

#             if uid != last_uid:
#                 print("📥 read new tag:", uid)
#                 last_uid = uid

#                 # get UID tag befor get tag
#                 ceach_sum = ceachar('0A', 'D3', '03', '40', '01')[-2:]
#                 get_uid_tag = bytes.fromhex(f'0A D3 03 40 01 {ceach_sum}')
#                 ser.write(get_uid_tag)
#                 response_UID = ser.read(64)
#                 real_uid = response_UID.hex()[6*2:14*2]
#                 print('📥 UID:', real_uid)
#                 send_uid_to_server(real_uid, reader="gate-1")
#                 # time.sleep(0.03)

#                 # clear data of buffer befor get UID tag
#                 ceach_sum = ceachar('0A', 'D3', '02', '44')[-2:]
#                 clear_data = bytes.fromhex(f'0A D3 02 44 {ceach_sum}')
#                 ser.write(clear_data)
#             else:
#                 print("🔁Duplicate - Previous tag is close.")
#         else:
#             print("⏳No response from the device...")

#         time.sleep(0.03)

#     except (serial.SerialException, OSError):
#         print('⚠️ Connection lost. Trying to reconnect...')
#         ser.close()
#         ser = None
#         while not ser:
#             ser = connect_to_rfid()
#             if not ser:
#                 print('⏳ Reconnecting in 5 seconds...')
#                 time.sleep(1)

#     except Exception as e:
#         print("❌ error in connections")
#         break


# # بستن ارتباط
# ser.close()

# print("🏁 end")


# # ports = serial.tools.list_ports.comports()
# Windsurf Plugin (formerly Codeium): AI Coding Autocomplete and Chat for Python, JavaScript, TypeScript, and more
# Windsurf: Unable to download language server. If issues persist after restarting your IDE, please contact vscode@windsurf.com. Attempted download URL: https://releases.codeiumdata.com/language-server-v1.48.2/language_server_linux_x64.gz.

# # for i in ports:
# #     print(i)
