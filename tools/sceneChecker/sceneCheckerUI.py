#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`sceneCheckerUI`
===================================

.. module:: sceneCheckerUI
   :platform: Windows
   :synopsis: check maya scene
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.07.12
'''

from PySide import QtGui, QtCore
from pipeline.core import log
import os

__version__ = '0.1.0'

sceneCheckerLog = log.Log('SCENE_CHECKER_UI')

sceneCheckerWin = None
SOFTWARE = None


class SceneCheckerUI(QtGui.QWidget):
    def __init__(self):
        super(SceneCheckerUI, self).__init__()

        self.setWindowTitle('Scene Checker - {}'.format(__version__))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.dictTask = None
        self.checkList = []

        self.createLayout()
        self.createWidget()
        self.createHierarchy()
        self.createConnections()

    def createLayout(self):
        self.mainLayout = QtGui.QVBoxLayout()

    def createWidget(self):

        # Combo Box for Category choice
        self.categoryCombo = QtGui.QComboBox()
        self.dictTask = getAllTask()
        for task in self.dictTask:
            self.categoryCombo.addItem(task)

    def createHierarchy(self):

        self.mainLayout.addWidget(self.categoryCombo)

        self.setLayout(self.mainLayout)

    def createConnections(self):
        self.categoryCombo.activated.connect(self.changeTask)

    def changeTask(self):

        if self.dictTask:
            task = str(self.categoryCombo.currentText())
            try:
                exec self.dictTask[task]
            except:
                print 'Nothing'

            self.dictCheck = {}

            for check in self.checkList:

                checkWidget = CheckWidget(check)
                self.mainLayout.addWidget(checkWidget)
                checkClass = task + '.' + check + '()'

                self.dictCheck[check] = {checkClass}

                checkWidget.checkBtn.clicked.connect(lambda _:self.check(checkClass))
                checkWidget.fixBtn.clicked.connect(lambda _:self.fix(checkClass))

    def check(self, command):
        exec command + '.check()'

    def fix(self, command):
        exec command + '.fix()'

class CheckWidget(QtGui.QWidget):

    def __init__(self, title, fixExist=True, optional=False):
        super(CheckWidget, self).__init__()

        self.title = title
        self.fixExist = fixExist
        self.optional = optional

        self.mainLayout = QtGui.QVBoxLayout()
        self.headerLayout = QtGui.QHBoxLayout()

        self.titleLabel = QtGui.QLabel()
        self.titleLabel.setText(self.title)

        self.checkBtn = QtGui.QPushButton()
        self.checkBtn.setText('Check')

        self.headerLayout.addWidget(self.titleLabel)

        if self.fixExist:
            self.fixBtn = QtGui.QPushButton()
            self.fixBtn.setText('fix')
            self.headerLayout.addWidget(self.fixBtn)

        self.headerLayout.addWidget(self.checkBtn)

        self.mainLayout.addLayout(self.headerLayout)
        self.setLayout(self.mainLayout)


def getAllTask():

    listRemoveFile = ['__init__.py']
    dictTask = {}
    scriptFolder = os.path.dirname(os.path.realpath(__file__))
    taskFolder = os.sep.join([scriptFolder, 'task'])
    if os.path.exists(taskFolder):
        listAllFile = os.listdir(taskFolder)
        if listAllFile:
            for file in listAllFile:
                if file not in listRemoveFile:
                    task, extension = file.rsplit('.',1)
                    if extension == 'py':
                        dictTask[task] = 'from task import {0}\nreload({0})\nself.checkList = {0}.CHECKLIST'.format(task)

    return dictTask


def mayaLaunch():
    ''' Def to call to launch tool in maya '''

    global sceneCheckerWin, SOFTWARE

    SOFTWARE = 'maya'

    if sceneCheckerWin:
        sceneCheckerWin.close()

    sceneCheckerWin = SceneCheckerUI()
    sceneCheckerWin.show()