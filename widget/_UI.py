#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

try:
    from PySide import QtGui
    from PySide import QtCore
except:
    from PySide2 import QtGui
    from Pyside2 import QtWidgets as QtGui
    from PySide2 import QtCore

from action import action
from action import maya
from main import _widgets
from widget.qss.Utils import *

##################### Global Value #####################
SW = maya.Maya()
ASSETROOT = ["Character", "Prop", "Set"]
SEQUENCEROOT = ["Sequences"]

OS = action.OS()
ConfigData = action.ReadCofig()
file_mes = action.FileMessage()
ProjectPath = ConfigData.get_global()['project_path']
AssetStep = ConfigData.allSteps('asset')
ShotStep = ConfigData.allSteps('shot')


class InfoWin(QtGui.QDialog):
    def __init__(self, message, parent=None):
        '''

        :param message: 提示语
        '''
        super(InfoWin, self).__init__(parent)
        self.mes = message
        self._ui()

    def _ui(self):
        QtGui.QMessageBox.information(self, "Tip", self.mes, QtGui.QMessageBox.Yes)


class WarningWin(QtGui.QDialog):
    def __init__(self, message, parent=None):
        '''

        :param message: 提示语
        '''
        super(WarningWin, self).__init__(parent)
        self.mes = message
        self._ui()

    def _ui(self):
        self.reply = QtGui.QMessageBox.question(self, 'Warning', self.mes,
                                                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)


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
        self.inputBtn = _widgets.PushButton(u"导入")
        self.referBtn = _widgets.PushButton(u"参考")
        self.openBtn = _widgets.PushButton(u"打开")

        # ------------------ 布局 -------------------
        self.mid = QtGui.QHBoxLayout()
        self.mid.addWidget(self.lab)
        self.mid.addStretch()
        self.mid.addWidget(self.asset_search)

        self.mid1 = QtGui.QVBoxLayout()
        self.mid1.addWidget(tabwin)

        self.bottom = QtGui.QHBoxLayout()
        self.bottom.addStretch()
        self.bottom.addWidget(self.inputBtn)
        self.bottom.addWidget(self.referBtn)
        self.bottom.addWidget(self.openBtn)

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

        for i in ASSETROOT:
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
        self.asset_win.openBtn.clicked.connect(self.openFile)


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
        展开添加文件详细信息
        '''
        if hasattr(self, 'file_win'):
            self.file_win.clear()
            self.file_win1.clear()

        try:
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


    def openFile(self):
        '''
        打开选中的文件
        :return:
        '''

        if self.file_win.currentItem():
            path_clm = self.file_win.getHeaderCount(u"路径")
            # SW.open(self.file_win.currentItem().text(path_clm))
        elif self.file_win1.currentItem():
            path_clm = self.file_win1.getHeaderCount(u"路径")
            # SW.open(self.file_win1.currentItem().text(path_clm))
        else:
            InfoWin(u"请选择文件")

    def importFile(self):
        '''
        导入选中的文件
        :return:
        '''
        if self.file_win.currentItem():
            path_clm = self.file_win.getHeaderCount(u"路径")
            # SW.open(self.file_win.currentItem().text(path_clm))
        elif self.file_win1.currentItem():
            path_clm = self.file_win1.getHeaderCount(u"路径")
            # SW.open(self.file_win1.currentItem().text(path_clm))
        else:
            InfoWin(u"请选择文件")

    def referenceFile(self):
        '''
        导入选中的文件
        :return:
        '''
        if self.file_win.currentItem():
            path_clm = self.file_win.getHeaderCount(u"路径")
            # SW.reference(self.file_win.currentItem().text(path_clm))
        elif self.file_win1.currentItem():
            path_clm = self.file_win1.getHeaderCount(u"路径")
            # SW.reference(self.file_win1.currentItem().text(path_clm))
        else:
            InfoWin(u"请选择文件")



class ShotWin(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ShotWin, self).__init__(parent)

        self._ui()

    def _ui(self):

        self.shot_win = BasicWin()
        self.folder_win = self.shot_win.folder_win
        self.file_win = self.shot_win.file_win
        self.file_win1 = self.shot_win.file_win1

        for i in SEQUENCEROOT:
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
        self.shot_win.openBtn.clicked.connect(self.openFile)

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
        if hasattr(self, 'file_win'):
            self.file_win.clear()
        if hasattr(self, 'file_win1'):
            self.file_win1.clear()

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

    def openFile(self):
        '''
        打开选中的文件
        :return:
        '''

        if self.file_win.currentItem():
            path_clm = self.file_win.getHeaderCount(u"路径")
            # SW.open(self.file_win.currentItem().text(path_clm))
        elif self.file_win1.currentItem():
            path_clm = self.file_win1.getHeaderCount(u"路径")
            # SW.open(self.file_win1.currentItem().text(path_clm))
        else:
            InfoWin(u"请选择文件")

    def importFile(self):
        '''
        导入选中的文件
        :return:
        '''
        if self.file_win.currentItem():
            path_clm = self.file_win.getHeaderCount(u"路径")
            # SW.open(self.file_win.currentItem().text(path_clm))
        elif self.file_win1.currentItem():
            path_clm = self.file_win1.getHeaderCount(u"路径")
            # SW.open(self.file_win1.currentItem().text(path_clm))
        else:
            InfoWin(u"请选择文件")

    def referenceFile(self):
        '''
        导入选中的文件
        :return:
        '''
        if self.file_win.currentItem():
            path_clm = self.file_win.getHeaderCount(u"路径")
            # SW.reference(self.file_win.currentItem().text(path_clm))
        elif self.file_win1.currentItem():
            path_clm = self.file_win1.getHeaderCount(u"路径")
            # SW.reference(self.file_win1.currentItem().text(path_clm))
        else:
            InfoWin(u"请选择文件")


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


class CreateAssetWin(QtGui.QDialog):

    def __init__(self, style_ls=[], asset_ls=[], step_ls=[], parent=None):
        '''

        :param syle_ls: 资产类型
        :param asset_ls: 资产列表
        :param step_ls: 环节列表
        '''
        super(CreateAssetWin, self).__init__(parent)
        self.syle_ls = style_ls
        self.asset_ls = asset_ls
        self.step_ls = step_ls

        self._UI()

    def _UI(self):
        self.setWindowTitle(u"Create Asset")
        self.resize(250, 200)
        lab1 = QtGui.QLabel(u"Asset Style:")
        lab2 = QtGui.QLabel(u"Asset Name:")
        lab3 = QtGui.QLabel(u"Step:")

        self.styleComb = _widgets.ComboBox()
        self.assetComb = _widgets.ComboBox()
        self.stepComb = _widgets.ComboBox()
        self.save = _widgets.PushButton("Save")
        self.cancel = _widgets.PushButton("Cancel")

        # 自动补全下拉菜单
        self.assetComb.setEditable(True)

        # 布局
        lay1 = QtGui.QHBoxLayout()
        lay1.addStretch()
        lay1.addWidget(self.save)
        lay1.addWidget(self.cancel)
        lay = QtGui.QGridLayout()
        lay.addWidget(lab1, 0, 0)
        lay.addWidget(self.styleComb, 0, 1)
        lay.addWidget(lab2, 1, 0)
        lay.addWidget(self.assetComb, 1, 1)
        lay.addWidget(lab3, 2, 0)
        lay.addWidget(self.stepComb, 2, 1)
        lay.addLayout(lay1, 3, 1)

        self.setLayout(lay)

        # 初始化combobox
        self.init_combobox()

        # 信号
        self.save.clicked.connect(self.saveCon)

    def init_combobox(self):
        # 增加选项元素
        for i in range(len(self.syle_ls)):
            self.styleComb.addItem(self.syle_ls[i])
        self.styleComb.setCurrentIndex(-1)
        for i in range(len(self.asset_ls)):
            self.assetComb.addItem(self.asset_ls[i])
        self.assetComb.setCurrentIndex(-1)
        for i in range(len(self.step_ls)):
            self.stepComb.addItem(self.step_ls[i])
        self.stepComb.setCurrentIndex(-1)

        # 增加自动补全
        self.completer = QtGui.QCompleter(self.asset_ls)
        self.assetComb.setCompleter(self.completer)

    def saveCon(self):
        '''
        若果创建的资产不存在则创建资产，存在不创建。 返回界面所填的的信息
        :return: 返回界面选择的字典
        '''

        if self.styleComb.currentText() and self.assetComb.currentText() and self.stepComb.currentText():
            self.save_data = {
                'style_ls': self.styleComb.currentText(),
                'asset_ls': self.assetComb.currentText(),
                'step_ls': self.stepComb.currentText()
            }

            work_set = (ProjectPath, "Assets", self.save_data['style_ls'], self.save_data['asset_ls'],
                        self.save_data['step_ls'], "Work", '')
            approve_set = (ProjectPath, "Assets", self.save_data['style_ls'], self.save_data['asset_ls'],
                        self.save_data['step_ls'], "Approve", '')
            work_path = "/".join(work_set)
            approve_path = "/".join(approve_set)

            if os.path.exists(work_path) and os.path.exists(approve_path):
                tip = InfoWin(u"资产已经存在, 无需创建")
                tip.show()
                # self.styleComb.clear()
                # self.assetComb.clear()
                # self.stepComb.clear()

            else:
                OS.makeFolder(work_path)
                OS.makeFolder(approve_path)
                tip = InfoWin(u"资产创建成功")
                tip.show()
                self.close()

            return self.save_data

        else:
            tip = InfoWin('Please check selection')
            tip.show()


class AssetDataWin(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AssetDataWin, self).__init__(parent)

        self._ui()

    def _ui(self):
        self.resize(600, 700)
        self.setWindowTitle('Asset library')

        # --------------------- Asset Widget ---------------------
        asset_win = BasicWin()
        self.assetTree = asset_win.folder_win

        for i in ASSETROOT:
            root = QtGui.QTreeWidgetItem(self.assetTree)
            root.setText(0, i)
            child = QtGui.QTreeWidgetItem(root)
            child.setText(0, "")

        # --------------------- Menu ---------------------
        '''
        将ContextMenuPolicy设置为QtGui.CustomContextMenu.
        否则无法使用customContextMenuRequested信号
        '''
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QtGui.QMenu(self)
        self.add = self.contextMenu.addAction('Create asset')
        self.delete = self.contextMenu.addAction('Delete asset')
        # 二级菜单
        # self.GN = self.contextMenu.addMenu("功能")
        # self.ZJ = self.GN.addAction('增加')

        # --------------------- Layout ---------------------
        lay = QtGui.QVBoxLayout()
        lay.addWidget(self.assetTree)

        self.setLayout(lay)

        # --------------------- 信号 ---------------------
        self.par_fun = AssetWin(self)
        self.assetTree.itemClicked.connect(self.par_fun.click)
        self.assetTree.itemExpanded.connect(self.par_fun.addChild)
        # 事件绑定
        self.add.triggered.connect(self.addAsset)
        self.delete.triggered.connect(self.delAsset)

    def showMenu(self, pos):
        '''
        菜单显示前,将它移动到鼠标点击的位置

        :param pos: 鼠标位置
        '''
        if self.assetTree.selectedItems():
            # print self.assetTree.selectedItems()[0].text(0)
            self.contextMenu.exec_(QtGui.QCursor.pos())  # 在鼠标位置显示


    def addAsset(self):
        '''

        鼠标右键弹出来的添加资产界面
        '''

        # 获取所有资产类型
        for i in self.assetTree.selectedItems():
            # 如果选中的是子节点, sel是父级
            try:
                sel = i.parent().text(0)
            except:
                sel = i.text(0)
        set = (ProjectPath, "Assets", sel)
        child1 = OS.get_folders("/".join(set))

        # 获取所有的环节
        child2 = AssetStep

        kwarg = {
            'style_ls': ASSETROOT,
            'asset_ls': child1,
            'step_ls': child2
        }

        popwin = CreateAssetWin(**kwarg)
        popwin.exec_()

    def delAsset(self):
        '''
        删除资产
        '''
        for i in self.assetTree.selectedItems():
            # 如果选中的是子节点, sel是父级
            try:
                if i.parent():
                    popwin = WarningWin('Do you want to delete %s--%s ?' % (i.text(0), i.text(1)))
                    if popwin.reply == QtGui.QMessageBox.Yes:
                        set = (ProjectPath, "Assets", i.parent().text(0), i.text(0), i.text(1))
                        # print "/".join(set)
                        OS.delFolder("/".join(set))
                        popwin1 = InfoWin("Delete successful")
                        popwin1.show()
                    else:
                        popwin.close()
            except:
                pass











