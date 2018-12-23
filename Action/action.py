#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import time
import datetime

from Data import analysis


config_data = analysis.ReadCofig()

FileType = [".mb", ".abc", ".ma"]

class OS(object):

    def cg_type(self, path):
        '''
        
        :param path: 路径 
        :return: 如果在FileType中，返回扩展名, 否则为Folse
        '''
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1]
            if ext in FileType:
                return ext
            else:
                return False

    def get_folders(self, path):
        '''
        
        :param path: 路径
        :return: 返回path下边所有的文件夹列表
        '''
        if os.path.exists(path):
            folder = []
            list = os.listdir(path)  # 列出文件夹下所有的目录
            for i in range(0, len(list)):
                temp = os.path.join(path, list[i])
                if os.path.isdir(temp):
                    folder.append(list[i])
            return folder
        else:
            return []

    def get_filses(self, path):
        '''
        
        :param path: 路径
        :return: 返回path下边所有的文件列表
        '''
        if os.path.exists(path):
            files = []
            list = os.listdir(path)  # 列出文件夹下所有的文件
            for i in range(0, len(list)):
                temp = os.path.join(path, list[i])
                if os.path.isfile(temp):
                    if self.cg_type(temp):
                        files.append(list[i])
            return files
        else:
            return []

    def get_basename(self, path):
        '''

        :param path: 路径
        :return: 返回文件名
        '''
        if os.path.exists(path):
            return os.path.basename(path).split(".")[0]
        else:
            return ""


gf = OS()
# print gf.get_basename(r"D:/JXY_Work/GraduatioProject/UI/GUI.py")

class FileMessage(object):

    # 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    #获取文件的大小,结果保留两位小数，单位为MB
    def get_FileSize(self, filePath):
        fsize = os.path.getsize(filePath)
        fsize1 = fsize / float(1024 * 1024)
        print fsize
        if fsize1 > 1:
            return str(round(fsize1, 1)) + "MB"
        else:
            fsize1 = fsize / float(1024)
            return str(round(fsize1, 1)) + "KB"

    # 获取文件的修改时间
    def get_FileModifyTime(self, filePath):
        t = os.path.getmtime(filePath)
        return self.TimeStampToTime(t)
fl = FileMessage()
# print fl.get_FileSize(r"D:\JXY_Work\test\yanshi.mpg")