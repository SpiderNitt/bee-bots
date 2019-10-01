
import vrep
import time

class scene:
    def __init__(self, port):
        self.port=port
        self.obstacles_handles={'x':1}
        self.obstacles_initpos={}
        self.obstacles_final_pos={}
        self.scenesinit(self.port)
    def scenesinit(self,port):

        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
            _,handles,_,_,stringData=vrep.simxGetObjectGroupData(clientID,vrep.sim_appobj_object_type,0,vrep.simx_opmode_oneshot_wait)

            for i in range(len(stringData)):
                if stringData[i].find("Cuboid")>=0:
                    print(stringData[i])
                    self.obstacles_handles.update({stringData[i]:handles[i]})
                    _,pos=vrep.simxGetObjectPosition(clientID,handles[i],-1,vrep.simx_opmode_oneshot_wait)
                    self.obstacles_initpos.update({stringData[i]:pos})
            print(self.obstacles_handles,self.obstacles_initpos)

if __name__ == '__main__':
    a=scene(19999)
