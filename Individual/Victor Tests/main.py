# These are my files, feel free to copy or test.

import math
import random
import pygame
import winsound

pygame.init()


blood_moon = False
# Music. For fun, added chance for ambience/music. 33% chance for music, 66% chance for ambience, and 1% chance for Something Different and different earth img.
music_chance = random.randint(1,99)
if music_chance <= 33:
    BG = pygame.mixer.Sound('Hackathon BG - USE.wav')
    BG.play(999)
elif music_chance <= 99:
    ambience = pygame.mixer.Sound("Hackathon 2024 Abmience - USE.wav")
    ambience.play(999)
else:
    SOMETHING_DIFFERENT = pygame.mixer.Sound("Something Different - Hackathon 2024 Copy.wav")
    SOMETHING_DIFFERENT.play(99999)
    blood_moon = True


def show_text(msg, x, y, color, font_size, font_name="comicsans", bold=False, italic=False):
    fontobj = pygame.font.SysFont(font_name, font_size, bold, italic)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))


# Win variable
win = False
# Show Display variable
show = True
# Var to set fuel to when called:
fuelsetto = 750
# Fuel variable
fuel = fuelsetto
# Initial velocity slider value variable
initial_velocity_slider_value = 10
# Fast-forward variable
fastforward = False
# FPS variable
FPS = 10
# Constants
WIDTH, HEIGHT = 900, 700
GRAVITY_CONSTANT = 200  # Gravitational constant
EARTH_MASS = 35  # Mass of the Earth
MOON_MASS = 10  # Mass of the Moon
EARTH_RADIUS = 40  # Radius of the Earth in pixels
MOON_RADIUS = 10
EARTH_POSITION = (WIDTH // 2, HEIGHT // 2)  # Position of the Earth in the center
MOON_ORBIT_RADIUS = 200  # Distance from Earth to the Moon in pixels
MOON_ORBIT_SPEED = 0.02  # Speed of the Moon's orbit around the Earth
MAX_TRAJECTORY_POINTS = 99999999999  # Maximum number of trajectory points to display
start_from_moon = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PLATFORM_COLOR = (150, 75, 0)
GRAY = (200, 200, 200)
CONFETTI_COLORS = [RED, BLUE, GREEN, (255, 165, 0)]

# Load images
if blood_moon == False:
    earth_image = pygame.transform.scale(pygame.image.load("Hackathon/earth - Copy.png"), (EARTH_RADIUS * 2, EARTH_RADIUS * 2))
    moon_image = pygame.transform.scale(pygame.image.load("Hackathon/moon - Copy.png"), (MOON_RADIUS * 2, MOON_RADIUS * 2))
else:
    earth_image = pygame.transform.scale(pygame.image.load("Hackathon/tech earth.jpg"), (EARTH_RADIUS * 2, EARTH_RADIUS * 2))
    moon_image = pygame.transform.scale(pygame.image.load("Hackathon/Steven-g-bloodmoon.jpg"), (MOON_RADIUS * 2, MOON_RADIUS * 2))



# Colors
YELLOW = (255, 255, 0)  # Color for the trajectory
GREEN = (0, 255, 0)  # Color for the slider indicator
BLUE = (0, 0, 255)  # Color for the button background


class Spacecraft:
    def __init__(self, initial_velocity: float):
        self.reset(initial_velocity)
        self.start_from_moon = False
        self.pause_movement = False
        self.time_to_movement = 300
        self.has_reached_moon = False
        self.path = []
        self.earthr = False
        self.played_audio_sound_for_no_fuel_left = False

    def reset(self, initial_velocity: float):
        self.x = EARTH_POSITION[0] + 5  # Slightly outside Earth's surface
        self.y = EARTH_POSITION[1]
        self.vx = 0  # Start with a horizontal velocity
        self.vy = initial_velocity  # Set initial vertical velocity
        self.path = []  # Clear the path when resetting
        self.start_from_moon = False
        self.pause_movement = False
        self.time_to_movement = 300
        self.has_reached_moon = False
        self.earthr = False
        self.played_audio_sound_for_no_fuel_left = False
        self.played_audio_sound_for_extracting_probes = False



    def update(self, moon_position):
        if not self.pause_movement:
            # Calculate gravitational force from Earth
            dx_earth = EARTH_POSITION[0] - self.x
            dy_earth = EARTH_POSITION[1] - self.y
            distance_earth = math.sqrt(dx_earth ** 2 + dy_earth ** 2)

            # Calculate gravitational force from Earth
            if distance_earth > EARTH_RADIUS:
                force_earth = (GRAVITY_CONSTANT * EARTH_MASS) / (distance_earth ** 2)
                theta_earth = math.atan2(dy_earth, dx_earth)
            else:
                force_earth = 0
                theta_earth = 0  # Default value if close to Earth

            # Calculate gravitational force from Moon
            dx_moon = moon_position[0] - self.x
            dy_moon = moon_position[1] - self.y
            distance_moon = math.sqrt(dx_moon ** 2 + dy_moon ** 2)

            # Initialize theta_moon
            theta_moon = 0  # Default value

            # Calculate gravitational force from Moon
            if distance_moon > MOON_RADIUS:
                force_moon = (GRAVITY_CONSTANT * MOON_MASS) / (distance_moon ** 2)
                theta_moon = math.atan2(dy_moon, dx_moon)
            else:
                force_moon = 0

            # Update velocities based on both gravitational forces
            self.vx += force_earth * math.cos(theta_earth) + force_moon * math.cos(theta_moon)
            self.vy += force_earth * math.sin(theta_earth) + force_moon * math.sin(theta_moon)

            # Cap maximum velocity to prevent it from escaping quickly
            max_velocity = 10  # Maximum allowable velocity
            speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
            if speed > max_velocity:
                self.vx = (self.vx / speed) * max_velocity
                self.vy = (self.vy / speed) * max_velocity

            # Update position
            self.x += self.vx
            self.y += self.vy

            if distance_earth <= EARTH_RADIUS: # Collision with the Earth
                if self.has_reached_moon == True:
                    global win

                    # End game
                    win = True

                    # Pause all movement
                    self.time_to_movement = math.inf
                    self.pause_movement = True
                elif self.earthr == False:
                    global fuel
                    fuel = fuelsetto
                    self.earthr = True

            # Check if spacecraft touches the Moon
            if distance_moon <= MOON_RADIUS and not self.start_from_moon:  # Collision with the Moon
                if self.played_audio_sound_for_extracting_probes != True:
                    sound = pygame.mixer.Sound("audio (1).wav")
                    sound.play()
                    self.played_audio_sound_for_extracting_probes = True
                self.moon_enter_pos = self.path[::-1]
                winsound.Beep(50,100)
                self.reset(initial_velocity=-initial_velocity)  # Set a new initial velocity for the blast off
                self.x = moon_position[0] + MOON_RADIUS + 10  # Position just outside the Moon
                self.y = moon_position[1]  # Maintain the same y-coordinate as the Moon
                self.start_from_moon = True
                self.has_reached_moon = True
                self.pause_movement = True

            # Store the path
            if len(self.path) < MAX_TRAJECTORY_POINTS:
                new_position = (self.x, self.y)
                print(f"New position before adding to path: {new_position}")  # Debugging line
                # Ensure valid position before adding
                if isinstance(new_position, tuple) and len(new_position) == 2:
                    self.path.append(new_position)
        else:
            self.time_to_movement -= 1
            if self.time_to_movement > 0:
                print("Movement Paused")
            else:
                self.pause_movement = False

    def draw(self, screen):
        # Draw the trajectory path as lines
        if len(self.path) > 1:
            pygame.draw.lines(screen, YELLOW, False, self.path, 2)  # Draw lines connecting trajectory points

    def draw_progress_bar(self, moon_position):
        # Draw a progress bar based on time_to_movement
        if self.pause_movement:
            if fuel != 0:
                bar_width = 100
                filled_width = (bar_width * (self.time_to_movement / 300))  # 300 is the initial pause time
                bar_x = moon_position[0] - bar_width // 2
                bar_y = moon_position[1] + MOON_RADIUS + 20  # Below the Moon

                # Draw the background
                pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, 10))
                # Draw the filled part
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, filled_width, 10))
                # Draw the text above the bar
                show_text("Gathering probes", bar_x, bar_y - 20, WHITE, 25, "trebuchems", False,True)
            else:
                if self.played_audio_sound_for_no_fuel_left != True:
                    sound = pygame.mixer.Sound("audio.wav")
                    sound.play()
                    self.played_audio_sound_for_no_fuel_left = True

                bar_width = 100
                bar_x = moon_position[0] - bar_width // 2
                bar_y = moon_position[1] + MOON_RADIUS + 20  # Below the Moon
                self.time_to_movement = math.inf
                # Draw the background
                pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, 10))
                # Draw the text above the bar
                show_text("⚠ NO FUEL LEFT : PLEASE RESTART SIMULATION ⚠", bar_x, bar_y - 20, WHITE, 20, "trebuchems", False, True)


