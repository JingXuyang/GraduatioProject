# -*- coding: utf-8 -*-

############################# Pipeline Toolkit Menu ##########################

import maya.utils as utils
import maya.cmds as cmds


import sys,os
sys.path.append(os.path.dirname(os.path.realpath('__file__'))+"\\widget")

print 'Building Pipeline Toolkit...'

openWin = '''
# import plwin
# reload(plwin)
# plwin.open()

import sys
sys.path.append("D:\GraduatioProject\widget")
import _ui
win = _ui.OpenWidget()
win.show()
win.exec_()

'''

saveWin = '''
import plwin
reload(plwin)
plwin.save()
'''

publishWin = '''
import plwin
reload(plwin)
plwin.publish()
'''


def main_ui():
    #cmds.evalDeferred()
    cmds.menu('my_tool', label=u"Maya Pipeline", parent="MayaWindow", tearOff=True)
    cmds.menuItem("open", label=u"Open", parent='my_tool', c=openWin)
    cmds.menuItem("submite", label=u"Submite File", parent="my_tool", c=saveWin)
    cmds.menuItem("publish", label=u"Publish File", parent="my_tool", c=publishWin)
    cmds.setParent( '..', menu=True )
    cmds.menuItem(divider=True,  dividerLabel='Rough Render')
    cmds.menuItem("Play Blast", label=u"Play Blast", parent="my_tool")
    cmds.menuItem("Check and Fix", label=u"Check and Fix", parent="my_tool")

utils.executeDeferred(main_ui)

