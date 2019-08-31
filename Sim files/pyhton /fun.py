import vrep

import sys
import ctypes

def path(endpath):
    vrep.simxFinish(-1)                                                                    
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)                            
    if clientID!=-1:
        emptyBuff = bytearray()
        
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'threadFunction',[],endpath,[],emptyBuff,vrep.simx_opmode_blocking)

    return path

def position(position):
    
    vrep.simxFinish(-1) 
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
    if clientID!=-1:
        _,ebot=vrep.simxGetObjectHandle(clientID,'eBot',vrep.simx_opmode_oneshot_wait)
        _=vrep.simxSetObjectPosition(clientID,ebot,-1,position,vrep.simx_opmode_oneshot_wait)
                
def velocity(lmvelocity,rmvelocity):
    
    vrep.simxFinish(-1) 
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
    if clientID!=-1:
        _,lm=vrep.simxGetObjectHandle(clientID,'LeftJoint',vrep.simx_opmode_oneshot_wait)
        _,rm=vrep.simxGetObjectHandle(clientID,'RightJoint',vrep.simx_opmode_oneshot_wait)
        _=vrep.simxSetJointTargetVelocity(clientID,lm,lmvelocity,vrep.simx_opmode_oneshot_wait)
        _=vrep.simxSetJointTargetVelocity(clientID,rm,rmvelocity,vrep.simx_opmode_oneshot_wait) 
        
