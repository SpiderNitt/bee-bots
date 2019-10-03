import vrep
import math
import sys
import ctypes

def path(endpath,port):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
    if clientID!=-1:
        emptyBuff = bytearray()
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'threadFunction',[],endpath,[],emptyBuff,vrep.simx_opmode_blocking)
    return path

def get_object_handle(port,object):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
    if clientID!=-1:
            _,handle=vrep.simxGetObjectHandle(clientID,object,vrep.simx_opmode_oneshot_wait)
            return handle

def Get_position(port):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
    if clientID!=-1:
            _,ebot=vrep.simxGetObjectHandle(clientID,'eBot',vrep.simx_opmode_oneshot_wait)
            _,pos=vrep.simxGetObjectPosition(clientID,ebot,-1,vrep.simx_opmode_oneshot_wait)
            return pos

def velocity(lmvelocity,rmvelocity,port):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
    if clientID!=-1:
        _,lm=vrep.simxGetObjectHandle(clientID,'LeftJoint',vrep.simx_opmode_oneshot_wait)
        _,rm=vrep.simxGetObjectHandle(clientID,'RightJoint',vrep.simx_opmode_oneshot_wait)
        _=vrep.simxSetJointTargetVelocity(clientID,lm,lmvelocity,vrep.simx_opmode_oneshot_wait)
        _=vrep.simxSetJointTargetVelocity(clientID,rm,rmvelocity,vrep.simx_opmode_oneshot_wait)

def pick(port):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
    if clientID!=-1:
        _,ps=vrep.simxGetObjectHandle(clientID,'ProximitySensor',vrep.simx_opmode_oneshot_wait)
        _,detectionState,detectionPoint,detectionObjectHandle,_=vrep.simxReadProximitySensor(clientID,ps,vrep.simx_opmode_oneshot_wait)
        print(detectionState,detectionPoint,detectionObjectHandle)
        dis = math.sqrt(detectionPoint[0]**2+detectionPoint[1]**2+detectionPoint[2]**2)
        if (detectionState==True and dis<0.5):
                _=vrep.simxSetObjectPosition(clientID,detectionObjectHandle,ps,[0,0,12],vrep.simx_opmode_oneshot_wait)
                return detectionObjectHandle
        else :
                print("not able to pick any block")
                return 0

def place(objecthandle,port):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
    if clientID!=-1:
            _,ps=vrep.simxGetObjectHandle(clientID,'ProximitySensor',vrep.simx_opmode_oneshot_wait)
            _,picksubs=vrep.simxGetObjectHandle(clientID,'Cuboid14',vrep.simx_opmode_oneshot_wait)
            _=vrep.simxSetObjectPosition(clientID,picksubs,-1,[-2,-2,0],vrep.simx_opmode_oneshot_wait)
            _=vrep.simxSetObjectPosition(clientID,objecthandle,ps,[0,0.3,0.2],vrep.simx_opmode_oneshot_wait)

def place_block(port,objecthandle,position):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
    if clientID!=-1:
            print("kept")
            handle=get_object_handle(port,'Cuboid12')
            _=vrep.simxSetObjectPosition(clientID,handle,-1,position,vrep.simx_opmode_oneshot_wait)

def send_to_ros(port,path):
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
    if clientID!=-1:
        emptyBuff=bytearray()
        _,_,retFloats,_,_=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'threadFunction',[],path,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
        x=len(retFloats)
        _,_,_,_,_=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'publishRos',[x],retFloats,[],emptyBuff,vrep.simx_opmode_oneshot_wait)