import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from car import Car
from world import World
from camera import Camera

class CarSimulator:
    def __init__(self):
        pygame.init()
        pygame.font.init()  # Initialize font system
        display = (1024, 768)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Car Simulator")
        
        # Create and store fonts
        self.font = pygame.font.Font(None, 64)
        self.gear_texture = None
        self.speed_texture = None  # New texture for speed display
        
        # Initialize OpenGL settings
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)
        
        # Set up perspective with larger far plane
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0]/display[1]), 0.1, 2000.0)  # Increased far plane
        
        # Set up better lighting
        glLightfv(GL_LIGHT0, GL_POSITION, (500.0, 500.0, 1000.0, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
        
        # Set global ambient light
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize world, car and camera
        self.world = World()
        self.car = Car(x=0, y=0, z=0)
        self.camera = Camera(self.car)
        
        # Add key press tracking
        self.last_gear_shift_time = 0
        self.gear_shift_cooldown = 0.3  # Time required between gear shifts
        self.key_states = {
            pygame.K_a: False,  # Track 'A' key state
            pygame.K_d: False   # Track 'D' key state
        }
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        
        # Steering
        if keys[pygame.K_LEFT]:
            self.car.apply_steering(-1)
        elif keys[pygame.K_RIGHT]:
            self.car.apply_steering(1)
        else:
            self.car.apply_steering(0)
            
        # Throttle and brake
        if keys[pygame.K_UP]:
            self.car.apply_throttle(1)
            self.car.apply_brake(0)
        elif keys[pygame.K_DOWN]:
            self.car.apply_throttle(0)
            self.car.apply_brake(1)
        else:
            self.car.apply_throttle(0)
            self.car.apply_brake(0)
            
        # Gear shifting with cooldown and key press detection
        if current_time - self.last_gear_shift_time >= self.gear_shift_cooldown:
            # Check for new key presses
            if keys[pygame.K_a] and not self.key_states[pygame.K_a]:  # Shift down
                if self.car.shift_down():  # Only shift if the method returns True
                    self.last_gear_shift_time = current_time
            elif keys[pygame.K_d] and not self.key_states[pygame.K_d]:  # Shift up
                if self.car.shift_up():    # Only shift if the method returns True
                    self.last_gear_shift_time = current_time
        
        # Update key states
        self.key_states[pygame.K_a] = keys[pygame.K_a]
        self.key_states[pygame.K_d] = keys[pygame.K_d]
            
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Update camera position
        self.camera.update()
        
        # Draw world and car
        self.world.draw()
        self.car.draw()
        
        # Switch to 2D mode for HUD
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 1024, 768, 0, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Disable lighting and depth test for HUD
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        
        # Draw all HUD elements
        self.draw_hud()
        
        # Restore 3D mode
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
        pygame.display.flip()

    def draw_hud(self):
        # Setup for 2D rendering once for all HUD elements
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Draw gear indicator
        self.draw_gear_indicator()
        # Draw speed indicator
        self.draw_speed_indicator()
        
        # Cleanup once after all HUD elements
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

    def draw_gear_indicator(self):
        # Delete old texture if it exists
        if self.gear_texture is not None:
            glDeleteTextures([self.gear_texture])
        
        # Create new text surface
        gear_text = f"GEAR: {self.car.current_gear}"
        text_surface = self.font.render(gear_text, True, (255, 255, 255))  # Removed background color
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width = text_surface.get_width()
        height = text_surface.get_height()
        
        # Generate and setup texture
        self.gear_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.gear_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Draw textured quad
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(20, 20)
        glTexCoord2f(1, 1); glVertex2f(20 + width, 20)
        glTexCoord2f(1, 0); glVertex2f(20 + width, 20 + height)
        glTexCoord2f(0, 0); glVertex2f(20, 20 + height)
        glEnd()

    def draw_speed_indicator(self):
        # Delete old texture if it exists
        if self.speed_texture is not None:
            glDeleteTextures([self.speed_texture])
        
        # Convert velocity to km/h and format text
        speed_kmh = abs(self.car.velocity * 3.6)  # Convert m/s to km/h
        speed_text = f"{speed_kmh:.0f} km/h"
        
        # Create new text surface
        text_surface = self.font.render(speed_text, True, (255, 255, 255))  # Removed background color
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width = text_surface.get_width()
        height = text_surface.get_height()
        
        # Generate and setup texture
        self.speed_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.speed_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Draw textured quad (positioned below gear indicator)
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(20, 80)  # Adjusted position
        glTexCoord2f(1, 1); glVertex2f(20 + width, 80)
        glTexCoord2f(1, 0); glVertex2f(20 + width, 80 + height)
        glTexCoord2f(0, 0); glVertex2f(20, 80 + height)
        glEnd()
            
    def run(self):
        while self.running:
            dt = 1/60  # Fixed time step
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            self.handle_input()
            self.car.update(dt)  # Pass the time step to update
            self.render()
            
            # Limit frame rate
            self.clock.tick(60)
            
        pygame.quit()

if __name__ == "__main__":
    simulator = CarSimulator()
    simulator.run() 