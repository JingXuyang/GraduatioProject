#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from pprint import pprint

from qtlb.Qt import QtCore
from qtlb.Qt import QtGui
from qtlb.Qt import QtWidgets


from action import action
import widget.qss.Utils as qss

# 按钮样式
button_style_list = ['MediumGray', 'DarkGray', 'BlueJeans', 'Aqua',
                     'Mint', 'Grass', 'Sunflower', 'Bittersweet',
                     'Grapefruit', 'Lavender', 'PinkRose'
                     ]


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        pass


class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)

        # 根据内容自动调整列宽
        # self.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def sort_enable(self, boolen):
        # 可排�?
        if boolen == True:
            self.setSortingEnabled(True)
        else:
            self.setSortingEnabled(False)

    def auto_scroll(self, boolen):
        # 需要时水平滚动�?, 双击滚动条不会还�?
        if boolen == True:
            self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            # self.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            self.header().setStretchLastSection(False)
            self.setAutoScroll(False)

    def set_header_labels(self, ls=[]):
        # 设置头部
        if type(ls) == list:
            self.setHeaderLabels(ls)
        else:
            return ''

    def getSelectItem(self, item, row):
        # 返回选中的文�?
        return item.text(row)

    def getHeaderCount(self, headername):
        # 返回headername的列�?
        count = self.columnCount()
        for i in range(count):
            if self.headerItem().text(i) == headername:
                return i

    def addChild(self, item, pro_path):
        '''
        搜索文件夹添加到资产的item
        '''
        item.takeChildren()
        set = (pro_path, "Assets", item.text(0))
        child = tree_item("/".join(set))
        # 如果有资�?
        if len(child) > 0:
            for name in child:
                asset_step = action.OS.get_folders("/".join(set)+"/"+name)
                asset_step.sort()
                for chi in asset_step:
                    root = QtWidgets.QTreeWidgetItem(item)
                    root.setText(0, name)
                    root.setText(1, chi)
        else:
            root = QtGui.QTreeWidgetItem(item)
            root.setText(1, "")


class PushButton(QtWidgets.QPushButton):
    def __init__(self, name, parent=None):
        super(PushButton, self).__init__(parent)

        qss.load_style(self)

        # button style
        qss.button_style(self, "Mint")

        self.setText(name)
        self.setMinimumWidth(45)
        self.setMinimumHeight(25)

class ComboBox(QtWidgets.QComboBox):
    def __init__(self):
        super(ComboBox, self).__init__()

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()



