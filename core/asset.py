#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`asset`
===================================

.. module:: asset
   :platform: Windows
   :synopsis: pipeline asset library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

import os
import project, file, task, log
import maya.cmds as mc


assetLog = log.Log('ASSET')

ASSETS_PATH = os.sep.join(['prod', 'assets'])

ASSET_TYPES = ['props', 'sets', 'characters']

ASSET_TASKS = ('artwork', 'modeling', 'texturing', 'shading', 'rigging', 'cloth')


class Asset(object):

    def __init__(self,referenceNode):

        self.node = referenceNode
        self.namespace = None
        self.filename = None

        self.getNamespace()
        self.getFilename()

        self.file = file.File(self.filename)

        self.type = self.file.type
        self.name = self.file.name
        self.task = self.file.task
        self.variant = self.file.variant
        self.software = self.file.software
        self.workingDir = self.file.workingDir

    def getNamespace(self):

        namespace = mc.referenceQuery(self.node, namespace=True)
        self.namespace = namespace
        return namespace

    def getFilename(self):

        filename = mc.referenceQuery(self.node, filename=True)
        self.filename = filename
        return filename



def createAsset(type, name):
    projectName, projectPath = project.getCurrentProject()
    if projectName and projectPath:
        if type in ASSET_TYPES:
            assetTaskPath = os.sep.join([projectPath, ASSETS_PATH, type, name])
            for assetTask in ASSET_TASKS:
                asset = task.Task(assetTask, assetTaskPath)
                asset.createTask()

        else:
            assetLog.error('Asset type "{0}" does not exist'.format(type))

    else:
        assetLog.error('Current project does not exist')


def assetTypeExist(type):
    projectName, projectPath = project.getCurrentProject()
    if projectName and projectPath:
        if type in ASSET_TYPES:
            assetTypePath = os.sep.join([projectPath, ASSETS_PATH, type])
            if os.path.exists(assetTypePath):
                return True
            else:
                return False



def getAssetByType(type):

    projectName, projectPath = project.getCurrentProject()

    dictAssets = {}

    if type == 'all':

        for assetType in ASSET_TYPES:

            assetTypePath = os.sep.join([projectPath, ASSETS_PATH, assetType])
            if os.path.exists(assetTypePath):
                listAssets = os.listdir(assetTypePath)

                for assetName in listAssets:
                    dictAssets[assetName] = assetType

        return dictAssets


    else:
        if type in ASSET_TYPES:

            assetTypePath = os.sep.join([projectPath, ASSETS_PATH, type])
            listAssets = os.listdir(assetTypePath)

            for assetName in listAssets:
                dictAssets[assetName] = type

            return dictAssets


def getAssetTask(type, name):

    projectName, projectPath = project.getCurrentProject()

    assetTypePath = os.sep.join([projectPath, ASSETS_PATH, type])
    if os.path.exists(assetTypePath):
        assetPath = os.sep.join([assetTypePath, name])
        if os.path.exists(assetPath):
            return os.listdir(assetPath)


def getTaskVariant(type, name, task):

    projectName, projectPath = project.getCurrentProject()

    assetTypePath = os.sep.join([projectPath, ASSETS_PATH, type])
    if os.path.exists(assetTypePath):
        assetPath = os.sep.join([assetTypePath, name])
        if os.path.exists(assetPath):
            taskPath = os.sep.join([assetPath, task])
            if os.path.exists(taskPath):
                return os.listdir(taskPath)




def getAssetFilePath(type, name, task, variant, software, workingDirectory):

    projectName, projectPath = project.getCurrentProject()

    listMayaAsciiFile = []

    allTask = getAssetTask(type, name)
    if task in allTask:
        softwarePath = os.sep.join([projectPath, ASSETS_PATH, type, name, task, variant, software])
        if os.path.exists(softwarePath):
            workingDirectoryPath = os.sep.join([softwarePath, workingDirectory])
            if os.path.exists(workingDirectoryPath):
                listAllFile = os.listdir(workingDirectoryPath)
                for file in listAllFile:
                    if file.rsplit('.',1)[-1] == 'ma':
                        listMayaAsciiFile.append(file)

                return listMayaAsciiFile


def getAssetInfoFromAssetScene(software):

    dictAssetInfo = {}

    if software == 'maya':

        filePath = mc.file(query=True, sceneName=True)

        if filePath:
            dictAssetInfo['type'],\
                dictAssetInfo['name'],\
                dictAssetInfo['task'],\
                dictAssetInfo['variant'],\
                dictAssetInfo['software'],\
                dictAssetInfo['workingDirectory'] = filePath.rsplit(os.sep, 7)[1:-1]

            return dictAssetInfo

        else:
            return None


def getAllAssetsNode():
    return mc.ls(references=True)