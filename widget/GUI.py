#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide import QtGui
from PySide import QtCore
import _UI

class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

    def open(self):
        '''
        打开 open 窗口
        '''
        win = _UI.OpenWidget()
        win.show()

    def save(self):
        '''
        打开 save as 窗口
        '''
        win = _UI.SaveWidget()
        win.show()






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # main = Window()
    # main = _UI.OpenWidget()
    main = _UI.SaveWidget()
    # main = _UI.SubWin("shot", "Animation")
    main.show()
    app.exec_()

