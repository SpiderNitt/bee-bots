
import vrep
import time

class scene:
    def __init__(self, port):
        self.port=port
        self.obstacles_handles={'x':1}
        self.obstacles_initpos={}
        self.obstacles_final_pos={}
        self.scenesinit(self.port)


if __name__ == '__main__':
    a=scene(20000)
