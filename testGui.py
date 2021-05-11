import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


from comPort import comPort
# from PyQt4.QtWidgets import *
# QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QWidget
# print 'aaa'

class parameter(QWidget):
   def __init__(self, packetCode, minVal, maxVal, label = "", parent = None):
      super(parameter, self).__init__(parent)
      self.__packetCode = packetCode
      self.__paramValue = 5
      self.__maxVal = maxVal
      self.__minVal = minVal

      self.__comPort = comPort()
      
      layout = QHBoxLayout()

      self.slider = QSlider(Qt.Horizontal)
      if label != "":
         self.lbl = QLabel(label+":")
         layout.addWidget(self.lbl)

      self.slider.setMinimum(self.__minVal)
      self.slider.setMaximum(self.__maxVal)
      self.slider.setFixedWidth (150)
      # self.slider.valueChanged.connect(self.__sliderChanged)
      # self.slider.sliderReleased.connect(self.__sliderChanged)
      self.slider.valueChanged.connect(self.__sliderChanged)
      # self.slider.sliderPressed .connect(self.__sliderChanged)
      # self.slider.initStyleOption()
      # QSlider.initStyleOption (Qt.QMacStyle)
      layout.addWidget(self.slider)

      # splitter = QSplitter(Qt.Vertical)
      # splitter.setFixedHeight(2)
      # layout.addWidget(splitter)

      self.lineEdit = QLineEdit()
      self.lineEdit.setFixedWidth (45)
      self.lineEdit.returnPressed.connect(self.__lineEditChanged)
      layout.addWidget(self.lineEdit)

      self.hexLabel = QLabel("= "+str(hex(0)))
      layout.addWidget(self.hexLabel)

      self.setLayout(layout)
      # self.setWindowTitle("combo box demo")


   def __sliderChanged(self):
      val = self.slider.sliderPosition ()
      print (val)
      self.lineEdit.setText (str(self.slider.sliderPosition ()))
      self.hexLabel.setText("= "+str(hex(int(self.lineEdit.text()))))
      self.__comPort.sendComPort(bytearray([self.__packetCode, val]))

   def __lineEditChanged (self):
      val = int(self.lineEdit.text())
      if val <= self.__maxVal and val >= self.__minVal:
         self.__paramValue = val
         self.slider.setSliderPosition(val)
      else:
         self.lineEdit.setText(str(self.__paramValue))
      self.hexLabel.setText("= "+str(hex(int(self.lineEdit.text()))))

      # self.slider.setSliderPosition(float(self.lineEdit.text()))

   def __sendPacket(self, val):
      self.__comPort.sendComPort(bytearray([self.__packetCode, val]))

		
def main():
   app = QApplication(sys.argv)
   ex = parameter(0, 0, 100, "aaaa")
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()



