#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import yaml
import os
import re

yamlname = os.path.join(os.path.dirname(__file__), 'config.yaml').replace("\\", "/")


def get_variable(str):
    '''
    
    :param str: yaml文件中带{}的字符串
    :return: 返回解析后的正确的值
    '''

    print str
    funct_ls =  re.findall(r"{(.*?)}", str)

    for i in funct_ls:
        if hasattr(ReadCofig, i):
        # if i == "describtion_item":
            a = ReadCofig()
            # eval() 把字符串改为对应的的变量名，例如：eval("a." + i) <=> ReadCofig.i
            ins = eval("a." + i)
            print ins("asset", "Model")


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

    return  "_".join(after)



class ReadCofig(object):

    def __init__(self):

        self.path = os.path.join(os.path.dirname(__file__), 'config.yaml').replace("\\", "/")

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

get_variable("{asset_name}_{short_name}_{describtion_item}_v###.{work_format}")

# ana = ReadCofig()
# a = ana.get_step_message("asset", "Model")
# print a
# # b = ana.allSteps()
# c = ana.get_global()
# print a
# # print b
# # print c