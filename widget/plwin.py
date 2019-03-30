#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from qtlb.Qt import QtGui
from qtlb.Qt import QtWidgets

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath('__file__'))))

import _ui
reload(_ui)

def open():
    '''
    打开 open 窗口
    '''
    win = _ui.OpenWidget()
    win.show()

def save():
    '''
    打开 save as 窗口
    '''
    win = _ui.SaveWidget()
    win.exec_()

def publish():
    '''
    打开 save as 窗口
    '''
    win = _ui.PublishWidget()
    win.show()
    
def submite():
    win = _ui.SubWin()
    win.show()




app = QtWidgets.QApplication(sys.argv)
# # # main = Window()
# # # main = _ui.AssetDataWin()
main = _ui.OpenWidget()
# # # main = _ui.SaveWidget()
# # # main = _ui.PublishWidget()
# # # main = _UI.SubWin("shot", "Animation")
main.show()
app.exec_()

