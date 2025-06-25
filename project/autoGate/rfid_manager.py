from rfid_reader import RfidThread
from threading import Thread, Lock, Event
import serial


class RfidManager:
    def __init__(self):
        self.lock = Lock()
        self.stop_event = Event()
        self.threads = []

    def start_readers(self, reader_info):
        """
            reader_info : list of dicts like:
            [
                {'adder' : 210, 'reader_id' : 'oneDoor', port:'/devttyUSB0' },
                {'adder' : 211, 'reader_id' : 'oneDoor', port:'/devttyUSB0' },
            ]
        """
        for info in reader_info:
            ser = serial.Serial(info['port'], 9600, timeout=0.1)
            thread = RfidThread(
                ser=ser,
                lock=self.lock,
                addr=info['adder'],
                reader_id=info['reader_id'],
                stop_evt=self.stop_event
            )
            thread.start()
            self.threads.append(thread)

    def stop_all(self):
        self.stop_event.set()
        for t in self.threads:
            t.join()
