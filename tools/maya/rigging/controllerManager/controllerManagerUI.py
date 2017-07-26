#from PySide2 import QtWidgets
#from PySide2 import QtCore
#from PySide2 import QtGui


from pipeline.core.Qt import QtGui
from pipeline.core.Qt import QtCore
from pipeline.core.Qt import QtWidgets
'''
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-


''':mod:`shotManagerUI`
===================================

.. module:: shotManagerUI
   :platform: Windows
   :synopsis: manage shot and sequence in maya
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

from pipeline.core import log

controllerManagerLog = log.Log('CONTROLLER_MANAGER_UI')

try:
    import maya.cmds as mc
except:
    controllerManagerLog.warning('maya module not found')

try:
    import nuke
except:
    controllerManagerLog.warning('nuke module not found')

controllerManagerWin = None
SOFTWARE = None


class ControllerManagerUI(QtWidgets.QWidget):
    def __init__(self):
        super(ControllerManagerUI, self).__init__()

        self.setWindowTitle('Controller Manager')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.mainLayout = QtWidgets.QVBoxLayout()

        self.sequenceTxt = QtWidgets.QLineEdit()
        self.createSequenceBtn = QtWidgets.QPushButton()
        self.createSequenceBtn.setText('Create new Controller')

        self.mainLayout.addWidget(self.sequenceTxt)
        self.mainLayout.addWidget(self.createSequenceBtn)

        self.setLayout(self.mainLayout)

        self.createSequenceBtn.clicked.connect(self.newSequence)

    def newSequence(self):
        if SOFTWARE == 'maya':
            mc.circle()
            controllerManagerLog.info(SOFTWARE)
        if SOFTWARE == 'nuke':
            import nuke
            nuke.createNode("Blur")
            controllerManagerLog.info(SOFTWARE)


def launch(soft):
    ''' Def to call to launch tool in maya '''

    global controllerManagerWin, SOFTWARE

    SOFTWARE = soft

    if controllerManagerWin:
        controllerManagerWin.close()

    controllerManagerWin = ControllerManagerUI()
    controllerManagerWin.show()