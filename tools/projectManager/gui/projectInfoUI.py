#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`projectInfoUI`
===================================

.. module:: projectInfoUI
   :platform: Windows
   :synopsis: manage project's information
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

from PySide import QtGui,QtCore
from pipeline.core import project,log,widget


projectInfoLog = log.Log('PROJECT_INFO')

projectInfoWin = None
SOFTWARE = None


class ProjectInfoUi(QtGui.QWidget):

    def __init__(self):
        super(ProjectInfoUi, self).__init__()

        projectInfoLog.info('init UI')

        self.setWindowTitle('Project Info')
        self.setMinimumSize(200,300)
        self.resize(200,300)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.currentProject = project.Project()

        self.getCurrentInfo()



        # UI
        self.mainLayout = QtGui.QVBoxLayout()

        self.widthWidget = widget.LineEdit('Width')
        self.widthWidget.lineEdit.setText(self.projectWidth)

        self.heightWidget = widget.LineEdit('Height')
        self.heightWidget.lineEdit.setText(self.projectHeight)

        self.aspectRatioWidget = widget.LineEdit('Aspect ratio')
        self.aspectRatioWidget.lineEdit.setText(self.projectAspectRatio)

        self.renderWidget = widget.LineEdit('Render Engine')
        self.renderWidget.lineEdit.setText(self.projectRenderingEngine)

        # Buttons
        self.saveInfoBtn = QtGui.QPushButton()
        self.saveInfoBtn.setText('Save info')


        self.mainLayout.addWidget(self.widthWidget)
        self.mainLayout.addWidget(self.heightWidget)
        self.mainLayout.addWidget(self.aspectRatioWidget)
        self.mainLayout.addWidget(self.renderWidget)

        self.mainLayout.addWidget(self.saveInfoBtn)

        self.setLayout(self.mainLayout)

        # Connections
        self.saveInfoBtn.clicked.connect(self.saveInfo)

    def saveInfo(self):

        self.currentProject.width = int(self.widthWidget.lineEdit.text())
        self.currentProject.height = int(self.heightWidget.lineEdit.text())
        self.currentProject.aspectRatio = float(self.aspectRatioWidget.lineEdit.text())
        self.currentProject.renderingEngine = str(self.renderWidget.lineEdit.text())

        self.currentProject.setProjectInfo()

    def getCurrentInfo(self):



        self.projectPathInfo = self.currentProject.projectInfoPath

        self.projectWidth = str(self.currentProject.width)
        self.projectHeight = str(self.currentProject.height)
        self.projectAspectRatio = str(self.currentProject.aspectRatio)
        self.projectRenderingEngine = str(self.currentProject.renderingEngine)


def mayaLaunch():
    ''' Def to call to launch tool in maya '''

    global projectInfoWin, SOFTWARE

    SOFTWARE = 'maya'

    if projectInfoWin:
        projectInfoWin.close()

    projectInfoWin = ProjectInfoUi()
    projectInfoWin.show()