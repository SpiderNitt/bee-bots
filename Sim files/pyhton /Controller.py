import vrep
import numpy as np
import math
from time import sleep

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import sys
import ctypes
print ('Program started')
vrep.simxFinish(-1) 
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
if clientID!=-1:
        pos_on_path=0
        dis=0
        path_pos={}
        _,robotHandle=vrep.simxGetObjectHandle(clientID,'Start',vrep.simx_opmode_oneshot_wait)
        _,targetHandle=vrep.simxGetObjectHandle(clientID,'End',vrep.simx_opmode_oneshot_wait)
        _,lm=vrep.simxGetObjectHandle(clientID,'LeftJoint',vrep.simx_opmode_oneshot_wait)
        _,rm=vrep.simxGetObjectHandle(clientID,'RightJoint',vrep.simx_opmode_oneshot_wait)
        _,ebot=vrep.simxGetObjectHandle(clientID,'eBot',vrep.simx_opmode_oneshot_wait)
        print(vrep.simxGetObjectPosition(clientID,ebot,-1,vrep.simx_opmode_oneshot_wait))
        emptyBuff=bytearray()
        end=[2.5,2.5,0]
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'threadFunction',[],[],[],emptyBuff,vrep.simx_opmode_blocking)
        if res==vrep.simx_return_ok:
            print ('Return value: ') 
        else:
            print ('Remote function call failed')
        
        while(1):
            path_pos={retFloats[pos_on_path],retFloats[pos_on_path+1],retFloats[pos_on_path+2]}
            _=vrep.simxSetObjectPosition(clientID,robotHandle,-1,path_pos,vrep.simx_opmode_oneshot_wait)
            _,_,[dis,phi],_,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'follow',[],path_pos,[],emptyBuff,vrep.simx_opmode_blocking)
            #print(path1_pos)
            #dis=math.sqrt((path1_pos[0])**2+(path1_pos[1])**2) 
            print(dis)
            #phi=math.atan2(path1_pos[1],path1_pos[0])
            v_des = -0.05
            om_des = -2*phi
            d=0.06
            v_r=(v_des+d*om_des)
            v_l=(v_des-d*om_des)
            r_w=0.0275 
            omega_right=v_r/r_w
            omega_left=v_l/r_w
            _=vrep.simxSetJointTargetVelocity(clientID,lm,-omega_left,vrep.simx_opmode_oneshot_wait)
            _=vrep.simxSetJointTargetVelocity(clientID,rm,-omega_right,vrep.simx_opmode_oneshot_wait) 
            if(dis<0.1):
                pos_on_path+=3  
            print(pos_on_path)