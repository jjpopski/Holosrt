
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import *
from HolographyBackend_ui import Ui_MainWindow
from Acspy.Clients.SimpleClient import PySimpleClient # Import the acspy.PySimpleClient class

import Acspy.Common.Err
import maciErrType
import maciErrTypeImpl
import ClientErrorsImpl 
import ACSLog


import ACSErrTypeCommonImpl
import ACSErrTypeCommon
import ACSErrTypeOKImpl




class MainWindow(QMainWindow, Ui_MainWindow):
   def __init__(self):
       super(MainWindow, self).__init__()
       self.setupUi(self)
       self.assignWidgets()
       self.show()
        

   def assignWidgets(self):
       
#self.goButton.clicked.connect(self.goPushed)
#QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), someFunc)

       self.connect(self.startButton,SIGNAL('clicked()'), self.start)
       self.connect(self.stopButton,SIGNAL('clicked()'), self.stop)
       self.simpleClient = PySimpleClient()
       
       self.component= self.simpleClient.getComponent("BACKENDS/Holography")


 #      self.connect(self.stopButton,self.start())
                
       
       
   def start(self):
       self.startButton.setEnabled(False)
       self.stopButton.setEnabled(True)
       self.component.sendHeader()
       self.component.sendData(0)
       
       
       print ("start")
       
   def stop(self):
       self.startButton.setEnabled(True)
       self.stopButton.setEnabled(False)
       self.component.sendStop()
       self.component.terminate()
       
       print ("stop")
  
   def quit(self):
       print ("Closing")
       self.simpleClient.releaseComponent("BACKENDS/Holography")
       self.simpleClient.disconnect()

       MainWindow.close(self)     
       
   


if __name__ == '__main__':
   app = QApplication(sys.argv)
   mainWin = MainWindow()
   ret = app.exec_()
   sys.exit(ret)