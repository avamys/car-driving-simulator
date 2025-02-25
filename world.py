from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from terrain import Terrain
from skybox import Skybox
from road import Road
from vegetation import TreeSystem

class World:
    def __init__(self):
        # World dimensions and settings
        self.size = 2000.0
        self.chunk_size = 100.0
        self.view_distance = 500.0
        
        # Terrain variety
        self.terrain_types = {
            'GRASS': {'color': (0.2, 0.8, 0.2), 'height_mod': 1.0},
            'FOREST': {'color': (0.1, 0.6, 0.1), 'height_mod': 1.2},
            'DESERT': {'color': (0.8, 0.7, 0.2), 'height_mod': 0.7},
            'MOUNTAIN': {'color': (0.6, 0.6, 0.6), 'height_mod': 2.0},
            'SNOW': {'color': (0.9, 0.9, 0.9), 'height_mod': 1.5}
        }
        
        # Setup lighting first
        self.setup_lighting()
        
        # Initialize all components
        self.terrain = Terrain(self)
        self.road = Road(self)
        self.vegetation = TreeSystem(self)
        self.skybox = Skybox()
        
        # Generate base terrain after all components are initialized
        self.generate_base_terrain()
        
    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Main directional light (sun)
        glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 2.0, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 0.9, 1.0))
        
        # Global ambient light
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        
        # Material properties
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.2, 0.2, 0.2, 1.0))
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 8.0)

    def generate_base_terrain(self):
        # Generate initial chunks around origin
        chunk_radius = 5  # Number of chunks in each direction
        for x in range(-chunk_radius, chunk_radius + 1):
            for z in range(-chunk_radius, chunk_radius + 1):
                chunk_x = x * self.chunk_size
                chunk_z = z * self.chunk_size
                
                # Generate terrain for this chunk
                chunk_mesh = self.terrain.generate_chunk(chunk_x, chunk_z)
                self.terrain.display_lists[(chunk_x, chunk_z)] = chunk_mesh
                
                # Generate vegetation for this chunk
                biome = self.terrain.get_biome(chunk_x, chunk_z)
                self.vegetation.generate_chunk_vegetation(chunk_x, chunk_z, biome)

    def update(self, camera_pos):
        # Get camera chunk position
        camera_chunk_x = int(camera_pos[0] / self.chunk_size) * self.chunk_size
        camera_chunk_z = int(camera_pos[1] / self.chunk_size) * self.chunk_size
        
        # Load/unload chunks based on distance
        chunk_radius = int(self.view_distance / self.chunk_size)
        for x in range(-chunk_radius, chunk_radius + 1):
            for z in range(-chunk_radius, chunk_radius + 1):
                chunk_x = camera_chunk_x + x * self.chunk_size
                chunk_z = camera_chunk_z + z * self.chunk_size
                
                # Check if chunk needs to be generated
                if (chunk_x, chunk_z) not in self.terrain.display_lists:
                    chunk_mesh = self.terrain.generate_chunk(chunk_x, chunk_z)
                    self.terrain.display_lists[(chunk_x, chunk_z)] = chunk_mesh
                    
                    # Generate vegetation for new chunk
                    biome = self.terrain.get_biome(chunk_x, chunk_z)
                    self.vegetation.generate_chunk_vegetation(chunk_x, chunk_z, biome)

    def draw(self):
        # Draw skybox first
        glDisable(GL_LIGHTING)
        self.skybox.draw()
        
        # Enable lighting for terrain and objects
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        
        # Draw terrain chunks
        for chunk_pos, display_list in self.terrain.display_lists.items():
            glPushMatrix()
            glTranslatef(chunk_pos[0], chunk_pos[1], 0)  # Move to chunk position
            glCallList(display_list)
            glPopMatrix()
        
        # Draw roads
        self.road.draw()
        
        # Draw vegetation
        self.vegetation.draw()

    def get_height_at(self, x, z):
        # Get the height of terrain at any world position
        chunk_x = int(x / self.chunk_size) * self.chunk_size
        chunk_z = int(z / self.chunk_size) * self.chunk_size
        
        # Ensure the chunk exists
        if (chunk_x, chunk_z) not in self.terrain.display_lists:
            chunk_mesh = self.terrain.generate_chunk(chunk_x, chunk_z)
            self.terrain.display_lists[(chunk_x, chunk_z)] = chunk_mesh
        
        # Get local coordinates within chunk
        local_x = x - chunk_x
        local_z = z - chunk_z
        
        return self.terrain.get_height_at(local_x, local_z, chunk_x, chunk_z) 