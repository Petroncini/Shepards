import math
import random
import sys
import time

import pygame
from pygame.locals import *

pygame.init()

LARGURA, ALTURA = 800, 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Rocket Landing Game")
#setting font settings
font_text = pygame.font.SysFont(None, 30)
font_h1 = pygame.font.SysFont(None, 80)
clock = pygame.time.Clock()

# A variable to check for the status later
click = False

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

GRAVIDADE = 9.8  #m/s^2
IMPULSO = 7600000    #kg*m/s^2
RAPIDEZ_ROTACAO = 2 #RAD/s
MAX_COMBUSTIVEL = 100
FATOR_ESCALA = 1
VISCOSIDADE_AR = 1.225
RESISTENCIA_AR = 50 #na verdade é b
COEFICIENTE_ARRASTO = 5
FUEL_WEIGHT = 1500
DRY_MASS = 22000

VELOCIDADE_INICIAL = random.uniform(150, 200)

"""
A function that can be used to write text on our screen and buttons
"""
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_back_to_menu_button(screen):
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

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0
        self.color = pygame.Color(random.randint(200, 255), random.randint(50, 150), 0, 150)
        self.a = 150
        self.expansion_rate = random.randrange(7, 15)

    def update(self):
        self.r += self.expansion_rate
        self.expansion_rate -= 0.05
        self.a -= 1
        if self.color.a > 0:
            self.color.a -= 1
        else:
            self.color.a = 0

    def draw(self, screen):
        superfice = pygame.Surface((2*ALTURA, 2*LARGURA), pygame.SRCALPHA)
        pygame.draw.circle(superfice, self.color, center=(self.x, self.y), radius = self.r)
        screen.blit(superfice, (0, 0))



class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.clouds = []
        for _ in range(10):
            self.clouds.append(Cloud(self.x + random.randrange(1, 50), self.y + random.randrange(1, 50)))
    
    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def draw(self, screen):
        for cloud in self.clouds:
            cloud.draw(screen)

    def is_done(self):
        if(self.clouds[0].a == -30):
            return True
        else:
            return False




