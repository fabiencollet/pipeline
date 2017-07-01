#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`project`
===================================

.. module:: project
   :platform: Windows
   :synopsis: pipeline project library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

import os
import json
import log

projectLog = log.Log('PROJECT')

parentScriptFolder = os.path.dirname(os.path.realpath(__file__))

# Structure

JSON_CURRENT_PROJECT_PATH= os.sep.join([parentScriptFolder, 'data', 'curent_project.json'])
JSON_ALL_PROJECTS_PATH= os.sep.join([parentScriptFolder, 'data', 'all_projects.json'])

PROJECT_INFO_FOLDER = os.sep.join(['info', 'project'])
PROJECT_HIERARCHY = {'editing':('animatique',
                                'making_off',
                                'montage'),
                     'fromThird':('from',
                                  'to'),
                     'info':('contact',
                             'planning',
                             'project'),
                     'preProd':('artwork',
                                'ref',
                                'scenario',
                                'univers'),
                     'presentation':('documents',
                                     'film',
                                     'images'),
                     'prod':('assets',
                             'sequences'),
                     'trash':('_')
                     }


class Project(object):
    '''

    '''
    def __init__(self, name=None ,folder=None):

        if name:
            self.name = name
        else:
            try:
                self.name = getCurrentProject()[0]
            except:
                self.name = ''

        if folder:
            self.folder = folder
        else:
            try:
                self.folder = getCurrentProject()[1].rsplit(os.sep, 1)[0]
            except:
                self.folder = ''

        self.width = None
        self.height = None
        self.aspectRatio = None
        self.renderingEngine = None

        self.path = os.sep.join([self.folder, self.name])

        self.projectInfoFolderPath = os.sep.join([self.path, PROJECT_INFO_FOLDER])
        self.projectInfoPath = os.sep.join([self.projectInfoFolderPath, 'project_info.json'])

        self.currentProject = {}

        self.getProjectInfo()

    def createProject(self):

        for key in PROJECT_HIERARCHY:
            for item in PROJECT_HIERARCHY[key]:
                childPath = os.sep.join([self.path, key, item])
                if not os.path.exists(childPath):
                    os.makedirs(childPath)

        self.setCurrentProject()

    def setCurrentProject(self):

        projectName, projectPath = getCurrentProject()

        if projectName != self.name or projectPath != self.path:

            self.currentProject['name'] = self.name
            self.currentProject['path'] = self.path

            currentProjectData = json.dumps(self.currentProject, indent=2)

            f = open(JSON_CURRENT_PROJECT_PATH, 'w')
            f.write(currentProjectData)
            f.close()

        else:
            projectLog.info('Json File "current_project" is already set with this project')

    def getProjectInfo(self):

        if os.path.exists(self.projectInfoPath):

            f = open(self.projectInfoPath, 'r')
            projectInfoDict = json.loads(f.read())
            f.close()

            self.width = projectInfoDict['width']
            self.height = projectInfoDict['height']
            self.aspectRatio = projectInfoDict['aspectRatio']
            self.renderingEngine = projectInfoDict['renderingEngine']

            return projectInfoDict

        else:
            self.setDefaultProjectInfo()

    def setDefaultProjectInfo(self):

        self.width = 1920
        self.height = 803
        self.aspectRatio = 2.391
        self.renderingEngine = 'arnold'

        self.setProjectInfo()

    def setProjectInfo(self):

        projectInfoDict = {}
        projectInfoDict['width'] = self.width
        projectInfoDict['height'] = self.height
        projectInfoDict['aspectRatio'] = self.aspectRatio
        projectInfoDict['renderingEngine'] = self.renderingEngine

        json_data = json.dumps(projectInfoDict, indent=4)

        f = open(self.projectInfoPath, 'w')
        f.write(json_data)
        f.close()

        return projectInfoDict


def getCurrentProject():
    if os.path.exists(JSON_CURRENT_PROJECT_PATH):
        f = open(JSON_CURRENT_PROJECT_PATH, 'r')
        currentProjectData = json.loads(f.read())
        f.close()
        return currentProjectData['name'], currentProjectData['path']

    else:
        projectLog.warning('No current project set')
        return None, None


if __name__ == '__main__':
    project = Project('myProjectTest', 'E:\\Users\\Fab\\Documents\\arbre')
    project.createProject()

