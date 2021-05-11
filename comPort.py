import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import serial.tools.list_ports

class comPortComboBox(QWidget):
	def __init__(self, parent = None):
		super(comPortComboBox, self).__init__(parent)
		self.__comPort = comPort()

		layout = QHBoxLayout()
		self.__cb = QComboBox()
		self.__cb.setFixedWidth (100)
		self.__cb.currentIndexChanged.connect(self.setComPort)

		label = QLabel("Com Ports:")
		layout.addWidget(label)
		layout.addWidget(self.__cb)
		layout.addStretch()
		self.setLayout(layout)
		self.__updateWidget()

	def setComPort(self):
		newCom = self.__cb.currentText()
		self.__comPort.setComPort(newCom)


	def mouseReleaseEvent (self, event):
		pass
		# current = self.currentText ()
		# availablePorts = self.__getAvailableComPorts()
		# print (current)
		# self.clear()
		# self.addItem("")
		# self.addItems(availablePorts)
		# if current in availablePorts:
		# 	self.setCurrentIndex (availablePorts.index(current) + 1)

	def __updateWidget(self):
		self.__cb.addItem("")
		self.__cb.addItems(self.__comPort.getAvailableComPorts())

	def test(self):
		print ("test")




class comPort():
	__instance = None
	def __new__(cls,):
		if cls.__instance is None:
			print ("Create the object")
			comPort.__instance = super(comPort, cls).__new__(cls)
			# cls._instance = super(comPort, cls).__new__(cls)
		return comPort.__instance

	def __init__(self):
		super(comPort, self).__init__()

		self.__activeCom = ""
		self.__ser = serial.Serial(
    		baudrate=19200,\
    		parity=serial.PARITY_NONE,\
    		stopbits=serial.STOPBITS_ONE,\
    		bytesize=serial.EIGHTBITS,\
        	timeout=0)

	def setComPort(self, newCom):
		# newCom = self.__cb.currentText()
		if newCom != self.__ser.name and newCom != "":
			if self.__ser.is_open:
				self.__ser.close()
			self.__ser.port = newCom
			self.__ser.open()

	def sendComPort(self, bytes):
		if self.__ser.is_open == True:
			print ("send")
			print (self.__ser.write(bytes))
			print ("sent")


	def closeComPort(self):
		if self.__ser.is_open == True:
			self.__ser.close()

	def getAvailableComPorts(self):
	    """ Lists serial port names

	        :raises EnvironmentError:
	            On unsupported or unknown platforms
	        :returns:
	            A list of the serial ports available on the system
	    """
	    if sys.platform.startswith('win'):
	        ports = ['COM%s' % (i + 1) for i in range(256)]
	    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
	        # this excludes your current terminal "/dev/tty"
	        ports = glob.glob('/dev/tty[A-Za-z]*')
	    elif sys.platform.startswith('darwin'):
	        ports = glob.glob('/dev/tty.*')
	    else:
	        raise EnvironmentError('Unsupported platform')

	    result = []
	    for port in ports:
	        try:
	            s = serial.Serial(port)
	            s.close()
	            result.append(port)
	        except (OSError, serial.SerialException):
	            pass
	    return result

def main():
	app = QApplication(sys.argv)
	ex = comPortComboBox()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
