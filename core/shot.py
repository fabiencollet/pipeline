#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`shot`
===================================

.. module:: shot
   :platform: Windows
   :synopsis: pipeline shot library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

import xml.etree.ElementTree as ET
import os
import project, file, task, log
import maya.cmds as mc


shotLog = log.Log('shot')

PIPE_SHOTS = os.sep.join(['prod', 'sequences'])

SHOT_TASKS = ('animation', 'cloth', 'fx', 'ligthing', 'compositing', 'light', 'camera')
MASTER_TASKS = ('layout', 'fx', 'ligthing', 'light', 'camera')

# EDITING

SEQUENCE_NAME = './project/children/sequence/name'
SEQUENCE_DURATION = './project/children/sequence/duration'

ALL_SHOT = './project/children/sequence/media/video/track/clipitem'


class Sequence(object):
    
    def __init__(self, name):
        
        self.project = project.Project()
        self.projectPath = self.project.path
        
        self.name = name
        self.shots = None
        self.path = os.sep.join([self.projectPath, PIPE_SHOTS, self.name])

        self.edlFolder = os.sep.join([self.projectPath, 'editing', 'edl', self.name])

        if not os.path.exists(self.edlFolder):
            os.makedirs(self.edlFolder)

        self.allEDLFile = os.listdir(self.edlFolder)

        if self.allEDLFile:
            self.lastEdl = self.allEDLFile[-1]
            self.lastEdlPath = os.sep.join([self.edlFolder, self.lastEdl])
        else:
            self.lastEdl = None

            # Function
        self.getShots()
        
    def getShots(self):
        self.shots = os.listdir(self.path)
        return self.shots

    def getShotOrder(self):
        tree = ET.parse(self.lastEdlPath)
        for s in tree.findall(ALL_SHOT):
            print s.find('name').text

    def getLastEDL(self):
        tree = ET.parse(self.lastEdlPath)
        for s in tree.findall(ALL_SHOT):
            print s.find('start').text


class Shot(object):

    def __init__(self,referenceNode):

        self.node = referenceNode
        self.namespace = None
        self.filename = None

        self.getNamespace()
        self.getFilename()

        self.file = file.File(self.filename)

        self.sequence = self.file.type
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


def createSequence(name):
    projectName, projectPath = project.getCurrentProject()
    if projectName and projectPath:
        sequencePath = os.sep.join([projectPath, PIPE_SHOTS, name])
        if not os.path.exists(sequencePath):
            os.makedirs(sequencePath)

    else:
        shotLog.error('Current project does not exist')


def createShot(sequence, name):
    projectName, projectPath = project.getCurrentProject()

    shotName = '_'.join([sequence, name])

    if projectName and projectPath:
        if sequence in getAllSequeces():
            shotTaskPath = os.sep.join([projectPath, PIPE_SHOTS, sequence, shotName])
            for shotTask in SHOT_TASKS:
                shot = task.Task('shot', shotTask, shotTaskPath)
                shot.createTask()

        else:
            shotLog.error('shot sequence "{0}" does not exist'.format(sequence))

    else:
        shotLog.error('Current project does not exist')


def createMaster(sequence, name):
    projectName, projectPath = project.getCurrentProject()

    masterName = '_'.join([sequence, 'm'+name])

    if projectName and projectPath:
        if sequence in getAllSequeces():
            masterTaskPath = os.sep.join([projectPath, PIPE_SHOTS, sequence, masterName])
            for masterTask in MASTER_TASKS:
                shot = task.Task('master', masterTask, masterTaskPath)
                shot.createTask()

        else:
            shotLog.error('shot sequence "{0}" does not exist'.format(sequence))

    else:
        shotLog.error('Current project does not exist')

def sequenceExist(sequence):
    projectName, projectPath = project.getCurrentProject()
    if projectName and projectPath:
        if sequence in getAllSequeces():
            shotSequencePath = os.sep.join([projectPath, PIPE_SHOTS, sequence])
            if os.path.exists(shotSequencePath):
                return True
            else:
                return False

def getAllSequeces():
    projectName, projectPath = project.getCurrentProject()
    if projectName and projectPath:
        sequencesPath = os.sep.join([projectPath, PIPE_SHOTS])
        return os.listdir(sequencesPath)


