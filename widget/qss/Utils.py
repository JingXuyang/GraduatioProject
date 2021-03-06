# -*- coding:utf-8 -*-

import os

from qtlb.Qt import QtCore
from qtlb.Qt import QtGui

from MessageWidget import MessageAsk, Message


def message(msg, msg_type="info"):
    """
    msg_type:['success','info','warning','error']
    """
    m = Message()
    if msg_type == "info":
        m.info(msg)
    elif msg_type == "success":
        m.success(msg)
    elif msg_type == "warning":
        m.warning(msg)
    elif msg_type == "error":
        m.error(msg)
    else:
        raise ValueError

    m.exec_()


def message_ask(msg, msg_type="info"):
    """
    msg_type:['info','warning']
    """
    ma = MessageAsk()
    if msg_type == "info":
        ma.info(msg)
    elif msg_type == "warning":
        ma.info(msg)
    else:
        raise ValueError

    ma.exec_()

    return ma.status


def load_style(obj):
    return obj.setStyleSheet(open("%s/Style.css" % os.path.dirname(__file__)).read().replace("%PATH%", os.path.dirname(
        __file__).replace("\\", "/")))


def button_style(button, style):
    """
    style:['MediumGray','DarkGray','BlueJeans','Aqua','Mint','Grass','Sunflower','Bittersweet','Grapefruit','Lavender','PinkRose']
    """
    return button.setProperty("class", style)


def combobox_style(combobox):
    return combobox.setItemDelegate(QtGui.QStyledItemDelegate())


def table_style(table):
    table.setAlternatingRowColors(True)
    table.setShowGrid(False)
    table.setFocusPolicy(QtCore.Qt.NoFocus)
    table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

def tree_style(tree):
    pass

def progress_style(progress, style):
    """
    style:['Aqua','Grass','Sunflower','Grapefruit']
    """
    return progress.setProperty("class", style)


def calendar_style(obj):
    obj.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
    obj.setHorizontalHeaderFormat(QtGui.QCalendarWidget.NoHorizontalHeader)
