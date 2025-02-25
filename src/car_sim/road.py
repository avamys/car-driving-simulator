from OpenGL.GL import *
import numpy as np
import math

class Road:
    def __init__(self, world):
        self.world = world
        self.width = 8.0
        
        # Road types with properties
        self.road_types = {
            'ASPHALT': {'color': (0.2, 0.2, 0.2), 'friction': 1.0},
            'DIRT': {'color': (0.6, 0.4, 0.2), 'friction': 0.7},
            'GRAVEL': {'color': (0.5, 0.5, 0.5), 'friction': 0.8}
        }
        
        # Road network
        self.points = self.generate_road_points()
        self.segments = self.create_road_segments()
        self.display_list = None  # Initialize as None
    
    def generate_road_points(self):
        points = []
        # Create a more interesting road layout
        segments = 32  # Number of segments in the main loop
        
        # Main loop
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            # Create an interesting shape using multiple sine waves
            radius = 100 + math.sin(angle * 3) * 20 + math.cos(angle * 2) * 15
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            points.append((x, y))
        
        # Add some additional connecting roads
        # Cross road 1
        points.extend([
            (-150, 0), (150, 0),
            (0, -150), (0, 150)
        ])
        
        return points
    
    def create_road_segments(self):
        segments = []
        # Connect main loop points
        for i in range(len(self.points) - 1):
            segments.append((i, i + 1))
        # Close the loop
        segments.append((len(self.points) - 1, 0))
        return segments
    
    def draw(self):
        # Create or recreate display list every frame
        if self.display_list is not None:
            glDeleteLists(self.display_list, 1)
        
        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)
        
        # Draw road surface
        glColor3f(0.2, 0.2, 0.2)  # Asphalt color
        
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            
            # Get terrain heights
            h1 = self.world.get_height_at(p1[0], p1[1]) + 0.1
            h2 = self.world.get_height_at(p2[0], p2[1]) + 0.1
            
            # Calculate road edges
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                nx = -dy/length * self.width/2
                ny = dx/length * self.width/2
                
                # Draw road segment
                glBegin(GL_QUADS)
                glVertex3f(p1[0] - nx, p1[1] - ny, h1)
                glVertex3f(p1[0] + nx, p1[1] + ny, h1)
                glVertex3f(p2[0] + nx, p2[1] + ny, h2)
                glVertex3f(p2[0] - nx, p2[1] - ny, h2)
                glEnd()
                
                # Draw road markings
                glColor3f(1.0, 1.0, 1.0)  # White for markings
                glBegin(GL_LINES)
                glVertex3f(p1[0], p1[1], h1 + 0.01)  # Slightly above road
                glVertex3f(p2[0], p2[1], h2 + 0.01)
                glEnd()
                glColor3f(0.2, 0.2, 0.2)  # Back to asphalt color
        
        glEndList()
        glCallList(self.display_list)
    
    def get_road_type_at(self, x, y):
        # Find nearest road segment and return its type
        min_dist = float('inf')
        road_type = 'ASPHALT'
        
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            
            # Calculate distance to road segment
            dist = self.point_to_segment_distance(x, y, p1[0], p1[1], p2[0], p2[1])
            if dist < min_dist:
                min_dist = dist
        
        return road_type if min_dist < self.width/2 else None
    
    def point_to_segment_distance(self, x, y, x1, y1, x2, y2):
        # Calculate distance from point to line segment
        A = x - x1
        B = y - y1
        C = x2 - x1
        D = y2 - y1
        
        dot = A * C + B * D
        len_sq = C * C + D * D
        
        if len_sq == 0:
            return math.sqrt((x - x1)**2 + (y - y1)**2)
            
        param = dot / len_sq
        
        if param < 0:
            return math.sqrt((x - x1)**2 + (y - y1)**2)
        elif param > 1:
            return math.sqrt((x - x2)**2 + (y - y2)**2)
        
        x_proj = x1 + param * C
        y_proj = y1 + param * D
        return math.sqrt((x - x_proj)**2 + (y - y_proj)**2) 