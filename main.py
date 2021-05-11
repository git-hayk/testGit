import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from comPort import comPort, comPortComboBox
from testGui import parameter

class mainApp(QWidget):
	def __init__(self, parent = None):
		super(mainApp, self).__init__(parent)

		self.__comPort = comPort()
		layout = QVBoxLayout()
		splitter = QSplitter(Qt.Horizontal)
		layout.addWidget(splitter)

		self.__comPortCombo = comPortComboBox()
		layout.addWidget(self.__comPortCombo)

		self.__resistor = parameter(0x01, 0, 255, "Resistance")
		layout.addWidget(self.__resistor)

		self.__opampGain = parameter(0x02, 0, 255, "OpAmp Gain")
		layout.addWidget(self.__opampGain)


		hbox = QHBoxLayout()
		self.__m_rb_single = QRadioButton("Single Puls")
		self.__m_rb_single.setChecked(True)
				
		self.__m_rb_continues = QRadioButton("Continues Pulses")

		hbox.addWidget(self.__m_rb_single)
		hbox.addWidget(self.__m_rb_continues)
		layout.addLayout(hbox)

		hbox2 = QHBoxLayout()
		self.__sendPulse = QPushButton("Send Pulse")
		hbox2.addWidget(self.__sendPulse)
		hbox2.addStretch()
		layout.addLayout(hbox2)

		self.setLayout(layout)

		self.__m_rb_single.toggled.connect(lambda: self.m_testMode(self.__m_rb_single))
		self.__m_rb_continues.toggled.connect(lambda: self.m_testMode(self.__m_rb_continues))
		self.__sendPulse.released.connect(self.__sendSinglePulse)

	def __sendSinglePulse(self):
		print ("sent single pulse command")
		self.__comPort.sendComPort(bytearray([0x03, 0x00]))
		# self.__comPort.sendComPort(bytearray([self.__packetCode, val]))

	def closeEvent(self, event):
		print ("CLOSED")
		self.__comPort.closeComPort

	def m_testMode(self, bt):
		# print (bt.text())
		# return
		if bt.text() == "Single Puls" and bt.isChecked() == True:
			print ("0")
			self.__sendPulse.setEnabled (True)
			# self.__comPort.sendComPort(bytearray([0x00]))
			pass
		if bt.text() == "Continues Pulses" and bt.isChecked() == True:
			print ("1")
			self.__sendPulse.setEnabled (False)
			self.__comPort.sendComPort(bytearray([0x04, 0x00]))
			pass




def main():
	app = QApplication(sys.argv)
	ex = mainApp()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
   main()
