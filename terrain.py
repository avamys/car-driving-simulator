import numpy as np
from OpenGL.GL import *
from PIL import Image
import random
import math

class Terrain:
    def __init__(self, world):
        self.world = world
        
        # Terrain generation parameters
        self.height_scale = 20.0
        self.detail_scale = 10.0
        self.biome_scale = 200.0
        self.base_height = 0.0
        
        # Optimization
        self.display_lists = {}
        self.vertex_buffers = {}
        
        self.size = world.size
        # Make resolution an integer
        self.resolution = 25  # Fixed resolution per chunk
        self.scale = world.chunk_size / float(self.resolution)
        
        # Terrain generation seeds
        self.seed1 = random.randint(0, 10000)
        self.seed2 = random.randint(0, 10000)
    
    def improved_noise(self, x, y, seed):
        # Simple but effective noise function
        x = x * 0.1 + seed
        y = y * 0.1 + seed
        
        # Get integer and fractional parts
        x_int = int(x)
        y_int = int(y)
        x_frac = x - x_int
        y_frac = y - y_int
        
        # Smooth interpolation
        u = x_frac * x_frac * (3 - 2 * x_frac)
        v = y_frac * y_frac * (3 - 2 * y_frac)
        
        # Generate random heights for corners
        def get_random(a, b):
            return (math.sin(a * 12.9898 + b * 78.233) * 43758.5453123) % 1.0
        
        # Get corner values
        a = get_random(x_int, y_int)
        b = get_random(x_int + 1, y_int)
        c = get_random(x_int, y_int + 1)
        d = get_random(x_int + 1, y_int + 1)
        
        # Interpolate
        value = a * (1 - u) * (1 - v) + b * u * (1 - v) + c * (1 - u) * v + d * u * v
        return value

    def get_biome(self, x, z):
        # Determine biome based on height and position
        value = self.improved_noise(x * 0.005, z * 0.005, self.seed2)
        height = self.improved_noise(x * 0.02, z * 0.02, self.seed1)
        
        if height > 0.7:
            return 'MOUNTAIN'
        elif height > 0.6:
            return 'SNOW' if value > 0.6 else 'FOREST'
        elif height > 0.4:
            return 'FOREST' if value > 0.5 else 'GRASS'
        elif height > 0.2:
            return 'GRASS'
        else:
            return 'DESERT'

    def generate_chunk(self, chunk_x, chunk_z):
        vertices = []
        colors = []
        normals = []
        
        # Generate terrain with multiple frequencies
        for x in range(self.resolution + 1):
            for z in range(self.resolution + 1):
                # Calculate world position for noise
                world_x = chunk_x + x * (self.world.chunk_size / self.resolution)
                world_z = chunk_z + z * (self.world.chunk_size / self.resolution)
                
                # Generate height using multiple frequencies
                height = (
                    self.improved_noise(world_x * 0.02, world_z * 0.02, self.seed1) * 1.0 +
                    self.improved_noise(world_x * 0.04, world_z * 0.04, self.seed1) * 0.5 +
                    self.improved_noise(world_x * 0.08, world_z * 0.08, self.seed1) * 0.25
                ) * self.height_scale
                
                # Get biome and adjust height
                biome = self.get_biome(world_x, world_z)
                height *= self.world.terrain_types[biome]['height_mod']
                color = self.world.terrain_types[biome]['color']
                
                # Use local coordinates for vertices
                local_x = x * (self.world.chunk_size / self.resolution)
                local_z = z * (self.world.chunk_size / self.resolution)
                
                vertices.append((local_x, local_z, height))
                colors.append(color)
                
                # Calculate normal
                if x > 0 and z > 0:
                    prev_x = vertices[-2][2] - height
                    prev_z = vertices[-self.resolution-1][2] - height
                    normal = (prev_x, 1.0, prev_z)  # Changed normal calculation
                    length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
                    normals.append((normal[0]/length, normal[1]/length, normal[2]/length))
                else:
                    normals.append((0, 1, 0))
        
        return self.create_optimized_mesh(vertices, colors, normals)

    def create_optimized_mesh(self, vertices, colors, normals):
        display_list = glGenLists(1)
        glNewList(display_list, GL_COMPILE)
        
        glBegin(GL_TRIANGLES)
        for i in range(self.resolution):
            for j in range(self.resolution):
                idx = i * (self.resolution + 1) + j
                
                # Calculate indices for the two triangles
                v1 = idx
                v2 = idx + 1
                v3 = idx + self.resolution + 1
                v4 = idx + self.resolution + 2
                
                # First triangle
                glNormal3fv(normals[v1])
                glColor3fv(colors[v1])
                glVertex3fv(vertices[v1])
                
                glNormal3fv(normals[v2])
                glColor3fv(colors[v2])
                glVertex3fv(vertices[v2])
                
                glNormal3fv(normals[v3])
                glColor3fv(colors[v3])
                glVertex3fv(vertices[v3])
                
                # Second triangle
                glNormal3fv(normals[v2])
                glColor3fv(colors[v2])
                glVertex3fv(vertices[v2])
                
                glNormal3fv(normals[v4])
                glColor3fv(colors[v4])
                glVertex3fv(vertices[v4])
                
                glNormal3fv(normals[v3])
                glColor3fv(colors[v3])
                glVertex3fv(vertices[v3])
        
        glEnd()
        glEndList()
        
        return display_list

    def draw(self):
        glCallList(self.display_list)

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

    def get_height_at(self, local_x, local_z, chunk_x, chunk_z):
        # Convert world coordinates to height calculation
        world_x = chunk_x + local_x
        world_z = chunk_z + local_z
        
        # Use the same noise function as in generation
        height = (
            self.improved_noise(world_x * 0.02, world_z * 0.02, self.seed1) * 1.0 +
            self.improved_noise(world_x * 0.04, world_z * 0.04, self.seed1) * 0.5 +
            self.improved_noise(world_x * 0.08, world_z * 0.08, self.seed1) * 0.25
        ) * self.height_scale
        
        # Add base height to lift terrain
        height += self.base_height
        
        # Apply biome modification
        biome = self.get_biome(world_x, world_z)
        height *= self.world.terrain_types[biome]['height_mod']
        
        return height 