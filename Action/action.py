#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
from Data import analysis

config_data = analysis.ReadCofig()
rootdir = config_data.get_global()

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
                path = os.path.join(path, list[i])
                if os.path.isdir(path):
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
                path = os.path.join(rootdir, list[i])
                if os.path.isfile(path):
                    if self.cg_type(path):
                        files.append(list[i])
            return files
        else:
            return []
