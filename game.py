import pygame
import random
import math

class Ship:
    def __init__(self, position, max_velocity, drag_constant, shield, max_shield, health, max_health, bounds, dimensions, image):
        self.position = position
        self.velocity = 0
        self.max_velocity = max_velocity

        self.tilt = 0

        self.drag_constant = drag_constant

        self.shield = shield
        self.max_shield = max_shield
        self.health = health
        self.max_health = max_health

        self.bounds = bounds

        self.dimensions = dimensions

        self.image = pygame.transform.scale(image, self.dimensions)


    def update_motion(self):
        if not self.sfp_on:
            if abs(self.velocity + self.acceleration) >= self.max_velocity:
                if self.velocity + self.acceleration < 0:
                    self.velocity = -self.max_velocity
                else:
                    self.velocity = self.max_velocity
                    self.acceleration = 0
            else:
                self.velocity += self.acceleration

            self.velocity -= self.drag_constant * self.velocity

            if self.bounds[0] <= self.position + self.velocity <= self.bounds[1]:
                self.position += self.velocity
            else:
                if self.position + self.velocity < self.bounds[0]:
                    self.position = self.bounds[0]
                    self.velocity = 0
                    self.acceleration = 0
                else:
                    self.position = self.bounds[1] 
                    self.velocity = 0
                    self.acceleration = 0

        else:
            self.velocity = self.acceleration #*constant

            if self.bounds[0] <= self.position + self.velocity <= self.bounds[1]:
                self.position += self.velocity
            else:
                if self.position + self.velocity < self.bounds[0]:
                    self.position = self.bounds[0]
                    self.velocity = 0
                    self.acceleration = 0
                else:
                    self.position = self.bounds[1]   
                    self.velocity = 0
                    self.acceleration = 0           


    def update_health(self, hit, damage = 0):
        if hit:
            if self.shield - damage >= 0 and self.shield > 0:
                self.shield -= damage
            
            elif self.shield - damage <= 0 and self.shield > 0:
                self.shield = 0

            else:
                self.health -= 1

        else:
            if self.shield < self.max_shield:
                self.shield += 1 / 30


    def render(self, screen):
        if self.tilt < 0:
            self.tilt = max(-12, self.tilt - 1.8 * self.acceleration - 0.05 * self.tilt)
        else:
            self.tilt = min(12, self.tilt - 1.8 * self.acceleration - 0.05 * self.tilt)

        screen.blit(pygame.transform.rotate(self.image, self.tilt), (self.position, 450)) 


    def game_tick(self, acceleration, hit, damage, sfp_on, screen):
        self.acceleration = acceleration
        self.sfp_on = sfp_on

        self.update_motion()

        self.update_health(hit, damage)

        self.render(screen)


class ParticleBeam:
    def __init__(self, position, velocity, bounds_x, bounds_y, damage, dimensions, image):
        self.position = position
        self.velocity = velocity
        self.relativistic_velocity = self.velocity

        self.bounds_x = bounds_x
        self.bounds_y = bounds_y

        self.damage = damage

        self.dimensions = dimensions
        self.relativistic_dimensions = self.dimensions

        self.image = image

        self.exists = True


    def update_motion(self):
        if self.bounds_x[0] < self.position[0] + self.relativistic_velocity[0] < self.bounds_x[1]:
            self.position[0] += self.relativistic_velocity[0]
        else:
            if self.position[0] + self.relativistic_velocity[0] < self.bounds_x[0]:
                self.position[0] = self.bounds_x[0]
                self.exists = False
            else:
                self.position[0] = self.bounds_x[1]
                self.exists = False 

        if self.bounds_y[0] < self.position[1] + self.relativistic_velocity[1] < self.bounds_y[1]:
            self.position[1] += self.relativistic_velocity[1]

        else:
            if self.position[1] + self.relativistic_velocity[1] < self.bounds_y[0]:
                self.exists = False
            else:
                self.exists = False

    
    def render(self, screen):
        screen.blit(pygame.transform.scale(self.image, self.relativistic_dimensions), self.position)


    def game_tick(self, screen):
        self.update_motion()

        self.render(screen)


class Enemy:
    def __init__(self, position, health, dimensions, image):
        self.position = position

        self.health = health

        self.dimensions = dimensions
        self.relativistic_dimensions = self.dimensions

        self.image = image

        self.firing = False

        self.exists = True


    def fire(self):
        if random.random() < 0.006:
            self.firing = True

    
    def render(self, screen):
        screen.blit(pygame.transform.scale(self.image, self.relativistic_dimensions), self.position)
        

    def game_tick(self, screen):
        self.firing = False

        self.fire()

        self.render(screen)


def calculate_gamma_parallel(velocity1, velocity2): #velocities are expressed in tenths of c
    velocity1 = abs(velocity1) / 10
    velocity2 = abs(velocity2) / 10

    combined_velocity = (velocity1 + velocity2) / (1 + velocity1 * velocity2) 

    gamma = 1 / math.sqrt(1 - combined_velocity ** 2)

    return gamma


