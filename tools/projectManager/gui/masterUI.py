#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`masterUI`
===================================

.. module:: masterUI
   :platform: Windows
   :synopsis: masterUI
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

from PySide import QtGui, QtCore
from pipeline.core import log, shot

projectInfoLog = log.Log('MASTER_UI')

masterWin = None
SOFTWARE = None

class NewMasterUi(QtGui.QWidget):

    def __init__(self):
        super(NewMasterUi, self).__init__()

        self.setWindowTitle('New Master')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.mainLayout = QtGui.QVBoxLayout()

        self.sequenceCombo = QtGui.QComboBox()

        self.sequenceCombo.addItems(shot.getAllSequeces())

        self.masterTxt = QtGui.QLineEdit()
        self.createMasterBtn = QtGui.QPushButton()
        self.createMasterBtn.setText('Create new Master')

        self.mainLayout.addWidget(self.sequenceCombo)
        self.mainLayout.addWidget(self.masterTxt)
        self.mainLayout.addWidget(self.createMasterBtn)

        self.setLayout(self.mainLayout)

        self.createMasterBtn.clicked.connect(self.newMaster)


    def newMaster(self):
        listMasters = str(self.masterTxt.text()).split(',')
        sequence = str(self.sequenceCombo.currentText())

        if listMasters and sequence:
            for masterName in listMasters:
                shot.createMaster(sequence, masterName)
            self.close()


def mayaLaunch():
    ''' Def to call to launch tool in maya '''

    global masterWin, SOFTWARE

    SOFTWARE = 'maya'

    if masterWin:
        masterWin.close()

    masterWin = NewMasterUi()
    masterWin.show()