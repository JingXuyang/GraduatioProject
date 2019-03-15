#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
try:
    from PySide import QtGui
    from PySide import QtCore
except:
    from PySide2 import QtGui
    from Pyside2 import QtWidgets as QtGui
    from PySide2 import QtCore
from pprint import pprint
from action import _maya

from action import action
from main.widgets import _widgets
from widget.qss.Utils import *

##################### Global Value #####################
# sw = _maya.Maya()

OS = action.OS()
ConfigData = action.ReadCofig()
file_mes = action.FileMessage()
ProjectPath = ConfigData.get_global()['project_path']
AssetStep = ConfigData.allSteps('asset')
ShotStep = ConfigData.allSteps('shot')


class InfoWin(QtGui.QDialog):
    def __init__(self, message, parent=None):
        super(InfoWin, self).__init__(parent)
        self.mes = message
        self._ui()

    def _ui(self):
        QtGui.QMessageBox.information(self, "Tip", self.mes, QtGui.QMessageBox.Yes)


class BasicWin(QtGui.QDialog):
    def __init__(self, parent=None):
        super(BasicWin, self).__init__(parent)

        self._ui()

    def _ui(self):
        # ------------------ asset窗口 -------------------
        self.folder_win = _widgets.TreeWidget()
        # 可排序
        self.folder_win.sort_enable(True)
        # 需要时水平滚动条, 双击滚动条不会还原
        self.folder_win.auto_scroll(True)

        head_list = [u"名称", u"环节", u"说明"]
        self.folder_win.set_header_labels(head_list)

        # ------------------ 中间部分 -------------------
        self.lab = QtGui.QLabel(u"工作文件")
        self.asset_search = QtGui.QLineEdit()
        self.asset_search.setMaximumWidth(100)
        # 设置提示输入文本
        self.asset_search.setPlaceholderText(u"搜索...")

        # ------------------ 文件窗口 -------------------
        self.file_win = _widgets.TreeWidget()
        self.file_win1 = _widgets.TreeWidget()
        # 需要时水平滚动条, 双击滚动条不会还原
        self.file_win.auto_scroll(True)
        self.file_win1.auto_scroll(True)

        head_list = [u"名称", u"艺术家", u"说明", u"修改时间", u"大小", u"路径"]
        self.file_win.setHeaderLabels(head_list)
        self.file_win1.setHeaderLabels(head_list)

        tabwin = QtGui.QTabWidget()
        tabwin.addTab(self.file_win, 'Work')
        tabwin.addTab(self.file_win1, 'Approved')

        # ------------------ 底部部分 -------------------
        input = _widgets.PushButton(u"导入")
        refer = _widgets.PushButton(u"参考")
        open = _widgets.PushButton(u"打开")

        # ------------------ 布局 -------------------
        self.mid = QtGui.QHBoxLayout()
        self.mid.addWidget(self.lab)
        self.mid.addStretch()
        self.mid.addWidget(self.asset_search)

        self.mid1 = QtGui.QVBoxLayout()
        self.mid1.addWidget(tabwin)

        self.bottom = QtGui.QHBoxLayout()
        self.bottom.addStretch()
        self.bottom.addWidget(input)
        self.bottom.addWidget(refer)
        self.bottom.addWidget(open)

        lay = QtGui.QVBoxLayout()
        lay.setSpacing(3)
        lay.addWidget(self.folder_win)
        lay.addLayout(self.mid)
        lay.addLayout(self.mid1)
        lay.addLayout(self.bottom)

        self.setLayout(lay)


