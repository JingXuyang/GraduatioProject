# -*- coding: utf-8 -*-

'''
This module contains common used functions.
'''

import os
import json


class Common(object):
    
    def parseConfigs(self, configs):
        if type(configs) in (str, unicode) and os.path.isfile(configs):
            f = open(configs, 'r')
            t = f.read()
            f.close()
            configs = json.loads(t)
        
        return configs
    
    def app(self):
        return 'app'
    
    def extension(self):
        return self.extensions()[0]
    
    def extensions(self):
        return ['']
    
    
    #---------------------------------- Basic Parameters -------------------------------
    
    _fpsMap = {
        'game': 15,
        'film': 24,
        'pal': 25,
        'ntsc': 30,
        'show': 48,
        'palf': 50,
        'ntscf': 60,
    }
    def fps(self): 
        return 24
    
    def setFps(self, value):
        pass
    
    def resolution(self):
        return 1920,1080
    
    def setResolution(self, width, height):
        return 
    
    def currentFrame(self):
        return 1
    
    def frameRange(self):
        return [1, 24]
    
    def setFrameRange(self, firstFrame, lastFrame):
        pass
    
    def filename(self):
        return ''
    
    def filepath(self):
        return ''
    
    def fileType(self, path=''):
        return ''
    
    def hasUnsavedChanges(self):
        '''Checks whether or not there're unsaved changes.'''
        return False

    def isUntitled(self):
        '''Checks whether or not the current file is untitled.'''
        return False
    
    def sceneUnit(self):
        '''Gets the linear unit of the current scene.'''
        return 'centimeter'
    
    def setSceneUnit(self, value):
        '''
        Sets the current linear unit. Valid strings are:
            [mm | millimeter | cm | centimeter | m | meter | km | kilometer |
             in | inch | ft | foot | yd | yard | mi | mile] 
        '''
        pass
    
    
    
    #---------------------------------- Input and Output -------------------------------
    
    def new(self, force=False):
        return True
    
    def open(self, path, force=False):
        return True
    
    def hasSavingError(self):
        '''
        Sometimes we can open the file but with RuntimeError.
        For this situation, when we try to save the file,
        we got an error below: 
            # Error: line 1: A file must be given a name before saving. Use file -rename first, then try saving again.
            # Traceback (most recent call last):
            #   File "<maya console>", line 1, in <module>
            # RuntimeError: A file must be given a name before saving. Use file -rename first, then try saving again. #
        
        The current filepath has been changed on the window title,
        but it seems that the maya api doesn't get this update.
        
        This funtion will try to get that type of error.
        '''
        pass
    
    def save(self, force=False, type=''):        
        return True
    
    def saveAs(self, path, force=False):
        return True
    
    def close(self):
        pass
    
    def exit(self):
        pass
    
    def setProject(self, path):
        '''Sets project folder for the scene.'''
        pass
    
    def getSceneHierarchy(self):
        return []
    
    def mergeImport(self, path):
        return []
    
    def normalImport(self, path, removeNamespace=False):
        return ''
    
    def import_(self, path, removeNamespace=False):        
        info = {
            'namespace': '',
            'path': path
        }
        return info
    
    def importFbx(self, path):
        return True
    
    def importAbc(self, path, groupOption=None, displayMode=None):
        return True
    
    def importGpuCache(self, path, name=''):
        '''Import gpu cache into the scene.'''
        info = {
            'node': '',
            'namespace': '',
            'ref_path': path,
            'path': path
        }
        return info
    
    def importCamera(self, template, srcName, dstName):
        pass
    
    def rename(self, src, dst):
        pass
    
    def exportFbx(self, path):
        pass
    
    def exportAbc(self, path, singleFrame=False, frameRange=None, objects=[]):
        '''Exports abc cache file.'''
        pass
    
    def exportGpuCache(self, path, singleFrame=False, frameRange=None, objects=[]):
        '''Exports gpu cache abc file.'''
        pass
    
    def exportSelected(self, path):
        pass
    
    def exportAll(self, path):
        pass
    
    def addCustomAttributes(self, data, node):
        pass
    
    def reference(self, path, frameRange=[],
                  groupOption=None, displayMode=None,
                  customAttributes=[]):
        info = {
            'node': '',
            'namespace': '',
            'ref_path': path,
            'path': path
        }
        return info
    
    def referenceCamera(self, path, resolution=None):
        pass
    
    def removeReference(self, refPath):
        pass
    
    def getReferences(self):
        result = []
        return result
    
    def setReferencePath(self, ref, path):
        '''Sets the reference path to a new path.'''
        pass
    
    def getReferenceObjects(self):
        result = []
        return result
    
    def getTopLevelObjectsOfMeshes(self):
        '''Gets top level objects of the meshes.'''
        result = []
        return result
    
    def getGpuCaches(self):
        return []
    
    def setGpuCachePath(self, path):
        pass
    
    def setAssemblyReferencePath(self, path):
        pass
    
    def getAssemblyReferences(self):
        return []
    
    def find(self, name, namespace='', type='transform'):
        '''Finds the objects in the scene.'''
        result = []
        return result
    
    def findObjects(self, name):
        '''
        Finds objects for the object with the name. If the object does not exist,
        try to find it from referenced nodes.
        '''
        result = []
        return result
    
    
    #---------------------------------- Geometry -------------------------------
    
    def select(self, path, replace=True, add=False, noExpand=False):
        pass
    
    def clearSelection(self):
        pass
    
    def delete(self, objects):
        pass
    
    def exists(self, path):
        return True
    
    def getObjects(self, type):
        '''Gets one type of objects.'''
        return []
    
    def getSets(self, root='', removeNamespace=True,
                types=['objectSet'], parms=[]):
        '''
        Gets scene sets of the type.
        If root is not an empty string, it will only list the
        sets which has objects under the root node.
        
        types has options below:
            objectSet
            shadingEngine
        If types is an empty list, it will get all of sets.
        
        Returns a list of dictionaries.
        Example:
            - name: Plastic
              parms: 
                level: 0.5
              components:
                - '|dog|base|pSphere1'
            
            - name: Wood
              parms: 
                level: 0.6
              components:
                - '|dog|base|pCone1'
        '''        
        result = []
        return result
    
    def createSet(self, name, type='objectSet', components=[]):
        '''
        Creates one set with the components.
        Supported types:
            objectSet
            RedshiftObjectId
            RedshiftMeshParameters
            RedshiftVisibility
            RedshiftMatteParameters
        '''
        pass
    
    def createSets(self, sets, namespace=''):
        '''
        Creates scene sets.
        
        sets is a list of dictionaries.
        Example:
            - name: Plastic
              type: objectSet
              parms: 
                level: 0.5
              components:
                - '|dog|base|pSphere1'
            
            - name: Wood
              type: RedshiftObjectId
              parms: 
                level: 0.6
              components:
                - '|dog|base|pCone1'
        
        redshift: redshiftCreateObjectIdNode()
        
        '''
        pass
    
    def getChildren(self, path):
        return []
    
    def getCameras(self):
        cameraL = []
        return cameraL
    
    def getShots(self):
        result = []
        return result
    
    def getCameraSequenceCurrentFrame(self):
        return 1
    
    def getObjectKeyframeRange(self, obj):
        return [1, 24]
    
    def createHierachy(self, data):
        '''
        Creates nodes with the given data.
        The node types support:
            group
            locator
        
        Example of the data:
            - name: dog
              type: group
              subs:
                - name: high
                  type: group
                  subs:
                    - name: model
                    - name: rig
                - name: low
                  type: group
                  subs:
                    - name: ctrl
                      type: locator
        '''
        pass
    
    def getExceptionObjects(self, tree):
        '''Gets objects which are not in the hierachy tree.'''
        return []
    
    def checkHierachy(self, data):
        '''
        Checks whether the outliner hierachy matches the data.
        
        The node types support:
            group
            locator
        
        Example of the data:
            - name: dog
              type: group
              subs:
                - name: high
                  type: group
                  subs:
                    - name: model
                    - name: rig
                - name: low
                  type: group
                  subs:
                    - name: ctrl
                      type: locator
        
        '''
        result = []
        return result
    
    def createShot(self, name, firstFrame, lastFrame, camera=None):
        pass
    
    def createSound(self, startTime, fileName, name):
        pass
    
    def addExtraAttribute(self, objectName, attributeName, attributeValue, dataType='string'):
        '''Adds an extra attribute to the object.'''
        pass
    
    def getAttribute(self, obj, name):
        return ''
    
    def setAttribute(self, obj, name, value):
        pass
    
    def removeObjectNamespaces(self, namespace):
        '''Removes namespaces of the scene objects.'''
        pass
    
    def removeStringNamespace(self, name):
        '''
        Removes namespaces of the name.
        For instance:
            name: |dog:dog|dog:base|dog:box|dog:boxShape
            return: |dog|base|box|boxShape
            
            name: |dog:box.f[10:13]
            return: |box.f[10:13]
        '''
        return name
    
    def addObjectNamespace(self, name, namespace):
        '''
        Adds namespaces to the name.
        For instance:
            name: |dog|base|box|boxShape
            namespace: dog
            return: |dog:dog|dog:base|dog:box|dog:boxShape
            
            name: |box.f[10:13]
            namespace: dog
            return: |dog:box.f[10:13]
        '''
        return name
    
    def getObjectNamespace(self, name):
        '''
        Gets namespaces of the name.
        For instance:
            name: |dog:dog|dog:base|dog:box|dog:boxShape
            namespace: dog
            
            name: |dog:box.f[10:13]
            namespace: dog
        '''
        return ''
    
    def getSceneNamespaces(self):
        result = []
        return result
    
    def clearSceneNamespaces(self):
        pass
    
    def getIsolatedVetices(self):
        newObjectDic = {}
        return newObjectDic
    
    def getIsolatedFaces(self):
        errorPoly = []
        return errorPoly
    
    def getNPolygonFaces(self, n=4):
        allMultilateralFace = {}
        return allMultilateralFace
    
    def getOverlappedUVs(self):
        return []
    
    def getUnFreezedObjects(self):
        absent_name = []
        return absent_name
    
    def freezeObjects(self, objects):
        pass
    
    def getProblemNormals(self):
        model_name_list = []
        return model_name_list
    
    def repairNormals(self, obj):
        pass
    
    def getNonManifoldObjects(self):
        model_name_list = []
        return model_name_list
    
    def getSmallEdges(self):
        model_name_list = []
        return model_name_list
    
    def renameChildren(self, node, replace, to):
        pass
    
    
    #---------------------------------- Materials -------------------------------
    
    def getShadingEngines(self):
        '''Gets shading engine nodes.'''
        result = []
        return result
    
    def getMaterials(self, removeNamespace=False):
        '''
        Gets materials to a dictionary of which keys are materials and values are
        shapes and faces.
        Example of the returned dictionary:
            {
                'metal': {
                    'box': ['box.face[1-29]', 'box.face[33]'],
                    'sphere': [],
                }
            }
        '''
        result = {}
        return result
    
    def exportMaterials(self, path, generateMapping=False, mappingFilename='mapping',
                        removeNamespace=False):
        '''Exports all materials to a new ma file.'''
        materials = self.getMaterials(removeNamespace=removeNamespace)
        return materials.keys()
    
    def importMaterials(self, path, configs={}):
        pass
    
    def assignMaterials(self, mapping, geoNamespace='', matNamespace=''):
        '''
        Example of mapping:
            {
                "blinn1SG": {
                    "|dog|base|box|boxShape": [
                        "|box.f[0:5]", 
                        "|box.f[7:9]"
                    ]
                },
                "blinn2SG": {
                    "|dog|base|pCone1|pConeShape1": []
                }
            }
            
            {
                "blinn1SG": {
                    "|dog|base|body|bodyShape": [
                        "|body.f[200:359]", 
                        "|body.f[380:399]"
                    ]
                }, 
                "blinn2SG": {
                    "|dog|base|body|bodyShape": [
                        "|body.f[0:199]", 
                        "|body.f[360:379]"
                    ]
                }
            }
        '''
        pass
    
    def getFileNodes(self, materials):
        '''
        Gets file texture nodes for the materials.
        materials is a list of material names.
        '''
        fileNodes = []
        return fileNodes
    
    def getTexturePaths(self, fileNodes):
        '''Gets texture paths for the file nodes.'''
        texDic = {}
        return texDic
    
    def replaceTexturePaths(self, maPath, pathInfo):
        pass
    
    
    #---------------------------------- Render -------------------------------
    
    def getActiveCamera(self):
        return []
    
    def setActiveCameraAttributes(self, filmPivot=False, filmOrigin=False,
                                  safeAction=False, resolution=False, gateMask=False):
        '''Sets display attributes of the active camera.'''
        pass
    
    def removeAllHUDs(self):
        pass
    
    def setHUD(self, name='', section=1, block=1, blockSize='small', labelWidth=70,
               label='', labelFontSize='large'):
        '''Sets the heads up display.'''
        pass
    
    def setHUDs(self, data):
        '''
        Sets a list of HUD items.
        data is a list of dictionaries like this:
        [
            {'name': 'combo', 'section': 1, 'block': 1, 'blockSize': 'small',
            'labelWidth': 70, 'label': 'TST', 'labelFontSize': 'large'},
            {},
        ]
        '''
        for d in data:
            #print 'HUD:', d
            self.setHUD(**d)
    
    def playblast(self, path, scale=50, quality=100, resolution=None, override=False,
                  firstFrame=None, lastFrame=None, ao=True, antiAliasing=True,
                  camera=None, useCameraKeyframeRange=False):
        '''
        Makes playblast for the current scene.
        Arguments:
            path: a image sequence or a avi file
                image sequence:
                    /abc/abc.####.jpg
                avi:
                    /abc/abc.avi
            scale: percent of the output image
            quality: quality of the output image
            resolution: a list of width and height, default is from render setting dialog
        '''
        return True
    
    def getCurrentView(self):
        return []
    
    def makeSuitableCamera(self, pos=1, objects=[]):
        '''Makes a camera based the bounding box of the geometry.'''
        return ''
    
    def setKeyframe(self, geo, channel, frame, value):
        pass
    
    def deleteKeyframe(self, geo, channel, frame):
        pass
    
    def moveObjectsKeyframes(self, objs, frame):
        '''Moves all of the keyframes of the objects to the frame.'''
        result = {
            'original_frame_range': [1, 24],
            'offset_frames': 10, 
        }
        return result
    
    def setSubsTransform(self, obj, lastNode=None, info=[]):
        pass
    
    def makeTurntablePlayblast(self, path, geo, firstFrame=1, lastFrame=60,
                               resolution=None, scale=100, quality=100, override=False):
        '''Makes playblast preview render for the geo.'''
        pass
    
    def makeSceneThumbnail(self, path, objects=[]):
        '''Makes a snapshot image as the scene thumbnail.'''
        pass
    
    def createRenderNode(self, path, render='', firstFrame=1, lastFrame=60,
               resolution=[1920,1080], camera=None, overrideMaterials=False,
               enableAOVs=False, frameStep=1, renderSettings={}):
        pass
    
    
    #---------------------------------- Dialog -------------------------------
    
    def confirmDialog(self, *args, **kwargs):
        return 
    
    def newSceneConfirmDialog(self):
        return True
    
    def saveAsFileDialog(self):
        return ''
    
    def newDialog(self):
        if self.hasUnsavedChanges():
            confirm = self.newSceneConfirmDialog()
            if confirm == True:
                result = self.saveDialog()
                if result:
                    self.new(force=True)
                    return True
                else:
                    return False
            
            elif confirm == False:
                self.new(force=True)
                return True
        
        else:
            self.new(force=True)
            return True
    
    def saveDialog(self):
        if self.isUntitled():
            path = self.saveAsFileDialog()
            if path:
                self.saveAs(path, force=True)
                return True
        
        else:
            self.save(force=True)
            return True

