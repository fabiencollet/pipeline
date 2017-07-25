#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`rigging`
===================================

.. module:: rigging
   :platform: Windows
   :synopsis: pipeline rigging library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

import maya.cmds as mc

### SHAPE

SHAPE = {'circle':
             {'periodic':True,
              'points':[(0.783611624891225, 4.798237340988468e-17, -0.7836116248912238),
                        (-1.2643170607829326e-16, 6.785732323110913e-17, -1.108194187554388),
                        (-0.7836116248912243, 4.798237340988471e-17, -0.7836116248912243),
                        (-1.108194187554388, 1.966335461618786e-32, -3.21126950723723e-16),
                        (-0.7836116248912245, -4.7982373409884694e-17, 0.783611624891224),
                        (-3.3392053635905195e-16, -6.785732323110915e-17, 1.1081941875543881),
                        (0.7836116248912238, -4.798237340988472e-17, 0.7836116248912244),
                        (1.108194187554388, -3.644630067904792e-32, 5.952132599280585e-16),
                        (0.783611624891225, 4.798237340988468e-17, -0.7836116248912238),
                        (-1.2643170607829326e-16, 6.785732323110913e-17, -1.108194187554388),
                        (-0.7836116248912243, 4.798237340988471e-17, -0.7836116248912243)],
              'knots':[-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
              'degree':3
              },
         'square':
             {'periodic':False,
              'points':[(1, 0, 1),
                        (-1, 0, 1),
                        (-1, 0, -1),
                        (1, 0, -1),
                        (1, 0, 1)],
              'degree':1}
         }


class Controller(object):

    def __init__(self, name):
        super(Controller, self).__init__()

        self.name = name
        self.localTranslation = [0,0,0]
        self.worldTranslation = [0,0,0]
        self.localRotation = [0,0,0]
        self.worldRotation = [0,0,0]
        self.localScale = [1,1,1]
        self.worldScale = [1,1,1]

        self.shape='circle'

    def exist(self):
        if self.name \
        and mc.objExists(self.name) \
        and mc.objectType(self.name) == 'transform':
            return True

        else:
            return False

    def setWorldTransformation(self):
        if self.exist():
            mc.xform(self.name,
                     worldSpace=True,
                     scale=self.worldScale,
                     translation=self.worldTranslation,
                     rotation=self.worldRotation)

    def create(self):
        if not self.exist():
            if SHAPE[self.shape]['periodic']:
                crv = mc.curve(periodic=SHAPE[self.shape]['periodic'],
                               point=SHAPE[self.shape]['points'],
                               knot=SHAPE[self.shape]['knots'],
                               degree=SHAPE[self.shape]['degree'])
            else:
                crv = mc.curve(point=SHAPE[self.shape]['points'],
                               degree=SHAPE[self.shape]['degree'])

            mc.rename(crv,self.name)

            self.setWorldTransformation()

def isController(objectName):
    ''' Test if maya objectName is a controller

    :param objectName: name of the controller
    :return: Boolean
    '''
    splitName = objectName.rsplit('_',1)
    if len(splitName) == 2 and splitName[1] == 'ctrl':
        return True
    else:
        return False
