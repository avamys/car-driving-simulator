from OpenGL.GL import *
import numpy as np
from PIL import Image
import math

class Skybox:
    def __init__(self):
        self.size = 1000.0
        self.display_list = self.create_display_list()
        
    def create_display_list(self):
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)
        
        # Draw simplified sky dome
        segments = 16  # Reduced segments
        rings = 8     # Reduced rings
        radius = self.size
        
        glBegin(GL_TRIANGLE_STRIP)
        
        for ring in range(rings):
            ring_angle1 = math.pi * ring / (2 * rings)
            ring_angle2 = math.pi * (ring + 1) / (2 * rings)
            
            for segment in range(segments + 1):
                angle = 2 * math.pi * segment / segments
                
                # Calculate positions for two vertices
                for ring_angle in [ring_angle1, ring_angle2]:
                    height = radius * math.sin(ring_angle)
                    curr_radius = radius * math.cos(ring_angle)
                    x = curr_radius * math.cos(angle)
                    y = curr_radius * math.sin(angle)
                    
                    # Simplified color calculation
                    height_factor = math.sin(ring_angle)
                    glColor3f(0.4 + height_factor * 0.3,
                            0.6 + height_factor * 0.2,
                            0.9 + height_factor * 0.1)
                    glVertex3f(x, y, height)
                    
        glEnd()
        glEndList()
        
        return display_list
        
    def draw(self):
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glDepthMask(GL_FALSE)
        
        glCallList(self.display_list)
        
        glDepthMask(GL_TRUE)
        glEnable(GL_LIGHTING)
        glPopMatrix() 