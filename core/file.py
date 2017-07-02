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


class File(object):

    def __init__(self, filePath):
        super(File, self).__init__()

        self.getInfo(filePath)

    def getInfo(self, filePath):

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

    def incrementAndSave(self):

        allFile = os.listdir(self.path)

        listAllVersion = []

        for file in allFile:
            fileName, extension = file.rsplit('.', 1)

            fileNameWithoutVersion, version = fileName.rsplit('-', 1)

            versionNumber = int(version.split('v', 1)[-1])

            listAllVersion.append(versionNumber)


        lastestVersion = sorted(listAllVersion)[-1]

        newVersionNumber = lastestVersion+1
        newVersion = 'v%03d' % newVersionNumber

        newFileName = '-'.join([self.name, self.task, self.variant, self.workingDir, newVersion])

        newFile = '.'.join([newFileName, self.extension])

        newPath = os.sep.join([self.path, newFile])

        mc.file(rename=newPath)
        mc.file(save=True, type='mayaAscii')
