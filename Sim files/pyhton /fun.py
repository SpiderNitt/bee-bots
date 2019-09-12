import vrep
import math
import sys
import ctypes

def path(endpath):
    vrep.simxFinish(-1)                                                                    
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)                            
    if clientID!=-1:
        emptyBuff = bytearray()
        
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'threadFunction',[],endpath,[],emptyBuff,vrep.simx_opmode_blocking)

    return path

def Get_position():
    
                vrep.simxFinish(-1) 
                clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
                if clientID!=-1:
                        _,ebot=vrep.simxGetObjectHandle(clientID,'eBot',vrep.simx_opmode_oneshot_wait)
                        _,pos=vrep.simxGetObjectPosition(clientID,ebot,-1,vrep.simx_opmode_oneshot_wait)
                        return pos         

def velocity(lmvelocity,rmvelocity):
    
    vrep.simxFinish(-1) 
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
    if clientID!=-1:
        _,lm=vrep.simxGetObjectHandle(clientID,'LeftJoint',vrep.simx_opmode_oneshot_wait)
        _,rm=vrep.simxGetObjectHandle(clientID,'RightJoint',vrep.simx_opmode_oneshot_wait)
        _=vrep.simxSetJointTargetVelocity(clientID,lm,lmvelocity,vrep.simx_opmode_oneshot_wait)
        _=vrep.simxSetJointTargetVelocity(clientID,rm,rmvelocity,vrep.simx_opmode_oneshot_wait) 
        
def pick():
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
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

def place(objecthandle):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
        if clientID!=-1:
                _,ps=vrep.simxGetObjectHandle(clientID,'ProximitySensor',vrep.simx_opmode_oneshot_wait) 
                _=vrep.simxSetObjectPosition(clientID,objecthandle,ps,[0,0.3,0.2],vrep.simx_opmode_oneshot_wait)      
                        