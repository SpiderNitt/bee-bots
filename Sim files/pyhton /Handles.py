import vrep
class bot():
	
	def __init__(self,ClientID):
		self.ClientID=ClientID
		returncode,self.leftJoint=vrep.simxGetObjectHandle(self.ClientID,"LeftJoint",vrep.simx_opmode_oneshot_wait)
		returncode,self.rightJoint=vrep.simxGetObjectHandle(self.ClientID, "RightJoint",vrep.simx_opmode_oneshot_wait)
		returncode,self.lineSensor=vrep.simxGetObjectHandle(self.ClientID, "LineSensor",vrep.simx_opmode_oneshot_wait)
		returncode,self.colorSensor=vrep.simxGetObjectHandle(self.ClientID, "ColorSensor",vrep.simx_opmode_oneshot_wait)
		returncode,self.eBot=vrep.simxGetObjectHandle(self.ClientID, "eBot",vrep.simx_opmode_oneshot_wait)
		returncode,self.proxSensor=vrep.simxGetObjectHandle(self.ClientID, "ProximitySensor",vrep.simx_opmode_oneshot_wait)
		returncode,self.proxSensor2=vrep.simxGetObjectHandle(self.ClientID, "ProximitySensor2", vrep.simx_opmode_oneshot_wait)
		returncode,self.proxSensor1=vrep.simxGetObjectHandle(self.ClientID, "ProximitySensor1", vrep.simx_opmode_oneshot_wait)
		returncode,[self.x,self.y,self.z]=vrep.simxGetObjectPosition(self.ClientID,self.eBot,-1,vrep.simx_opmode_streaming)
		returncode,[self.alpha,self.beta,self.gamma]=vrep.simxGetObjectOrientation(self.ClientID,self.eBot,-1,vrep.simx_opmode_streaming)
	
	def set_Position(self,ClientID):
		returncode,[self.x,self.y,self.z]=vrep.simxGetObjectPosition(self.ClientID,self.eBot,-1,vrep.simx_opmode_streaming)
		return [self.x,self.y,self.z]
	
	def Get_Orientation(self,ClientID):
		returncode,[self.alpha,self.beta,self.gamma]=vrep.simxGetObjectOrientation(self.ClientID,self.eBot,-1,vrep.simx_opmode_streaming)
		return [self.alpha,self.beta,self.gamma]

class pid():

	def __init__(self,kp,ki,kd):
		self.kp=kp
		self.ki=ki
		self.kd=kd
		self.error=0.0
		self.error_old=0.0
		self.error_sum=0.0
		self.d_error = self.error - self.error_old
	
		
	def control(self,error):
		self.error = error
		self.error_sum += error
		self.d_error = self.error - self.error_old
		P = self.kp*self.error
		I = self.ki*self.error_sum
		D = self.kd*self.d_error
		self.error_old = self.error
		return P+I+D




	
	