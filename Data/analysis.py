#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import yaml
import os

yamlname = os.path.join(os.path.dirname(__file__), 'config.yaml').replace("\\", "/")


def get_variable(str):

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
                        print get_variable(self.data[i][ii])
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

    def get_step_message(self, sequence='', step=''):

        '''
        :sequence :  shot 或者 asset
        :step :  环节
        
        return:
         {
         'short_name': model,
         'file_name': test_model_v001.mb
         }
        '''
        dir = {}

        for seq in self.data:
            if seq == self.sequence:
                ls = []
                for step in self.data[seq]:
                    ls.append(step)
                    if step == self.step:
                        for detail in self.data[seq][step]:
                            if detail == "short_name":
                                dir["short_name"] = self.data[seq][step][detail]
                            if detail == "file_name":
                                dir["file_name"] = self.data[seq][step][detail]

        return dir




# ana = ReadCofig()
# # a = ana.get_step_message()
# # b = ana.allSteps()
# c = ana.get_global()
# # print a
# # print b
# print c