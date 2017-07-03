#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`build`
===================================

.. module:: build
   :platform: Windows
   :synopsis: pipeline build library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.06.25
'''

import maya.cmds as mc


def buildInitScene(software, task):

    result = mc.confirmDialog(
        title='Save Changes',
        message='Save your scene:',
        button=["Don't Save", "Cancel"],
        defaultButton='Cancel',
        cancelButton='Cancel',
        dismissString='Cancel')

    if result == 'Cancel':
        return

    else:
        if software == 'maya':
            mc.file(new=True, force=True)

            if task == 'modeling':
                modGroup = mc.group(empty=True, name='MOD')
                mc.group(modGroup, name='GRP')

                mc.sets(empty=True, name='toRig_set')
                mc.sets(empty=True, name='hi_set')
                mc.sets(empty=True, name='lo_set')
                mc.sets(['hi_set', 'lo_set'], name='modeling_set')

            elif task == 'layout':
                mc.group(empty=True, name='__CAMS__')
                mc.group(empty=True, name='__SETS__')
                mc.group(empty=True, name='__CHARACTERS__')
                mc.group(empty=True, name='__PROPS__')
                mc.group(empty=True, name='__LIGHTS__')