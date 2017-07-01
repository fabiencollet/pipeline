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
from pipeline.core import project,asset,log,file
from gui import projectInfoUI
import maya.cmds as mc
import json

projectManagerLog = log.Log('PROJECT_MANAGER')

projectManagerWin = None
SOFTWARE = None

class ProjectManagerUi(QtGui.QMainWindow):

    def __init__(self):
        super(ProjectManagerUi, self).__init__()

        projectManagerLog.info('init UI')

        self.project = project.Project()


        self.setMinimumSize(700,450)
        self.resize(700,450)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.newProjectUI = NewProjectUi()
        self.setProjectUI = SetProjectUi()
        self.newAssetUI = NewAssetUi()
        self.projectInfoUI = projectInfoUI.ProjectInfoUi()

        self.createMenu()
        self.createLayout()
        self.createWidget()
        self.createConnection()
        self.createLayoutHierarchy()

        self.getCurrentProjectInfo()
        self.setMyWindowTitle()

        self.assetType = 'all'
        self.assetName = ''
        self.assetTask = ''
        self.taskVariant = 'base'
        self.software = SOFTWARE
        self.workingDir = 'work'
        self.fileName = ''

        self.getAllAssetType()
        self.getAssetByType(self.assetType)
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

        # Actions
        self.projectMenu.addAction(self.newProjectAct)
        self.projectMenu.addAction(self.setProjectAct)
        self.projectMenu.addAction(self.projectInfoAct)

        self.assetMenu.addAction(self.newAssetAct)

        # MenuBar
        self.menuBar = QtGui.QMenuBar()

        self.menuBar.addMenu(self.projectMenu)
        self.menuBar.addMenu(self.assetMenu)

        self.setMenuBar(self.menuBar)

    def createLayout(self):

        self.mainWidget = QtGui.QWidget()
        self.mainLayout = QtGui.QVBoxLayout()

        self.mainAssetLayout = QtGui.QHBoxLayout()

        self.assetsLayout = QtGui.QVBoxLayout()
        self.assetInfoLayout = QtGui.QVBoxLayout()

        self.fileBtnLayout = QtGui.QHBoxLayout()

        self.currentProjectLayout = QtGui.QHBoxLayout()


    def createWidget(self):

        self.assetTypeCombo = QtGui.QComboBox()

        # Label Info
        self.assetTypeLabel = QtGui.QLabel()
        self.assetNameLabel = QtGui.QLabel()
        self.assetTaskLabel = QtGui.QLabel()
        self.taskVariantLabel = QtGui.QLabel()
        self.softwareLabel = QtGui.QLabel()
        self.workingDirLabel =QtGui.QLabel()

        self.listAssets = QtGui.QListWidget()
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

    def createConnection(self):
        self.newProjectAct.triggered.connect(self.showNewProjectUI)
        self.setProjectAct.triggered.connect(self.showSetProjectUI)
        self.projectInfoAct.triggered.connect(self.showProjectInfoUI)

        self.newAssetAct.triggered.connect(self.showNewAssetUI)
        self.setProjectUI.projectBtn.clicked.connect(self.getCurrentProjectInfo)

        self.listAssets.itemClicked.connect(self.getAssetTask)

        self.assetTaskCombo.activated.connect(self.getTaskVariant)

        self.assetTypeCombo.activated.connect(self.listCurrentAssetType)

        self.setProjectUI.projectBtn.clicked.connect(lambda: self.getAssetByType(self.assetType))
        self.newAssetUI.createAssetBtn.clicked.connect(lambda : self.getAssetByType(self.assetType))

        # List File
        self.assetTaskCombo.activated.connect(self.getAssetFilePath)
        self.taskVariantCombo.activated.connect(self.getAssetFilePath)

        # Open File
        self.listFile.doubleClicked.connect(self.openFile)
        self.openFileBtn.clicked.connect(self.openFile)

        # Import Ref
        self.importRefBtn.clicked.connect(self.importReference)

        # Save File
        self.saveAsBtn.clicked.connect(self.incrementAndSave)

        # Change self attribute
        self.listAssets.itemClicked.connect(self.getCurrentAssetType)
        self.listAssets.itemClicked.connect(self.getCurrentAssetName)
        self.assetTaskCombo.activated.connect(self.getCurrentAssetTask)
        self.taskVariantCombo.activated.connect(self.getCurrentTaskVariant)
        self.listFile.itemClicked.connect(self.getCurrentFileName)

    def createLayoutHierarchy(self):

        self.assetsLayout.addWidget(self.assetTypeCombo)
        self.assetsLayout.addWidget(self.listAssets)

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

        self.mainAssetLayout.addLayout(self.assetsLayout)


        self.mainAssetLayout.addLayout(self.assetInfoLayout)

        self.mainLayout.addLayout(self.mainAssetLayout)
        self.mainLayout.addLayout(self.currentProjectLayout)


        # Main Layout > Main Widget
        self.mainWidget.setLayout(self.mainLayout)

        # Main Widget > Window
        self.setCentralWidget(self.mainWidget)

    #----------------------------------------------------------------------------
    #  METHODS
    #----------------------------------------------------------------------------

    def getCurrentAssetName(self):
        currentItem = self.listAssets.currentItem()
        self.assetName = self.listAssets.itemWidget(currentItem).name
        self.assetNameLabel.setText(self.assetName)

    def listCurrentAssetType(self):
        type = self.assetTypeCombo.currentText()
        self.getAssetByType(type)
        self.assetType = type

    def getCurrentAssetType(self):
        currentItem = self.listAssets.currentItem()
        self.assetType = self.listAssets.itemWidget(currentItem).type
        self.assetTypeLabel.setText(self.assetType)

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

    def openFile(self):

        if self.currentProjectPath and self.assetType and self.assetName and self.assetTask and self.taskVariant and SOFTWARE and self.workingDir:

            result = mc.confirmDialog(
                title='Save Changement',
                message='Save your scene:',
                button=["Save", "Don't Save", "Cancel"],
                defaultButton='Cancel',
                cancelButton='Cancel',
                dismissString='Cancel')

            filePath = os.sep.join(
                [self.currentProjectPath, 'prod', 'assets', self.assetType,
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

    def incrementAndSave(self):

        currentScenePath = mc.file(query=True, sceneName=True)

        currentScene = file.File(currentScenePath)

        currentScene.incrementAndSave()


    def importReference(self):

        filePath = os.sep.join(
            [self.currentProjectPath, 'prod', 'assets', self.assetType, self.assetName,
             self.assetTask, self.taskVariant, SOFTWARE, self.workingDir, self.fileName])

        mc.file(filePath, reference=True, namespace=self.assetName)

    def getAssetFilePath(self):

        self.getCurrentTaskVariant()

        listFile = asset.getAssetFilePath(self.assetType,
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

            allVariant = asset.getTaskVariant(self.assetType, self.assetName, self.assetTask)
            self.taskVariantCombo.clear()
            self.taskVariantCombo.addItems(allVariant)


    def getAssetTask(self):

        self.getCurrentAssetName()
        self.getCurrentAssetType()

        self.assetTaskCombo.clear()
        self.assetTaskCombo.addItems(asset.getAssetTask(self.assetType, self.assetName))


    def getAssetByType(self, type):

        self.listAssets.clear()

        allAssets = asset.getAssetByType(type)
        for assetName in allAssets:
            assetWidget = AssetItem(assetName, allAssets[assetName])
            assetListWidgetItem = QtGui.QListWidgetItem(self.listAssets)

            assetListWidgetItem.setSizeHint(assetWidget.sizeHint())

            self.listAssets.addItem(assetListWidgetItem)

            self.listAssets.setItemWidget(assetListWidgetItem, assetWidget)

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


class NewAssetUi(QtGui.QWidget):

    def __init__(self):
        super(NewAssetUi, self).__init__()

        self.setWindowTitle('New Asset')

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


class NewProjectUi(QtGui.QWidget):

    def __init__(self):
        super(NewProjectUi, self).__init__()

        self.setWindowTitle('New Project')

        self.mainLayout = QtGui.QVBoxLayout()

        self.projectTxt = QtGui.QLineEdit()
        self.projectPath = LineEditBrowse()
        self.projectBtn = QtGui.QPushButton()
        self.projectBtn.setText('Create new project')

        self.mainLayout.addWidget(self.projectTxt)
        self.mainLayout.addWidget(self.projectPath)
        self.mainLayout.addWidget(self.projectBtn)

        self.setLayout(self.mainLayout)

        self.projectBtn.clicked.connect(self.newProject)


    def newProject(self):
        projectName = str(self.projectTxt.text())
        projectPath = str(self.projectPath.lineEdit.text())

        if projectName and projectPath:
            newProject = project.Project(projectName, projectPath)
            newProject.createProject()
            self.close()


class SetProjectUi(NewProjectUi):

    def __init__(self):
        super(SetProjectUi, self).__init__()

        self.setWindowTitle('Set Project')

        self.projectBtn.setText('Set project')

        self.projectTxt.hide()

        self.projectBtn.clicked.connect(self.setProject)

    def setProject(self):

        projectPath, projectName = str(self.projectPath.lineEdit.text()).rsplit(os.sep, 1)

        if projectName and projectPath:
            newProject = project.Project(projectName, projectPath)
            newProject.setCurrentProject()
            self.close()


class LineEditBrowse(QtGui.QWidget):

    def __init__(self):
        super(LineEditBrowse, self).__init__()

        self. mainLayout = QtGui.QHBoxLayout()

        self.lineEdit = QtGui.QLineEdit()
        self.browseBtn = QtGui.QPushButton()
        self.browseBtn.setText('...')

        self.mainLayout.addWidget(self.lineEdit)
        self.mainLayout.addWidget(self.browseBtn)

        self.setLayout(self.mainLayout)

        self.mainLayout.setSpacing(0)

        self.browseBtn.clicked.connect(self.selectDirectory)

    def selectDirectory(self):
        folderPath =str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folderPath:
            self.lineEdit.setText(folderPath)

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

        self.mainLayout.addWidget(self.nameTxt)
        self.mainLayout.addWidget(self.typeTxt)

        self.setLayout(self.mainLayout)


def mayaLaunch():
    ''' Def to call to launch tool in maya '''

    global projectManagerWin, SOFTWARE

    SOFTWARE = 'maya'

    if projectManagerWin:
        projectManagerWin.close()

    projectManagerWin = ProjectManagerUi()
    projectManagerWin.show()