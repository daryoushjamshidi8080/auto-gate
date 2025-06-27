from rfid_reader import RfidThread
from threading import Thread, Lock, Event
import serial


class RfidManager:
    def __init__(self):
        self.lock = Lock()
        self.threads = []
        self.info_reader = []

    def start_readers(self, reader_info):
        stop_event = Event()
        print('start 7899999999999999999999999999999999999999999999999999999999999')
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
                stop_evt=stop_event
            )
            thread.start()
            self.threads.append(thread)
            self.info_reader.append(
                {'reader_id': info['reader_id'], 'adder': info['adder'], 'thread': thread})
        # for t in self.threads:
        #     t.join()

    def stop_tread(self, reader_id, adder):
        print(f'addr : {adder}    |||||||| reader id : {reader_id}')

        to_remove = None
        for t in self.info_reader:
            if t['adder'] == adder and t['reader_id'] == reader_id:
                print('goooooooooooo too iffffffffffff')
                t['thread'].stop_evt.set()
                t['thread'].join()
                to_remove = t
                break

        if to_remove:
            self.info_reader.remove(to_remove)
            if to_remove['thread'] in self.threads:
                self.threads.remove(to_remove['thread'])
            print(f"✅ Reader {reader_id} - {adder} stopped.")
            return True
        else:
            print(f"⚠️ Reader {reader_id} - {adder} not found.")
            return False

        # self.stop_event.set()


rfid_manager = RfidManager()
