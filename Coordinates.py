# This file contains the definitions and methods for the coordinate classes used in the modeling,
# including rotating coordinate frames and transforming between one type and the other

from abc import ABCMeta, abstractmethod
import numpy as np

class Coordinates(object):
    """
    Coordinate class, for storing information about 3-dimensional position

    Attributes:
         system: A string indicating the coordinate system used to store information
         q: A dictionary of floats containing the position information
    """

    __metaclass__ = ABCMeta
    q_1 = 'foo'
    q_2 = 'bar'
    q_3 = 'huh'
    def __init__(self, system, q):
        self.system = system
        self.q = {q_1 : q[0], q_2 : q[1], q_3 : q[2]}
        
    @abstractmethod
    def transform(self, to):
        """ 
        Transforms the coordinate vector q into a different system

        input:
             to - coordinate system to convert to
        output:
             out - a Coordinate object, of type 'to'
        """
        pass

    def rotate(self, inc):
        """
        Inclines a coordinate system with respect to itself,
        and returns the coordinate object containing the new position

        input:
             inc - the angle by which the system is inclined, in radians
        output:
             rot - a Coordinate object of the input coordinates in the rotated frame
        """
        
        rot = self
        if rot.system != "cartesian":
            rot = rot.transform("cartesian")

        # Rotation matrix of the first (and only, for this case) Euler angle
        euler = np.array([[1, 0, 0],[0,np.cos(inc), np.sin(inc)],[0,-np.sin(inc), np.cos(inc)]])

        rot = np.dot(rot, euler)
        
        if rot.system != self.system:
            rot = rot.transform(self.system)

        return rot

    

class Spherical(Coordinates):
    q_1 = 'r'
    q_2 = 'theta'
    q_3 = 'phi'

    def transform(self, to):
        if to == self.system:
            print "This transformation is invalid"

            return self
        
        Q = [0, 0, 0]
        r = self.q['r']
        theta = self.q['theta']
        phi = self.q['phi']

        if to == "cartesian":
            Q[0] = r * np.sin(theta) * np.cos(phi)
            Q[1] = r * np.sin(theta) * np.sin(phi)
            Q[2] = r * np.cos(theta)

            out = Cartesian(to, Q)

        if to == "cylindrical":
            Q[0] = r * np.sin(theta)
            Q[1] = phi
            Q[2] = r * np.cos(theta)

            out = Cylindrical(to, Q)

        return out
    

class Cartesian(Coordinates):
    q_1 = 'x'
    q_2 = 'y'
    q_3 = 'z'

    def transform(self, to):
        if to == self.system:
            print "This transformation is invalid"

            return self
        
        Q = [0, 0, 0]
        x = self.q['x']
        y = self.q['y']
        z = self.q['z']
        
        if to == "spherical":
            Q[0] = np.sqrt(x**2 + y**2 + z**2)
            Q[1] = np.arccos(z / Q[0])
            Q[2] = np.arctan2(y, x)

            out = Spherical(to, Q)

        if to == "cylindrical":
            Q[0] = np.sqrt(x**2 + y**2)
            Q[1] = np.arctan2(y, x)
            Q[2] = z

            out = Cylindrical(to, Q)

        return out
    

class Cylindrical(Coordinates):
    q_1 = 's'
    q_2 = 'phi'
    q_3 = 'z'
    
    def transform(self, to):
        if to == self.system:
            print "This transformation is invalid"

            return self
        
        Q = [0, 0, 0]
        s = self.q['s']
        phi = self.q['phi']
        z = self.q['z']

        if to == "spherical":
            Q[0] = np.sqrt(s**2 + z**2)
            Q[1] = np.arctan(s/z)
            Q[2] = phi

            out = Spherical(to, Q)

        if to == "cartesian":
            Q[0] = s * np.cos(phi)
            Q[1] = s * np.sin(phi)
            Q[2] = z

            out = Cartesian(to, Q)

        return out
    