def getShotBysequence(sequence):

    projectName, projectPath = project.getCurrentProject()

    dictshots = {}

    if sequence == 'all':

        for shotSequence in getAllSequeces():

            shotSequencePath = os.sep.join([projectPath, PIPE_SHOTS, shotSequence])
            if os.path.exists(shotSequencePath):
                listshots = os.listdir(shotSequencePath)
                for shotName in listshots:
                    if isShot(shotName):
                        dictshots[shotName] = shotSequence

        return dictshots


    else:
        if sequence in getAllSequeces():

            shotSequencePath = os.sep.join([projectPath, PIPE_SHOTS, sequence])
            listshots = os.listdir(shotSequencePath)

            for shotName in listshots:
                if isShot(shotName):
                    dictshots[shotName] = sequence

            return dictshots


def getMasterBysequence(sequence):

    projectName, projectPath = project.getCurrentProject()

    dictMasters = {}

    if sequence == 'all':

        for masterSequence in getAllSequeces():

            masterSequencePath = os.sep.join([projectPath, PIPE_SHOTS, masterSequence])
            if os.path.exists(masterSequencePath):
                listMasters = os.listdir(masterSequencePath)
                for masterName in listMasters:
                    if isMaster(masterName):
                        dictMasters[masterName] = masterSequence

        return dictMasters


    else:
        if sequence in getAllSequeces():

            masterSequencePath = os.sep.join([projectPath, PIPE_SHOTS, sequence])
            listMasters = os.listdir(masterSequencePath)

            for masterName in listMasters:
                if isMaster(masterName):
                    dictMasters[masterName] = sequence

            return dictMasters


def getShotTask(sequence, name):

    projectName, projectPath = project.getCurrentProject()

    shotSequencePath = os.sep.join([projectPath, PIPE_SHOTS, sequence])
    if os.path.exists(shotSequencePath):
        shotPath = os.sep.join([shotSequencePath, name])
        if os.path.exists(shotPath):
            return os.listdir(shotPath)


def getTaskVariant(sequence, name, task):

    projectName, projectPath = project.getCurrentProject()

    shotSequencePath = os.sep.join([projectPath, PIPE_SHOTS, sequence])
    if os.path.exists(shotSequencePath):
        shotPath = os.sep.join([shotSequencePath, name])
        if os.path.exists(shotPath):
            taskPath = os.sep.join([shotPath, task])
            if os.path.exists(taskPath):
                return os.listdir(taskPath)




def getshotFilePath(sequence, name, task, variant, software, workingDirectory):

    projectName, projectPath = project.getCurrentProject()

    listMayaAsciiFile = []

    allTask = getShotTask(sequence, name)
    if task in allTask:
        softwarePath = os.sep.join([projectPath, PIPE_SHOTS, sequence, name, task, variant, software])
        if os.path.exists(softwarePath):
            workingDirectoryPath = os.sep.join([softwarePath, workingDirectory])
            if os.path.exists(workingDirectoryPath):
                listAllFile = os.listdir(workingDirectoryPath)
                for file in listAllFile:
                    if file.rsplit('.',1)[-1] == 'ma':
                        listMayaAsciiFile.append(file)

                return listMayaAsciiFile


def getshotInfoFromshotScene(software):

    dictShotInfo = {}

    if software == 'maya':

        filePath = mc.file(query=True, sceneName=True)

        if filePath:
            dictShotInfo['sequence'],\
                dictShotInfo['name'],\
                dictShotInfo['task'],\
                dictShotInfo['variant'],\
                dictShotInfo['software'],\
                dictShotInfo['workingDirectory'] = filePath.rsplit(os.sep, 7)[1:-1]

            return dictShotInfo

        else:
            return None


def getAllshotsNode():
    return mc.ls(references=True)

def isShot(name):
    try:
        sequence, shotName = name.rsplit('_', 1)
        if not len(shotName.split('m')) > 1:
            return True
        else:
            return False
    except:
        return None

def isMaster(name):
    try:
        sequence, masterName = name.rsplit('_', 1)
        if len(masterName.split('m')) > 1:
            return True
        else:
            return False
    except:
        return None