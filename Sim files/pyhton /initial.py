
import vrep
import time

def scenesinit(port):

    vrep.simxFinish(-1) 
    clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)     
    if clientID!=-1:
        stringData=vrep.simxGetObjectGroupData(clientID,vrep.sim_appobj_object_type,0,)
        
            

    
    vrep.simxFinish(clientID)
    
if __name__ == '__main__':
    scenesinit(19999)
    