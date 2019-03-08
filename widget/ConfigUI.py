# -*- coding: utf-8 -*-
import sys
from PySide import QtGui
from PySide import QtCore


items_list=["C", "C++", "Java", "Python", "JavaScript",
            "C#", "Swift", "go", "Ruby", "Lua", "PHP"]

class AddAssetOrShot(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AddAssetOrShot, self).__init__(parent)

        self._UI()

    def _UI(self):
        self.setWindowTitle(u"配置界面")

        lab1 = QtGui.QLabel(u"项目:")
        lab2 = QtGui.QLabel(u"存储目录:")
        lab3 = QtGui.QLabel(u"集数数:")
        lab4 = QtGui.QLabel(u"镜头数:")

        self.pro = QtGui.QComboBox()
        self.folder = QtGui.QLineEdit()
        self.open = QtGui.QPushButton("...")
        self.open.setMaximumWidth(40)
        self.seq = QtGui.QLineEdit()
        self.shot = QtGui.QLineEdit()
        self.save = QtGui.QPushButton("Save")
        self.save.setMaximumWidth(40)

        # 自动补全下拉菜单
        self.pro.setEditable(True)

        # 设置输入文本中间对齐
        self.folder.setAlignment(QtCore.Qt.AlignCenter)
        self.seq.setAlignment(QtCore.Qt.AlignCenter)
        self.shot.setAlignment(QtCore.Qt.AlignCenter)

        # 设置提示输入文本
        self.folder.setPlaceholderText(u"请输入项目存储路径")
        self.seq.setPlaceholderText(u"请输入总集数")
        self.shot.setPlaceholderText(u"请输入总集数")

        # 限制输入
        self.seq.setValidator(QtGui.QIntValidator(self))
        self.shot.setValidator(QtGui.QIntValidator(self))


        lay = QtGui.QGridLayout()

        lay.addWidget(lab1, 0, 0)
        lay.addWidget(self.pro, 0, 1)
        lay.addWidget(lab2, 1, 0)
        lay.addWidget(self.folder, 1, 1)
        lay.addWidget(self.open, 1, 2)
        lay.addWidget(lab3, 2, 0)
        lay.addWidget(self.seq, 2, 1)
        lay.addWidget(lab4, 3, 0)
        lay.addWidget(self.shot, 3, 1)
        lay.addWidget(self.save, 4, 2)

        self.setLayout(lay)

        # 初始化combobox
        # self.init_lineedit()
        self.init_combobox()

        # 信号
        self.save.clicked.connect(self.saveCon)

    # def init_lineedit(self):
    #     # 增加自动补全
    #     self.completer = QtGui.QCompleter()
    #     self.lineedit.setCompleter(self.completer)

    def init_combobox(self):
        # 增加选项元素
        for i in range(len(items_list)):
            self.pro.addItem(items_list[i])
        self.pro.setCurrentIndex(-1)

        # 增加自动补全
        self.completer = QtGui.QCompleter(items_list)
        self.pro.setCompleter(self.completer)

    def saveCon(self):
        items_list.append(self.pro.currentText())
        print items_list
        self.completer.clear()
        self.completer = QtGui.QCompleter(items_list)




app= QtGui.QApplication(sys.argv)
con = AddAssetOrShot()
con.show()
sys.exit(app.exec_())
