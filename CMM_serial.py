from serial import Serial
import serial.tools.list_ports

import time
import threading

from rtu_conf.exchange import *

CMM_PRIEX = '[cmm] '

def SER_Get_available_com_name():
    plist = list(serial.tools.list_ports.comports())
    name_list = []
    for list_ in plist:
        available_com = list_[0]
        name_list.append(available_com)

    return name_list

class cmm_manager(threading.Thread):
    def __init__(self):
        super(cmm_manager, self).__init__()
        self._running = True
        self.Ser = Serial()
        self.ser_lock = threading.Lock()
        self.exchange = get_exchange('cmm')
        #self.thread = threading.Thread()

    def open(self, port, name, baud):
        with self.ser_lock:
            if not self.Ser.isOpen():
                try:
                    print('{} open {}, {}, {}'.format(CMM_PRIEX,port, name, baud))
                    self.Ser.port = port
                    self.Ser.name = name
                    self.Ser.baudrate = baud
                    self.Ser.open()

                except Exception as e:
                    print(e)
                    raise e


    def close(self, name):
        print('{} close_com {}'.format(CMM_PRIEX, name))
        with self.ser_lock:
            if self.Ser.isOpen():
                try:
                    self.Ser.close()
                except Exception as e:
                    raise e

    def set_baud(self, baud):
        with self.ser_lock:
            print('{} set_baud {}'.format(CMM_PRIEX, baud))
            self.Ser.baudrate = baud

    def change_port(self, name):
        print('{} change_port {}'.format(CMM_PRIEX, name))

    def start_thread(self):
        print('{} start_thread'.format(CMM_PRIEX))
        self.start()

    def exit(self):
        print('{} exit'.format(CMM_PRIEX))
        self._running = False

    def send_bytes(self, buf):
        with self.ser_lock:
            if self.Ser.is_open:
                print('{} send bytes {}'.format(CMM_PRIEX, buf))
                self.Ser.write(buf)

    def run(self):
        while self._running:
            #print('{} run ...'.format(CMM_PRIEX))
            with self.ser_lock:
                if self.Ser.isOpen() and self.Ser.inWaiting():
                    text = self.Ser.read(self.Ser.inWaiting())
                    self.exchange.send(EXC_TYPE_COM, msg=text)
            time.sleep(0.01)

        print("{} thread exit!".format(CMM_PRIEX))
        time.sleep(1)


if __name__ == '__main__':
    print("cmm start")