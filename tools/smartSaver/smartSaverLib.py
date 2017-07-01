import os
import maya.cmds as mc

class Scene(object):

    def __init__(self, filePath):
        super(Scene, self).__init__()

        self.path, self.file = filePath.rsplit(os.sep, 1)

        self.fileName, self.extension = self.file.rsplit('.', 1)

        self.fileNameWithoutVersion, self.version = self.fileName.rsplit('-', 1)

        self.versionNumber = int(self.version.split('v', 1)[-1])




scene = Scene('E:\Users\Fab\Documents\testProject\cops\prod\assets\props\car\modeling\base\maya\work\car-modeling-base-work-v001.ma')

print scene.file