# -*- coding: utf-8 -*-

import maya.utils as utils

print 'Building Pipeline Toolkit...'

import sfmg
reload(sfmg)

utils.executeDeferred(sfmg.buildMayaShelf)

#sfmg.buildMayaShelf()

