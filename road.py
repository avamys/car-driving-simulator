from OpenGL.GL import *
import numpy as np
import math

class Road:
    def __init__(self):
        self.width = 8.0
        self.points = self.generate_road_path()
        
    def generate_road_path(self):
        points = []
        # Simpler oval track with fewer segments
        segments = 16  # Reduced from 100
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = math.cos(angle) * 100
            y = math.sin(angle) * 150
            points.append((x, y))
        return points
    
    def draw(self):
        # Simplified road rendering
        glColor3f(0.2, 0.2, 0.2)  # Dark gray
        
        # Draw road surface
        glBegin(GL_QUAD_STRIP)
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            
            # Calculate road edges
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = math.sqrt(dx*dx + dy*dy)
            nx = -dy/length * self.width/2
            ny = dx/length * self.width/2
            
            glVertex3f(p1[0] - nx, p1[1] - ny, 0.1)
            glVertex3f(p1[0] + nx, p1[1] + ny, 0.1)
        glEnd()
        
        # Draw center line
        glColor3f(1.0, 1.0, 1.0)  # White
        glBegin(GL_LINES)
        for i in range(0, len(self.points), 2):  # Draw dashed line
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            glVertex3f(p1[0], p1[1], 0.15)
            glVertex3f(p2[0], p2[1], 0.15)
        glEnd() 