import pygame
from OpenGL.GL import *
import math

class Car:
    def __init__(self, x, y, z, world):
        # Position and orientation
        self.x = x
        self.y = y
        self.z = z
        self.angle = 0
        self.velocity = 0
        self.angular_velocity = 0
        
        # Store world reference
        self.world = world
        
        # Basic car properties
        self.mass = 1400  # kg
        self.wheel_base = 2.8  # meters
        self.steering_angle = 0
        self.max_steering_angle = math.pi / 6.5  # Reduced maximum steering angle
        self.steering_input = 0
        
        # Steering properties - adjusted for more natural turning
        self.steering_speed = 2.5        # Slightly reduced for less sharp response
        self.steering_return_speed = 6.0  # Keep fast return to center
        self.angular_damping = 0.85
        
        # Engine and transmission properties
        self.engine_power = 120000  # Keep at 120 kW
        self.current_gear = 1
        self.gear_ratios = [6.0, 3.8, 2.8, 2.0, 1.5, 1.0]
        self.differential_ratio = 3.9
        
        # Revised speed limits per gear (in km/h)
        self.gear_speed_limits = [25, 50, 80, 125, 160, 200]
        
        # Throttle and power delivery - adjusted for smoother acceleration
        self.throttle = 0
        self.current_throttle = 0
        self.throttle_smoothing = 0.15
        self.power_buildup = 0
        self.power_buildup_rate = 0.4
        self.power_decay_rate = 1.0
        
        # Physics properties - improved ground contact
        self.drag_coefficient = 0.35
        self.rolling_resistance = 0.015
        self.ground_contact_force = 2.0  # Added for better road holding
        
        # Added clutch simulation
        self.clutch_engagement = 1.0
        self.clutch_grip = 0.0
        self.stall_rpm = 500
        
        # Tire and grip properties - improved ground contact
        self.tire_grip = 2.2              # Base tire grip
        self.lateral_grip = 1.8           # Lateral grip coefficient
        self.slip_angle = 0
        self.max_slip_angle = math.pi / 6
        self.tire_rolling_radius = 0.3
        
        # Car dimensions (for rendering)
        self.length = 4.5
        self.width = 1.8
        self.height = 1.4
        
        # Gear change properties
        self.gear_changing = False
        self.gear_change_time = 0.5  # Time to change gears
        self.gear_change_timer = 0
        self.optimal_shift_rpm = 5500  # RPM to shift up for best acceleration
        self.downshift_rpm = 2500     # RPM to shift down
        
        # Inertia and momentum - more realistic weight
        self.acceleration_factor = 0.4   # Reduced for much slower acceleration
        self.momentum = 0.97
        
        # Vehicle dynamics - adjusted for game-like handling
        self.understeer_factor = 0.8    # Reduced for more responsive turning
        self.weight_transfer_factor = 0.2  # More pronounced weight transfer
        self.steering_weight_speed = 25.0  # Speed at which steering becomes heavy
        self.max_lateral_g = 1.1          # Maximum lateral G-force
        self.grip_factor = 1.2          # Reduced for less sharp turning
        self.turn_speed_factor = 0.65   # Reduced for smoother turns
        self.drift_threshold = 25.0     # Increased for better high-speed stability
        
        # Speed and acceleration characteristics
        self.max_speed = 60.0  # About 216 km/h
        self.acceleration_curve = 0.85  # More linear acceleration (was 0.7)
        self.current_rpm = 800
        self.idle_rpm = 800
        self.max_rpm = 6500
        self.optimal_rpm = 4000
        self.redline_rpm = 6800
        
        # Transmission properties
        self.transmission_efficiency = 0.9
        self.gear_shift_time = 0.3
        self.shifting = False
        self.shift_timer = 0
        
        # Speed and acceleration
        self.deceleration_factor = 0.98
        self.turn_response = 3.0       # Added to control turn responsiveness
        
        # Braking properties
        self.max_brake_force = 25000    # Reduced from 35000
        self.brake_response = 0.7       # Slightly slower response
        self.brake_efficiency = 1.2     # Reduced from 1.5
        self.abs_threshold = 0.2        # Speed below which ABS doesn't work
        
        # Low speed braking
        self.low_speed_threshold = 8.0  # km/h - increased for smoother transition
        self.stop_threshold = 0.8       # m/s
        self.parking_brake_factor = 0.92  # Gentler final stop
        
        # Tire grip for braking
        self.brake_grip = 1.8           # Grip coefficient during braking
        self.brake_distribution = 0.6    # Front brake bias (60% front, 40% rear)
        
        # Clutch and launch characteristics
        self.clutch_engaged = False
        self.clutch_bite_point = 0.2      # Point where clutch starts engaging
        self.clutch_slip = 1.0            # 1.0 = full slip, 0.0 = fully engaged
        self.clutch_engage_rate = 0.4     # How quickly clutch engages
        self.launch_control = 0.3         # Initial power limit for smooth starts
        
        # First gear characteristics
        self.initial_power_band = 8.0     # Reduced from 15.0
        self.clutch_engagement_speed = 0.4 # Slower clutch engagement
        self.launch_power = 0.4           # Reduced initial power
        self.post_launch_factor = 0.6     # Smoother power transition
        
        # Adjusted acceleration control
        self.initial_acceleration_limit = 0.6  # Increased from 0.3 for better launch
        self.acceleration_curve_factor = 1.4   # Adjusted for better power delivery
        self.speed_transition_point = 20.0     # Increased transition point
        
        # Stall prevention
        self.stall_threshold = 800      # RPM below which engine might stall
        self.min_start_speed = [0, 5, 15, 25, 35, 45]  # Minimum speed (km/h) needed for each gear
        self.stall_chance = [0.0, 0.3, 0.7, 0.9, 0.95, 0.98]  # Chance of stall at low speed per gear
        
        # Handbrake properties - adjusted for better drifting
        self.handbrake = 0.0               # Handbrake input (0-1)
        self.handbrake_grip_factor = 0.15  # Lower for more slide
        self.drift_angle = 0.0             # Current drift angle
        self.lateral_velocity = 0.0        # Sideways velocity component
        self.drift_momentum = 0.0          # Drift state momentum
        self.drift_recovery_rate = 0.95    # Slower recovery for longer drifts
        self.drift_traction = 0.3          # Lower traction during drift
        self.drift_speed_threshold = 12.0  # Lower speed threshold for drifting
        self.drift_angle_factor = 2.5      # Stronger drift angle effect

    def apply_throttle(self, amount):
        self.throttle = max(0, min(1, amount))
        
    def apply_brake(self, amount):
        self.brake = max(0, min(1, amount))
        
    def apply_steering(self, amount):
        self.steering_input = max(-1, min(1, amount))

    def apply_handbrake(self, amount):
        self.handbrake = max(0, min(1, amount))

    def change_gear(self, gear_change):
        if not self.gear_changing:
            new_gear = self.current_gear + gear_change
            if 0 <= new_gear < len(self.gear_ratios):
                self.gear_changing = True
                self.gear_change_timer = self.gear_change_time
                self.current_gear = new_gear
                # Simulate clutch effect during gear change
                self.clutch_grip = 0.2

    def calculate_engine_force(self):
        if self.shifting:
            self.power_buildup *= 0.5
            return 0
        
        # Throttle response
        throttle_diff = self.throttle - self.current_throttle
        self.current_throttle += throttle_diff * self.throttle_smoothing
        
        # Progressive power buildup
        if self.throttle > 0:
            power_increment = self.power_buildup_rate * self.current_throttle * 0.003  # Reduced from 0.006
            self.power_buildup = min(1.0, self.power_buildup + power_increment)
        else:
            self.power_buildup = max(0.0, self.power_buildup - self.power_decay_rate * 0.008)

        current_speed_kmh = abs(self.velocity * 3.6)

        # Enhanced first gear launch behavior
        if self.current_gear == 1:
            if current_speed_kmh < self.initial_power_band:
                if current_speed_kmh < 2.0:  # Very low speed handling
                    # Simulate clutch engagement
                    self.clutch_slip = max(0.0, 1.0 - (current_speed_kmh / 2.0))
                    
                    # Very gentle initial power
                    initial_factor = min(1.0, current_speed_kmh)
                    power_factor = self.launch_power * initial_factor
                    
                    # Apply clutch slip effect
                    power_factor *= (1.0 - self.clutch_slip * 0.7)
                else:
                    # Progressive power build from 2-8 km/h
                    speed_factor = (current_speed_kmh - 2.0) / (self.initial_power_band - 2.0)
                    power_factor = self.launch_power + (speed_factor * (1.0 - self.launch_power))
                    
                    # Gradual clutch engagement
                    clutch_factor = min(1.0, current_speed_kmh * self.clutch_engagement_speed)
                    power_factor *= 0.4 + (clutch_factor * 0.6)
                
                # Apply throttle sensitivity at launch
                power_factor *= (0.3 + self.current_throttle * 0.7)
            else:
                # Normal first gear power
                power_factor = 1.0
        
        # Check if we can start in current gear
        if current_speed_kmh < self.min_start_speed[self.current_gear - 1]:
            if self.current_gear > 2:  # Only prevent starting in higher gears
                return 0
        
        # Calculate RPM
        wheel_rpm = abs(self.velocity) * 60 / (2 * math.pi * 0.3)
        self.current_rpm = max(
            self.idle_rpm,
            wheel_rpm * self.gear_ratios[self.current_gear - 1] * self.differential_ratio
        )
        
        # Prevent starting in wrong gear
        if self.current_rpm < self.stall_threshold and self.current_gear > 1:
            if current_speed_kmh < self.min_start_speed[self.current_gear - 1]:
                return 0
        
        # Rest of power calculation
        rpm_factor = self.current_rpm / self.max_rpm
        if rpm_factor < 0.2:
            power_factor = rpm_factor * 1.5
        elif rpm_factor < 0.4:
            power_factor = 0.3 + rpm_factor * 0.8
        elif rpm_factor < 0.7:
            power_factor = 0.6 + rpm_factor * 0.4
        else:
            power_factor = 1.0 - (rpm_factor - 0.7) * 1.2
        
        # Higher gear low-speed penalty
        if current_speed_kmh < self.min_start_speed[self.current_gear - 1] * 1.2:
            speed_factor = current_speed_kmh / (self.min_start_speed[self.current_gear - 1] * 1.2)
            power_factor *= max(0.0, speed_factor - 0.2)
        
        # Calculate final engine force with all factors
        throttle_power = pow(self.current_throttle * self.power_buildup, 1.1)
        engine_force = (self.engine_power * 
                       power_factor * 
                       throttle_power * 
                       self.gear_ratios[self.current_gear - 1] * 
                       self.differential_ratio * 
                       self.transmission_efficiency)
        
        return engine_force

    def update_steering(self, dt):
        # More responsive steering with better speed consideration
        speed_factor = min(1.0, abs(self.velocity) / 30.0)
        
        # Calculate maximum steering angle based on speed
        effective_max_angle = self.max_steering_angle / (1.0 + speed_factor * 0.5)
        
        # Base steering response with speed limitation
        target_angle = -self.steering_input * effective_max_angle
        
        if abs(self.steering_input) > 0.1:
            # Smoother steering response
            steering_speed = self.steering_speed * (1.0 - speed_factor * 0.3)
            self.steering_angle += (target_angle - self.steering_angle) * steering_speed * dt
        else:
            # Keep quick return to center
            return_force = -self.steering_angle * self.steering_return_speed
            self.steering_angle += return_force * dt
            
            if abs(self.steering_angle) < 0.05:
                self.steering_angle = 0
                self.angular_velocity *= 0.5

    def calculate_slip_angle(self):
        if abs(self.velocity) < 0.1:
            return 0
        # Calculate slip angle based on steering and velocity
        return math.atan2(self.wheel_base * math.tan(self.steering_angle), abs(self.velocity))

    def update(self, dt):
        self.update_steering(dt)
        
        # Handle gear shifting
        if self.shifting:
            self.shift_timer -= dt
            if self.shift_timer <= 0:
                self.shifting = False
        
        # Enhanced handbrake physics
        if self.handbrake > 0:
            current_speed_kmh = abs(self.velocity * 3.6)
            
            # Calculate drift behavior
            if current_speed_kmh > self.drift_speed_threshold:
                # More pronounced steering effect during drift
                steering_factor = self.steering_angle * (current_speed_kmh / 40.0)
                self.drift_angle += steering_factor * self.handbrake * dt * self.drift_angle_factor
                
                # Apply drift physics
                self.drift_momentum = min(1.0, self.drift_momentum + dt * 1.5)
                grip_loss = self.handbrake * (1.0 - self.handbrake_grip_factor)
                
                # Enhanced vehicle dynamics during drift
                self.angular_velocity += self.drift_angle * dt * 3.5
                self.velocity *= (1.0 - grip_loss * 0.15)
                
                # More pronounced lateral movement
                self.lateral_velocity = math.sin(self.drift_angle) * self.velocity * 0.9
                
                # Reduce engine power during drift
                if self.throttle > 0:
                    self.throttle *= (1.0 - self.handbrake * 0.3)
        else:
            # Smoother recovery from drift
            self.drift_angle *= self.drift_recovery_rate
            self.drift_momentum = max(0.0, self.drift_momentum - dt * 0.8)
            self.lateral_velocity *= self.drift_recovery_rate
        
        # Apply drift effects to position
        if abs(self.lateral_velocity) > 0.01:
            drift_direction = math.atan2(self.lateral_velocity, abs(self.velocity))
            self.x += self.lateral_velocity * math.cos(self.angle + math.pi/2) * dt
            self.y += self.lateral_velocity * math.sin(self.angle + math.pi/2) * dt
        
        # Calculate forces
        engine_force = self.calculate_engine_force()
        
        # Enhanced brake force calculation
        if self.brake > 0:
            current_speed_kmh = abs(self.velocity * 3.6)
            
            if current_speed_kmh < self.low_speed_threshold:
                # Enhanced low-speed stopping
                if abs(self.velocity) < self.stop_threshold:
                    # Gentler stop when almost stopped
                    self.velocity *= self.parking_brake_factor
                    if abs(self.velocity) < 0.01:
                        self.velocity = 0
                else:
                    # Moderate deceleration at low speeds
                    brake_decel = 8.0  # Reduced from 12.0 m/s²
                    self.velocity = math.copysign(
                        max(0.0, abs(self.velocity) - brake_decel * dt),
                        self.velocity
                    )
            else:
                # Progressive braking based on speed
                # Harder to stop at higher speeds
                speed_factor = min(1.0, current_speed_kmh / 100.0)  # Progressive up to 100 km/h
                
                # Base brake force that reduces at higher speeds
                brake_force = self.max_brake_force * (1.0 - speed_factor * 0.3)
                
                # Apply brake with speed-dependent response
                brake_power = pow(self.brake, self.brake_response)
                brake_power *= (1.0 - speed_factor * 0.2)  # Less effective at high speeds
                
                total_brake_force = brake_force * brake_power * self.brake_efficiency
                
                # Calculate deceleration with speed-dependent effectiveness
                brake_decel = total_brake_force / self.mass
                brake_decel *= (1.0 - speed_factor * 0.3)  # Less effective at high speeds
                
                # More gradual velocity reduction
                self.velocity = math.copysign(
                    max(0.0, abs(self.velocity) - brake_decel * dt),
                    self.velocity
                )
        
        # Calculate forces
        drag_force = 0.4 * self.velocity * abs(self.velocity)
        rolling_resistance = 0.1 * self.velocity
        
        # Net force
        net_force = engine_force - drag_force - rolling_resistance
        
        # Base acceleration
        acceleration = net_force / self.mass
        
        if self.throttle > 0:
            current_speed_kmh = abs(self.velocity * 3.6)
            speed_limit = self.gear_speed_limits[self.current_gear - 1]
            
            # More gradual speed limiting
            if current_speed_kmh > speed_limit * 0.85:
                limit_factor = max(0, min(1.0, 
                    (speed_limit - current_speed_kmh) / (speed_limit * 0.15)))
                acceleration *= max(0.05, limit_factor)
            
            # More pronounced gear-specific acceleration
            gear_factor = 1.0 - (self.current_gear - 1) * 0.2
            acceleration *= max(0.1, gear_factor)
            
            # Additional acceleration smoothing
            acceleration *= self.acceleration_factor
        
        # Update velocity with smooth acceleration
        self.velocity += acceleration * dt * 0.5  # Reduced from 0.7
        
        # Natural deceleration
        if self.throttle < 0.1 and not self.brake:
            self.velocity *= (1.0 - dt * 0.1)
        
        # Simpler RPM calculation
        wheel_rpm = abs(self.velocity) * 60 / (2 * math.pi * 0.3)
        if not self.shifting:
            target_rpm = wheel_rpm * self.gear_ratios[self.current_gear - 1] * self.differential_ratio
            rpm_change_rate = 3000 * dt  # Faster RPM changes
            rpm_diff = target_rpm - self.current_rpm
            rpm_change = min(abs(rpm_diff), rpm_change_rate) * (1 if rpm_diff > 0 else -1)
            self.current_rpm = max(self.idle_rpm, 
                                 min(self.max_rpm, 
                                     self.current_rpm + rpm_change))
        
        # Speed limits
        self.velocity = max(-self.max_speed/2, min(self.max_speed, self.velocity))
        
        if abs(self.velocity) > 0.1:
            if abs(self.steering_angle) > 0.001:
                # Calculate turn radius with more gradual response
                turn_radius = self.wheel_base / math.sin(abs(self.steering_angle))
                
                # Smoother turning rate calculation
                base_turn_rate = (self.velocity / turn_radius) * self.grip_factor
                if self.steering_angle < 0:
                    base_turn_rate = -abs(base_turn_rate)
                
                # More gradual turn response
                speed_grip = max(0.4, 1.0 - (abs(self.velocity) / self.drift_threshold) * 0.4)
                turn_rate = base_turn_rate * speed_grip * self.turn_speed_factor
                
                # Smoother angular velocity changes
                self.angular_velocity += (turn_rate - self.angular_velocity) * self.turn_response * dt
                
                # Gentler speed loss in turns
                self.velocity *= (1.0 - abs(self.steering_angle) * 0.06 * dt)
            else:
                # Maintain smooth straightening
                self.angular_velocity *= self.angular_damping
        
        # Update position with terrain following
        old_x = self.x
        old_y = self.y
        
        # Calculate new position based on velocity
        new_x = self.x + self.velocity * math.cos(self.angle) * dt
        new_y = self.y + self.velocity * math.sin(self.angle) * dt
        
        # Get terrain heights with proper sampling
        current_height = self.world.get_height_at(self.x, self.y)
        new_height = self.world.get_height_at(new_x, new_y)
        
        # Calculate slope
        dx = new_x - self.x
        dy = new_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0.001:  # Prevent division by zero
            slope_angle = math.atan2(new_height - current_height, distance)
            
            # Adjust velocity based on slope (more pronounced effect)
            slope_factor = 1.0 - abs(math.sin(slope_angle)) * 0.05  # Increased from 0.5
            self.velocity *= slope_factor
        
        # Update position with proper height offset
        self.x = new_x
        self.y = new_y
        self.z = new_height + 1.0  # Increased from 0.5 to lift car higher
        
        # Calculate terrain normal for car orientation (sample points further apart)
        front_height = self.world.get_height_at(self.x + math.cos(self.angle) * 2.0, 
                                              self.y + math.sin(self.angle) * 2.0)
        right_height = self.world.get_height_at(self.x - math.sin(self.angle) * 2.0, 
                                              self.y + math.cos(self.angle) * 2.0)
        
        # Calculate pitch and roll (more pronounced angles)
        pitch = math.atan2(front_height - current_height, 2.0) * 1.2
        roll = math.atan2(right_height - current_height, 2.0) * 1.2
        
        # Store orientation for drawing
        self.pitch = pitch
        self.roll = roll
        
        # Update car angle
        self.angle += self.angular_velocity * dt
        
    def draw(self):
        glPushMatrix()
        
        # Move to car position
        glTranslatef(self.x, self.y, self.z)
        
        # Apply rotations in the correct order
        glRotatef(math.degrees(self.angle), 0, 0, 1)  # Yaw
        glRotatef(math.degrees(self.pitch), 0, 1, 0)  # Pitch
        glRotatef(math.degrees(self.roll), 1, 0, 0)   # Roll
        
        # Draw car body
        glColor3f(1.0, 0.0, 0.0)  # Red color
        self._draw_box(self.length, self.width, self.height)
        
        # Draw wheels with terrain adaptation
        self._draw_wheels()
        
        glPopMatrix()
        
    def _draw_box(self, length, width, height):
        l, w, h = length/2, width/2, height/2
        
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(l, w, -h)
        glVertex3f(l, -w, -h)
        glVertex3f(l, -w, h)
        glVertex3f(l, w, h)
        
        # Back face
        glVertex3f(-l, w, -h)
        glVertex3f(-l, -w, -h)
        glVertex3f(-l, -w, h)
        glVertex3f(-l, w, h)
        
        # Top face
        glVertex3f(l, w, h)
        glVertex3f(-l, w, h)
        glVertex3f(-l, -w, h)
        glVertex3f(l, -w, h)
        
        # Bottom face
        glVertex3f(l, w, -h)
        glVertex3f(-l, w, -h)
        glVertex3f(-l, -w, -h)
        glVertex3f(l, -w, -h)
        
        # Right face
        glVertex3f(l, w, -h)
        glVertex3f(-l, w, -h)
        glVertex3f(-l, w, h)
        glVertex3f(l, w, h)
        
        # Left face
        glVertex3f(l, -w, -h)
        glVertex3f(-l, -w, -h)
        glVertex3f(-l, -w, h)
        glVertex3f(l, -w, h)
        glEnd()
        
    def _draw_wheels(self):
        wheel_radius = 0.3
        wheel_width = 0.2
        
        # Wheel positions relative to car center
        wheels = [
            (self.length/3, self.width/2, -self.height/2),   # Front right
            (self.length/3, -self.width/2, -self.height/2),  # Front left
            (-self.length/3, self.width/2, -self.height/2),  # Rear right
            (-self.length/3, -self.width/2, -self.height/2)  # Rear left
        ]
        
        glColor3f(0.2, 0.2, 0.2)  # Dark gray for wheels
        for x, y, z in wheels:
            glPushMatrix()
            glTranslatef(x, y, z)
            self._draw_cylinder(wheel_radius, wheel_width)
            glPopMatrix()
            
    def _draw_cylinder(self, radius, height):
        # Simple cylinder implementation
        segments = 20
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, 0, y)
            glVertex3f(x, height, y)
        glEnd()

    def shift_up(self):
        if not self.shifting and self.current_gear < len(self.gear_ratios):
            # Only allow upshift if RPM is high enough
            if self.current_rpm > self.optimal_rpm:
                self.current_gear += 1
                self.shifting = True
                self.shift_timer = self.gear_shift_time
                return True
        return False

    def shift_down(self):
        if not self.shifting and self.current_gear > 1:
            # Only allow downshift if we won't over-rev the engine
            next_gear_rpm = self.current_rpm * (self.gear_ratios[self.current_gear - 2] / 
                                              self.gear_ratios[self.current_gear - 1])
            if next_gear_rpm < self.redline_rpm:
                self.current_gear -= 1
                self.shifting = True
                self.shift_timer = self.gear_shift_time
                return True
        return False 