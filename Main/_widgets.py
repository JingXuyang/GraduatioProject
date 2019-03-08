#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from PySide import QtGui
from PySide import QtCore
from pprint import pprint

# from Data import analysis
from action import action
import widget.qss.Utils as qss


button_style_list = ['MediumGray', 'DarkGray', 'BlueJeans', 'Aqua',
                     'Mint', 'Grass', 'Sunflower', 'Bittersweet', 'Grapefruit', 'Lavender', 'PinkRose']

class TreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)

        # 根据内容自动调整列宽
        self.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def sort_enable(self, boolen):
        # 可排序
        if boolen == True:
            self.setSortingEnabled(True)
        else:
            self.setSortingEnabled(False)

    def auto_scroll(self, boolen):
        # 需要时水平滚动条, 双击滚动条不会还原
        if boolen == True:
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            self.header().setStretchLastSection(False)
            self.setAutoScroll(False)

    def set_header_labels(self, ls=[]):
        # 设置头部
        if type(ls) == list:
            self.setHeaderLabels(ls)
        else:
            return ''

    def addChild(self, item, pro_path):
        '''
        搜索文件夹添加到资产的item
        '''
        item.takeChildren()
        set = (pro_path, "Assets", item.text(0))
        child = tree_item("/".join(set))
        # 如果有资产
        if len(child) > 0:
            for name in child:
                asset_step = action.OS.get_folders("/".join(set)+"/"+name)
                asset_step.sort()
                for chi in asset_step:
                    root = QtGui.QTreeWidgetItem(item)
                    root.setText(0, name)
                    root.setText(1, chi)
        else:
            root = QtGui.QTreeWidgetItem(item)
            root.setText(1, "")


class PushButton(QtGui.QPushButton):
    def __init__(self, name, parent=None):
        super(PushButton, self).__init__(parent)

        qss.load_style(self)

        # button style
        qss.button_style(self, "BlueJeans")

        self.setText(name)
        self.setMinimumWidth(45)
        self.setMinimumHeight(25)
