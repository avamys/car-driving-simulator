import numpy as np
from OpenGL.GL import *
from PIL import Image
import random
import math

class Terrain:
    def __init__(self, size, resolution):
        self.size = size
        # Reduce resolution significantly
        self.resolution = resolution // 4
        self.scale = size / self.resolution
        self.heights = self.generate_height_map()
        # Create display list for better performance
        self.display_list = self.create_display_list()
        
    def generate_height_map(self):
        heights = np.zeros((self.resolution, self.resolution))
        center = self.resolution // 2
        
        # Simplified terrain generation
        for y in range(self.resolution):
            for x in range(self.resolution):
                dx = (x - center) / self.resolution
                dy = (y - center) / self.resolution
                dist = math.sqrt(dx*dx + dy*dy)
                
                # Simpler height calculation
                height = (math.sin(dx * 3) + math.cos(dy * 3)) * 0.5
                height *= (1 - min(1, dist * 2))
                
                # Flatten center more aggressively
                if dist < 0.3:
                    height *= dist * 3.3
                    
                heights[y, x] = height
                
        return heights
    
    def create_display_list(self):
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)
        
        # Draw ground
        glBegin(GL_TRIANGLES)
        
        # Step size for reduced vertex count
        step = 2
        for y in range(0, self.resolution - 1, step):
            for x in range(0, self.resolution - 1, step):
                # Calculate positions
                x1 = (x - self.resolution/2) * self.scale
                x2 = ((x + step) - self.resolution/2) * self.scale
                y1 = (y - self.resolution/2) * self.scale
                y2 = ((y + step) - self.resolution/2) * self.scale
                
                h11 = self.heights[y, x]
                h21 = self.heights[y, min(x + step, self.resolution-1)]
                h12 = self.heights[min(y + step, self.resolution-1), x]
                h22 = self.heights[min(y + step, self.resolution-1), min(x + step, self.resolution-1)]
                
                # Set color based on position from center
                dist = math.sqrt(x*x + y*y) / self.resolution
                if dist < 0.3:
                    glColor3f(0.2, 0.6, 0.1)  # Darker green for center
                else:
                    glColor3f(0.3, 0.7, 0.2)  # Lighter green for outskirts
                
                # First triangle
                glVertex3f(x1, y1, h11)
                glVertex3f(x2, y1, h21)
                glVertex3f(x1, y2, h12)
                
                # Second triangle
                glVertex3f(x2, y1, h21)
                glVertex3f(x2, y2, h22)
                glVertex3f(x1, y2, h12)
                
        glEnd()
        glEndList()
        
        return display_list
    
    def draw(self):
        glCallList(self.display_list) 