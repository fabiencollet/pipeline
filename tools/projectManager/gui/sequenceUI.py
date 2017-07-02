#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`sequenceUI`
===================================

.. module:: sequenceUI
   :platform: Windows
   :synopsis: manage asset's information
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

from PySide import QtGui, QtCore
from pipeline.core import log, shot

projectInfoLog = log.Log('SEQUENCE_UI')

sequenceWin = None
SOFTWARE = None

class NewSequenceUi(QtGui.QWidget):

    def __init__(self):
        super(NewSequenceUi, self).__init__()

        self.setWindowTitle('New Sequence')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.mainLayout = QtGui.QVBoxLayout()

        self.sequenceTxt = QtGui.QLineEdit()
        self.createSequenceBtn = QtGui.QPushButton()
        self.createSequenceBtn.setText('Create new Sequence')

        self.mainLayout.addWidget(self.sequenceTxt)
        self.mainLayout.addWidget(self.createSequenceBtn)

        self.setLayout(self.mainLayout)

        self.createSequenceBtn.clicked.connect(self.newSequence)


    def newSequence(self):
        listSequences = str(self.sequenceTxt.text()).split(',')
        
        if listSequences:
            for sequenceName in listSequences:
                shot.createSequence(sequenceName)
            self.sequenceTxt.clear()
            self.close()


def mayaLaunch():
    ''' Def to call to launch tool in maya '''

    global sequenceWin, SOFTWARE

    SOFTWARE = 'maya'

    if sequenceWin:
        sequenceWin.close()

    sequenceWin = NewSequenceUi()
    sequenceWin.show()