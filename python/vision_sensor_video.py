import vrep
import time
import cv2
import sys
import numpy as np
import signal

vrep.simxFinish(-1)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out_name = "/home/saurav/NS_1_2_Submissions/Videos/Case_2/"+str(sys.argv[1])
out = cv2.VideoWriter(out_name,fourcc, 20.0, (640,480))
clientID = vrep.simxStart('127.0.0.1', 20002, True, True, 10000, 10)

print(clientID)
if clientID!=-1:
	print('Connected to remote API server')
else:
	print( "Failed to connect to remote API Server")
	vrep.simxFinish(clientID)

print('Vision Sensor object handling')
res, v1 = vrep.simxGetObjectHandle(clientID, 'VisionSensor', vrep.simx_opmode_blocking)
print(v1)
#v1 = 99
err = 1
while(err != 0):
	err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming+50)
print("Exited While")
cntr = 0
try:
	while (vrep.simxGetConnectionId(clientID) != -1):
		err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
		if err == vrep.simx_return_ok:
			cntr=cntr+1
			img = np.array(image,dtype=np.uint8)
			img.resize([resolution[1],resolution[0],3])
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
			out.write(img)            
			if err == vrep.simx_return_novalue_flag:
				print("no image yet")
				pass
			# else:
				
			# 	print(cntr)
			if cntr == 6000:
				returnCode = vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
				break
finally:
	returnCode = vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
	vrep.simxFinish(-1)
	out.release()

