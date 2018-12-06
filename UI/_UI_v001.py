# -*- coding: utf-8 -*-
import sys
sys.path.append("../Action")
from PyQt4 import QtGui
from PyQt4 import QtCore
from Action import action

# Global Value
PROJECT = "D:/projects/LongGong"

class Outliner(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Outliner, self).__init__(parent)
        self._UI()

    def _UI(self):
        tradeMark = QtGui.QLabel('Launch')
        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.setFrameShape(QtGui.QListWidget.NoFrame)
        self.listWidget.setMinimumWidth(100)
        self.listWidget.setMaximumWidth(200)
        list = ["Film", "Assests", "Processes"]
        for row, i in enumerate(list):
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.listWidget.addItem(item)

        left = QtGui.QVBoxLayout(self)
        left.setMargin(0)  # 表示控件与窗体的左右边距
        left.setSpacing(6)  # 表示各个控件之间的上下间距
        left.addWidget(tradeMark)
        left.addWidget(self.listWidget)

class Film(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Film, self).__init__(parent)
        self._UI()

    def _UI(self):
        # 中间顶部部件
        self.back = QtGui.QLabel('Back')
        self.move = QtGui.QLabel('Move')
        self.openFile = QtGui.QLabel('WorkFile')
        self.proPath =  QtGui.QLabel()
        # self.proPath.setFont()
        self.list_v1 = QtGui.QListWidget()
        self.list_v1.setFrameShape(QtGui.QListWidget.NoFrame)
        for i in self._first_data():
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list_v1.addItem(item)
        self.list_v2 = QtGui.QListWidget()
        self.list_v2.setFrameShape(QtGui.QListWidget.NoFrame)
        self.list_v3 = QtGui.QListWidget()
        self.list_v3.setFrameShape(QtGui.QListWidget.NoFrame)
        self.list_v4 = QtGui.QListWidget()
        self.list_v4.setFrameShape(QtGui.QListWidget.NoFrame)

        top_ly = QtGui.QHBoxLayout()
        top_ly.setSpacing(10)
        top_ly.addWidget(self.back)
        top_ly.addWidget(self.move)
        top_ly.addWidget(self.openFile)
        top_ly.addWidget(self.proPath)
        space = QtGui.QSpacerItem(10, 2, QtGui.QSizePolicy.Expanding)
        top_ly.addItem(space)

        middle_lay = QtGui.QHBoxLayout()

        middle_lay.addWidget(self.list_v1)
        middle_lay.addWidget(self.list_v2)
        middle_lay.addWidget(self.list_v3)
        middle_lay.addWidget(self.list_v4)

        mainLayout = QtGui.QVBoxLayout(self)
        mainLayout.setMargin(0)
        mainLayout.addLayout(top_ly)
        mainLayout.addLayout(middle_lay)

    # **************************** 界面数据 *********************************
    def _first_data(self):
        row = [str(i) for i in range(0, 15)]
        # action.getFolders()
        return row

    def _second_data(self):
        row = [str(i) for i in range(0, 6)]
        return row

    def _third_data(self):
        row = [str(i) for i in range(0, 3)]
        return row

    def _forth_data(self):
        row = [str(i) for i in range(0, 5)]
        return row

    def to_addsecond(self):
        self.proPath.setText(PROJECT+"/")
        self.Pro_path = ""
        self.list_v2.clear()
        self.list_v3.clear()
        self.list_v4.clear()
        for i in self._second_data():
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list_v2.addItem(item)

    def to_addthird(self):
        self.Pro_path = ""
        self.list_v3.clear()
        self.list_v4.clear()
        for i in self._third_data():
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list_v3.addItem(item)
        self.Pro_path = PROJECT+"/"+self.list_v1.currentItem().text()+"/" + self.list_v2.currentItem().text()
        self.proPath.setText(self.Pro_path)

    def to_addforth(self):
        self.list_v4.clear()
        for i in self._forth_data():
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list_v4.addItem(item)
        self.Pro_path = PROJECT + "/" + self.list_v1.currentItem().text() + "/" + self.list_v2.currentItem().text()+\
                        "/"+self.list_v3.currentItem().text()
        self.proPath.setText(self.Pro_path)

    def addforth_self(self):
        self.Pro_path = ""
        self.Pro_path = PROJECT + "/" + self.list_v1.currentItem().text() + "/" + self.list_v2.currentItem().text()+\
                        "/" + self.list_v3.currentItem().text() + "/"+self.list_v4.currentItem().text()
        self.proPath.setText(self.Pro_path)