def calculate_gamma_perpendicular(velocity1, velocity2): #velocities are expressed in tenths of c
    velocity1 = abs(velocity1) / 10
    velocity2 = abs(velocity2) / 10

    combined_velocity = math.sqrt(velocity1 ** 2 + velocity2 ** 2 - velocity1 ** 2 * velocity2 ** 2)

    gamma = 1 / math.sqrt(1 - combined_velocity ** 2)

    return gamma



if __name__ == '__main__':
    pygame.init()

    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    font_small = pygame.font.Font('assets/orbitron.ttf', 16)
    font_medium = pygame.font.Font('assets/orbitron.ttf', 25)
    font_big = pygame.font.Font('assets/orbitron.ttf', 48)

    pygame.display.set_caption('Relativistic Space Invaders')

    bg = pygame.transform.scale(pygame.image.load('assets/bg.png'), (screen_width, screen_height))

    player_img = pygame.image.load('assets/ship.png')
    player_dim = [150, 100]
    player_inputs = {'position': screen_width // 2 - player_dim[0] // 2, "max_velocity": 9, "drag_constant": 0.01, "shield": 10, "max_shield": 10, "health": 3, "max_health": 3, "bounds": [0, screen_width - player_dim[0]], "dimensions": player_dim, "image": player_img}
    player = Ship(**player_inputs)

    enemy_img = pygame.image.load('assets/alien.png')
    enemy_dim = [50, 50]
    num_enemies = 10
    enemies = []
    for i in range(num_enemies):
        enemy_inputs = {'position': [i * (enemy_dim[0] + 30) + (screen_width - num_enemies * (enemy_dim[0] + 30)) // 2, 250], 'health': 1, 'dimensions': enemy_dim, 'image': enemy_img}
        enemies.append(Enemy(**enemy_inputs))

    fire_cooldown = 600 #milliseconds
    last_time_fired = -fire_cooldown
    particle_beam_dim = [18, 18]
    particle_beam_player_img = pygame.image.load('assets/particle_beam_player.png')
    particle_beam_enemy_img = pygame.image.load('assets/particle_beam_enemy.png')
    particle_beams = []

    shield_img = pygame.transform.scale(pygame.image.load('assets/shield.png'), (40, 42))
    shield_bar_img = pygame.transform.scale(pygame.image.load('assets/shield_bar.png'), (16, 42)) 
    lost_shield_bar_img = pygame.transform.scale(pygame.image.load('assets/lost_shield_bar.png'), (16, 42)) 

    clock = pygame.time.Clock()

    game_over = False
    instructions_over = False
    dead = False

    keys_down = {'L': False, 'R': False, 'SPACE': False}

    while not game_over:
        clock.tick(30)

        screen.blit(bg, (0, 0))

        title = font_medium.render('Relativistic Space Invaders', True, (4, 217, 255))
        screen.blit(title, (620, 10))

        credit = font_small.render('Jaden Mu', True, (4, 217, 255))
        screen.blit(credit, (900, 40))

        if not instructions_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        instructions_over = True

            instructions_text1 = font_medium.render('USE ARROW KEYS TO MOVE. USE SPACE TO SHOOT.', True, (4, 217, 255))
            instructions_rect1 = instructions_text1.get_rect()
            instructions_rect1.center = (screen_width // 2, screen_height // 2 - 50)

            instructions_text2 = font_small.render('THE FASTER YOU MOVE, THE SLOWER AND THINNER EVERYTHING ELSE GETS.', True, (4, 217, 255))
            instructions_rect2 = instructions_text2.get_rect()
            instructions_rect2.center = (screen_width // 2, screen_height // 2)
            
            instructions_text3 = font_medium.render('HIT SPACE TO START.', True, (4, 217, 255))
            instructions_rect3 = instructions_text3.get_rect()
            instructions_rect3.center = (screen_width // 2, screen_height // 2 + 50)

            screen.blit(instructions_text1, instructions_rect1)
            screen.blit(instructions_text2, instructions_rect2)
            screen.blit(instructions_text3, instructions_rect3)

        if not dead and instructions_over:
            screen.blit(shield_img, (10, 10))
            for i in range(1, player.max_shield + 1):
                if i < math.floor(player.shield) + 1:
                    screen.blit(shield_bar_img, (42 + 16 * i, 10))
                else:
                    screen.blit(lost_shield_bar_img, (42 + 16 * i, 10))

            player_updates = {'acceleration': 0, 'hit': False, 'damage': 0, 'sfp_on': False, 'screen': screen}

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        keys_down['L'] = True

                    elif event.key == pygame.K_RIGHT:
                        keys_down['R'] = True

                    elif event.key == pygame.K_SPACE:
                        keys_down['SPACE'] = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        keys_down['L'] = False

                    elif event.key == pygame.K_RIGHT:
                        keys_down['R'] = False

                    elif event.key == pygame.K_SPACE:
                        keys_down['SPACE'] = False 

            if keys_down['L']:
                player_updates['acceleration'] -= 0.2

            if keys_down['R']:
                player_updates['acceleration'] += 0.2     

            if keys_down['SPACE']:
                if pygame.time.get_ticks() - last_time_fired > fire_cooldown:
                    last_time_fired = pygame.time.get_ticks()
                    particle_beam_inputs = {'position': [player.position + (player.dimensions[0] - particle_beam_dim[0]) // 2, 450], 'velocity': (0, -3), 'bounds_x': (0, screen_width - particle_beam_dim[0]), 'bounds_y': (0, screen_height - particle_beam_dim[1]), 'damage': 5, 'dimensions': particle_beam_dim, 'image': particle_beam_player_img}
                    particle_beams.append(ParticleBeam(**particle_beam_inputs))


            enemies = [enemy for enemy in enemies if enemy.exists]
            for enemy in enemies:
                if enemy.exists:
                    enemy.game_tick(screen)

                    enemy.relativistic_dimensions = [round(enemy.dimensions[0] / calculate_gamma_parallel(player.velocity, 0)), enemy.dimensions[1]]

                    if enemy.firing:
                        particle_beam_inputs = {'position': [enemy.position[0] + enemy.relativistic_dimensions[0] // 2 - particle_beam_dim[0] // 2, enemy.position[1] + enemy.relativistic_dimensions[1] // 2 - particle_beam_dim[1] // 2], 'velocity': (0, 3), 'bounds_x': (0, screen_width - particle_beam_dim[0]), 'bounds_y': (0, screen_height - particle_beam_dim[1]), 'damage': 5, 'dimensions': particle_beam_dim, 'image': particle_beam_enemy_img}
                        particle_beams.append(ParticleBeam(**particle_beam_inputs))

            particle_beams = [particle_beam for particle_beam in particle_beams if particle_beam.exists]
            for particle_beam in particle_beams:
                if particle_beam.exists:
                    particle_beam.game_tick(screen)

                    particle_beam.relativistic_dimensions = [round(particle_beam.dimensions[0] / calculate_gamma_parallel(player.velocity, 0)), particle_beam.dimensions[1]]
                    particle_beam.relativistic_velocity = [round(particle_beam.velocity[0] / calculate_gamma_perpendicular(player.velocity, particle_beam.velocity[1])), round(particle_beam.velocity[1] / calculate_gamma_perpendicular(player.velocity, particle_beam.velocity[1]))]

                    if particle_beam.relativistic_velocity[1] > 0:
                        if particle_beam.position[1] < 450 + player.dimensions[1] and particle_beam.position[1] + particle_beam.relativistic_dimensions[1] > 450 + player.dimensions[1] // 3:
                            if particle_beam.position[0] < player.position + player.dimensions[0] and particle_beam.position[0] + particle_beam.relativistic_dimensions[0] > player.position:
                                particle_beam.exists = False
                                player_updates['hit'] = True
                                player_updates['damage'] = 3
                                

                    elif particle_beam.relativistic_velocity[1] < 0:
                        for enemy in enemies:
                            if particle_beam.position[1] < enemy.position[1] + enemy.relativistic_dimensions[1] and particle_beam.position[1] + particle_beam.relativistic_dimensions[1] > enemy.position[1] :
                                if particle_beam.position[0] < enemy.position[0] + enemy.relativistic_dimensions[0] and particle_beam.position[0] + particle_beam.relativistic_dimensions[0] > enemy.position[0]:
                                    particle_beam.exists = False
                                    enemy.exists = False

            player.game_tick(**player_updates)

            if player.shield <= 0 or len(enemies) == 0:
                dead = True

        if dead and instructions_over:
            end_text = font_big.render('GAME OVER', True, (4, 217, 255))
            end_text_rect = end_text.get_rect()
            end_text_rect.center = (screen_width // 2, screen_height // 2)

            end_instructions = font_medium.render('HIT SPACE TO PLAY AGAIN', True, (4, 217, 255))
            end_instructions_rect = end_instructions.get_rect()
            end_instructions_rect.center = (screen_width // 2, screen_height // 2 + 50)

            screen.blit(end_text, end_text_rect)
            screen.blit(end_instructions, end_instructions_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        game_over = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        keys_down = {'L': False, 'R': False, 'SPACE': False}
                        
                        player_inputs = {'position': screen_width // 2 - player_dim[0] // 2, "max_velocity": 9, "drag_constant": 0.01, "shield": 10, "max_shield": 10, "health": 3, "max_health": 3, "bounds": [0, screen_width - player_dim[0]], "dimensions": player_dim, "image": player_img}
                        player = Ship(**player_inputs)
                        
                        enemies = []
                        for i in range(num_enemies):
                            enemy_inputs = {'position': [i * (enemy_dim[0] + 30) + (screen_width - num_enemies * (enemy_dim[0] + 30)) // 2, 250], 'health': 1, 'dimensions': enemy_dim, 'image': enemy_img}
                            enemies.append(Enemy(**enemy_inputs))

                        particle_beams = []

                        dead = False

        pygame.display.update()