class Rocket:
    def __init__(self):
        self.x = LARGURA / 2
        self.y = ALTURA / 4
        self.angulo = random.uniform(-(math.pi)/4 ,(math.pi)/4)  # Angle in radians
        self.rapidez = VELOCIDADE_INICIAL
        self.vx = math.cos(self.angulo + (math.pi/2)) * self.rapidez     # Horizontal velocity
        self.vy = math.sin(self.angulo + (math.pi/2)) * self.rapidez     # Vertical velocity
        self.x -= self.vx * 0.01
        self.y -= self.vy * 0.01
        self.combustivel = MAX_COMBUSTIVEL
        self.massa = DRY_MASS + self.combustivel * FUEL_WEIGHT
        self.cor = BRANCO
        self.colidiu = False
        self.impulsionando = False
        self.acelerador = 1
        self.altura = 12
        self.largura = 5
        self.ingnited = False
        self.explosion = None
        self.message = None
        self.last_time_update = time.perf_counter()

    def aplicar_impulso(self):
        if not self.ingnited:
            self.ingnited = True
            self.impulsionando = True
        else:
            self.impulsionando = False
            self.ingnited = False

    def update_color(self, color):
        self.cor = color

    def rotate_left(self):
        current_time = time.perf_counter()
        dt = (current_time - self.last_time_update)

        self.angulo -= RAPIDEZ_ROTACAO * dt

    def rotate_right(self):
        current_time = time.perf_counter()
        dt = (current_time - self.last_time_update)

        self.angulo += RAPIDEZ_ROTACAO * dt

    def update(self):
        current_time = time.perf_counter()
        dt = (current_time - self.last_time_update)
        self.last_time_update = current_time
        print(f"dt: {dt}")

        if not self.colidiu:
            self.vy += GRAVIDADE * dt

            self.x += self.vx * FATOR_ESCALA * dt
            self.y += self.vy * FATOR_ESCALA * dt

            forca_viscosa_x = -self.vx * RESISTENCIA_AR * dt
            forca_viscosa_y = -self.vy * RESISTENCIA_AR * dt
            self.vx += (forca_viscosa_x / self.massa)
            self.vy += (forca_viscosa_y / self.massa)


            if self.x < 0:
                self.x = 0
                self.vx = 0
            if self.x > LARGURA:
                self.x = LARGURA
                self.vx = 0
            if self.y > ALTURA:
                self.y = ALTURA
                self.vy = 0

            if self.impulsionando and not self.colidiu:
                if self.combustivel > 0:
                    forca_x = IMPULSO * self.acelerador * math.sin(self.angulo) * dt
                    forca_y = -IMPULSO * self.acelerador * math.cos(self.angulo) * dt
                    
                    self.vx += (forca_x / self.massa)
                    self.vy += (forca_y / self.massa)
                    self.combustivel -= 10 * self.acelerador * dt
                    self.massa = max(0, DRY_MASS + self.combustivel * FUEL_WEIGHT)
                    self.impulsionando = True


    def draw_flame(self, screen):
        if self.impulsionando and self.combustivel > 0:  # Only draw flame if thrust is applied
            flame_base_x = self.x - math.sin(self.angulo) * 6
            flame_base_y = self.y + math.cos(self.angulo) * 6
            flame_length = random.randint(5, int(200*self.acelerador) + 5)  # Vary flame length to simulate flicker

            flame_tip_x = flame_base_x - math.sin(self.angulo) * flame_length
            flame_tip_y = flame_base_y + math.cos(self.angulo) * flame_length

            flame_color = (random.randint(50, 150), random.randint(50, 100), random.randint(100, 255))  # Yellow-orange flicker
            pygame.draw.polygon(screen, flame_color, [
                (flame_base_x - 2*math.cos(self.angulo), flame_base_y - 2*math.sin(self.angulo),), 
                (flame_base_x + 2*math.cos(self.angulo), flame_base_y + 2*math.sin(self.angulo),),
                (flame_tip_x, flame_tip_y) 
            ])

    def draw(self, screen):

        points = [
            (self.x - self.largura / 2, self.y - self.altura / 2),
            (self.x + self.largura / 2, self.y - self.altura / 2),
            (self.x + self.largura / 2, self.y + self.altura / 2),
            (self.x - self.largura / 2, self.y + self.altura / 2)
        ]

        rotated_points = []
        for px, py in points:
            new_x = (px - self.x) * math.cos(self.angulo) - (py - self.y) * math.sin(self.angulo) + self.x
            new_y = (px - self.x) * math.sin(self.angulo) + (py - self.y) * math.cos(self.angulo) + self.y
            rotated_points.append((new_x, new_y))

        pygame.draw.polygon(screen, self.cor, rotated_points)

        font = pygame.font.Font(None, 36)
        fuel_text = font.render(f"Fuel: {int(self.combustivel)}", True, BRANCO)
        speed_text = font.render(f"Speed: {int(math.sqrt(self.vx**2 + self.vy**2))}", True, BRANCO)
        angle_text = font.render(f"Angle: {int((-1*self.angulo) * (180/math.pi) + 90)}", True, BRANCO)
    
        screen.blit(fuel_text, (10, 10))
        screen.blit(speed_text, (10, 40))
        screen.blit(angle_text, (10, 70))

    def throtle(self, delta):
        self.acelerador = abs(self.acelerador + (delta * 0.1))
        self.acelerador = max(min(self.acelerador, 1), 0.05)

    def desenhar_trajetoria(self, screen):
        dt = 1
        x_futuro = self.x
        y_futuro = self.y
        vx_futuro = self.vx
        vy_futuro = self.vy

        pontos_trajetoria = []
        pontos_trajetoria.append((int(x_futuro), int(y_futuro)))

        while True:
            vy_futuro += GRAVIDADE * dt
            x_futuro += vx_futuro * FATOR_ESCALA * dt
            y_futuro += vy_futuro * FATOR_ESCALA * dt
            vx_futuro += (-vx_futuro * RESISTENCIA_AR)/self.massa * dt
            vy_futuro += (-vy_futuro * RESISTENCIA_AR )/self.massa* dt


            pontos_trajetoria.append((int(x_futuro), int(y_futuro)))

            if y_futuro > ALTURA or y_futuro < 0 or x_futuro > (2*LARGURA) or x_futuro < 0:
                break

            dt += 0.01

        
        if len(pontos_trajetoria) > 1:
            superfice = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            cor = pygame.Color(255, 0, 0, 100)
            pygame.draw.lines(superfice, cor, False, pontos_trajetoria, 2)
            screen.blit(superfice, (0, 0))

def draw_landing_pad(screen):
    pad_width = 100
    pad_height = 10
    pad_x = LARGURA / 2 - pad_width / 2
    pad_y = ALTURA - pad_height
    pygame.draw.rect(screen, VERDE, (pad_x, pad_y, pad_width, pad_height))


def end_game(rocket, message, exploded):
    rocket.message = message
    if exploded:
        rocket.explosion = Explosion(rocket.x, rocket.y)
    rocket.colidiu = True


