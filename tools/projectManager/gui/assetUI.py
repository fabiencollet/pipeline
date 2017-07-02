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
from pipeline.core import log, asset

projectInfoLog = log.Log('ASSET_UI')

assetWin = None
SOFTWARE = None

class NewAssetUi(QtGui.QWidget):

    def __init__(self):
        super(NewAssetUi, self).__init__()

        self.setWindowTitle('New Asset')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.mainLayout = QtGui.QVBoxLayout()

        self.assetTypeCombo = QtGui.QComboBox()

        self.assetTypeCombo.addItems(asset.ASSET_TYPES)

        self.assetNameTxt = QtGui.QLineEdit()
        self.createAssetBtn = QtGui.QPushButton()
        self.createAssetBtn.setText('Create new asset')

        self.mainLayout.addWidget(self.assetTypeCombo)
        self.mainLayout.addWidget(self.assetNameTxt)
        self.mainLayout.addWidget(self.createAssetBtn)

        self.setLayout(self.mainLayout)

        self.createAssetBtn.clicked.connect(self.newAsset)


    def newAsset(self):
        assetName = str(self.assetNameTxt.text())
        assetType = str(self.assetTypeCombo.currentText())

        if assetName and assetType:
            asset.createAsset(assetType, assetName)
            self.close()

def mayaLaunch():
    ''' Def to call to launch tool in maya '''

    global assetWin, SOFTWARE

    SOFTWARE = 'maya'

    if assetWin:
        assetWin.close()

    assetWin = NewAssetUi()
    assetWin.show()