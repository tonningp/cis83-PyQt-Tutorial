#!/usr/bin/env python3
import serial, time
from PyQt5.QtCore import (
    Qt,
    QObject,
    QRunnable,
    QThread,
    QCoreApplication,
    pyqtSignal
    )

class EventEmitter(QObject):
    sig = pyqtSignal(str)

    def __init__(self,parent=0):
        super().__init__()


    def send(self,b):
        self.sig.emit(str(b))


class SerialManager(QThread):

    def initSerial(self):
        #initialization and open the port

        #possible timeout values:
        #    1. None: wait forever, block call
        #    2. 0: non-blocking mode, return immediately
        #    3. x, x is bigger than 0, float allowed, timeout block call

        self.ser = serial.Serial()
        self.ser.port = "/dev/cu.usbmodem1441"
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        self.ser.timeout = 1            #non-block read
        self.ser.xonxoff = False     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2     #timeout for write

    def setEmitter(self,emitter):
        self.emitter = emitter


    def run(self):
        self.initSerial()
        try: 
            self.ser.open()
        except Exception as e:
            print ("error open serial port: " + str(e))
            exit()
        if self.ser.isOpen():
            try:
                self.ser.flushInput() #flush input buffer, discarding all its contents
                time.sleep(1.0)  #give the serial port sometime to receive the data
                while True:
                    self.ser.write('6:255\n'.encode())
                    response = self.ser.readline().strip()
                    response = response.decode('utf-8')
                    if response == '':
                        pass
                    else:
                        if ':' in response:
                            mv = ( float(response.split(':')[1])/1024.0)*5000;
                            cel = mv/10;
                            farh = cel*9/5 + 32;
                            print("cel:{} farh:{}".format(cel,farh))

                    time.sleep(1.0)  
                    self.ser.write('6:0\n'.encode())
                    time.sleep(1.0)  
                        
                self.ser.close()
            except Exception as e1:
               print("error communicating...: " + str(e1))
        else:
            print ("cannot open serial port ")

if __name__ == "__main__":
    import sys
    app = QCoreApplication([])
    sreader = SerialManager()
    sreader.setEmitter(EventEmitter())
    sreader.finished.connect(app.exit)
    sreader.start()
    sys.exit(app.exec_())
