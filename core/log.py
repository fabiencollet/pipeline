#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`log`
===================================

.. module:: log
   :platform: Windows
   :synopsis: pipeline log library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''
import pprint

class Log(object):
    def __init__(self, scriptName):

        self.scripName = scriptName

    def error(self, text):
        print '[PIPELINE] [{0}] [ERROR]    | {1}'.format(self.scripName, text)


    def warning(self, text):
        print '[PIPELINE] [{0}] [WARNING]  | {1}'.format(self.scripName, text)


    def info(self, text):
        print '[PIPELINE] [{0}] [INFO]     | {1}'.format(self.scripName, text)

    def dict_print(self, dict):
        pprint.pprint(dict)