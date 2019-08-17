import vrep

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
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')

    # 1. First send a command to display a specific message in a dialog box:
    emptyBuff = bytearray()
    res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'Dummy',vrep.sim_scripttype_childscript,'threadFunction',[],[],[],emptyBuff,vrep.simx_opmode_blocking)
    if res==vrep.simx_return_ok:
        print ('Return value: ',retFloats) # display the reply from V-REP (in this case, just a string)
    else:
        print ('Remote function call failed')

else:
    print ('Failed connecting to remote API server')
print ('Program ended')