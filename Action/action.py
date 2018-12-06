#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os

FileType = [".mb", ".abc", ".ma"]

class OS(object):

    def getType(self, path):
        if os.path.isfile(path):
            if os.path.splitext(path)[1] in FileType:
                return True
            else:
                return False

    def getFolders(self, path):
        folder = []
        list = os.listdir(path)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(path, list[i])
            if os.path.isdir(path):
                folder.append(list[i])
        return folder

    def getFilses(self, path):
        files = []
        list = os.listdir(path)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(rootdir, list[i])
            if os.path.isfile(path):
                if getType(path):
                    files.append(list[i])
        return files
