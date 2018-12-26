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
file_mes = action.FileMessage()
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
        # 根据内容自动调整列宽
        self.asset_win.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
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
        # 需要时水平滚动条
        self.file_win.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        head_list = [u"名称", u"艺术家", u"说明", u"修改时间", u"大小", u"路径"]
        self.file_win.setHeaderLabels(head_list)

        # ------------------ 底部部分 -------------------
        input = QtGui.QPushButton(u"导入")
        refer = QtGui.QPushButton(u"参考")
        open = QtGui.QPushButton(u"打开")

        # ------------------ 布局 -------------------
        mid = QtGui.QHBoxLayout()
        mid.addWidget(self.lab)
        mid.addStretch()
        mid.addWidget(self.asset_search)

        bottom = QtGui.QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(input)
        bottom.addWidget(refer)
        bottom.addWidget(open)

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
        input.clicked.connect(self.input)


    def addChild(self, item):
        '''
        搜索文件夹添加到资产的item
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
        '''
        添加文件详细信息
        '''
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
                fl_path = work_path + "/" + i
                root.setText(0, gf.get_basename(fl_path))
                root.setText(3, file_mes.get_FileModifyTime(fl_path))
                root.setText(4, file_mes.get_FileSize(fl_path))
                root.setText(5, fl_path)

            # approve 下的子节点
            approve_set = (config_data.get_global()['project_path'], "Assets", par,
                           self.asset_win.currentItem().text(0), self.asset_win.currentItem().text(1), "Approve")
            approve_path = "/".join(approve_set)
            file_ls = gf.get_filses(approve_path)
            root = QtGui.QTreeWidgetItem(approve_root)
            for i in file_ls:
                fl_path = approve_path+"/"+i
                root.setText(0, gf.get_basename(fl_path))
                root.setText(3, file_mes.get_FileModifyTime(fl_path))
                root.setText(4, file_mes.get_FileSize(fl_path))
                root.setText(5, fl_path)

    def input(self):
        if self.file_win:
            print self.file_win.currentItem().text(5)


class ShotWin(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ShotWin, self).__init__(parent)

        self._ui()

    def _ui(self):

        # ------------------ shot窗口 -------------------
        self.shot_win = QtGui.QTreeWidget()
        # 可排序
        self.shot_win.setSortingEnabled(True)
        # 需要时水平滚动条
        self.shot_win.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # 根据内容自动调整列宽
        self.shot_win.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)

        head_list = [u"名称", u"环节", u"说明"]
        root_list = ["Sequences"]
        for i in root_list:
            root = QtGui.QTreeWidgetItem(self.shot_win)
            root.setText(0, i)
            child = QtGui.QTreeWidgetItem(root)
            child.setText(1, "")
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
        # 根据内容自动调整列宽
        self.file_win.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        # 需要时水平滚动条
        self.file_win.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.file_win.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.file_win.header().setStretchLastSection(False)
        self.file_win.setAutoScroll(False)

        head_list = [u"名称", u"艺术家", u"说明", u"修改时间", u"大小", u"路径"]
        self.file_win.setHeaderLabels(head_list)

        # ------------------ 底部部分 -------------------
        input = QtGui.QPushButton(u"导入")
        refer = QtGui.QPushButton(u"参考")
        open = QtGui.QPushButton(u"打开")

        # ------------------ 布局 -------------------
        mid = QtGui.QHBoxLayout()
        mid.addWidget(self.lab)
        mid.addStretch()
        mid.addWidget(self.asset_search)

        bottom = QtGui.QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(input)
        bottom.addWidget(refer)
        bottom.addWidget(open)

        lay = QtGui.QVBoxLayout()
        lay.setSpacing(0)
        lay.addWidget(self.shot_win)
        lay.addLayout(mid)
        lay.addWidget(self.file_win)
        lay.addLayout(bottom)

        self.setLayout(lay)

        # ------------------ 信号与槽 -------------------
        self.shot_win.itemClicked.connect(self.click)
        self.shot_win.itemExpanded.connect(self.addChild)
        input.clicked.connect(self.input)

    def get_root(self, item):
        '''
        返回item的根节点列表
        '''

        if item.parent():
            self.root_ls.insert(1, item.text(0))
            self.get_root(item.parent())

        else:
            self.root_ls.insert(1, item.text(0))

    def addChild(self, item):
        '''
        搜索文件夹添加到资产的item
        '''
        item.takeChildren()

        self.root_ls = [pro_path]
        self.get_root(item)
        child = tree_item("/".join(self.root_ls))
        child.sort()

        if len(child) > 0:
            for name in child:
                root = QtGui.QTreeWidgetItem(item)
                root.setText(0, name)
                # 环节文件夹时不再添加子节点
                if name not in shot_step:
                    root1 = QtGui.QTreeWidgetItem(root)
                    root1.setText(0, "")

    def click(self, item):
        '''
        添加文件详细信息
        '''
        self.file_win.clear()
        work_root = QtGui.QTreeWidgetItem(self.file_win)
        work_root.setText(0, "Work")
        approve_root = QtGui.QTreeWidgetItem(self.file_win)
        approve_root.setText(0, "Approve")
        # 点击子节点
        if not item.childCount():
            # work 下的子节点
            work_set = ("/".join(self.root_ls), self.shot_win.currentItem().text(0), "Work")
            work_path = "/".join(work_set)
            file_ls = gf.get_filses(work_path)
            root = QtGui.QTreeWidgetItem(work_root)
            for i in file_ls:
                fl_path = work_path + "/" + i
                root.setText(0, gf.get_basename(fl_path))
                root.setText(3, file_mes.get_FileModifyTime(fl_path))
                root.setText(4, file_mes.get_FileSize(fl_path))
                root.setText(5, fl_path)

            # approve 下的子节点
            approve_set = ("/".join(self.root_ls), self.shot_win.currentItem().text(0), "Approve")
            approve_path = "/".join(approve_set)
            file_ls = gf.get_filses(approve_path)
            root = QtGui.QTreeWidgetItem(approve_root)
            for i in file_ls:
                fl_path = approve_path+"/"+i
                root.setText(0, gf.get_basename(fl_path))
                root.setText(3, file_mes.get_FileModifyTime(fl_path))
                root.setText(4, file_mes.get_FileSize(fl_path))
                root.setText(5, fl_path)

    def input(self):
        if self.file_win:
            print self.file_win.currentItem().text(5)

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


