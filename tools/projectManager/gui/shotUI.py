#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`assetUI`
===================================

.. module:: assetUI
   :platform: Windows
   :synopsis: manage asset's information
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

from PySide import QtGui, QtCore
from pipeline.core import project, log, widget, shot

projectInfoLog = log.Log('ASSET_UI')

shotWin = None
SOFTWARE = None

class NewShotUi(QtGui.QWidget):

    def __init__(self):
        super(NewShotUi, self).__init__()

        self.setWindowTitle('New Shot')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.mainLayout = QtGui.QVBoxLayout()

        self.sequenceCombo = QtGui.QComboBox()

        self.sequenceCombo.addItems(shot.getAllSequeces())

        self.shotTxt = QtGui.QLineEdit()
        self.createAssetBtn = QtGui.QPushButton()
        self.createAssetBtn.setText('Create new Shot')

        self.mainLayout.addWidget(self.sequenceCombo)
        self.mainLayout.addWidget(self.shotTxt)
        self.mainLayout.addWidget(self.createAssetBtn)

        self.setLayout(self.mainLayout)

        self.createAssetBtn.clicked.connect(self.newShot)


    def newShot(self):
        listShots = str(self.shotTxt.text()).split(',')
        sequence = str(self.sequenceCombo.currentText())

        if listShots and sequence:
            for shotName in listShots:
                shot.createShot(sequence, shotName)
            self.close()


def mayaLaunch():
    ''' Def to call to launch tool in maya '''

    global shotWin, SOFTWARE

    SOFTWARE = 'maya'

    if shotWin:
        shotWin.close()

    shotWin = NewShotUi()
    shotWin.show()