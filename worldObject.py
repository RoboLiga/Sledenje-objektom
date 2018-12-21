import numpy as np
from numpy.linalg import inv
ROBOT=0
APPLE_GOOD=1
APPLE_BAD=2
CORNER=3

class Object(object):
    """description of class"""
    def __init__(self, type, id, position, direction, velocity, accel=(0,0), params=(0.003,0.6)):
        self.type = type
        self.id=id
        self.position = position
        self.velocity = velocity
        self.direction = direction
        self.Q=np.array([[position[0]],[position[1]],[velocity[0]],[velocity[1]],[accel[0]],[accel[1]]])
        self.Qestimate=self.Q
        self.accNoiseMag=params[0]
        self.dt=1 #sampling rate
        self.u=0.0 #acceleration magnitude
        self.measurementNoiseX=params[1];
        self.measurementNoiseY=params[1];
        self.detected=True;
        self.enabled=True;
        self.last_seen=0;
        self.lost_frames=0;
        self.Ez=np.array([[self.measurementNoiseX, 0],[0, self.measurementNoiseY]])
        #self.Ex=np.array([[self.dt**4/4, 0, self.dt**3/2, 0], \
        #                  [0, self.dt**4/4, 0, self.dt**3/2], \
        #                  [self.dt**3/2, 0, self.dt**2, 0], \
        #                  [0, self.dt**3/2, 0, self.dt**2] \
        #                 ])*self.accNoiseMag**2
        self.Ex=np.array([[self.dt**5/20, 0, self.dt**4/8, 0,self.dt**3/6, 0], \
                          [0, self.dt**5/20, 0, self.dt**4/8,0, self.dt**3/6], \
                          [self.dt**4/8, 0, self.dt**3/3,0, self.dt**2/2, 0], \
                          [0, self.dt**4/8, 0, self.dt**3/3,0,self.dt**2/2], \
                          [self.dt**3/6, 0, self.dt**2/2, 0, self.dt, 0], \
                          [0, self.dt**3/6, 0, self.dt**2/2,0,self.dt] \
                         ])*self.accNoiseMag**2/3
        self.P=self.Ex
        self.A=np.array([[1,0,self.dt,0,self.dt**2/2,0], \
                         [0,1,0,self.dt,0,self.dt**2/2], \
                         [0,0,1,0,self.dt,0], \
                         [0,0,0,1,0,self.dt], \
                         [0,0,0,0,1,0], \
                         [0,0,0,0,0,1] \
                        ])
        self.B=np.array([[self.dt**2/2], \
                         [self.dt**2/2], \
                         [self.dt], \
                         [self.dt] \
                        ])
        self.C=np.array([[1,0,0,0,0,0], \
                         [0,1,0,0,0,0] \
                        ])
    def updateState(self,position):
        self.Qestimate=np.dot(self.A,self.Qestimate)#+self.B*self.u
        
        self.P=np.dot(np.dot(self.A,self.P),np.transpose(self.A))+self.Ex
        K=np.dot(np.dot(self.P,np.transpose(self.C)),inv(np.dot(np.dot(self.C,self.P),np.transpose(self.C))+self.Ez))
        if position:
            QposMeasurment=np.array([[position[0]],[position[1]]])  
            self.Qestimate = self.Qestimate+np.dot(K,QposMeasurment-np.dot(self.C,self.Qestimate))
        self.P=np.dot(np.eye(6)-np.dot(K,self.C),self.P)
        self.velocity=(self.Qestimate[2][0],self.Qestimate[3][0])
        if not position:
            self.position=(self.Qestimate[0][0],self.Qestimate[1][0])   
        else:
             self.position=position





