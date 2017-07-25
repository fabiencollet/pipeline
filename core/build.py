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

from pipeline.lib import maya as mc


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

                mc.sets(empty=True, name='to_rigging_set')
                mc.sets(empty=True, name='modeling_hi_set')
                mc.sets(empty=True, name='modeling_lo_set')
                mc.sets(['modeling_hi_set', 'modeling_lo_set'], name='modeling_set')
                mc.sets(empty=True, name='connection_hi_set')
                mc.sets(empty=True, name='connection_lo_set')
                mc.sets(['connection_hi_set', 'connection_lo_set'], name='connection_set')
                mc.sets(empty=True, name='smooth0_set')
                mc.sets(empty=True, name='smooth1_set')
                mc.sets(empty=True, name='smooth2_set')
                mc.sets(empty=True, name='smooth3_set')
                mc.sets(empty=True, name='smooth4_set')
                mc.sets(['smooth0_set',
                         'smooth1_set',
                         'smooth2_set',
                         'smooth3_set',
                         'smooth4_set'], name='smooth_set')

                mc.sets(['modeling_set', 'smooth_set',
                         'connection_set'], name='GRP_set')

            elif task == 'layout':
                mc.group(empty=True, name='__CAMS__')
                mc.group(empty=True, name='__SETS__')
                mc.group(empty=True, name='__CHARACTERS__')
                mc.group(empty=True, name='__PROPS__')
                mc.group(empty=True, name='__LIGHTS__')

                mc.shot('s010NEW_0010')