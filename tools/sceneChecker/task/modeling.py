
from pipeline.core import log

modelingLog = log.Log('SCENE_CHECKER  MODELING')

CHECKLIST = ['NonUniqueName',
             'NonManifold']


class NonUniqueName(object):

    def __init__(self):

        self.title = 'Non-Unique name'
        self.fixExist = True

    def check(self):
        return False

    def log(self):
        modelingLog.error('error')

    def fix(self):
        modelingLog.info('Fix in progress')


class NonManifold(object):

    def __init__(self):

        self.title = 'Non-Manifold'
        self.fixExist = True

    def check(self):
        return True

    def log(self):
        modelingLog.error('NonManifold error')

    def fix(self):
        modelingLog.info('Fix in progress')