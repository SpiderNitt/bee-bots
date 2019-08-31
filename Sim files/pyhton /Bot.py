
import fun

class bot():
	
	def __init__(self,pos=[0,0,0],lmvelocity=0,rmvelocity=0):
		self.x=pos[0]
		self.y=pos[1]
		self.z=pos[2]
		self.lmvelocity=lmvelocity
		self.rmvelocity=rmvelocity
  
		fun.position(pos)
		fun.velocity(rmvelocity,lmvelocity)
     
	def get_path(self,path=[2.5,2.5,0]):
     		self.path=fun.path(path)
	
 	#def get_path(self,path=[2.5,2.5]):
		 #self.path=fun.path(path)
		
	
	#def Follow_path(self,path):
		
     
		





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




	
if __name__ == '__main__':
    	
    ebot1=bot([])
    ebot1.get_path([2.5,2.5,0])
		
	