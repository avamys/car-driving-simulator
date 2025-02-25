from OpenGL.GL import *
import numpy as np
import random
import math

class TreeSystem:
    def __init__(self, world):
        self.world = world
        self.tree_types = {
            'PINE': {'height': 15, 'width': 5, 'color': (0.1, 0.4, 0.1)},
            'OAK': {'height': 12, 'width': 8, 'color': (0.2, 0.5, 0.2)},
            'PALM': {'height': 18, 'width': 6, 'color': (0.3, 0.6, 0.2)},
            'CACTUS': {'height': 8, 'width': 3, 'color': (0.2, 0.5, 0.2)}
        }
        
        # Vegetation density per biome
        self.density = {
            'GRASS': 0.3,
            'FOREST': 0.8,
            'DESERT': 0.1,
            'MOUNTAIN': 0.2,
            'SNOW': 0.1
        }
        
        # Tree instances per chunk
        self.chunk_trees = {}
        
        # Display list for each tree type
        self.tree_display_lists = self.create_tree_display_lists()
    
    def create_tree_display_lists(self):
        display_lists = {}
        for tree_type, properties in self.tree_types.items():
            display_list = glGenLists(1)
            glNewList(display_list, GL_COMPILE)
            
            height = properties['height']
            width = properties['width']
            color = properties['color']
            
            # Draw trunk
            glColor3f(0.4, 0.2, 0.0)
            self.draw_cylinder(width * 0.2, height * 0.4)
            
            # Draw foliage
            glColor3fv(color)
            glTranslatef(0, 0, height * 0.4)
            if tree_type == 'PINE':
                self.draw_cone(width, height * 0.6)
            elif tree_type == 'CACTUS':
                self.draw_cylinder(width * 0.3, height * 0.6)
            else:
                self.draw_sphere(width * 0.5)
            
            glEndList()
            display_lists[tree_type] = display_list
        
        return display_lists
    
    def get_vegetation_type(self, biome):
        if biome == 'FOREST':
            return random.choice(['PINE', 'OAK'])
        elif biome == 'DESERT':
            return 'CACTUS'
        elif biome == 'SNOW':
            return 'PINE'
        else:
            return 'OAK'
    
    def generate_chunk_vegetation(self, chunk_x, chunk_z, biome):
        if (chunk_x, chunk_z) in self.chunk_trees:
            return
        
        trees = []
        density = self.density[biome]
        
        # Use deterministic random for consistent placement
        random.seed(f"{chunk_x},{chunk_z}")
        
        # Generate vegetation based on biome
        num_trees = int(self.world.chunk_size * self.world.chunk_size * density * 0.001)
        for _ in range(num_trees):
            x = chunk_x + random.random() * self.world.chunk_size
            z = chunk_z + random.random() * self.world.chunk_size
            
            tree_type = self.get_vegetation_type(biome)
            scale = random.uniform(0.8, 1.2)
            trees.append((x, z, tree_type, scale))
        
        self.chunk_trees[(chunk_x, chunk_z)] = trees
    
    def draw(self):
        glEnable(GL_LIGHTING)
        for chunk_pos, trees in self.chunk_trees.items():
            for x, z, tree_type, scale in trees:
                # Get terrain height at tree position
                height = self.world.get_height_at(x, z)
                
                glPushMatrix()
                glTranslatef(x, z, height)  # Place tree on terrain
                glScalef(scale, scale, scale)
                glCallList(self.tree_display_lists[tree_type])
                glPopMatrix()
    
    def draw_cylinder(self, radius, height, segments=8):
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, 0)
            glVertex3f(x, y, height)
        glEnd()
    
    def draw_cone(self, radius, height, segments=8):
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, height)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, 0)
        glEnd()
    
    def draw_sphere(self, radius, segments=8):
        for i in range(segments):
            lat0 = math.pi * (-0.5 + float(i) / segments)
            z0 = math.sin(lat0)
            zr0 = math.cos(lat0)
            
            lat1 = math.pi * (-0.5 + float(i + 1) / segments)
            z1 = math.sin(lat1)
            zr1 = math.cos(lat1)
            
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(segments + 1):
                lng = 2 * math.pi * float(j) / segments
                x = math.cos(lng)
                y = math.sin(lng)
                
                glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
                glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
            glEnd()

class Vegetation:
    def __init__(self, world):
        self.world = world
        self.tree_types = {
            'PINE': {'height': 15, 'width': 5, 'color': (0.1, 0.4, 0.1)},
            'OAK': {'height': 12, 'width': 8, 'color': (0.2, 0.5, 0.2)},
            'PALM': {'height': 18, 'width': 6, 'color': (0.3, 0.6, 0.2)},
            'CACTUS': {'height': 8, 'width': 3, 'color': (0.2, 0.5, 0.2)}
        }
        
        # Vegetation density per biome
        self.density = {
            'GRASS': 0.3,
            'FOREST': 0.8,
            'DESERT': 0.1,
            'MOUNTAIN': 0.2,
            'SNOW': 0.1
        }
        
        # Optimization
        self.instance_buffer = {}
        self.billboard_textures = {}
    
    def generate_vegetation(self, chunk_x, chunk_z, biome):
        vegetation = []
        density = self.density[biome]
        
        # Use deterministic random for consistent placement
        random.seed(f"{chunk_x},{chunk_z}")
        
        # Generate vegetation based on biome
        for _ in range(int(density * 100)):
            x = chunk_x + random.random() * self.world.chunk_size
            z = chunk_z + random.random() * self.world.chunk_size
            
            # Choose appropriate vegetation type
            veg_type = self.get_vegetation_type(biome)
            vegetation.append((x, z, veg_type))
        
        return vegetation 