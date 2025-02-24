from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from terrain import Terrain
from skybox import Skybox
from road import Road
from vegetation import TreeSystem

class World:
    def __init__(self):
        # Initialize with better scale
        self.terrain = Terrain(size=400, resolution=100)  # More detailed terrain
        self.skybox = Skybox()
        self.road_system = Road()
        self.trees = TreeSystem(density=0.0001)  # More trees
        
        # Enhanced lighting
        self.setup_lighting()
        
    def setup_lighting(self):
        # Directional light (sunlight)
        glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 2.0, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 0.9, 1.0))
        
        # Global ambient light
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    
    def draw(self):
        # Draw in order of distance (skybox first, then terrain, etc.)
        self.skybox.draw()
        
        # Enable depth testing for the rest
        glEnable(GL_DEPTH_TEST)
        
        self.terrain.draw()
        self.road_system.draw()
        self.trees.draw() 