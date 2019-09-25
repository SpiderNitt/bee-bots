
import fun
import Controller

class bot():
    
    def __init__(self,port,lmvelocity=0,rmvelocity=0):
        self.lmvelocity=lmvelocity
        self.rmvelocity=rmvelocity
        
        fun.velocity(rmvelocity,lmvelocity,port)
        self.path={}
        self.pos={}
        self.objectPicked=0
        self.port=port
        self.Get_postiton()
    
    def get_path(self,path=[2.5,2.5,0.0]):
        self.path=fun.path(path,self.port)
        return path
    
    def Follow_path(self,path):
        self.Get_postiton()
        Controller.followpath(path,self.objectPicked,self.port)
        self.Get_postiton()
    
    def Get_postiton(self):
        self.pos=fun.Get_position(self.port)
    
    def pick(self):
        self.objectPicked=fun.pick(self.port)
        
    
    def place(self):
        if self.objectPicked==0:
            print("noting to place")
        else:
            fun.place(self.objectPicked,self.port)
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
    	
    ebot2=bot(20000,0,0)
    ebot2.pick()
    ebot2.Follow_path([0.5,2,0.0])
    ebot2.place()
   
		
	