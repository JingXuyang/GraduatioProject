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
        # qss_file = open("style.qss").read()
        # self.setStyleSheet(qss_file)
        # qss_file = open("style_RF.qss").read()
        # self.setStyleSheet(qss_file)
        self.setWindowTitle("Open")
        self.resize(800, 600)

        # 实例化窗口
        self.assetWin = _UI.MyTabWidget()

        self._Ui()

        # **************************** 界面布局 *********************************
    def _Ui(self):
        lay = QtGui.QVBoxLayout()
        lay.addWidget(self.assetWin)

        self.setLayout(lay)

        # **************************** 信号与槽 *********************************


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = Window()
    main.show()
    app.exec_()