def game():
    rocket = Rocket()
    print(rocket.explosion)
    running = True
    landing_pad = pygame.Rect(LARGURA / 2 - 50, ALTURA - 10, 100, 10)
    game_over = False
    landed = False
    global click
    click = False
    qtd_impulsos = 2

    while running:
        # print(f"rocket at {rocket.x},{rocket.y} vel: {rocket.vx},{rocket.vy}")
        screen.fill(PRETO)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and qtd_impulsos:
                    qtd_impulsos -= 1
                    rocket.aplicar_impulso()
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        
        keys = pygame.key.get_pressed()
        
        if not game_over:
            if keys[pygame.K_LEFT]:
                rocket.rotate_left()
            if keys[pygame.K_RIGHT]:
                rocket.rotate_right()

            if keys[pygame.K_q]:
                rocket.throtle(-0.01)

            elif keys[pygame.K_e]:
                rocket.throtle(0.01)

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
                if landing_pad.collidepoint(x, y):
                    rocket.colidiu = True
                    font = pygame.font.Font(None, 74)

                    if abs(math.sqrt(rocket.vx**2 + rocket.vy**2)) < 50:
                        if abs(rocket.angulo) < math.pi/6:
                            end_game(rocket, "Landed!", False)
                            landed = True
                        else:
                            end_game(rocket, "Toppled :(", True)

                    else:
                        end_game(rocket, f"Crashed at {int(math.sqrt(rocket.vx**2 + rocket.vy**2))}km/h", True)

                    game_over = True




        if rocket.y > 590 and not game_over:
            end_game(rocket, "Missed landing site", True)
            game_over = True

        if rocket.explosion is None:
            rocket.desenhar_trajetoria(screen)
            rocket.draw_flame(screen)
            rocket.draw(screen)
            # Draw the "Back to Menu" button
            back_button_rect = draw_back_to_menu_button(screen)

            # Check if the back button was clicked
            mx, my = pygame.mouse.get_pos()
            if back_button_rect.collidepoint(mx, my):
                if click:
                    menu()
        draw_landing_pad(screen)

        if game_over:
            if rocket.explosion:
                rocket.explosion.update()
                rocket.explosion.draw(screen)
                if rocket.explosion.is_done():
                    # Display the end message after the explosion is done
                    font = pygame.font.Font(None, 74)
                    text = font.render(rocket.message, True, BRANCO)
                    text_rect = text.get_rect(center=(LARGURA / 2, ALTURA / 2))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    print("explosion is done")
                    running = False
                    game()
            else:
                font = pygame.font.Font(None, 74)
                text = font.render(rocket.message, True, BRANCO)
                text_rect = text.get_rect(center=(LARGURA / 2, ALTURA / 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)
                game()



        
        pygame.display.flip()

    pygame.quit()

class Star:
    def __init__(self):
        self.x = random.randint(0, LARGURA)
        self.y = random.randint(-ALTURA, 0)  # Start above the screen
        self.size = random.randint(1, 3)
        self.speed = random.uniform(1, 2)  # Falling speed
        self.is_slowing = False

    def update(self):
        if self.is_slowing:
            # Exponential slowdown
            self.speed *= 0.97
            if abs(self.speed) < 0.005:
                self.speed = 0

        self.y += self.speed
        if self.y > ALTURA:  # Reset the star to the top when it reaches the bottom
            self.y = random.randint(-ALTURA, 0)
            self.x = random.randint(0, LARGURA)
            self.size = random.randint(1, 3)
            self.speed = random.uniform(1, 3)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 200), (self.x, int(self.y)), self.size)

    def slowdown(self):
        self.is_slowing = True

def title_screen():
    # Create a list of stars
    stars = [Star() for _ in range(80)]  # 100 stars
    global click
    click = False

    while True:
        screen.fill(PRETO)
        for star in stars:
            star.update()
            star.draw(screen)

        title_text = 'Suicide Burn'
        title_surface = font_h1.render(title_text, True, BRANCO)
        title_rect = title_surface.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
        screen.blit(title_surface, title_rect)

        subtext = 'Press SPACE or click to start'
        subtext_surface = pygame.font.SysFont(None, 40).render(subtext, True, (150, 150, 150))
        subtext_rect = subtext_surface.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
        screen.blit(subtext_surface, subtext_rect)
       
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_SPACE or event.key == K_RETURN:
                    menu(stars)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu(stars)

            

        pygame.display.update()
        clock.tick(60)

def menu(stars):
    global click
    click = False

    button_width, button_height = 200, 60
    button_y_spacing = 30
    button_color_normal = (50, 50, 50)  # Dark gray
    button_color_hover = (100, 100, 100)  # Lighter gray
    text_color = (BRANCO)

    # Define buttons
    buttons = [
        {"text": "Button 1", "action": planet1},
        {"text": "Button 2", "action": planet2},
        {"text": "Button 3", "action": planet3},
        {"text": "Button 4", "action": planet4},
        {"text": "Button 5", "action": planet5},
        {"text": "Button 6", "action": planet6}
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
                            transition(button['action'], button['text'], stars)()
        
        pygame.display.update()
        clock.tick(60)

def transition(planet, planet_name, stars):
    sky_static = False
    while True:
        screen.fill(PRETO)
        stars_stopped = True
        for star in stars:
            if not sky_static:
                star.slowdown()
            star.update()
            star.draw(screen)

        # if not stars_stopped:
        #     # Slow down stars
        #     for star in stars:
        #         star.slow()
            
        #     # Check if all stars have stopped
        #     stars_stopped = all(star.speed == 0 for star in stars)

        #     for star in stars:
        #         star.update()
        #         star.draw(screen)

        if abs(star.speed) > 0.1:
                stars_stopped = False
        else:
            stars_stopped = True

        # If all stars have stopped, transition to game
        if stars_stopped:
            return game()

        text = 'Get ready to land on ' + planet_name
        text_surface = pygame.font.SysFont(None, 70).render(text, True, (100, 100, 100))
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

def planet1():
    game()

def planet2():
    game()

def planet3():
    game()

def planet4():
    game()

def planet5():
    game()

def planet6():
    game()

if __name__ == "__main__":
    title_screen()
