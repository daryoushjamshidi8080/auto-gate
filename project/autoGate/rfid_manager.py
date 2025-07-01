from rfid_reader import RfidThread
from threading import Thread, Lock, Event
import serial


# list IDs of Arfid device
ALLOWED_DEVICES = [
    ('1a86', '7523')
]


def connect_to_rfid():
    # print('✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ man shoroo be kar kadam')
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


class RfidManager:
    def __init__(self):
        self.lock = Lock()
        self.thread = None
        self.info_thread = []

    def start_readers(self, reader_info: dict):
        """
            reader_info : list of dicts like:
            [
                {'adder' : 210, 'reader_id' : 'oneDoor', port:'/devttyUSB0' },
                {'adder' : 211, 'reader_id' : 'oneDoor', port:'/devttyUSB0' },
            ]
        """

        print('🛑 Stopping previous thread:', self.thread)
        if self.thread:
            self.thread.stop_evt.set()
            # self.thread.join()  # خیلی مهم
            print('✅ Previous thread fully stopped.')

        self.info_thread = reader_info
        stop_event = Event()
        ser = connect_to_rfid()
        ser = serial.Serial(ser.port, 9600, timeout=0.1)
        thread = RfidThread(
            ser=ser,
            lock=self.lock,
            stop_evt=stop_event,
            info_reader=reader_info
        )
        thread.start()
        self.thread = thread

    def stop_tread(self, reader_id, adder):

        to_remove = None
        for index, info in enumerate(self.info_thread):
            print('index : ', index, 'info : ', info)
            if info['reader_id'] == reader_id and int(info['addr']) == int(adder):
                print('info thread : ', self.info_thread)
                self.info_thread.pop(index)
                to_remove = True
                break

        if to_remove:
            if self.thread:
                self.thread.stop_evt.set()
                # self.thread.join()
                self.thread = None

            if self.info_thread:
                self.start_readers(self.info_thread)

            print('sucsses delete hoooraaaa')
            return True

        else:
            print(f"⚠️ Reader {reader_id} - {adder} not found.")
            return False


rfid_manager = RfidManager()


if __name__ == '__main__':
    print('🏁 start ')

    reader_info = [
        {'addr': 210, 'reader_id': 'D2', 'port': '/dev/ttyUSB0'},
        {'addr': 211, 'reader_id': 'D3', 'port': '/dev/ttyUSB0'},
    ]

    rfid_manager = RfidManager()

    rfid_manager.start_readers(reader_info=reader_info)

    # rfid_manager.start()

    # rfid_manager.join()
