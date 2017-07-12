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

from PySide import QtGui, QtCore
from pipeline.core import log, shot

shotManagerLog = log.Log('SHOT_MANAGER_UI')

shotManagerWin = None
SOFTWARE = None


class ShotManagerUI(QtGui.QWidget):
    def __init__(self):
        super(ShotManagerUI, self).__init__()

        self.setWindowTitle('Shot Manager')
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

    global shotManagerWin, SOFTWARE

    SOFTWARE = 'maya'

    if shotManagerWin:
        shotManagerWin.close()

    shotManagerWin = ShotManagerUI()
    shotManagerWin.show()