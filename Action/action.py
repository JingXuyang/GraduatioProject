#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import yaml
import re
import shutil
import getpass
import datetime

# from Data import analysis

##################### Global Value #####################
YamlPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data/config.yaml').replace("\\", "/")
MayaPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "")
FileType = ['.ma', '.mb', '.abc']
CachePath = "C:/Users/" + os.getenv('username') + "/.gdpj"


def get_variable(file_name,
                 type='',
                 sequence='',
                 asset_name='',
                 step='',
                 seq='',
                 shot='',
                 describtion='',
                 describtion_item=''
                 ):
    '''

    当{}中的字符串在"ReadCofig"中有对应的方法名时， 运行对应的函数返回；
    不存在时返回字符串

    :param file_name: yaml文件中带{}的字符串
    :return: 返回解析后的正确的值
    '''

    # print str
    kwarg = {
        'type': type,
        'sequence': sequence,
        'file_name': file_name,
        'asset_name': asset_name,
        'step': step,
        'seq': seq,
        'shot': shot,
        'describtion': describtion,
        'describtion_item': describtion_item
    }

    result = []

    funct_ls = re.findall(r"{(.*?)}", file_name)

    for i in funct_ls:
        # 如果class ReadCofig 存在这个变量的action， 则执行相应的action
        if hasattr(ReadCofig, i):
            a = ReadCofig()
            # eval() 把字符串改为对应的的变量名，例如：eval("a." + i) <=> ReadCofig.i
            ins = eval("a." + i)
            if type == "asset":
                if i == "describtion_item":
                    result.append(kwarg[i])
                else:
                    result.append(ins("asset", step))
            else:
                if i == "describtion_item":
                    result.append(kwarg[i])
                elif i == "shot":
                    result.append(kwarg[i])
                else:
                    result.append(ins("shot", step))
        else:
            # 如果不存在变量的action, 先看传入进来的kwarg是不是有这个变量，
            # 如果没有则返回变量本身
            if kwarg.has_key(i):
                result.append(kwarg[i])
            else:
                result.append(i)

    # print "_".join(result)
    # return  result
    result[-2] = result[-2]+"."+result[-1]
    result.pop()
    return "_".join(result)


_vnPattern = re.compile('([a-zA-Z]+)?(#+)')
def parseVersionPattern(s):
    result = _vnPattern.findall(s)
    if result:
        # s: tst_lgt_v###.ma
        # result: [('v', '###')]
        # prefix: v
        # padPat: ###
        # vnPat: v###
        # vnFormat: v%03d
        # rePat: tst_lgt_v(\d{3}).ma
        # formatS: tst_lgt_v%03d.ma
        prefix,padPat = result[-1]
        vnPat = prefix + padPat
        count = len(padPat)
        rePat = s.replace(padPat, '(\d{%s})' % count)
        rePat = re.compile(rePat)
        theF = '%0'+str(count)+'d'
        formatS = s.replace(padPat, theF)
        vnFormat = prefix + theF
        return rePat, formatS, vnPat, vnFormat
    else:
        return s, s, '', ''


_digitsPattern = re.compile('([a-zA-Z]+)?(\d+)')
def toVersionPattern(string):
    '''
    Converts the string to a version pattern.

    Example:
        string: tst_lgt_v002.ma
        return: tst_lgt_v###.ma
    '''
    result = _digitsPattern.findall(string)
    if result:
        # s: tst_lgt_v002.ma
        # result: [('v', '002')]
        # prefix: v
        # digits: 002
        # digitsPat: v002
        # vnPat: v###
        # pattern: tst_lgt_v###.ma
        prefix, digits = result[-1]
        digitsPat = prefix + digits
        vnPat = prefix + len(digits) * '#'
        pattern = string.replace(digitsPat, vnPat)
        return pattern


