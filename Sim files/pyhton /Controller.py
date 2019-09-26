import vrep
import numpy as np
import math
import time
from time import sleep
import sys
import ctypes


def followpath(path,objectHandle,port):
    vrep.simxFinish(-1) 
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5) 
    if clientID!=-1:
            
            prev_time=0
            pos_on_path=1
            dis=0
            path_pos={}
            flag=0
            x=0
            
            _,robotHandle=vrep.simxGetObjectHandle(clientID,'Start',vrep.simx_opmode_oneshot_wait)  
            _,targetHandle=vrep.simxGetObjectHandle(clientID,'End',vrep.simx_opmode_oneshot_wait)
            _,lm=vrep.simxGetObjectHandle(clientID,'LeftJoint',vrep.simx_opmode_oneshot_wait)
            _,rm=vrep.simxGetObjectHandle(clientID,'RightJoint',vrep.simx_opmode_oneshot_wait)
            _,ebot=vrep.simxGetObjectHandle(clientID,'eBot',vrep.simx_opmode_oneshot_wait)

            
            
            #res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'threadFunction',[],path,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
            
            #print(len(retFloats))
            
            while(1):
                
                if (time.time()-prev_time)>1:
                   if (not flag) :
                        retFloats=path_5_sec(clientID,path)
                        sleep(0.1)
                        pos_on_path=1
                        prev_time=time.time()
                   
                   
                emptyBuff=bytearray()   
                _,_,dis,_,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'follow',[pos_on_path],retFloats,[],emptyBuff,vrep.simx_opmode_blocking)
                
                v_des = -0.05
                om_des = -0.8*dis[1]
                d=0.06
                v_r=(v_des+d*om_des)
                v_l=(v_des-d*om_des)
                r_w=0.0275 
                omega_right=(v_r/r_w)
                omega_left=(v_l/r_w)
                
                _=vrep.simxSetJointTargetVelocity(clientID,lm,(-1*omega_left),vrep.simx_opmode_oneshot_wait)
                _=vrep.simxSetJointTargetVelocity(clientID,rm,(-1*omega_right),vrep.simx_opmode_oneshot_wait) 
                
                if(dis[0]<0.1):
                    pos_on_path+=3 
                
                if(flag==1):
                    if (math.sqrt((path[0]-retFloats[pos_on_path-1])**2+(path[1]-retFloats[pos_on_path])**2)<0.01):
                        _=vrep.simxSetJointTargetVelocity(clientID,lm,0,vrep.simx_opmode_oneshot_wait)
                        _=vrep.simxSetJointTargetVelocity(clientID,rm,0,vrep.simx_opmode_oneshot_wait) 
                        print("exit")
                        x=1
                        break
                
                if(x==1):
                    break 
                
                
                print(math.sqrt((path[0]-retFloats[pos_on_path-1])**2+(path[1]-retFloats[pos_on_path])**2))
                if(math.sqrt((path[0]-retFloats[pos_on_path-1])**2+(path[1]-retFloats[pos_on_path])**2)<0.5):
                    flag=1
                    
                
                if(objectHandle):
                    _=vrep.simxSetObjectPosition(clientID,objectHandle,ebot,[0,0,0.052],vrep.simx_opmode_oneshot_wait)
                
                
def path_5_sec(clientID,path):
        
        pos_on_path=1
        emptyBuff=bytearray()
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'threadFunction',[],path,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
        return (retFloats)
                
