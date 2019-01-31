#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import yaml
import re
import datetime

# from Data import analysis

##################### Global Value #####################
YamlPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data/config.yaml').replace("\\", "/")
FileType = [".mb", ".abc", ".ma"]
CachePath = "C:/Users/" + os.getenv('username') + "/.jxy"


def get_variable(str):
    '''
    :param str: yaml文件中带{}的字符串
    :return: 返回解析后的正确的值
    '''

    # print str
    funct_ls = re.findall(r"{(.*?)}", str)

    for i in funct_ls:
        if hasattr(ReadCofig, i):
            # if i == "describtion_item":
            a = ReadCofig()
            # eval() 把字符串改为对应的的变量名，例如：eval("a." + i) <=> ReadCofig.i
            ins = eval("a." + i)
            # print ins("asset", "Model")

    ref_con = ReadCofig()

    state = {}
    state["project_path"] = ref_con.get_global()
    state["type"] = ref_con.allSteps('asset')
    state["asset_name"] = "char"
    state["file_name"] = ref_con.get_global()
    # state["seq"] = ref_con.get_global()
    # state["shot"] = ref_con.get_global()

    before = str.split("/")
    after = []
    for i in before:
        if "{" in i:
            var = i[1:-1]
            if var in state.keys():
                var = state[var]
            after.append(var)
        else:
            after.append(i)

    return "_".join(after)


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

    def get_files(self, path):
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

    def get_filetype(self, path):
        '''
        :param path: 路径
        :return: 文件扩展名
        '''
        if os.path.exists(path):
            return os.path.basename(path).split(".")[1]
        else:
            return ""

# a = OS()
# print a.get_files(r"D:/JXY_Work/GraduatioProject/project/WSF_CG01/Sequences/Seq01/Shot001/Animation/Approve")

class FileMessage(object):

    # 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
    def TimeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    #获取文件的大小,结果保留两位小数，单位为MB
    def get_FileSize(self, filePath):
        fsize = os.path.getsize(filePath)
        fsize1 = fsize / float(1024 * 1024)
        # print fsize
        if fsize1 > 1:
            return str(round(fsize1, 1)) + "MB"
        else:
            fsize1 = fsize / float(1024)
            return str(round(fsize1, 1)) + "KB"

    # 获取文件的修改时间
    def get_FileModifyTime(self, filePath):
        t = os.path.getmtime(filePath)
        return self.TimeStampToTime(t)


class CacheInfo(object):

    def read_json(self, path):
        '''
        :param path: json 文件路径
        :return: 返回json内容 
        '''
        with open(path) as file:
            return json.loads(file.read())

    def write_json(self, info, path, filename):
        '''
        :param info: 需要写入的文件信息，写入到
        :param filename: json文件名
        :return: 返回文件信息
        '''
        text = json.dumps(info, indent=4)
        # jsonPath = "{0}/{1}.json".format(CachePath, filename)
        jsonPath = "{0}/{1}.json".format(path, filename)
        f = open(jsonPath, "w")
        f.write(text)
        f.close()

        return text


class ReadCofig(object):

    def __init__(self):
        self.path = YamlPath

        with open(self.path, 'r') as f:
            self.data = yaml.load(f.read())

    def get_global(self):
        dir = {}
        for i in self.data:
            if i == "global":
                for ii in self.data[i]:
                    if ii == "project_path":
                        dir['project_path'] = self.data[i][ii]
        return dir

    def get_save_path(self):
        dir = {}
        for i in self.data:
            if i == "global":
                for ii in self.data[i]:
                    if ii == "asset_work_path":
                        dir['asset_work_parh'] = self.data[i][ii]
                        # print get_variable(self.data[i][ii])
                    elif ii == "asset_approve_path":
                        dir['asset_approve_path'] = self.data[i][ii]
                    elif ii == "shot_work_path":
                        dir['shot_work_path'] = self.data[i][ii]
                    elif ii == "shot_approve_path":
                        dir['shot_approve_path'] = self.data[i][ii]
        return dir

    def allSteps(self, sequence=''):
        '''
        :sequence :  shot 或者 asset
        '''
        ls = []

        for seq in self.data:
            if seq == sequence:
                for step in self.data[seq]:
                    ls.append(step)

        ls.sort()
        return ls

    def get_step_message(self, sequence='', step='', fun=""):
        '''
        :sequence :  shot 或者 asset
        :step :  环节
        :fun :  方法名

        如果没有传入 fun
        return:
         {
         'short_name': model,
         'file_name': test_model_v001.mb
         }
        如果传入方法，则返回对应json中的值
        return :
         {
         ['low_mid', 'middle_mid', 'high_mid']
         }
        '''
        dir = {}

        for seq in self.data:
            if seq == sequence:
                ls = []
                for stp in self.data[seq]:
                    ls.append(step)
                    if stp == step:
                        for detail in self.data[seq][stp]:
                            dir[detail] = self.data[seq][stp][detail]
        if fun:
            return dir[fun]
        else:
            return dir

    def name(self, sequence='', step=''):
        return self.get_step_message(sequence, step)['name']

    def short_name(self, sequence='', step=''):
        return self.get_step_message(sequence, step)['short_name']

    def describtion_item(self, sequence='', step=''):
        return self.get_step_message(sequence, step)['describtion_item']

    def work_format(self, sequence='', step=''):
        return self.get_step_message(sequence, step)['work_format']




# get_variable("{asset_name}_{short_name}_{describtion_item}_v###.{work_format}")

# ana = ReadCofig()
# a = ana.get_step_message("asset", "Model")
# print a
# # b = ana.allSteps()
# c = ana.get_global()
# print a
# # print b
# # print c