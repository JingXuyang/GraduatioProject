# -*- coding: utf-8 -*-
import sys
from PySide import QtGui
from PySide import QtCore


items_list=["C", "C++", "Java", "Python", "JavaScript",
            "C#", "Swift", "go", "Ruby", "Lua", "PHP"]

class AddAssetOrShot(QtGui.QWidget):
    def __init__(self, items_list=[], parent=None):
        super(AddAssetOrShot, self).__init__(parent)
        self.item_list = items_list

        self._UI()

    def _UI(self):
        self.setWindowTitle(u"Create Asset")
        self.resize(300, 200)
        lab1 = QtGui.QLabel(u"Asset Style:")
        lab2 = QtGui.QLabel(u"Asset Name:")
        lab3 = QtGui.QLabel(u"Step:")

        self.asseSty = ()
        self.asseSty = QtGui.QComboBox()
        self.step = QtGui.QComboBox()
        self.save = QtGui.QPushButton("Save")
        self.save.setMaximumWidth(40)
        self.cancel = QtGui.QPushButton("Cancel")
        self.cancel.setMaximumWidth(40)

        # 自动补全下拉菜单
        self.asseSty.setEditable(True)
        self.asseSty.setEditable(True)
        self.asseSty.setEditable(True)

        # 布局
        lay1 = QtGui.QHBoxLayout()
        lay1.addStretch()
        lay1.addWidget(self.save)
        lay1.addWidget(self.cancel)
        lay = QtGui.QGridLayout()
        lay.addWidget(lab1, 0, 0)
        lay.addWidget(self.asseSty, 0, 1)
        lay.addWidget(lab2, 1, 0)
        lay.addWidget(self.assetName, 1, 1)
        lay.addWidget(lab3, 2, 0)
        lay.addWidget(self.step, 2, 1)
        lay.addLayout(lay1, 3, 1)

        self.setLayout(lay)

        # 初始化combobox
        self.init_combobox()

        # 信号
        self.save.clicked.connect(self.saveCon)

    def init_combobox(self):
        # 增加选项元素
        for i in range(len(self.item_list)):
            self.asseSty.addItem(self.item_list[i])
        self.asseSty.setCurrentIndex(-1)

        # 增加自动补全
        self.completer = QtGui.QCompleter(self.item_list)
        self.asseSty.setCompleter(self.completer)

    def saveCon(self):
        self.item_list.append(self.asseSty.currentText())
        print self.item_list
        self.completer.clear()
        self.completer = QtGui.QCompleter(self.item_list)




app= QtGui.QApplication(sys.argv)
con = AddAssetOrShot(['model'])
con.show()
sys.exit(app.exec_())
