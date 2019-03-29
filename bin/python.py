import os

mayaPath="%s/bin/maya.exe"%(os.environ['MAYA_LOCATION'])
mayapyPath="%s/bin/mayapy.exe"%(os.environ['PYTHONPATH'])
mayabatchPath="%s/bin/mayabatch.exe"%(os.environ['MAYA_LOCATION'])
maya_ver = filter(str.isdigit, str(os.environ['MAYA_LOCATION']))
maya_script = "%s\package\maya\%s\scripts"%(os.path.dirname(os.path.realpath('__file__')), maya_ver)


import subprocess
subprocess.call("%s"%(mayaPath))

import maya.mel as mel
import pymel.core as pm

SETENV = 'putenv PATH (`getenv PATH` + ";{ENV}")'.format(ENV=maya_script)
pm.mel.eval(SETENV)


import yaml









