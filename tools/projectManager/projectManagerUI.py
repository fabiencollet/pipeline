#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`projectManagerUI`
===================================

.. module:: projectManagerUI
   :platform: Windows
   :synopsis: Create and manage your project
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''
import os
from PySide import QtGui,QtCore
from pipeline.core import project,asset,log,file,shot
from gui import projectUI, assetUI, shotUI, sequenceUI, masterUI
import maya.cmds as mc
import json

reload(projectUI)
reload(assetUI)

projectManagerLog = log.Log('PROJECT_MANAGER')

projectManagerWin = None
SOFTWARE = None

class ProjectManagerUi(QtGui.QMainWindow):

    def __init__(self):
        super(ProjectManagerUi, self).__init__()

        projectManagerLog.info('init UI')

        self.project = project.Project()

        # Color
        self.lightGreyColor = QtGui.QColor()
        self.lightGreyColor.setHslF(0.6, 0.01, 0.25)
        ############################################

        self.setMinimumSize(700,450)
        self.resize(700,450)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Third-Part UI
        self.newProjectUI = projectUI.NewProjectUi()
        self.setProjectUI = projectUI.SetProjectUi()
        self.newAssetUI = assetUI.NewAssetUi()
        self.projectInfoUI = projectUI.ProjectInfoUi()
        self.newShotUI = shotUI.NewShotUi()
        self.newSequenceUI = sequenceUI.NewSequenceUi()
        self.newMasterUI = masterUI.NewMasterUi()
        ############################################

        self.createMenu()
        self.createLayout()
        self.createWidget()
        self.createConnection()
        self.createLayoutHierarchy()

        self.getCurrentProjectInfo()
        self.setMyWindowTitle()

        self.pipeline = 'asset'
        self.assetType = 'all'
        self.assetName = ''
        self.assetTask = ''
        self.taskVariant = 'base'
        self.software = SOFTWARE
        self.workingDir = 'work'
        self.fileName = ''

        self.getAllAssetType()
        self.getAssetByType()
        self.setCurrentAssetInfo()

    def createMenu(self):

        # Project
        self.projectMenu = QtGui.QMenu()
        self.projectMenu.setTitle('Projects')

        self.newProjectAct = QtGui.QAction(self.projectMenu)
        self.newProjectAct.setText('New Project')

        self.setProjectAct = QtGui.QAction(self.projectMenu)
        self.setProjectAct.setText('Set Project')

        self.projectInfoAct = QtGui.QAction(self.projectMenu)
        self.projectInfoAct.setText('Project info')

        # Assets
        self.assetMenu = QtGui.QMenu()
        self.assetMenu.setTitle('Assets')

        self.newAssetAct = QtGui.QAction(self.assetMenu)
        self.newAssetAct.setText('New Asset')

        # Sequences
        self.sequenceMenu = QtGui.QMenu()
        self.sequenceMenu.setTitle('Sequences')

        self.newSequenceAct = QtGui.QAction(self.sequenceMenu)
        self.newSequenceAct.setText('New Sequence')

        # Masters
        self.masterMenu = QtGui.QMenu()
        self.masterMenu.setTitle('Masters')

        self.newMasterAct = QtGui.QAction(self.masterMenu)
        self.newMasterAct.setText('New Master')

        # Shots
        self.shotMenu = QtGui.QMenu()
        self.shotMenu.setTitle('Shots')

        self.newShotAct = QtGui.QAction(self.shotMenu)
        self.newShotAct.setText('New Shot')

        # Actions
        self.projectMenu.addAction(self.newProjectAct)
        self.projectMenu.addAction(self.setProjectAct)
        self.projectMenu.addAction(self.projectInfoAct)

        self.assetMenu.addAction(self.newAssetAct)

        self.sequenceMenu.addAction(self.newSequenceAct)

        self.masterMenu.addAction(self.newMasterAct)

        self.shotMenu.addAction(self.newShotAct)

        # MenuBar
        self.menuBar = QtGui.QMenuBar()

        self.menuBar.addMenu(self.projectMenu)
        self.menuBar.addMenu(self.assetMenu)
        self.menuBar.addMenu(self.sequenceMenu)
        self.menuBar.addMenu(self.masterMenu)
        self.menuBar.addMenu(self.shotMenu)

        self.setMenuBar(self.menuBar)

    def createLayout(self):

        self.mainWidget = QtGui.QWidget()
        self.mainLayout = QtGui.QVBoxLayout()

        self.mainAssetLayout = QtGui.QHBoxLayout()

        self.typeLayout = QtGui.QVBoxLayout()
        
        self.assetsLayout = QtGui.QVBoxLayout()
        self.shotsLayout = QtGui.QVBoxLayout()
        self.mastersLayout = QtGui.QVBoxLayout()
        
        self.assetInfoLayout = QtGui.QVBoxLayout()

        self.fileBtnLayout = QtGui.QHBoxLayout()

        self.currentProjectLayout = QtGui.QHBoxLayout()


    def createWidget(self):

        self.assetsTab = QtGui.QTabWidget()

        self.assetTypeCombo = QtGui.QComboBox()

        # Label Info
        self.assetTypeLabel = QtGui.QLabel()
        self.assetNameLabel = QtGui.QLabel()
        self.assetTaskLabel = QtGui.QLabel()
        self.taskVariantLabel = QtGui.QLabel()
        self.softwareLabel = QtGui.QLabel()
        self.workingDirLabel =QtGui.QLabel()

        self.listAssets = QtGui.QListWidget()
        self.listShots = QtGui.QListWidget()
        self.listMasters = QtGui.QListWidget()

        self.listFile = QtGui.QListWidget()

        self.assetTaskCombo = QtGui.QComboBox()

        self.taskVariantCombo = QtGui.QComboBox()
        self.taskVariantCombo.addItem('base')

        # Buttons
        self.openFileBtn = QtGui.QPushButton()
        self.openFileBtn.setText('Open')
        self.saveAsBtn = QtGui.QPushButton()
        self.saveAsBtn.setText('Save as')
        self.importRefBtn = QtGui.QPushButton()
        self.importRefBtn.setText('Import reference')

        self.currentProjectPathTxt = QtGui.QLabel()
        self.currentProjectPathTxt.setFixedHeight(15)

    def createLayoutHierarchy(self):

        # Assets
        self.typeLayout.addWidget(self.assetTypeCombo)

        self.assetsLayout.addWidget(self.listAssets)

        self.assetsTab.addTab(self.listAssets, 'Assets')
        self.assetsTab.addTab(self.listShots, 'Shots')
        self.assetsTab.addTab(self.listMasters, 'Masters')
        self.typeLayout.addWidget(self.assetsTab)

        self.fileBtnLayout.addWidget(self.openFileBtn)
        self.fileBtnLayout.addWidget(self.saveAsBtn)
        self.fileBtnLayout.addWidget(self.importRefBtn)

        self.assetInfoLayout.addWidget(self.assetTaskCombo)
        self.assetInfoLayout.addWidget(self.taskVariantCombo)
        self.assetInfoLayout.addWidget(self.listFile)
        self.assetInfoLayout.addLayout(self.fileBtnLayout)

        self.currentProjectLayout.addWidget(self.assetTypeLabel)
        self.currentProjectLayout.addWidget(self.assetNameLabel)
        self.currentProjectLayout.addWidget(self.assetTaskLabel)
        self.currentProjectLayout.addWidget(self.taskVariantLabel)
        self.currentProjectLayout.addWidget(self.softwareLabel)
        self.currentProjectLayout.addWidget(self.workingDirLabel)

        self.mainAssetLayout.addLayout(self.typeLayout)


        self.mainAssetLayout.addLayout(self.assetInfoLayout)

        self.mainLayout.addLayout(self.mainAssetLayout)
        self.mainLayout.addLayout(self.currentProjectLayout)


        # Main Layout > Main Widget
        self.mainWidget.setLayout(self.mainLayout)

        # Main Widget > Window
        self.setCentralWidget(self.mainWidget)

    def createConnection(self):

        self.assetsTab.currentChanged.connect(self.changeAssetType)

        self.newProjectAct.triggered.connect(self.showNewProjectUI)
        self.setProjectAct.triggered.connect(self.showSetProjectUI)
        self.projectInfoAct.triggered.connect(self.showProjectInfoUI)
        self.newShotAct.triggered.connect(self.showNewShotUI)
        self.newSequenceAct.triggered.connect(self.showNewSequenceUI)
        self.newMasterAct.triggered.connect(self.showNewMasterUI)

        self.newAssetAct.triggered.connect(self.showNewAssetUI)
        self.setProjectUI.projectBtn.clicked.connect(self.getCurrentProjectInfo)

        self.listAssets.itemClicked.connect(self.getAssetTask)
        self.listShots.itemClicked.connect(self.getAssetTask)
        self.listMasters.itemClicked.connect(self.getAssetTask)

        self.assetTaskCombo.activated.connect(self.getTaskVariant)

        self.assetTypeCombo.activated.connect(self.changeCurrentAssetType)

        self.setProjectUI.projectBtn.clicked.connect( self.getAssetByType)
        self.newAssetUI.createAssetBtn.clicked.connect(self.getAssetByType)
        self.newSequenceUI.createSequenceBtn.clicked.connect(self.getAllSequence)

        # List File
        self.assetTaskCombo.activated.connect(self.getAssetFilePath)
        self.taskVariantCombo.activated.connect(self.getAssetFilePath)

        # Open File
        self.listFile.doubleClicked.connect(self.openFile)
        self.openFileBtn.clicked.connect(self.openFile)

        # Import Ref
        self.importRefBtn.clicked.connect(self.importReference)

        # Save File
        self.saveAsBtn.clicked.connect(self.saveAs)

        # Change self attribute
        self.listAssets.itemClicked.connect(self.getCurrentAssetNameAndType)
        self.listShots.itemClicked.connect(self.getCurrentAssetNameAndType)
        self.listMasters.itemClicked.connect(self.getCurrentAssetNameAndType)

        self.assetTaskCombo.activated.connect(self.getCurrentAssetTask)
        self.taskVariantCombo.activated.connect(self.getCurrentTaskVariant)
        self.listFile.itemClicked.connect(self.getCurrentFileName)

    #----------------------------------------------------------------------------
    #  METHODS
    #----------------------------------------------------------------------------

    def changeAssetType(self):

        index = self.assetsTab.currentIndex()
        type = self.assetsTab.tabText(index)

        if type == 'Assets':
            self.pipeline = 'asset'
            self.getAllAssetType()

        if type == 'Shots':
            self.pipeline = 'shot'
            self.getAllSequence()

        if type == 'Masters':
            self.pipeline = 'master'
            self.getAllSequence()

    def getCurrentAssetNameAndType(self):
        if self.pipeline == 'asset':
            currentItem = self.listAssets.currentItem()
            self.assetName = self.listAssets.itemWidget(currentItem).name
            self.assetType = self.listAssets.itemWidget(currentItem).type

        if self.pipeline == 'shot':
            currentItem = self.listShots.currentItem()
            self.assetName = self.listShots.itemWidget(currentItem).name
            self.assetType = self.listShots.itemWidget(currentItem).type

        if self.pipeline == 'master':
            currentItem = self.listMasters.currentItem()
            self.assetName = self.listMasters.itemWidget(currentItem).name
            self.assetType = self.listMasters.itemWidget(currentItem).type

        self.assetNameLabel.setText(self.assetName)
        self.assetTypeLabel.setText(self.assetType)

    def changeCurrentAssetType(self):
        type = self.assetTypeCombo.currentText()
        self.assetType = type
        self.getAssetByType()

    def getCurrentShot(self):
        currentItem = self.listShots.currentItem()
        self.sequence = self.listShots.itemWidget(currentItem).type
        self.assetTypeLabel.setText(self.sequence)

    def getCurrentMaster(self):
        currentItem = self.listMasters.currentItem()
        self.sequence = self.listMasters.itemWidget(currentItem).type
        self.assetTypeLabel.setText(self.sequence)

    def getCurrentAssetTask(self):
        self.assetTask = self.assetTaskCombo.currentText()
        self.assetTaskLabel.setText(self.assetTask)

    def getCurrentTaskVariant(self):
        self.taskVariant = self.taskVariantCombo.currentText()
        self.taskVariantLabel.setText(self.taskVariant)

    def setCurrentAssetInfo(self):
        self.assetTypeLabel.setText(self.assetType)
        self.assetNameLabel.setText(self.assetName)
        self.assetTaskLabel.setText(self.assetTask)
        self.taskVariantLabel.setText(self.taskVariant)
        self.softwareLabel.setText(self.software)
        self.workingDirLabel.setText(self.workingDir)

    def getCurrentFileName(self):

        self.fileName = self.listFile.currentItem().text()

    def closeEvent(self, event):
        projectManagerLog.info('UI Closed')

    def initScene(self):
        print 'init'

    def openFile(self):

        if self.currentProjectPath and self.assetType and self.assetName and self.assetTask and self.taskVariant and SOFTWARE and self.workingDir:

            result = mc.confirmDialog(
                title='Save Changement',
                message='Save your scene:',
                button=["Save", "Don't Save", "Cancel"],
                defaultButton='Cancel',
                cancelButton='Cancel',
                dismissString='Cancel')

            if self.pipeline == 'asset':
                filePath = os.sep.join(
                    [self.currentProjectPath, asset.PIPE_ASSETS, self.assetType,
                     self.assetName, self.assetTask, self.taskVariant, SOFTWARE,
                     self.workingDir, self.fileName])

            if self.pipeline == 'shot' or self.pipeline == 'master':
                filePath = os.sep.join(
                    [self.currentProjectPath, shot.PIPE_SHOTS, self.assetType,
                     self.assetName, self.assetTask, self.taskVariant, SOFTWARE,
                     self.workingDir, self.fileName])

            if result == 'Cancel':
                return

            elif result == 'Save':
                self.incrementAndSave()
                mc.file(filePath, f=1, options='v=1', ignoreVersion=True, open=True)
            else:
                # Open file force mode
                # mc.file(filePath, force=True, options='v=0', ignoreVersion=True, open=True)

                # mc.file(mc.file(q=1, sn=1), rename=1)

                mc.file(filePath, f=1, options='v=1', ignoreVersion=True, open=True)

    def saveAs(self):

        if self.assetType and self.assetName and self.assetTask and self.taskVariant and SOFTWARE and self.workingDir:
            newFile = file.File()
            newFile.saveAs(self.assetType, self.assetName, self.assetTask, self.taskVariant, SOFTWARE, self.workingDir)

    def importReference(self):

        if self.pipeline == 'asset':
            filePath = os.sep.join(
                [self.currentProjectPath, asset.PIPE_ASSETS, self.assetType,
                 self.assetName, self.assetTask, self.taskVariant, SOFTWARE,
                 self.workingDir, self.fileName])

        if self.pipeline == 'shot' or self.pipeline == 'master':
            filePath = os.sep.join(
                [self.currentProjectPath, shot.PIPE_SHOTS, self.assetType,
                 self.assetName, self.assetTask, self.taskVariant, SOFTWARE,
                 self.workingDir, self.fileName])

        mc.file(filePath, reference=True, namespace=self.assetName)

    def getAssetFilePath(self):

        self.getCurrentTaskVariant()

        if self.pipeline == 'asset':
            listFile = asset.getAssetFilePath(self.assetType,
                                              self.assetName,
                                              self.assetTask,
                                              self.taskVariant,
                                              self.software,
                                              self.workingDir)

        if self.pipeline == 'shot' or self.pipeline == 'master':
            listFile = shot.getshotFilePath(self.assetType,
                                            self.assetName,
                                            self.assetTask,
                                            self.taskVariant,
                                            self.software,
                                            self.workingDir)

        self.listFile.clear()
        self.listFile.addItems(listFile)

    def getTaskVariant(self):

        self.getCurrentAssetTask()

        if self.assetType and self.assetName and self.assetTask:

            if self.pipeline == 'asset':
                allVariant = asset.getTaskVariant(self.assetType, self.assetName,
                                                  self.assetTask)

            if self.pipeline == 'shot' or self.pipeline == 'master':
                allVariant = shot.getTaskVariant(self.assetType, self.assetName,
                                                  self.assetTask)
            self.taskVariantCombo.clear()
            self.taskVariantCombo.addItems(allVariant)


    def getAssetTask(self):

        self.getCurrentAssetNameAndType()

        self.assetTaskCombo.clear()
        if self.pipeline == 'asset':
            self.assetTaskCombo.addItems(asset.getAssetTask(self.assetType, self.assetName))
        if self.pipeline == 'shot' or self.pipeline == 'master':
            self.assetTaskCombo.addItems(shot.getShotTask(self.assetType, self.assetName))


    def getAssetByType(self):

        if self.pipeline == 'asset':
            self.listAssets.clear()
            allAssets = asset.getAssetByType(self.assetType)

        if self.pipeline == 'shot':
            self.listShots.clear()
            allAssets = shot.getShotBysequence(self.assetType)

        if self.pipeline == 'master':
            self.listMasters.clear()
            allAssets = shot.getMasterBysequence(self.assetType)

        i = 0

        for assetName in allAssets:
            i+=1
            assetWidget = AssetItem(assetName, allAssets[assetName])

            if self.pipeline == 'asset':
                assetListWidgetItem = QtGui.QListWidgetItem(self.listAssets)
            if self.pipeline == 'shot':
                assetListWidgetItem = QtGui.QListWidgetItem(self.listShots)
            if self.pipeline == 'master':
                assetListWidgetItem = QtGui.QListWidgetItem(self.listMasters)

            assetListWidgetItem.setSizeHint(assetWidget.sizeHint())

            if not i%2 == 0:
                assetListWidgetItem.setBackground(self.lightGreyColor)


            if self.pipeline == 'asset':
                self.listAssets.addItem(assetListWidgetItem)
                self.listAssets.setItemWidget(assetListWidgetItem, assetWidget)

            if self.pipeline == 'shot':
                self.listShots.addItem(assetListWidgetItem)
                self.listShots.setItemWidget(assetListWidgetItem, assetWidget)

            if self.pipeline == 'master':
                self.listMasters.addItem(assetListWidgetItem)
                self.listMasters.setItemWidget(assetListWidgetItem, assetWidget)


    def getAllSequence(self):
        allSequence = shot.getAllSequeces()
        allSequence.append('all')
        self.assetTypeCombo.clear()
        self.assetTypeCombo.addItems(sorted(allSequence))


    def getAllAssetType(self):

        allAssetType = asset.ASSET_TYPES
        allAssetType.append('all')
        sorted(allAssetType)

        listAssetType =[]

        if allAssetType:
            self.assetTypeCombo.clear()
            for assetType in sorted(allAssetType):
                if asset.assetTypeExist(assetType) or assetType=='all':
                    listAssetType.append(assetType)
                    self.assetTypeCombo.addItem(assetType)

        currentIndex = listAssetType.index(self.assetType)
        self.assetTypeCombo.setCurrentIndex(currentIndex)

    def getCurrentProjectInfo(self):

        currentProject = project.Project()

        self.currentProjectName = currentProject.name
        self.currentProjectPath = currentProject.path


    def setMyWindowTitle(self):

        self.windowTitle = 'Project Manager - '+str(self.currentProjectPath)

        self.setWindowTitle(self.windowTitle)

    def showProjectInfoUI(self):
        self.projectInfoUI.show()

    def showNewProjectUI(self):
        self.newProjectUI.show()

    def showSetProjectUI(self):
        self.setProjectUI.show()

    def showNewAssetUI(self):
        self.newAssetUI.show()

    def showNewShotUI(self):
        self.newShotUI.show()

    def showNewSequenceUI(self):
        self.newSequenceUI.show()

    def showNewMasterUI(self):
        self.newMasterUI.show()


class AssetItem(QtGui.QWidget):

    def __init__(self, name, type):
        super(AssetItem, self).__init__()

        self.name = name
        self.type = type

        self.mainLayout = QtGui.QHBoxLayout()

        self.nameTxt = QtGui.QLabel()
        self.nameTxt.setText(self.name)
        self.typeTxt = QtGui.QLabel()
        self.typeTxt.setText(self.type)
        self.typeTxt.setMaximumWidth(70)

        self.mainLayout.addWidget(self.typeTxt)
        self.mainLayout.addWidget(self.nameTxt)

        self.setLayout(self.mainLayout)


def mayaLaunch():
    ''' Def to call to launch tool in maya '''

    global projectManagerWin, SOFTWARE

    SOFTWARE = 'maya'

    if projectManagerWin:
        projectManagerWin.close()

    projectManagerWin = ProjectManagerUi()
    projectManagerWin.show()