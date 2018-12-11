#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
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
print gf.get_basename(r"D:/JXY_Work/GraduatioProject/project/WSF_CG01/Assets/Character/QIU/Model/Work/QIU_model_v001_high.mb")