def getLatestVersion(files, filenamePattern):
    '''
    Gets latest version file of the files.
    files is a list of string of filenames,
    filenamePattern is a string for filtering the files.

    Example:
        files:
            tst_lgt_v001.ma
            tst_lgt_v002.ma
        filenamePattern:
            tst_lgt_v###.ma or tst_lgt_v001.ma
        return:
            {version_pattern: v###
             version_format: v%03d
             file_format: tst_lgt_v%03d.ma
             latest_version: v002
             latest_version_number: 2
             latest_file: tst_lgt_v002.ma
             current_version: v003
             current_version_number: 3
             current_file: tst_lgt_v003.ma
            }
    '''
    # Parse patterns
    # filenamePattern: tst_lgt_v###.ma
    # filenameRePattern: tst_lgt_v(\d{3}).ma
    # filenameFormat: tst_lgt_v%03d.ma
    # versionPattern: v###
    # versionRePattern: v(\d{3})
    # versionFormat: v%03d
    filenameRePattern, filenameFormat, versionPattern, versionFormat = parseVersionPattern(filenamePattern)
    # print 'filenameRePattern:',filenameRePattern
    # print 'filenameFormat:', filenameFormat
    # print 'versionPattern:',versionPattern
    # print 'versionFormat:', versionFormat

    if filenameRePattern == filenamePattern:
        # filenameRePattern: tst_lgt_v001.ma
        # filenameRePattern: tst_lgt_v###.ma
        filenamePattern = toVersionPattern(filenamePattern)
        if filenamePattern:
            filenameRePattern, filenameFormat, versionPattern, versionFormat = parseVersionPattern(filenamePattern)
        else:
            return

    # Filter the files
    okFiles = {}
    for f in files:
        r = filenameRePattern.findall(f)
        # print 'r:',r
        if r:
            vn = int(r[0])
            if not okFiles.has_key(vn):
                okFiles[vn] = []
            okFiles[vn].append(f)

    if okFiles:
        lastVersionNumber = sorted(okFiles.keys())[-1]
        latestVersion = versionFormat % lastVersionNumber
        latestFile = okFiles[lastVersionNumber][0]
    else:
        lastVersionNumber = 0
        latestVersion = ''
        latestFile = ''

    currentVersionNumber = lastVersionNumber + 1
    currentVersion = versionFormat % currentVersionNumber
    currentFile = filenameFormat % currentVersionNumber

    result = {
        'version_pattern': versionPattern,
        'version_format': versionFormat,
        'latest_version': latestVersion,
        'latest_version_number': lastVersionNumber,
        'latest_file': latestFile,
        'current_version': currentVersion,
        'current_version_number': currentVersionNumber,
        'current_file': currentFile,
    }
    return result



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

    def get_user(self):
        '''

        :return: 返回当前系统的用户名
        '''
        return getpass.getuser()

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

    def makeFolder(self, path):
        '''

        创建文件夹
        :param path: 文件夹路径
        '''
        folder = os.path.dirname(path)
        if not os.path.isdir(folder):
            os.makedirs(folder)

    def delFolder(self, path):
        '''
        删除指定的路径
        :param path:
        '''
        shutil.rmtree(path)

    def copyFile(self, src, dst):
        '''

        :param src: 源文件
        :param dst: 目标文件
        '''
        src = src.replace('\\', '/')
        dst = dst.replace('\\', '/')
        if os.path.exists(src) and src != dst:
            shutil.copyfile(src, dst)


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
        :param info: 需要写入的文件信息
        :param filename: json文件名
        :return: 返回文件信息
        '''
        text = json.dumps(info, indent=4)
        # jsonPath = "{0}/{1}.json".format(CachePath, filename)
        jsonPath = "{0}/{1}.json".format(path, filename)
        f = open(jsonPath, "a")
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

    def file_name(self, sequence='', step=''):
        return self.get_step_message(sequence, step)['file_name']

    def describtion_item(self, sequence='', step=''):
        return self.get_step_message(sequence, step)['describtion_item']

    def work_format(self, sequence='', step=''):
        return self.get_step_message(sequence, step)['work_format']

    # def asset_name(self, name):
    #     return name
    #
    # def describtion_item(self, name):
    #     return name


# dir = {'assetname':'WO', 'step':'Model'}
#
# print get_variable('{asset_name}_{short_name}_{describtion_item}_v###.{work_format}',
#                    **dir
#                    )



