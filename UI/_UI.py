#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from PySide import QtGui
from PySide import QtCore
from pprint import pprint

from Data import analysis
from Action import action

# Global Value

gf = action.OS()
config_data = analysis.ReadCofig()
pro_path = config_data.get_global()['project_path']
asset_step = config_data.allSteps('asset')
shot_step = config_data.allSteps('shot')

def tree_item(path):
    folder = gf.get_folders(path)
    return folder


class AssetWin(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AssetWin, self).__init__(parent)

        self._ui()

    def _ui(self):

        # ------------------ asset窗口 -------------------
        self.asset_win = QtGui.QTreeWidget()
        # 可排序
        self.asset_win.setSortingEnabled(True)
        # self.header().setStretchLastSection(True)
        head_list = [u"名称", u"环节", u"说明"]
        root_list = ["Character", "Prop", "Set"]
        for i in root_list:
            root = QtGui.QTreeWidgetItem(self.asset_win)
            root.setText(0, i)
            child = QtGui.QTreeWidgetItem(root)
            child.setText(0, "")

        self.asset_win.setHeaderLabels(head_list)

        # ------------------ 中间部分 -------------------
        self.lab = QtGui.QLabel(u"工作文件")
        self.asset_search = QtGui.QLineEdit()
        self.asset_search.setMaximumWidth(100)
        # 设置提示输入文本
        self.asset_search.setPlaceholderText(u"搜索...")

        # ------------------ 文件窗口 -------------------
        self.file_win = QtGui.QTreeWidget()
        head_list = [u"名称", u"艺术家", u"说明", u"修改时间", u"大小", u"路径"]
        self.file_win.setHeaderLabels(head_list)

        # ------------------ 底部部分 -------------------
        self.export = QtGui.QPushButton(u"导入")
        self.refer = QtGui.QPushButton(u"参考")
        self.open = QtGui.QPushButton(u"打开")

        # ------------------ 布局 -------------------
        mid = QtGui.QHBoxLayout()
        mid.addWidget(self.lab)
        mid.addStretch()
        mid.addWidget(self.asset_search)

        bottom = QtGui.QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(self.export)
        bottom.addWidget(self.refer)
        bottom.addWidget(self.open)

        lay = QtGui.QVBoxLayout()
        lay.setSpacing(0)
        lay.addWidget(self.asset_win)
        lay.addLayout(mid)
        lay.addWidget(self.file_win)
        lay.addLayout(bottom)

        self.setLayout(lay)

        # ------------------ 信号与槽 -------------------
        self.asset_win.itemClicked.connect(self.click)
        self.asset_win.itemExpanded.connect(self.addChild)

    def addChild(self, item):
        '''
        搜索文件夹添加到item
        '''
        item.takeChildren()
        set = (pro_path, "Assets", item.text(0))
        child = tree_item("/".join(set))
        # 如果有资产
        if len(child) > 0:
            for name in child:
                asset_step = gf.get_folders("/".join(set)+"/"+name)
                asset_step.sort()
                for chi in asset_step:
                    root = QtGui.QTreeWidgetItem(item)
                    root.setText(0, name)
                    root.setText(1, chi)
        else:
            root = QtGui.QTreeWidgetItem(item)
            root.setText(1, "")


    def click(self, item):
        self.file_win.clear()
        work_root = QtGui.QTreeWidgetItem(self.file_win)
        work_root.setText(0, "Work")
        approve_root = QtGui.QTreeWidgetItem(self.file_win)
        approve_root.setText(0, "Approve")
        # 点击子节点
        if not item.childCount():
            par = self.asset_win.currentItem().parent().text(0)

            # work 下的子节点
            work_set = (config_data.get_global()['project_path'], "Assets", par,
                        self.asset_win.currentItem().text(0), self.asset_win.currentItem().text(1), "Work")
            work_path = "/".join(work_set)
            file_ls = gf.get_filses(work_path)
            root = QtGui.QTreeWidgetItem(work_root)
            for i in file_ls:
                root.setText(0, gf.get_basename(i))

            # approve 下的子节点
            approve_set = (config_data.get_global()['project_path'], "Assets", par,
                           self.asset_win.currentItem().text(0), self.asset_win.currentItem().text(1), "Approve")
            approve_path = "/".join(approve_set)
            file_ls = gf.get_filses(approve_path)
            root = QtGui.QTreeWidgetItem(approve_root)
            for i in file_ls:
                root.setText(0, gf.get_basename(i))


class ShotWin(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ShotWin, self).__init__(parent)

        self._ui()

    def _ui(self):

        # ------------------ shot窗口 -------------------
        self.shot_win = QtGui.QTreeWidget()
        # 可排序
        self.shot_win.setSortingEnabled(True)
        # self.header().setStretchLastSection(True)
        head_list = [u"名称", u"环节", u"说明"]
        root_list = ["char", "prop", "set"]
        for i in root_list:
            root = QtGui.QTreeWidgetItem(self.shot_win)
            root.setText(0, i)
            shot_step.sort()
            for chi in shot_step:
                child = QtGui.QTreeWidgetItem(root)
                child.setText(1, chi)
        self.shot_win.setHeaderLabels(head_list)

        # ------------------ 中间部分 -------------------

        # 搜索框
        self.lab = QtGui.QLabel(u"工作文件")
        self.asset_search = QtGui.QLineEdit()
        self.asset_search.setMaximumWidth(100)
        # 设置提示输入文本
        self.asset_search.setPlaceholderText(u"搜索...")

        # ------------------ 文件窗口 -------------------
        self.file_win = QtGui.QTreeWidget()
        head_list = [u"名称", u"艺术家", u"说明", u"大小"]
        self.file_win.setHeaderLabels(head_list)

        # ------------------ 底部部分 -------------------
        self.export = QtGui.QPushButton(u"导入")
        self.refer = QtGui.QPushButton(u"参考")
        self.open = QtGui.QPushButton(u"打开")

        # ------------------ 布局 -------------------
        mid = QtGui.QHBoxLayout()
        mid.addWidget(self.lab)
        mid.addStretch()
        mid.addWidget(self.asset_search)

        bottom = QtGui.QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(self.export)
        bottom.addWidget(self.refer)
        bottom.addWidget(self.open)

        lay = QtGui.QVBoxLayout()
        lay.setSpacing(0)
        lay.addWidget(self.shot_win)
        lay.addLayout(mid)
        lay.addWidget(self.file_win)
        lay.addLayout(bottom)

        self.setLayout(lay)

        # ------------------ 信号与槽 -------------------


class MyTabWidget(QtGui.QTabWidget):

    def __init__(self, parent=None):
        super(MyTabWidget, self).__init__(parent)
        self.setWindowTitle("Open")
        self.resize(700, 600)
        self._ui()

    def _ui(self):

        # ------------------主界面 -------------------

        self.tab1 = AssetWin()
        self.tab2 = ShotWin()

        self.addTab(self.tab1, u"资产")
        self.addTab(self.tab2, u"镜头")


