import math
import random
import sys
import time

import pygame
from pygame.locals import *

# Initialization of pygame 
pygame.init()

# Screen settings 
LARGURA, ALTURA = 800, 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Rocket Landing Game")

# Font settings
font_text = pygame.font.SysFont(None, 30)
font_h1 = pygame.font.SysFont(None, 80)
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("Space.mp3")

# A variable to check for the status later
click = False

# Color settings 
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Physical constants 
GRAVIDADE = 9.8  # Gravity [m/s^2]
IMPULSO = 7600000 # Impulse [kg*m/s^2]
RAPIDEZ_ROTACAO = 2 # Rotation speed [RAD/s]
MAX_COMBUSTIVEL = 100 # Fuel 
FATOR_ESCALA = 1 # Scale factor 
VISCOSIDADE_AR = 0.05 # Coefficient of air viscosity 
RESISTENCIA_AR = 50 # Coefficient of air resistance 
VELOCIDADE_INICIAL = random.uniform(150, 200) # Initial speed random value between 150-200
COEFICIENTE_ARRASTO = 1000
FUEL_WEIGHT = 1300
DRY_MASS = 22000
DROPOFF_RATE = 1200

VELOCIDADE_INICIAL = random.uniform(150, 200)

"""
A function that can be used to write text on our screen and buttons
"""
def draw_text(text, font, color, surface, x, y):
    """
    A function that can be used to write text on our screen and buttons

    Parameters:
        text: the text displayed 
        font: the font used to render the text 
        color: the color of the text 
        surface: the surface where the text will be drawn
        x: the x-coordinate of the top left corner 
        y: the y-coordinate of the top left corner 
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_back_to_menu_button(screen):
    """
    Draws a button which return to the menu

    Parameters:
        screen: the surface where the button will be drawn 
    
    Return:
        button_rect: the retangle representing the button's position and size
    """
    # Button settings (size and position)
    button_width, button_height = 150, 30
    button_x = 10
    button_y = 100  # Position it below the game-over message
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Draw the button
    pygame.draw.rect(screen, (100, 100, 255), button_rect)  # Blue color for the button

    # Draw the text on the button
    font = pygame.font.Font(None, 25)
    text_surface = font.render("Voltar ao Menu", True, (255, 255, 255))  # White text
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect

class Planet:
    def __init__(self, name, gravity, air_density, pad_color):
        self.name = name
        self.gravity = gravity
        self.density = air_density
        self.pad_color = pad_color

def create_planets():
    return {
        "Earth": Planet("Earth",
                        gravity = 9.8,
                        air_density = 1.225,
                        pad_color = (61, 73, 144)),
        
        "Venus": Planet("Venus", 
                        gravity=8.87,
                        air_density = 65,
                        pad_color = (185, 115, 31)),
        
        "Mars": Planet("Jupiter", 
                       gravity= 24.79,
                       air_density = 0.16,
                       pad_color = (201, 87, 43)),
        
        "Moon": Planet("Luna", 
                       gravity=1.62,
                       air_density = 0,
                       pad_color = (194, 193, 191)),
        
        "Europa": Planet("Europa", 
                         gravity=1.31,
                         air_density=0,
                         pad_color = (179, 159, 156)),
        
        "Titan": Planet("Titan", 
                        gravity=1.352,
                        air_density= 5.4,
                        pad_color = (84, 130, 112))
    }    
    

class Cloud:
    """
    Class that represents the cloud after an explosion 
    """
    def __init__(self, x, y):
        """
        Initializes a new cloud instance in the position (x, y)
        """
        self.x = x # x-coordinate 
        self.y = y # y-coordinate 
        self.r = 0 # radius of the cloud 
        # Defines a random color in a range of red and orange with semi-transparency 
        self.color = pygame.Color(random.randint(200, 255), random.randint(50, 150), 0, 150) 
        self.a = 150 # transparency 
        self.expansion_rate = random.randrange(7, 15) # Expansion rate 

    def update(self):
        """
        Update the cloud's properties 
        """
        self.r += self.expansion_rate 
        self.expansion_rate -= 0.05 
        self.a -= 1
        # Ensures the transparency is never below 0 
        if self.color.a > 0:
            self.color.a -= 1
        else:
            self.color.a = 0

    def draw(self, screen):
        """
        Draws the cloud in the given screen 
        """
        # Create a surface 
        superfice = pygame.Surface((2*ALTURA, 2*LARGURA), pygame.SRCALPHA)
        # Draw a circle with the given positions and characteristics 
        pygame.draw.circle(superfice, self.color, center=(self.x, self.y), radius = self.r)
        # Copy the cloud surface into the main screen 
        screen.blit(superfice, (0, 0))


class Explosion:
    """
    Class that represents the explosion (formed by multiple clouds)
    """
    def __init__(self, x, y):
        """
        Initializes a new explosion instance in the position (x, y)
        """
        self.x = x
        self.y = y
        # Define the clouds
        self.clouds = []
        for _ in range(10):
            self.clouds.append(Cloud(self.x + random.randrange(1, 50), self.y + random.randrange(1, 50)))
    
    def update(self):
        """
        Updates the explosion (each cloud)
        """
        for cloud in self.clouds:
            cloud.update()

    def draw(self, screen):
        """
        Draws the explosion (the clouds)
        """
        for cloud in self.clouds:
            cloud.draw(screen)

    def is_done(self):
        """
        Verifies if the explosion is over based on the transparacy of the cloud
        """
        if(self.clouds[0].a == -30):
            return True
        else:
            return False


class Rocket:
    """
    Class that represents the rocket 
    """
    def __init__(self):
        self.x = LARGURA / 2 # x-coordinate 
        self.y = ALTURA / 4 # y-coordinate 
        self.angulo = random.uniform(-(math.pi)/4 ,(math.pi)/4)  # Angle in radians
        self.rapidez = VELOCIDADE_INICIAL
        self.vx = math.cos(self.angulo + (math.pi/2)) * self.rapidez     # Horizontal velocity
        self.vy = math.sin(self.angulo + (math.pi/2)) * self.rapidez     # Vertical velocity
        self.x -= self.vx * 1
        self.y -= self.vy * 1
        self.combustivel = MAX_COMBUSTIVEL # fuel 
        self.massa = DRY_MASS + self.combustivel * FUEL_WEIGHT # mass of the rocket 
        self.cor = BRANCO # color 
        self.colidiu = False # collision status 
        self.impulsionando = False 
        self.acelerador = 1 # Controls the rocket's thrust 
        self.altura = 12 # height of the rocket 
        self.largura = 5 # width of the rocket 
        self.ingnited = False 
        self.explosion = None # explosion status 
        self.message = None # message status 
        self.last_time_update = time.perf_counter()

    def aplicar_impulso(self):
        """
        Changes rocket's thrust state 
        """
        # If it's off, turns it on and starts thrust 
        if not self.ingnited:
            self.ingnited = True
            self.impulsionando = True
        # If it's on, turns it off
        else:
            self.impulsionando = False
            self.ingnited = False

    def update_color(self, color):
        """
        Update the rocket's color with the given color 
        """
        self.cor = color

    def rotate_left(self):
        """
        Rotate the rocket to the left by changing its angle
        """
        current_time = time.perf_counter()
        dt = (current_time - self.last_time_update)
        self.angulo -= RAPIDEZ_ROTACAO * dt
        if self.angulo < -math.pi:
            self.angulo = 2*math.pi + self.angulo

    def rotate_right(self):
        """
        Rotate the rocket to the right by changing its angle
        """
        current_time = time.perf_counter()
        dt = (current_time - self.last_time_update)
        self.angulo += RAPIDEZ_ROTACAO * dt
        if self.angulo > math.pi:
            self.angulo = -2*math.pi + self.angulo

    def update(self):
        """
        Update the rocket's position, velocity and 
        """
        # Computes the time delta 
        current_time = time.perf_counter()
        dt = (current_time - self.last_time_update)
        self.last_time_update = current_time

        # Verifies if the rocket hasn't collided 
        if not self.colidiu:
            # Applies gravity 
            self.vy += GRAVIDADE * dt

            # Updates position according to velocity and scale factor 
            self.x += self.vx * FATOR_ESCALA * dt
            self.y += self.vy * FATOR_ESCALA * dt
            DROP_OFF = 1/((self.x/DROPOFF_RATE) + 1)

            # Change velocity depending of air resistence 
            forca_viscosa_x = -self.vx * (DENSIDADE_AR * COEFICIENTE_ARRASTO * DROP_OFF)  * dt
            forca_viscosa_y = -self.vy * (DENSIDADE_AR * COEFICIENTE_ARRASTO * DROP_OFF) * dt
            self.vx += (forca_viscosa_x / self.massa)
            self.vy += (forca_viscosa_y / self.massa)

            # Ensures the rocket stays in screen limits 
            if self.x < 0:
                self.x = 0
                self.vx = 0
            if self.x > LARGURA:
                self.x = LARGURA
                self.vx = 0
            if self.y > ALTURA:
                self.y = ALTURA
                self.vy = 0
            
            # If the rocket has thrust 
            if self.impulsionando and not self.colidiu:
                # If it has fuel 
                if self.combustivel > 0:
                    forca_x = IMPULSO * self.acelerador * math.sin(self.angulo) * dt
                    forca_y = -IMPULSO * self.acelerador * math.cos(self.angulo) * dt
                    # Update the velocity and decreases mass and fuel 
                    self.vx += (forca_x / self.massa)
                    self.vy += (forca_y / self.massa)
                    self.combustivel -= 10 * self.acelerador * dt
                    self.massa = max(0, DRY_MASS + self.combustivel * FUEL_WEIGHT)
                    self.impulsionando = True


    def draw_flame(self, screen):
        """
        Function that draw the flames of the rocket 
        """
        # Only draw flame if thrust is applied
        if self.impulsionando and self.combustivel > 0: 
            flame_base_x = self.x - math.sin(self.angulo) * 6
            flame_base_y = self.y + math.cos(self.angulo) * 6
            flame_length = random.randint(5, int(200*self.acelerador) + 5)  # Vary flame length to simulate flicker

            flame_tip_x = flame_base_x - math.sin(self.angulo) * flame_length
            flame_tip_y = flame_base_y + math.cos(self.angulo) * flame_length

            flame_color = (random.randint(50, 150), random.randint(50, 100), random.randint(100, 255))  # Yellow-orange flicker
            # Draws the flame 
            pygame.draw.polygon(screen, flame_color, [
                (flame_base_x - 2*math.cos(self.angulo), flame_base_y - 2*math.sin(self.angulo),), 
                (flame_base_x + 2*math.cos(self.angulo), flame_base_y + 2*math.sin(self.angulo),),
                (flame_tip_x, flame_tip_y) 
            ])

    def draw(self, screen):
        """
        Draws the rocket's body and informations on the screen (fuel, speed, angle)
        """

        # Defines the rectangular shape of the rocket 
        points = [
            (self.x - self.largura / 2, self.y - self.altura / 2),
            (self.x + self.largura / 2, self.y - self.altura / 2),
            (self.x + self.largura / 2, self.y + self.altura / 2),
            (self.x - self.largura / 2, self.y + self.altura / 2)
        ]
        # Rotates the rocket based on the angle 
        rotated_points = []
        for px, py in points:
            new_x = (px - self.x) * math.cos(self.angulo) - (py - self.y) * math.sin(self.angulo) + self.x
            new_y = (px - self.x) * math.sin(self.angulo) + (py - self.y) * math.cos(self.angulo) + self.y
            rotated_points.append((new_x, new_y))
        # Draws the rocket 
        pygame.draw.polygon(screen, self.cor, rotated_points)
        #  Defines the informations 
        font = pygame.font.Font(None, 36)
        fuel_text = font.render(f"Fuel: {int(self.combustivel)}", True, BRANCO)
        speed_text = font.render(f"Speed: {int(math.sqrt(self.vx**2 + self.vy**2))}", True, BRANCO)
        angle_text = font.render(f"Angle: {int((-1*self.angulo) * (180/math.pi) + 90)}", True, BRANCO)
        # Draws the information 
        screen.blit(fuel_text, (10, 10))
        screen.blit(speed_text, (10, 40))
        screen.blit(angle_text, (10, 70))

    def throtle(self, delta):
        """
        Adjust the throtle of the rocket according to delta 
        """
        self.acelerador = abs(self.acelerador + (delta * 0.1))
        self.acelerador = max(min(self.acelerador, 1), 0.05)

    def desenhar_trajetoria(self, screen):
        """
        Draws the predicted trajectory of the rocket 
        """
        dt = 1
        x_futuro = self.x
        y_futuro = self.y
        vx_futuro = self.vx
        vy_futuro = self.vy

        pontos_trajetoria = []
        pontos_trajetoria.append((int(x_futuro), int(y_futuro)))

        while True:
            # Determines the trajectory under gravity and air resistence in small gaps (dt)
            vy_futuro += GRAVIDADE * dt
            x_futuro += vx_futuro * FATOR_ESCALA * dt
            y_futuro += vy_futuro * FATOR_ESCALA * dt
            DROP_OFF = 1/((x_futuro/DROPOFF_RATE) + 1)

            vx_futuro += (-vx_futuro * (DENSIDADE_AR * COEFICIENTE_ARRASTO * DROP_OFF) )/self.massa * dt
            vy_futuro += (-vy_futuro * (DENSIDADE_AR * COEFICIENTE_ARRASTO * DROP_OFF) )/self.massa* dt


            pontos_trajetoria.append((int(x_futuro), int(y_futuro)))

            # Stops if the rocket is not in screen boundries 
            if y_futuro > ALTURA or y_futuro < 0 or x_futuro > (2*LARGURA) or x_futuro < 0:
                break

            dt += 0.01
        
        # Draws the trajectory 
        if len(pontos_trajetoria) > 1:
            superfice = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            cor = pygame.Color(255, 0, 0, 100)
            pygame.draw.lines(superfice, cor, False, pontos_trajetoria, 2)
            screen.blit(superfice, (0, 0))

def draw_landing_pad(screen):
    """
    Function that draws the pad where the rocket is supposed to land 
    """
    pad_width = 100
    pad_height = 10
    pad_x = LARGURA / 2 - pad_width / 2
    pad_y = ALTURA - pad_height
    pygame.draw.rect(screen, PAD_COLOR, (pad_x, pad_y, pad_width, pad_height))


def end_game(rocket, message, exploded):
    """ 
    Function that handles end game given the result 
    Parameters:
    rocket: a ca
    message: the message to be displayed 
    exploded: if the rocket has exploded 
    """
    rocket.message = message
    # If the rocket exploded there's an explosin 
    if exploded:
        rocket.explosion = Explosion(rocket.x, rocket.y)
    rocket.colidiu = True

def create_gradient_surface(width, height, background_color):
    # Create a new surface with the same dimensions as the screen
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for y in range(height):
        # Calculate alpha from 0 at the top to 128 at the bottom
        alpha = int(255 * (y / height) / 2)  # 128 is 50% transparency (255 = opaque, 0 = transparent)
        
        # Create a color with the desired alpha value (RGBA)
        color = background_color + (alpha,)
        
        # Draw a line across the surface with the calculated transparency
        pygame.draw.line(gradient_surface, color, (0, y), (width, y))
    
    return gradient_surface


def game(planet):
    # Initializes the game 
    global GRAVIDADE, DENSIDADE_AR, PAD_COLOR
    GRAVIDADE = planet.gravity
    DENSIDADE_AR = planet.density
    PAD_COLOR = planet.pad_color

    gradient_background = create_gradient_surface(LARGURA, ALTURA, PAD_COLOR)

    rocket = Rocket()
    running = True # Controls game loop 
    landing_pad = pygame.Rect(LARGURA / 2 - 50, ALTURA - 10, 100, 10)
    game_over = False
    landed = False # if the rocket has landed 
    global click
    click = False
    qtd_impulsos = 2 # numeber of thrust impulses 

    while running:
        screen.fill(PRETO)
        screen.blit(gradient_background, (0, 0))
        
        for star in stars:
            star.speed = 0
            star.update()
            star.draw(screen)
        
        for event in pygame.event.get():
            # If the player closes the window, the game ends 
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # If the player presses escape, the game ends 
                if event.key == pygame.K_ESCAPE:
                    menu()
                if event.key == pygame.K_SPACE and qtd_impulsos:
                    qtd_impulsos -= 1
                    rocket.aplicar_impulso()
            # Tracks mouse's clicks 
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        
        keys = pygame.key.get_pressed()
        
        if not game_over:
            # Rotate the rocket with keyboard arrows  
            if keys[pygame.K_LEFT]:
                rocket.rotate_left()
            if keys[pygame.K_RIGHT]:
                rocket.rotate_right()
            # Q and E adjust the rocket's throttle 
            if keys[pygame.K_q]:
                rocket.throtle(-0.01)
            elif keys[pygame.K_e]:
                rocket.throtle(0.01)
            # A terminates the flight (end game)            
            if keys[pygame.K_a]:
                end_game(rocket, "Flight Terminated", True)
                game_over = True
            

            
        rocket.update()

        rocket_points = [
            (rocket.x - rocket.largura / 2, rocket.y - rocket.altura / 2),
            (rocket.x + rocket.largura / 2, rocket.y - rocket.altura / 2),
            (rocket.x + rocket.largura / 2, rocket.y + rocket.altura / 2),
            (rocket.x - rocket.largura / 2, rocket.y + rocket.altura / 2)
        ]

        if not game_over:
            for x, y in rocket_points:
                # Checks if the rocket has collided with the landing pad 
                if landing_pad.collidepoint(x, y):
                    rocket.colidiu = True
                    font = pygame.font.Font(None, 74)

                    # Verifies with the rocket's speed is not so fast 
                    if abs(math.sqrt(rocket.vx**2 + rocket.vy**2)) < 50:
                        # The rocket lands correctly if its speed and its angle are adequate 
                        if abs(rocket.angulo) < math.pi/6:
                            end_game(rocket, "Landed!", False)
                            landed = True
                        # The angle is not within 30 degrees 
                        else:
                            end_game(rocket, "Toppled :(", True)
                    else:
                        end_game(rocket, f"Crashed at {int(math.sqrt(rocket.vx**2 + rocket.vy**2))}km/h", True)

                    game_over = True

        # The game ends if the rocket falls without landing on the site 
        if rocket.y > 590 and not game_over:
            end_game(rocket, "Missed landing site", True)
            game_over = True

        if rocket.explosion is None:
            # Draws trajectory, flame and rocket 
            rocket.desenhar_trajetoria(screen)
            rocket.draw_flame(screen)
            rocket.draw(screen)
            """
            # Draw the "Back to Menu" button
            back_button_rect = draw_back_to_menu_button(screen)

            # Check if the back button was clicked
            mx, my = pygame.mouse.get_pos()
            if back_button_rect.collidepoint(mx, my):
                if click:
                    menu()
            """
        draw_landing_pad(screen)

        if game_over:
            if rocket.explosion:
                rocket.explosion.update()
                rocket.explosion.draw(screen)
                if rocket.explosion.is_done():
                    # Display the end message after the explosion is done and restarts the game     
                    font = pygame.font.Font(None, 74)
                    text = font.render(rocket.message, True, BRANCO)
                    text_rect = text.get_rect(center=(LARGURA / 2, ALTURA / 2))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(1300)
                    #print("explosion is done")
                    running = False
                    game(planet)
            # If there's no explosion, displays the message and restats the game 
            else:
                font = pygame.font.Font(None, 74)
                text = font.render(rocket.message, True, BRANCO)
                text_rect = text.get_rect(center=(LARGURA / 2, ALTURA / 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)
                game(planet)

        
        pygame.display.flip()

    pygame.quit()

class Star:
    """
    Class that represent the stars shown in the menu 
    """
    def __init__(self):
        self.x = random.randint(0, LARGURA)
        self.y = random.randint(0, ALTURA)
        self.size = random.uniform(1, 2.2)
        self.speed = random.uniform(0.7, 2.7)  # Falling speed
        self.max_speed = self.speed
        self.is_slowing = False
        self.is_moving = True
        self.speeding_up = False
        self.brightness = random.randint(200, 255)
        self.twinkle_speed = random.uniform(20, 80)

    def update(self):
        """
        Updates the speed of the stars and its position 
        """
        if self.speed == 0:
            self.is_slowing = False
            self.is_moving = False

        if self.is_slowing:
            self.speed *= 0.98
            if abs(self.speed) < 0.005:
                self.speed = 0

        if self.is_moving:
            self.y += self.speed
            if self.y > ALTURA:  # Reset the star to the top when it reaches the bottom
                self.y = random.randint(-ALTURA, 0)
                self.x = random.randint(0, LARGURA)
                self.size = random.randint(1, 2)
                self.speed = random.uniform(0.7, 2.7)

        if self.speeding_up:
            self.speed *= 1.04
            if self.speed > self.max_speed:
                self.speed = self.max_speed
                self.speeding_up = False
        self.brightness += self.twinkle_speed
        if self.brightness >= 255 or self.brightness <= 200:
            self.twinkle_speed *= -1  # Reverse direction of brightness change
        self.brightness = max(100, min(255, self.brightness))  # Clamp after updating


    def draw(self, surface):
        """
        Draw the stars 
        """
        # Ensure brightness is within valid range
        bright_color = (int(self.brightness), int(self.brightness), int(self.brightness))  # Adjust color based on brightness
        pygame.draw.circle(surface, bright_color, (self.x, int(self.y)), int(self.size))

    def slowdown(self):
        """
        Changes the status, so the stars slow down 
        """
        self.is_slowing = True

    def speed_up(self):
        self.speed = random.uniform(0.1, 0.2)
        self.is_moving = True
        self.speeding_up = True



def title_screen():
    # Create a list of stars
    global stars
    stars = [Star() for _ in range(100)]  # 100 stars
    global click
    click = False

    while True:
        screen.fill(PRETO)
        # Update and draw the stars 
        for star in stars:
            star.update()
            star.draw(screen)

        # Display the title 
        title_text = 'Suicide Burn'
        title_surface = font_h1.render(title_text, True, BRANCO)
        title_rect = title_surface.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
        screen.blit(title_surface, title_rect)

        # Display the sub-title 
        subtext = 'Press SPACE or click to start'
        subtext_surface = pygame.font.SysFont(None, 40).render(subtext, True, (150, 150, 150))
        subtext_rect = subtext_surface.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
        screen.blit(subtext_surface, subtext_rect)
       
        # Handle user input to determine whether to start ou exit program 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE or event.key == K_RETURN:
                    menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu(stars)

            
        # Updates the screen at 60 frames per second 
        pygame.display.update()
        clock.tick(60)

def menu():
    global click
    click = False

    button_width, button_height = 200, 60
    button_y_spacing = 30
    button_color_normal = (50, 50, 50)  # Dark gray
    button_color_hover = (100, 100, 100)  # Lighter gray
    text_color = (BRANCO)

    planets = create_planets()
    planet_list = list(planets.values())

    buttons = [
    {
        "text": planet.name,
        "action": lambda p=planet: transition(p)
    }
    for planet in planet_list
    ]

    # Calculate button positions in two rows
    button_rects = []
    for col in range(2):
        # Calculate the total height of buttons in this column
        total_column_height = len(buttons) // 2 * button_height + (len(buttons) // 2 - 1) * button_y_spacing
       
        # Starting y position to center the column vertically
        start_y = (ALTURA - total_column_height) // 2 + 50
       
        for row in range(3):
            # Calculate index in the buttons list
            index = col * 3 + row
           
            # Create button rect
            button_rect = pygame.Rect(
                LARGURA // 4 * (1 + col * 1.5) - button_width // 2 + 50,  # Center each column horizontally
                start_y + row * (button_height + button_y_spacing),
                button_width,
                button_height
            )
            button_rects.append((button_rect, buttons[index]))

    # Main menu loop
    while True:
        screen.fill(PRETO)
        for star in stars:
            if not star.is_moving:
                star.speed_up()
            star.update()
            star.draw(screen)
        
        title_text = 'Select planet'
        title_surface = pygame.font.SysFont(None, 60).render(title_text, True, BRANCO)
        title_rect = title_surface.get_rect(center=(LARGURA // 2, ALTURA // 4))
        screen.blit(title_surface, title_rect)
        
        mx, my = pygame.mouse.get_pos()
        
        # Draw and handle buttons
        for button_rect, button in button_rects:
            # Determine button color (hover or normal)
            current_color = button_color_hover if button_rect.collidepoint((mx, my)) else button_color_normal
           
            # Draw button
            pygame.draw.rect(screen, current_color, button_rect, border_radius=10)
           
            # Render button text
            text_surface = font_text.render(button['text'], True, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_BACKSPACE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button_rect, button in button_rects:
                        if button_rect.collidepoint((mx, my)):
                            button['action']()
        
        pygame.display.update()
        clock.tick(60)

def transition(planet):
    sky_static = False
    while True:
        screen.fill(PRETO)
        stars_stopped = True
        for star in stars:
            if not sky_static:
                star.slowdown()
            star.update()
            star.draw(screen)

        if abs(star.speed) > 0.1:
                stars_stopped = False
        else:
            stars_stopped = True

        # If all stars have stopped, transition to game
        if stars_stopped:
            return game(planet)

        text = 'Get ready to land on ' + planet.name
        text_surface = pygame.font.SysFont(None, 70).render(text, True, (150, 150, 150))
        text_rect = text_surface.get_rect(center=(LARGURA // 2, ALTURA // 2))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_BACKSPACE:
                    return
                
        pygame.display.update()  # Update display each frame
        clock.tick(60)  # Limit frame rate

if __name__ == "__main__":
    pygame.mixer.music.play(loops=-1)
    title_screen()
