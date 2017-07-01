#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`task`
===================================

.. module:: task
   :platform: Windows
   :synopsis: pipeline task library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

import os

import project
import log

taskLog = log.Log('TASK')

TASK_SOFTWARES = {'artwork':['photoshop',
                             'zbrush'],
                  'modeling':['maya',
                             'cinema4d',
                             'modo',
                             'houdini',
                             'zbrush'],
                  'texturing':['photoshop',
                               'mari',
                               'zbrush'],
                  'shading':['maya',
                             'katana',
                             'max',
                             'houdini',
                             'cinema4d'],
                  'rigging':['maya',
                             'cinema4d'],
                  'cloth':['maya',
                           'marvelous',
                           'houdini'],
                  'animation':['maya'],
                  'fx':['maya',
                        'houdini'],
                  'ligthing':['maya',
                              'octane',
                              'katana',
                              'guerilla'],
                  'compositing':['nuke',
                                 'after']
                 }

TASK_VARIANTS = {'artwork':['base'],
                'modeling':['base',
                            'lo',
                            'hi'],
                'texturing':['base'],
                'shading':['base'],
                'rigging':['base',
                           'lo',
                           'hi'],
                'cloth':['base'],
                'animation':['base'],
                'fx':['base'],
                'ligthing':['base'],
                'compositing':['base']
                }

SUBTASK_FOLDERS = {'asset':['work', 'publish', 'images', 'description'],
                   'master': ['work', 'publish', 'images', 'description'],
                   'shot': ['work', 'publish', 'images', 'caches', 'description']}

class Task(object):

    def __init__(self, type, name, path):

        if not name in TASK_SOFTWARES:
            taskLog.error('Task "{0}" does not exist'.format(name))

        self.type = type
        self.name = name
        self.path = path

        self.listSoftwares = TASK_SOFTWARES[name]

    def createTask(self):

        taskPath = os.sep.join([self.path, self.name])

        for variant in TASK_VARIANTS[self.name]:
            variantPath = os.sep.join([taskPath, variant])

            for software in self.listSoftwares:
                softwarePath = os.sep.join([variantPath, software])

                for subTask in SUBTASK_FOLDERS[self.type]:
                    subTaskPath = os.sep.join([softwarePath, subTask])
                    if not os.path.exists(subTaskPath):
                        os.makedirs(subTaskPath)
