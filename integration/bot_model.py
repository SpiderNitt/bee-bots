import vrep
import math
import sys
import ctypes
import numpy as np
import math
import time
from time import sleep


# bot_config = {
# "bot": 'eBot1',
# "script": 'Dummy',
# "thread_function": "threadFunction",
# "left_joint": "LeftJoint1",
# "right_joint": "RightJoint1",
# "proximity_sensor_one": "ProximitySensor5",
# "proximity_sensor_two": "ProximitySensor6",
# "proximity_sensor_three": "ProximitySensor7",
# 'publish_ros': "publishRos",
# "follow": "follow",
# "start":"Start", 
# "end":"End",
# "sentinel":"Cuboid14",
# "follow" :"follow"
# }

# def initialise(bot_configuration):
#     bot_config = bot_configuration




class bot:
    def __init__(self, port,config,lmvelocity=0, rmvelocity=0):
        self.lmvelocity = lmvelocity
        self.rmvelocity = rmvelocity
        self.bot_config = config
        self.velocity(rmvelocity, lmvelocity, port)
        self.path = {}
        self.pos = {}
        self.objectPicked = 0
        self.port = port
        self.Get_postiton()
        self.Get_position_b(self.port)
        
       

    def get_path(self, path=[2.5, 2.5, 0.0]):
        self.path = path(path, self.port)
        return path

    def Follow_path(self, path):
        self.Get_postiton()
        self.followpath(path, self.objectPicked, self.port)
        self.Get_postiton()

    def Get_postiton(self):
        self.pos = self.Get_position_b(self.port)
        return self.pos

    def pick(self):
        self.objectPicked = self.pick_b(self.port)

    def place_from_other_sceme(self, objectHandle, pos):
        self.place_block(self.port, objectHandle, pos)

    def place(self):
        if self.objectPicked == 0:
            print("noting to place")
        else:
            print("Blacing block")
            self.place_b(self.objectPicked, self.port)
            self.objectPicked = 0

    def path(self,endpath,port):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
            emptyBuff = bytearray()
            res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,self.bot_config["script"],vrep.sim_scripttype_childscript,bot_config['thread_function'],[],endpath,[],emptyBuff,vrep.simx_opmode_blocking)
        return path

    def get_object_handle(self,port,object):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
                _,handle=vrep.simxGetObjectHandle(clientID,object,vrep.simx_opmode_oneshot_wait)
                return handle

    def Get_position_b(self,port):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
                _,ebot=vrep.simxGetObjectHandle(clientID,self.bot_config['bot'],vrep.simx_opmode_oneshot_wait)
                _,pos=vrep.simxGetObjectPosition(clientID,ebot,-1,vrep.simx_opmode_oneshot_wait)
                # print("output of get position:::: ", pos)
                self.coordinates = {"x":pos[0], "y":pos[1]}
                # print("coordinates inside bot instance::: ", self.coordinates)
                return pos

    def velocity(self,lmvelocity,rmvelocity,port):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
            _,lm=vrep.simxGetObjectHandle(clientID,self.bot_config['left_joint'],vrep.simx_opmode_oneshot_wait)
            _,rm=vrep.simxGetObjectHandle(clientID,self.bot_config['right_joint'],vrep.simx_opmode_oneshot_wait)
            _=vrep.simxSetJointTargetVelocity(clientID,lm,lmvelocity,vrep.simx_opmode_oneshot_wait)
            _=vrep.simxSetJointTargetVelocity(clientID,rm,rmvelocity,vrep.simx_opmode_oneshot_wait)
    


    def pick_b(self,port):
        dis1_flag = False
        dis2_flag = False
        dis3_flag = False
        dis4_flag = False
        dis5_flag = False
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
            _,ps1=vrep.simxGetObjectHandle(clientID,self.bot_config['proximity_sensor_one'],vrep.simx_opmode_oneshot_wait)
            _,detectionState1,detectionPoint1,detectionObjectHandle1,_=vrep.simxReadProximitySensor(clientID,ps1,vrep.simx_opmode_oneshot_wait)
            _,ps2=vrep.simxGetObjectHandle(clientID,self.bot_config['proximity_sensor_two'],vrep.simx_opmode_oneshot_wait)
            _,detectionState2,detectionPoint2,detectionObjectHandle2,_=vrep.simxReadProximitySensor(clientID,ps2,vrep.simx_opmode_oneshot_wait)
            _,ps3=vrep.simxGetObjectHandle(clientID,self.bot_config['proximity_sensor_three'],vrep.simx_opmode_oneshot_wait)
            _,detectionState3,detectionPoint3,detectionObjectHandle3,_=vrep.simxReadProximitySensor(clientID,ps3,vrep.simx_opmode_oneshot_wait)
            _,ps4=vrep.simxGetObjectHandle(clientID,self.bot_config['proximity_sensor_four'],vrep.simx_opmode_oneshot_wait)
            _,detectionState4,detectionPoint4,detectionObjectHandle4,_=vrep.simxReadProximitySensor(clientID,ps4,vrep.simx_opmode_oneshot_wait)
            _,ps5=vrep.simxGetObjectHandle(clientID,self.bot_config['proximity_sensor_five'],vrep.simx_opmode_oneshot_wait)
            _,detectionState5,detectionPoint5,detectionObjectHandle5,_=vrep.simxReadProximitySensor(clientID,ps5,vrep.simx_opmode_oneshot_wait)
            dis = 10000
            print(detectionState1,detectionState2,detectionState3, detectionState4, detectionState5)
            if detectionState1:
                dis = math.sqrt(detectionPoint1[0]**2+detectionPoint1[1]**2+detectionPoint1[2]**2)
                dis1_flag = True
            elif detectionState2:
               dis = math.sqrt(detectionPoint2[0]**2+detectionPoint2[1]**2+detectionPoint2[2]**2)
               dis2_flag = True
            elif detectionState3:
                dis = math.sqrt(detectionPoint3[0]**2+detectionPoint3[1]**2+detectionPoint3[2]**2)
                dis3_flag = True
            elif detectionState4:
                dis = math.sqrt(detectionPoint4[0]**2+detectionPoint4[1]**2+detectionPoint4[2]**2)
                dis4_flag = True
            elif detectionState5:
                dis = math.sqrt(detectionPoint5[0]**2+detectionPoint5[1]**2+detectionPoint5[2]**2)
                dis5_flag = True

            # print("inside pick:::: ", dis)
            if (dis<0.3):
                if (dis1_flag):
                    _=vrep.simxSetObjectPosition(clientID,detectionObjectHandle1,ps1,[0,0,12],vrep.simx_opmode_oneshot_wait)
                    return detectionObjectHandle1
                elif dis2_flag:
                    _=vrep.simxSetObjectPosition(clientID,detectionObjectHandle2,ps2,[0,0,12],vrep.simx_opmode_oneshot_wait)
                    return detectionObjectHandle2
                elif dis3_flag:
                    _=vrep.simxSetObjectPosition(clientID,detectionObjectHandle3,ps3,[0,0,12],vrep.simx_opmode_oneshot_wait)
                    return detectionObjectHandle3
                elif (dis4_flag):
                    _=vrep.simxSetObjectPosition(clientID,detectionObjectHandle4,ps4,[0,0,12],vrep.simx_opmode_oneshot_wait)
                    return detectionObjectHandle4
                elif (dis5_flag):
                    _=vrep.simxSetObjectPosition(clientID,detectionObjectHandle5,ps5,[0,0,12],vrep.simx_opmode_oneshot_wait)
                    return detectionObjectHandle5
            else :
                    print("not able to pick any block")
                    return 0

    def place_b(self,objecthandle,port):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
                _,ps=vrep.simxGetObjectHandle(clientID,self.bot_config['proximity_sensor_one'],vrep.simx_opmode_oneshot_wait)
                _,picksubs=vrep.simxGetObjectHandle(clientID,self.bot_config['sentinel'],vrep.simx_opmode_oneshot_wait)
                _=vrep.simxSetObjectPosition(clientID,picksubs,-1,[-2,-2,0],vrep.simx_opmode_oneshot_wait)
                _=vrep.simxSetObjectPosition(clientID,objecthandle,ps,[0.5,0.5,0.2],vrep.simx_opmode_oneshot_wait)   #change the coordinates to experiment the placement of blocks

    def place_block(self,port,objecthandle,position):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
                print("kept")
                handle=self.get_object_handle(port,self.bot_config['sentinel'])  # ! CUBOID 12 or CUBOID 14
                _=vrep.simxSetObjectPosition(clientID,handle,-1,position,vrep.simx_opmode_oneshot_wait)

    def send_to_ros(self,port,path):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
            emptyBuff=bytearray()
            _,_,retFloats,_,_=vrep.simxCallScriptFunction(clientID,self.bot_config["script"],vrep.sim_scripttype_childscript,self.bot_config['thread_function'],[],path,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
            x=len(retFloats)
            _,_,_,_,_=vrep.simxCallScriptFunction(clientID,self.bot_config["script"],vrep.sim_scripttype_childscript,self.bot_config['publish_ros'],[x],retFloats,[],emptyBuff,vrep.simx_opmode_oneshot_wait)


    def stop_function(self, port):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',port,True,True,5000,5)
        if clientID!=-1:
            _,ps=vrep.simxGetObjectHandle(clientID,self.bot_config['proximity_bot'],vrep.simx_opmode_oneshot_wait)
            _,detectionState,detectionPoint,detectionObjectHandle,_=vrep.simxReadProximitySensor(clientID,ps,vrep.simx_opmode_oneshot_wait)
            return detectionState



    def followpath(self, path, objectHandle, port):
        vrep.simxFinish(-1)
        print("following path")
        
        clientID = vrep.simxStart("127.0.0.1", port, True, True, 5000, 5)
        if clientID != -1:
            prev_time = 0
            pos_on_path = 1
            dis = 0
            path_pos = {}
            flag = 0
            x = 0
            check = 0

            _, robotHandle = vrep.simxGetObjectHandle(
                clientID, self.bot_config['start'], vrep.simx_opmode_oneshot_wait
            )
            _, targetHandle = vrep.simxGetObjectHandle(
                clientID, self.bot_config['end'], vrep.simx_opmode_oneshot_wait
            )
            _, lm = vrep.simxGetObjectHandle(
                clientID, self.bot_config['left_joint'], vrep.simx_opmode_oneshot_wait
            )
            _, rm = vrep.simxGetObjectHandle(
                clientID, self.bot_config['right_joint'], vrep.simx_opmode_oneshot_wait
            )
            _, ebot = vrep.simxGetObjectHandle(
                clientID, self.bot_config['bot'], vrep.simx_opmode_oneshot_wait
            )
            _, picksubs = vrep.simxGetObjectHandle(
                clientID, self.bot_config['sentinel'], vrep.simx_opmode_oneshot_wait
            )
            emptyBuff = bytearray()
            res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,self.bot_config['script'],vrep.sim_scripttype_childscript,self.bot_config["thread_function"],[],path,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
            

            while 1:

                        if objectHandle:
                            _ = vrep.simxSetObjectPosition(
                            clientID,
                            picksubs,
                            ebot,
                            [0, 0, 0.052],
                            vrep.simx_opmode_oneshot_wait,
                        )

                        #if self.stop_function(self.port):
                            #pos_on_path = 1
                            #emptyBuff = bytearray()
                            #res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,self.bot_config['script'],vrep.sim_scripttype_childscript,self.bot_config["thread_function"],[],path,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
                            
                        
                #if self.obstacle(self.port)<0.5:
                #    print("danger")
                #    print(self.obstacle(self.port))
                #    _= vrep.simxSetJointTargetVelocity(
                #        clientID, lm, 0, vrep.simx_opmode_oneshot_wait
                #    )
                #    _= vrep.simxSetJointTargetVelocity(
                #        clientID, rm, 0, vrep.simx_opmode_oneshot_wait
                #    )
                
                #else :

                        emptyBuff = bytearray()
                        _, _, dis, _, _ = vrep.simxCallScriptFunction(
                            clientID,
                            self.bot_config["script"],
                            vrep.sim_scripttype_childscript,
                            self.bot_config['follow'],
                            [pos_on_path],
                            retFloats,
                            [],
                            emptyBuff,
                            vrep.simx_opmode_blocking,
                        )
                        if pos_on_path >= len(retFloats):
                                _ = vrep.simxSetJointTargetVelocity(
                                clientID, lm, 0, vrep.simx_opmode_oneshot_wait
                            )
                                _ = vrep.simxSetJointTargetVelocity(
                                clientID, rm, 0, vrep.simx_opmode_oneshot_wait
                            )
                            
                                break
                        
                        v_des = -0.1
                        om_des = -0.8 * dis[1]
                        d = 0.06
                        v_r = v_des + d * om_des
                        v_l = v_des - d * om_des
                        r_w = 0.0275
                        omega_right = v_r / r_w
                        omega_left = v_l / r_w

                        _ = vrep.simxSetJointTargetVelocity(
                            clientID, lm, (-1 * omega_left), vrep.simx_opmode_oneshot_wait
                        )
                        _ = vrep.simxSetJointTargetVelocity(
                            clientID, rm, (-1 * omega_right), vrep.simx_opmode_oneshot_wait
                        )

                    
                        
                        if (
                            math.sqrt(
                                (path[0] - retFloats[pos_on_path - 1]) ** 2
                                + (path[1] - retFloats[pos_on_path]) ** 2
                            )
                            < 0.15
                        ):
                        

                            _ = vrep.simxSetJointTargetVelocity(
                                clientID, lm, 0, vrep.simx_opmode_oneshot_wait
                            )
                            _ = vrep.simxSetJointTargetVelocity(
                                clientID, rm, 0, vrep.simx_opmode_oneshot_wait
                            )
                            #_ = vrep.simxSetObjectOrientation(
                            #    clientID , ebot,-1,[0,0,0],vrep.simx_opmode_oneshot_wait
                            #)
			                


                            print("exit")
                            break
                            

                    
                        
                        if dis[0] < 0.1:
                            pos_on_path += 3
                        


    def path_5_sec(self,clientID, path):
        pos_on_path = 1
        emptyBuff = bytearray()
        res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(
            clientID,
            self.bot_config["script"],
            vrep.sim_scripttype_childscript,
        self.bot_config['thread_function'],
            [],
            path,
            [],
            emptyBuff,
            vrep.simx_opmode_oneshot_wait,
        )
        return retFloats

        


class pid:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0.0
        self.error_old = 0.0
        self.error_sum = 0.0
        self.d_error = self.error - self.error_old


    def control(self, error):
        self.error = error
        self.error_sum += error
        self.d_error = self.error - self.error_old
        P = self.kp * self.error
        I = self.ki * self.error_sum
        D = self.kd * self.d_error
        self.error_old = self.error
        return P + I + D

    


if __name__ == "__main__":

    ebot1 = bot(19999, 0, 0)
    # ebot1.pick()
    ebot1.Follow_path([0.5, 2, 0.0])
    # ebot1.place()
    ebot1.Follow_path([0.25, 1, 0])
    ebot1.place_from_other_sceme(21, [0.5, 2, 0.0])

