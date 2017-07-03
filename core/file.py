#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`scene`
===================================

.. module:: scene
   :platform: Windows
   :synopsis: pipeline scene library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

import os
import maya.cmds as mc
import project, asset, shot

ASSET_TYPE = ('props', 'cameras', 'characters', 'sets', 'lights')

class File(object):

    def __init__(self, filePath=None):
        super(File, self).__init__()

        if filePath:
            self.getInfofromCurrentFile(filePath)
        else:
            self.projectPath = None
            self.pipelinePath = None
            self.path = None

            self.pipeline = None
            self.type = None
            self.name = None
            self.task = None
            self.variant = None
            self.software = None
            self.workingDir = None



    def getInfofromCurrentFile(self, filePath):

        self.path, self.file = filePath.rsplit('/', 1)

        print self.path

        self.fileName, self.extension = self.file.rsplit('.', 1)

        self.fileNameWithoutVersion, self.version = self.fileName.rsplit('-', 1)

        self.versionNumber = int(self.version.split('v', 1)[-1])

        self.type, \
        self.name, \
        self.task, \
        self.variant, \
        self.software, \
        self.workingDir = self.path.rsplit('/', 6)[1:]

        self.getPipeline()

    def getPipeline(self):
        if self.type in ASSET_TYPE:
            self.pipeline = 'asset'
        else:
            self.pipeline = 'shot'

    def saveAs(self, type, name, task, variant, software, workingDir):

        self.type = type
        self.name = name
        self.task = task
        self.variant = variant
        self.software = software
        self.workingDir = workingDir

        currentProject = project.Project()
        self.projectPath = currentProject.path

        self.getPipeline()

        if self.pipeline == 'asset':
            self.prodPath = os.sep.join([self.projectPath, asset.PIPE_ASSETS])
        if self.pipeline == 'shot':
            self.prodPath = os.sep.join([self.projectPath, shot.PIPE_SHOTS])

        self.path = os.sep.join([self.prodPath, self.type, self.name, self.task,
                                 self.variant, self.software, self.workingDir])

        if self.software == 'maya':
            self.extension = 'ma'

        self.incrementAndSave()

    def incrementAndSave(self):

        currentProject = project.Project()
        self.projectPath = currentProject.path

        allFile = os.listdir(self.path)

        if allFile:

            listAllVersion = []

            for file in allFile:
                fileName, extension = file.rsplit('.', 1)

                fileNameWithoutVersion, version = fileName.rsplit('-', 1)

                versionNumber = int(version.split('v', 1)[-1])

                listAllVersion.append(versionNumber)

            lastestVersion = sorted(listAllVersion)[-1]

            newVersionNumber = lastestVersion+1
            newVersion = 'v%03d' % newVersionNumber

        else:
            newVersion = 'v001'

        newFileName = '-'.join([self.name, self.task, self.variant, self.workingDir, newVersion])

        newFile = '.'.join([newFileName, self.extension])

        newPath = os.sep.join([self.path, newFile])

        mc.file(rename=newPath)
        mc.file(save=True, type='mayaAscii')
