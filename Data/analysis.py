#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import yaml
import os

yamlname = os.path.join(os.path.dirname(__file__), 'config.yaml').replace("\\", "/")
print yamlname

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
                    elif ii == "asset_work_path":
                        dir['asset_work_parh'] = self.data[i][ii]
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




# ana = ReadCofig("asset","Model")
# a = ana.get_step_message()
# b = ana.allSteps()
# c = ana.get_global()
# # print a
# print b
# # print c