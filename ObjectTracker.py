"""Provides ObjectTracker class which implements Kalman filter"""
import numpy as np
from numpy.linalg import inv
from math import atan2
from Resources import ResKalmanFilter

class ObjectTracker:
    """Tracks object using Kalman filter"""
    def __init__(self, type, id, position, velocity, accel=(0,0,0,0)):
        self.type = type
        self.id = id
        self.position = position
        self.velocity = velocity
        self.direction = atan2(position[3] - position[1],position[2] - position[0])
        self.Q = np.array([[position[0]],[position[1]],[velocity[0]],[velocity[1]],[accel[0]],[accel[1]]])
        self.Q2 = np.array([[position[2]],[position[3]],[velocity[2]],[velocity[3]],[accel[2]],[accel[3]]])
        self.Qestimate = self.Q
        self.Qestimate2 = self.Q2
        self.accNoiseMag = ResKalmanFilter.accNoiseMag
        self.dt = ResKalmanFilter.dt
        self.u = ResKalmanFilter.u
        self.measurementNoiseX = ResKalmanFilter.measurementNoiseX
        self.measurementNoiseY = ResKalmanFilter.measurementNoiseY
        self.detected = True
        self.enabled = True
        self.last_seen = 0
        self.lost_frames = 0
        self.Ez = np.array([[self.measurementNoiseX, 0],[0, self.measurementNoiseY]])

        self.Ex = np.array([[self.dt ** 5 / 20, 0, self.dt ** 4 / 8, 0,self.dt ** 3 / 6, 0], \
                          [0, self.dt ** 5 / 20, 0, self.dt ** 4 / 8,0, self.dt ** 3 / 6], \
                          [self.dt ** 4 / 8, 0, self.dt ** 3 / 3,0, self.dt ** 2 / 2, 0], \
                          [0, self.dt ** 4 / 8, 0, self.dt ** 3 / 3,0,self.dt ** 2 / 2], \
                          [self.dt ** 3 / 6, 0, self.dt ** 2 / 2, 0, self.dt, 0], \
                          [0, self.dt ** 3 / 6, 0, self.dt ** 2 / 2,0,self.dt]]) * self.accNoiseMag ** 2 / 3
        self.P = self.Ex
        self.P2 = self.Ex
        self.A = np.array([[1,0,self.dt,0,self.dt ** 2 / 2,0], \
                         [0,1,0,self.dt,0,self.dt ** 2 / 2], \
                         [0,0,1,0,self.dt,0], \
                         [0,0,0,1,0,self.dt], \
                         [0,0,0,0,1,0], \
                         [0,0,0,0,0,1]])
        self.B = np.array([[self.dt ** 2 / 2], \
                         [self.dt ** 2 / 2], \
                         [self.dt], \
                         [self.dt]])
        self.C = np.array([[1,0,0,0,0,0], \
                         [0,1,0,0,0,0]])

    def updateState(self,position):
        self.Qestimate = np.dot(self.A,self.Qestimate)#+self.B*self.u
        self.Qestimate2 = np.dot(self.A,self.Qestimate2)#+self.B*self.u
        
        self.P2 = np.dot(np.dot(self.A,self.P2),np.transpose(self.A)) + self.Ex
        self.P = np.dot(np.dot(self.A,self.P),np.transpose(self.A)) + self.Ex
        K = np.dot(np.dot(self.P,np.transpose(self.C)),inv(np.dot(np.dot(self.C,self.P),np.transpose(self.C)) + self.Ez))
        K2 = np.dot(np.dot(self.P2,np.transpose(self.C)),inv(np.dot(np.dot(self.C,self.P2),np.transpose(self.C)) + self.Ez))
        if position:
            QposMeasurment = np.array([[position[0]],[position[1]]])
            QposMeasurment2 = np.array([[position[2]],[position[3]]])    
            self.Qestimate = self.Qestimate + np.dot(K,QposMeasurment - np.dot(self.C,self.Qestimate))
            self.Qestimate2 = self.Qestimate2 + np.dot(K2,QposMeasurment2 - np.dot(self.C,self.Qestimate2))
        self.P = np.dot(np.eye(6) - np.dot(K,self.C),self.P)
        self.P2 = np.dot(np.eye(6) - np.dot(K2,self.C),self.P2)
        self.velocity = (self.Qestimate[2][0],self.Qestimate[3][0])
        if not position:
            self.position = (self.Qestimate[0][0],self.Qestimate[1][0],self.Qestimate2[0][0],self.Qestimate2[1][0])
        else:
             self.position = position
        self.direction = atan2(self.position[3] - self.position[1],self.position[2] - self.position[0])





