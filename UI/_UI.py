#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
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

def get_step_message(AorS, step):
    '''
    
    :param AorS: 输入"asset"或者"shot"
    :param step: 环节
    :return: 
    {
    'file_name': '{sequence}_{shot}_{short_name}_v###.{work_format}', 
    'name': 'charEffect', 
    'short_name': 'cf'
    }
    '''
    return config_data.get_step_message(AorS, step)


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
        # 需要时水平滚动条, 双击滚动条不会还原
        self.asset_win.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.asset_win.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.asset_win.header().setStretchLastSection(False)
        self.asset_win.setAutoScroll(False)

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
        # 需要时水平滚动条, 双击滚动条不会还原
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
        self.mid = QtGui.QHBoxLayout()
        self.mid.addWidget(self.lab)
        self.mid.addStretch()
        self.mid.addWidget(self.asset_search)

        self.mid1 = QtGui.QVBoxLayout()
        self.mid1.addWidget(self.file_win)

        self.bottom = QtGui.QHBoxLayout()
        self.bottom.addStretch()
        self.bottom.addWidget(input)
        self.bottom.addWidget(refer)
        self.bottom.addWidget(open)

        lay = QtGui.QVBoxLayout()
        lay.setSpacing(3)
        lay.addWidget(self.asset_win)
        lay.addLayout(self.mid)
        lay.addLayout(self.mid1)
        lay.addLayout(self.bottom)

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
        try:
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
                file_ls = gf.get_files(work_path)
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
                file_ls = gf.get_files(approve_path)
                for i in file_ls:
                    fl_path = approve_path+"/"+i
                    root = QtGui.QTreeWidgetItem(approve_root)
                    root.setText(0, gf.get_basename(fl_path))
                    root.setText(3, file_mes.get_FileModifyTime(fl_path))
                    root.setText(4, file_mes.get_FileSize(fl_path))
                    root.setText(5, fl_path)
        except:
            pass
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
        # 需要时水平滚动条, 双击滚动条不会还原
        self.shot_win.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.shot_win.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.shot_win.header().setStretchLastSection(False)
        self.shot_win.setAutoScroll(False)
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
        # 需要时水平滚动条, 双击滚动条不会还原
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
        self.mid = QtGui.QHBoxLayout()
        self.mid.addWidget(self.lab)
        self.mid.addStretch()
        self.mid.addWidget(self.asset_search)

        self.mid1 = QtGui.QVBoxLayout()
        self.mid1.addWidget(self.file_win)

        self.bottom = QtGui.QHBoxLayout()
        self.bottom.addStretch()
        self.bottom.addWidget(input)
        self.bottom.addWidget(refer)
        self.bottom.addWidget(open)

        lay = QtGui.QVBoxLayout()
        lay.setSpacing(3)
        lay.addWidget(self.shot_win)
        lay.addLayout(self.mid)
        lay.addLayout(self.mid1)
        lay.addWidget(self.file_win)
        lay.addLayout(self.bottom)

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

        # root_ls 选中层级的所有父级的列表
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
        try:
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
                file_ls = gf.get_files(work_path)
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
                file_ls = gf.get_files(approve_path)
                for i in file_ls:
                    root = QtGui.QTreeWidgetItem(approve_root)
                    fl_path = approve_path+"/"+i
                    root.setText(0, gf.get_basename(fl_path))
                    root.setText(3, file_mes.get_FileModifyTime(fl_path))
                    root.setText(4, file_mes.get_FileSize(fl_path))
                    root.setText(5, fl_path)
        except:
            pass

    def input(self):
        if self.file_win:
            print self.file_win.currentItem().text(5)


class OpenWidget(QtGui.QTabWidget):

    def __init__(self, parent=None):
        super(OpenWidget, self).__init__(parent)
        self.setWindowTitle("Open")
        self.resize(700, 650)
        self._ui()

    def _ui(self):

        # ------------------主界面 -------------------

        self.tab1 = AssetWin()
        self.tab2 = ShotWin()

        self.addTab(self.tab1, u"资产")
        self.addTab(self.tab2, u"镜头")


class SaveWidget(QtGui.QTabWidget):

    def __init__(self, parent=None):
        super(SaveWidget, self).__init__(parent)
        self.setWindowTitle("Save")
        self.resize(700, 600)
        self._ui()

    def _ui(self):

        # ------------------主界面 -------------------

        self.tab1 = AssetWin()
        self.clearLayout(self.tab1.mid)
        self.clearLayout(self.tab1.mid1)
        self.clearLayout(self.tab1.bottom)

        saveBtn = QtGui.QPushButton(u"下一步")
        lay = QtGui.QHBoxLayout()
        lay.addStretch()
        lay.addWidget(saveBtn)
        self.tab1.layout().insertLayout(4, lay)

        self.tab2 = ShotWin()
        self.clearLayout(self.tab2.mid)
        self.clearLayout(self.tab2.mid1)
        self.clearLayout(self.tab2.bottom)

        saveBtn1 = QtGui.QPushButton(u"下一步")
        lay1 = QtGui.QHBoxLayout()
        lay1.addStretch()
        lay1.addWidget(saveBtn1)
        self.tab2.layout().insertLayout(4, lay1)

        self.addTab(self.tab1, u"资产")
        self.addTab(self.tab2, u"镜头")

        saveBtn.clicked.connect(self.next)
        saveBtn1.clicked.connect(self.next1)

    def clearLayout(self, layout):
        '''
        
        :param layout: 需要移除的布局
        '''

        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def next(self):
        subwin = SubWin("asset", self.tab1.asset_win.currentItem().text(1))
        # 子窗口不关闭无法操作父窗口
        subwin.setWindowModality(QtCore.Qt.ApplicationModal)
        subwin.exec_()

    def next1(self):
        subwin = SubWin("shot", self.tab2.shot_win.currentItem().text(0))
        # 子窗口不关闭无法操作父窗口
        subwin.setWindowModality(QtCore.Qt.ApplicationModal)
        subwin.exec_()

class SubWin(QtGui.QDialog):
    def __init__(self, AorS, step, parent=None):
        super(SubWin, self).__init__(parent)
        self.resize(300, 250)
        self.setWindowTitle(u"提交")
        self.a_or_s = AorS
        self.step = step

        self._ui()

    def _ui(self):

        # ------------------ 界面 -------------------
        self.setWindowTitle(self.step.capitalize() + " Submit")

        des_lab = QtGui.QLabel(u"描述：")
        self.des_win = QtGui.QTextEdit()

        extend_des_lab = QtGui.QLabel(u"文件描述:")
        self.des_com = QtGui.QComboBox()
        self.des_com.setMinimumWidth(100)
        items = get_step_message(self.a_or_s, self.step)["describtion_item"]
        self.des_com.addItems(items)

        sum_butt = QtGui.QPushButton(u"提交")
        sum_butt.setMaximumWidth(50)

        # ------------------ 布局 -------------------

        lay1 = QtGui.QHBoxLayout()
        lay1.addWidget(extend_des_lab)
        lay1.addWidget(self.des_com)
        lay1.addStretch()

        lay2 = QtGui.QHBoxLayout()
        lay2.addStretch()
        lay2.addWidget(sum_butt)

        lay = QtGui.QVBoxLayout()
        lay.addWidget(des_lab)
        lay.addWidget(self.des_win)
        lay.addLayout(lay1)
        lay.addLayout(lay2)

        self.setLayout(lay)

        # ------------------ 信号 -------------------
        sum_butt.clicked.connect(self.submite)


    def submite(self):
        print self.des_win.toPlainText()
        print self.des_com.currentText()







