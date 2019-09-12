
import fun
import Controller

class bot():
    
    def __init__(self,lmvelocity=0,rmvelocity=0):
        self.lmvelocity=lmvelocity
        self.rmvelocity=rmvelocity
        self.Get_postiton()
        fun.velocity(rmvelocity,lmvelocity)
        self.path={}
        self.pos={}
        self.objectPicked=0
    
    def get_path(self,path=[2.5,2.5,0.0]):
        self.path=fun.path(path)
        return path
    
    def Follow_path(self,path):
        Controller.followpath(path,self.objectPicked)
        self.Get_postiton()
    
    def Get_postiton(self):
        self.pos=fun.Get_position()
    
    def pick(self):
        self.objectPicked=fun.pick()
        
    
    def place(self):
        if self.objectPicked==0:
            print("noting to place")
        else:
            fun.place(self.objectPicked)
            self.objectPicked=0
        
		
		





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
    	
    ebot1=bot(0,0)
    ebot1.pick()
    ebot1.Follow_path([0.5,1.5,0.0])
    ebot1.place()
    #ebot1.Follow_path([0,0,0])
		
	