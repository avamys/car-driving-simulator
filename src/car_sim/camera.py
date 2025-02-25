from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Camera:
    def __init__(self, car):
        self.car = car
        self.distance = 6.0  # Distance behind car
        self.height = 2.5    # Height above car
        self.smoothing = 0.15
        self.current_pos = [0, 0, 0]
        self.target_angle = 0  # Added to track car's direction
        
    def update(self):
        # Smoothly follow car's angle
        angle_diff = (self.car.angle - self.target_angle)
        # Normalize angle difference to [-pi, pi]
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        # Update camera angle with smooth follow
        self.target_angle += angle_diff * self.smoothing * 2.0
        
        # Calculate camera position based on car's position and direction
        target_x = self.car.x - self.distance * math.cos(self.target_angle)
        target_y = self.car.y - self.distance * math.sin(self.target_angle)
        target_z = self.car.z + self.height
        
        # Smooth camera movement
        self.current_pos[0] += (target_x - self.current_pos[0]) * self.smoothing
        self.current_pos[1] += (target_y - self.current_pos[1]) * self.smoothing
        self.current_pos[2] += (target_z - self.current_pos[2]) * self.smoothing
        
        # Look slightly ahead of the car
        look_ahead = 3.0
        look_x = self.car.x + look_ahead * math.cos(self.car.angle)
        look_y = self.car.y + look_ahead * math.sin(self.car.angle)
        look_z = self.car.z + 1.0
        
        gluLookAt(
            self.current_pos[0], self.current_pos[1], self.current_pos[2],
            look_x, look_y, look_z,
            0, 0, 1
        ) 