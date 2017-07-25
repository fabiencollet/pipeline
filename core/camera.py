#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`camera`
===================================

.. module:: camera
   :platform: Windows
   :synopsis: pipeline camera library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

from pipeline.lib import maya as mc


class Camera(object):

    def __init__(self, name, focalLenght=50):
        super(Camera, self).__init__()

        self.name = name
        self.focalLenght = focalLenght

    def createCamera(self):

        newCamera = mc.camera()
        mc.rename(newCamera[0], self.name)

        mc.camera(self.name, edit=True, focalLength=self.focalLenght)