class Assests(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Assests, self).__init__(parent)
        self._UI()

    def _UI(self):
        # 中间顶部部件
        self.back = QtGui.QLabel('Back')
        self.move = QtGui.QLabel('Move')
        self.openFile = QtGui.QLabel('WorkFile')
        self.proPath =  QtGui.QLabel()
        # self.proPath.setFont()
        self.list_v1 = QtGui.QListWidget()
        self.list_v1.setFrameShape(QtGui.QListWidget.NoFrame)
        for i in self._first_data():
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list_v1.addItem(item)
        self.list_v2 = QtGui.QListWidget()
        self.list_v2.setFrameShape(QtGui.QListWidget.NoFrame)
        self.list_v3 = QtGui.QListWidget()
        self.list_v3.setFrameShape(QtGui.QListWidget.NoFrame)
        self.list_v4 = QtGui.QListWidget()
        self.list_v4.setFrameShape(QtGui.QListWidget.NoFrame)

        top_ly = QtGui.QHBoxLayout()
        top_ly.setSpacing(10)
        top_ly.addWidget(self.back)
        top_ly.addWidget(self.move)
        top_ly.addWidget(self.openFile)
        top_ly.addWidget(self.proPath)
        space = QtGui.QSpacerItem(10, 2, QtGui.QSizePolicy.Expanding)
        top_ly.addItem(space)

        middle_lay = QtGui.QHBoxLayout()

        middle_lay.addWidget(self.list_v1)
        middle_lay.addWidget(self.list_v2)
        middle_lay.addWidget(self.list_v3)
        middle_lay.addWidget(self.list_v4)

        mainLayout = QtGui.QVBoxLayout(self)
        mainLayout.setMargin(0)
        mainLayout.addLayout(top_ly)
        mainLayout.addLayout(middle_lay)

    # **************************** 界面数据 *********************************
    def _first_data(self):
        row = [str(i) for i in range(0, 15)]
        return row

    def _second_data(self):
        row = [str(i) for i in range(0, 6)]
        return row

    def _third_data(self):
        row = [str(i) for i in range(0, 3)]
        return row

    def _forth_data(self):
        row = [str(i) for i in range(0, 5)]
        return row

    def to_addsecond(self):
        self.proPath.setText(PROJECT+"/")
        self.Pro_path = ""
        self.list_v2.clear()
        self.list_v3.clear()
        self.list_v4.clear()
        for i in self._second_data():
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list_v2.addItem(item)

    def to_addthird(self):
        self.Pro_path = ""
        self.list_v3.clear()
        self.list_v4.clear()
        for i in self._third_data():
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list_v3.addItem(item)
        self.Pro_path = PROJECT+"/"+self.list_v1.currentItem().text()+"/" + self.list_v2.currentItem().text()
        self.proPath.setText(self.Pro_path)

    def to_addforth(self):
        self.list_v4.clear()
        for i in self._forth_data():
            item = QtGui.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list_v4.addItem(item)
        self.Pro_path = PROJECT + "/" + self.list_v1.currentItem().text() + "/" + self.list_v2.currentItem().text()+\
                        "/"+self.list_v3.currentItem().text()
        self.proPath.setText(self.Pro_path)

    def addforth_self(self):
        self.Pro_path = ""
        self.Pro_path = PROJECT + "/" + self.list_v1.currentItem().text() + "/" + self.list_v2.currentItem().text()+\
                        "/" + self.list_v3.currentItem().text() + "/"+self.list_v4.currentItem().text()
        self.proPath.setText(self.Pro_path)

class Processes(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Processes, self).__init__(parent)
        self._UI()

    def _UI(self):
        label = QtGui.QLabel("Prosess")

        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)

class MessageWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MessageWindow, self).__init__(parent)
        self._UI()

    def _UI(self):
        self.sw_label = QtGui.QLabel("Maya")
        self.tab_v1 = QtGui.QTableWidget(10, 4, self)
        self.tab_v1.horizontalHeader().resizeSection(0,30)
        self.pr_label = QtGui.QTableWidgetItem("Properties")
        newItem = QtGui.QTableWidgetItem(self.pr_label)
        self.tab_v1.horizontalHeader().setVisible(False)  # 隐藏表头
        self.tab_v1.verticalHeader().setVisible(False)
        self.tab_v1.setShowGrid(False)  # 隐藏网格
        self.tab_v1.setSpan(0, 0, 1, 4)  # 合并4列单元格

        self.tab_v1.setItem(0, 0, newItem)
        first_row = ['Path', 'ShortName', 'Name', 'Icon']
        for row, i in enumerate(first_row):
            newItem = QtGui.QTableWidgetItem(i)
            newItem.setTextAlignment(QtCore.Qt.AlignLeft)  # 居左对齐
            self.tab_v1.setSpan(row+1, 2, 1, 2)  # 合并后两列单元格
            self.tab_v1.setItem(row+1, 1, newItem)
            # A = QtGui.QTableWidgetItem("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            # self.tab_v1.setItem(row+1, 2, A)

        self.tab_v1.setSpan(5, 0, 1, 4)
        State = QtGui.QTableWidgetItem("State(debug)")
        self.tab_v1.setItem(len(first_row)+1, 0, State)
        first2_row = ['Status', 'Leaf', 'App', 'Part']
        for row, i in enumerate(first2_row):
            newItem = QtGui.QTableWidgetItem(i)
            self.tab_v1.setItem(len(first2_row)+row+2, 1, newItem)

        mainLayout = QtGui.QVBoxLayout(self)
        mainLayout.addWidget(self.sw_label, 0)
        mainLayout.addWidget(self.tab_v1, 2)

class FolderView(QtGui.QWidget):
    def __init__(self, parent = None):
        super(FolderView, self).__init__(parent)
        self._UI()

    def _UI(self):
        self.Folder = QtGui.QTreeWidget()
