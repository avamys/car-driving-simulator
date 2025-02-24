from OpenGL.GL import *
import numpy as np
import random

class TreeSystem:
    def __init__(self, density):
        self.density = density
        self.trees = self.generate_trees()
        
    def generate_trees(self):
        trees = []
        # Reduce number of trees and keep them away from the road
        area = 500 * 500  # Reduced area
        num_trees = int(area * self.density)
        
        for _ in range(num_trees):
            # Generate trees in four quadrants, avoiding the center
            quadrant = random.randint(0, 3)
            if quadrant == 0:  # Top-right
                x = random.uniform(50, 200)
                z = random.uniform(50, 200)
            elif quadrant == 1:  # Top-left
                x = random.uniform(-200, -50)
                z = random.uniform(50, 200)
            elif quadrant == 2:  # Bottom-left
                x = random.uniform(-200, -50)
                z = random.uniform(-200, -50)
            else:  # Bottom-right
                x = random.uniform(50, 200)
                z = random.uniform(-200, -50)
            
            height = random.uniform(8, 12)
            trees.append((x, z, height))
            
        return trees
    
    def draw(self):
        # Simplified tree rendering
        for x, z, height in self.trees:
            glPushMatrix()
            glTranslatef(x, z, 0)
            
            # Draw trunk (brown cylinder)
            glColor3f(0.4, 0.2, 0.0)
            self.draw_simple_cylinder(0.5, height * 0.3)
            
            # Draw foliage (green cone)
            glTranslatef(0, 0, height * 0.3)
            glColor3f(0.0, 0.4, 0.0)
            self.draw_simple_cone(height * 0.4, height * 0.7)
            
            glPopMatrix()
    
    def draw_simple_cylinder(self, radius, height):
        # Simplified cylinder with fewer segments
        segments = 6
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, height)
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            glVertex3f(radius * np.cos(angle), radius * np.sin(angle), 0)
        glEnd()
    
    def draw_simple_cone(self, radius, height):
        # Simplified cone with fewer segments
        segments = 6
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, height)
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            glVertex3f(radius * np.cos(angle), radius * np.sin(angle), 0)
        glEnd() 