class AssetWin(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AssetWin, self).__init__(parent)

        self._ui()

    def _ui(self):

        self.asset_win = BasicWin()
        self.folder_win = self.asset_win.folder_win
        self.file_win = self.asset_win.file_win
        self.file_win1 = self.asset_win.file_win1

        root_list = ["Character", "Prop", "Set"]
        for i in root_list:
            root = QtGui.QTreeWidgetItem(self.folder_win)
            root.setText(0, i)
            child = QtGui.QTreeWidgetItem(root)
            child.setText(0, "")

        lay = QtGui.QVBoxLayout()
        lay.setSpacing(0)
        lay.addWidget(self.asset_win)

        self.setLayout(lay)

        # ------------------ 信号与槽 -------------------
        self.folder_win.itemClicked.connect(self.click)
        self.folder_win.itemExpanded.connect(self.addChild)
        # input.clicked.connect(self.input)

    def addChild(self, item):
        '''
        搜索文件夹添加到资产的item
        '''
        item.takeChildren()
        set = (ProjectPath, "Assets", item.text(0))
        child = OS.get_folders("/".join(set))
        # 如果有资产
        if len(child) > 0:
            for name in child:
                AssetStep = OS.get_folders("/".join(set)+"/"+name)
                AssetStep.sort()
                for chi in AssetStep:
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

            # 点击子节点
            if not item.childCount():
                par = self.folder_win.currentItem().parent().text(0)

                # work 下的子节点
                work_set = (ConfigData.get_global()['project_path'], "Assets", par,
                            self.folder_win.currentItem().text(0), self.folder_win.currentItem().text(1), "Work")
                work_path = "/".join(work_set)
                file_ls = OS.get_files(work_path)
                for i in file_ls:
                    root = QtGui.QTreeWidgetItem(self.file_win)
                    fl_path = work_path + "/" + i
                    root.setText(0, OS.get_basename(fl_path))
                    root.setText(3, file_mes.get_FileModifyTime(fl_path))
                    root.setText(4, file_mes.get_FileSize(fl_path))
                    root.setText(5, fl_path)

                # approve 下的子节点
                approve_set = (ConfigData.get_global()['project_path'], "Assets", par,
                               self.folder_win.currentItem().text(0), self.folder_win.currentItem().text(1), "Approve")
                approve_path = "/".join(approve_set)
                # print approve_path
                file_ls = OS.get_files(approve_path)
                for i in file_ls:
                    root = QtGui.QTreeWidgetItem(self.file_win1)
                    fl_path = approve_path + "/" + i
                    # print "jxy", fl_path
                    root.setText(0, OS.get_basename(fl_path))
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

        self.shot_win = BasicWin()
        self.folder_win = self.shot_win.folder_win
        self.file_win = self.shot_win.file_win
        self.file_win1 = self.shot_win.file_win1

        root_list = ["Sequences"]
        for i in root_list:
            root = QtGui.QTreeWidgetItem(self.folder_win)
            root.setText(0, i)
            child = QtGui.QTreeWidgetItem(root)
            child.setText(1, "")

        lay = QtGui.QVBoxLayout()
        lay.addWidget(self.shot_win)

        self.setLayout(lay)

        # ------------------ 信号与槽 -------------------
        self.folder_win.itemClicked.connect(self.click)
        self.folder_win.itemExpanded.connect(self.addChild)
        # input.clicked.connect(self.input)

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
        self.root_ls = [ProjectPath]
        self.get_root(item)
        child = OS.get_folders("/".join(self.root_ls))
        child.sort()

        if len(child) > 0:
            for name in child:
                root = QtGui.QTreeWidgetItem(item)
                root.setText(0, name)
                # 环节文件夹时不再添加子节点
                if name not in ShotStep:
                    root1 = QtGui.QTreeWidgetItem(root)
                    root1.setText(0, "")

    def click(self, item):
        '''
        添加文件详细信息
        '''
        try:
            self.file_win.clear()

            # 点击子节点
            if not item.childCount():
                # work 下的子节点
                work_set = ("/".join(self.root_ls), self.folder_win.currentItem().text(0), "Work")
                work_path = "/".join(work_set)
                file_ls = OS.get_files(work_path)
                root = QtGui.QTreeWidgetItem(self.file_win)
                for i in file_ls:
                    fl_path = work_path + "/" + i
                    root.setText(0, OS.get_basename(fl_path))
                    root.setText(3, file_mes.get_FileModifyTime(fl_path))
                    root.setText(4, file_mes.get_FileSize(fl_path))
                    root.setText(5, fl_path)

                # approve 下的子节点
                approve_set = ("/".join(self.root_ls), self.folder_win.currentItem().text(0), "Approve")
                approve_path = "/".join(approve_set)
                file_ls = OS.get_files(approve_path)
                for i in file_ls:
                    root = QtGui.QTreeWidgetItem(self.file_win1)
                    fl_path = approve_path+"/"+i
                    root.setText(0, OS.get_basename(fl_path))
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

        # table_style(self)

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
        self.setWindowTitle("Save As")
        self.resize(700, 400)
        self._ui()

    def _ui(self):

        # ------------------主界面 -------------------
        self.tab1 = AssetWin()
        self.clearLayout(self.tab1.asset_win.mid)
        self.clearLayout(self.tab1.asset_win.mid1)
        self.clearLayout(self.tab1.asset_win.bottom)

        saveBtn = _widgets.PushButton(u"下一步")
        lay = QtGui.QHBoxLayout()
        lay.addStretch()
        lay.addWidget(saveBtn)
        self.tab1.layout().insertLayout(4, lay)
        self.tab1.layout().setSpacing(0)

        self.tab2 = ShotWin()
        self.clearLayout(self.tab2.shot_win.mid)
        self.clearLayout(self.tab2.shot_win.mid1)
        self.clearLayout(self.tab2.shot_win.bottom)

        saveBtn1 = _widgets.PushButton(u"下一步")
        lay1 = QtGui.QHBoxLayout()
        lay1.addStretch()
        lay1.addWidget(saveBtn1)
        self.tab2.layout().insertLayout(4, lay1)
        self.tab1.layout().setSpacing(0)

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
        try:
            subwin = SubWin("asset", self.tab1.asset_win.folder_win.currentItem().text(1))
            # 子窗口不关闭无法操作父窗口
            subwin.setWindowModality(QtCore.Qt.ApplicationModal)
            subwin.exec_()
        except:
            InfoWin(u"请选择相应的环节保存")

    def next1(self):
        try:
            subwin = SubWin("shot", self.tab2.shot_win.folder_win.currentItem().text(0))
            # 子窗口不关闭无法操作父窗口
            subwin.setWindowModality(QtCore.Qt.ApplicationModal)
            subwin.exec_()
        except:
            InfoWin(u"请选择相应的环节保存")


class SubWin(QtGui.QDialog):
    def __init__(self, AorS, step, parent=None):
        '''
        
        :param AorS: 'asset' or 'shot'
        :param step: 各个流程环节
        '''
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
        items = ConfigData.get_step_message(self.a_or_s, self.step)["describtion_item"]
        self.des_com.addItems(items)

        sum_butt = _widgets.PushButton(u"提交")
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

        cache = {}
        cache["description"] = self.des_win.toPlainText()


        self.close()