def draw_winner(text):
    for _ in range(100):  # Number of frames for animation
        screen.fill(BLACK)
        show_text("You have", 50, 100, WHITE, 100, "comicsans", False, False)
        show_text("successfully", 50, 200, WHITE, 100, "comicsans", False, False)
        show_text("completed the ", 50, 300, WHITE, 100, "comicsans", False, False)
        show_text("Artemis II", 50, 400, WHITE, 100, "comicsans", False, False)
        show_text("simulation!", 50, 500, WHITE, 100, "comicsans", False, False)

        # Draw confetti
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(screen, random.choice(CONFETTI_COLORS), (x, y), 5)
        pygame.display.update()
        pygame.time.delay(50)


# Initialize game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth and Moon Orbital Simulator")
clock = pygame.time.Clock()
running = True

# Create spacecraft with initial velocity
initial_velocity = 3.0  # Adjust this value for different orbital behaviors
spacecraft = Spacecraft(initial_velocity)

# Moon's angle for orbiting around the Earth
moon_angle = 0

# Main game loop
while running:
    # Check for Win
    if win:
        draw_winner("You have successfully completed the Artemis II Simulation!")

    # Update Moon's position
    moon_angle += MOON_ORBIT_SPEED
    moon_x = EARTH_POSITION[0] + MOON_ORBIT_RADIUS * math.cos(moon_angle)
    moon_y = EARTH_POSITION[1] + MOON_ORBIT_RADIUS * math.sin(moon_angle)
    moon_position = (moon_x, moon_y)

    if fuel >= 1 and abs(spacecraft.x - EARTH_POSITION[0]) <= 75 and abs(spacecraft.y - EARTH_POSITION[1]) <= 75 or fuel >= 1 and spacecraft.pause_movement == True or fuel >=1 and abs(spacecraft.x - moon_position[0]) <= 75 and abs(spacecraft.y - moon_position[1]) <= 75 and spacecraft.has_reached_moon == True:
        GRAVITY_CONSTANT = 50
        fuel = fuel - 1

    if fuel >= 1 and abs(spacecraft.x - EARTH_POSITION[0]) <= 75 and abs(spacecraft.y - EARTH_POSITION[1]) <= 75 or fuel >= 1 and spacecraft.pause_movement == True or fuel >=1 and abs(spacecraft.x - moon_position[0]) <= 75 and abs(spacecraft.y - moon_position[1]) <= 75 and spacecraft.has_reached_moon == True:
        GRAVITY_CONSTANT = 50
        fuel = fuel - 1
    else:
        GRAVITY_CONSTANT = 100
    # Update spacecraft
    spacecraft.update(moon_position)

    # Clear screen
    screen.fill(BLACK)

    # Draw Earth and Moon
    screen.blit(earth_image, (EARTH_POSITION[0] - EARTH_RADIUS, EARTH_POSITION[1] - EARTH_RADIUS))
    screen.blit(moon_image, (moon_x - MOON_RADIUS, moon_y - MOON_RADIUS))

    # Draw the trajectory
    spacecraft.draw(screen)

    if show:

        # Draw progress bar if paused
        spacecraft.draw_progress_bar(moon_position)

        # Display the initial velocity slider
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # If left mouse button is pressed
            if 50 <= mouse_x <= 550 and 550 <= mouse_y <= 570:  # Slider area
                initial_velocity = (mouse_x - 50) / 500.0 * initial_velocity_slider_value  # Scale from 0 to 10000
                spacecraft.reset(initial_velocity)  # Reset spacecraft with new velocity

        # Draw velocity slider
        pygame.draw.rect(screen, WHITE, (50, 550, 500, 20))  # Slider background
        pygame.draw.rect(screen, GREEN, (50 + (initial_velocity / initial_velocity_slider_value * 500), 550, 10, 20))  # Slider indicator

        # Draw the background of the fuel bar
        pygame.draw.rect(screen, WHITE, (9, 9, 502, 12))

        # Draw the filled part of the fuel bar
        pygame.draw.rect(screen, RED, (10, 10, fuel/float(1.5), 10))

        # Display fuel left
        if fuel == 0:
            show_text("⚠ NO FUEL LEFT ⚠",10,25,RED,10)
        else:
            show_text("Fuel left: "+str(fuel), 10,30,WHITE,10,"comicsans",False,False)

        # Display current velocity value
        font = pygame.font.SysFont(None, 24)
        text = font.render(f'Initial Velocity: {initial_velocity:.2f}', True, WHITE)
        screen.blit(text, (50, 520))

        # Draw "Blast Off" button
        button_rect = pygame.Rect(600, 550, 150, 40)
        pygame.draw.rect(screen, BLUE, button_rect)  # Draw button background
        button_text = font.render("Restart Simulation", True, WHITE)
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    # Fast-forward button configuration
    fast_forward_button_hitbox = pygame.Rect(880, 40, 20, 20)
    pygame.draw.circle(screen, WHITE, (890, 50), 10)
    show_text("- Fast-Forward - ^", 810, 65, WHITE, 10)
    if not fastforward:
        pygame.draw.circle(screen, RED, (890, 50), 7)
        FPS = 30
    else:
        pygame.draw.circle(screen, GREEN, (890, 50), 7)
        FPS = 60
    # Display on/off button configuration
    button_hitbox = pygame.Rect(880,0,20,20)
    pygame.draw.circle(screen,WHITE,(890,10), 10)
    show_text("Display on/off button^", 790,25,WHITE,10)
    if not show:
        pygame.draw.circle(screen,RED, (890,10),7)
    else:
        pygame.draw.circle(screen,GREEN, (890,10),7)
    # Show variables
    if show:
        show_text("------------",10,50,WHITE,10)
        show_text("X Velocity: " + str(round(spacecraft.vx*10)),10,75,WHITE,10)
        show_text("Y Velocity: " + str(round(spacecraft.vy * 10)), 10, 100, WHITE, 10)
        show_text("X: " + str(round(spacecraft.x * 10/10)), 10, 125, WHITE, 10)
        show_text("Y: " + str(round(spacecraft.y * 10/10)), 10, 150, WHITE, 10)
        if not spacecraft.pause_movement:
            show_text("Distance from Moon: "+str(round(math.dist((spacecraft.x,spacecraft.y), moon_position))),10,175,WHITE,10)
            show_text("Distance from Earth: "+str(round(math.dist((spacecraft.x,spacecraft.y),EARTH_POSITION))),10,200,WHITE,10)

        else:
            show_text("ON MOON", 10,175,WHITE,10)
            show_text("ON MOON", 10, 200, WHITE, 10)
        show_text("Has touched moon?: " + str(spacecraft.has_reached_moon), 10, 225, WHITE, 10)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                spacecraft.has_reached_moon = False
                spacecraft.reset(initial_velocity)  # Reset spacecraft with current velocity
            if button_hitbox.collidepoint(event.pos):
                if not show:
                    show = True
                else:
                    show = False
            if fast_forward_button_hitbox.collidepoint(event.pos):
                if not fastforward:
                    fastforward = True
                else:
                    fastforward = False


    # Refresh screen
    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
