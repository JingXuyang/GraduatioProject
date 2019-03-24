#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from PySide import QtGui
    from PySide import QtCore
except:
    from PySide2 import QtGui
    from Pyside2 import QtWidgets as QtGui
    from PySide2 import QtCore

import _ui

class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

    def open(self):
        '''
        打开 open 窗口
        '''
        win = _ui.OpenWidget()
        win.show()

    def save(self):
        '''
        打开 save as 窗口
        '''
        win = _ui.SaveWidget()
        win.show()






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # main = Window()
    # main = _ui.AssetDataWin()
    main = _ui.OpenWidget()
    # main = _ui.SaveWidget()
    # main = _ui.PublishWidget()
    # main = _UI.SubWin("shot", "Animation")
    main.show()
    app.exec_()

