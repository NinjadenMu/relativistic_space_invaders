import pygame
import random
import math
import relativity

from copy import copy

class Entity:
    def __init__(self, position, bounds_rect, damage, dimensions, image):
        self.position = position

        self.bounds_rect = bounds_rect

        self.damage = damage

        self.dimensions = dimensions

        self.image = image

        self.scaled_image = pygame.transform.scale(image, self.dimensions)

        self.rect = self.scaled_image.get_rect(center = self.position)

        self.exists = True

    def in_bounds(self):
        if self.bounds_rect.contains(self.rect):
            return True

        return False

    def is_hit(self, collider_rect):
        if pygame.Rect.colliderect(self.rect, collider_rect):
            return True

        return False


class Player(Entity):
    def __init__(self, position, bounds_rect, max_velocity, drag_constant, damage, reload, shield, max_shield, shield_regen_time, dimensions, image):
        super().__init__(position, bounds_rect, damage, dimensions, image)

        self.velocity = 0
        self.max_velocity = max_velocity

        self.acceleration = 0

        self.tilt = 0

        self.drag_constant = drag_constant

        self.reload = reload
        self.last_shot_time = 0

        self.shield = shield
        self.max_shield = max_shield
        self.shield_regen_time = shield_regen_time
        self.last_regen_time = 0

        self.shield_img = pygame.transform.scale(pygame.image.load('assets/shield.png'), (40, 42))
        self.shield_bar_img = pygame.transform.scale(pygame.image.load('assets/shield_bar.png'), (16, 42)) 
        self.lost_shield_bar_img = pygame.transform.scale(pygame.image.load('assets/lost_shield_bar.png'), (16, 42)) 

    def update_motion(self):
        if abs(self.velocity + self.acceleration) >= self.max_velocity:
            if self.velocity + self.acceleration < 0:
                self.velocity = -self.max_velocity
                self.acceleration = 0
            else:
                self.velocity = self.max_velocity
                self.acceleration = 0
        else:
            self.velocity += self.acceleration

        self.velocity -= self.drag_constant * self.velocity

        self.position[0] += self.velocity

        if not self.in_bounds():
            self.position[0] -= self.velocity
            self.position[0] -= (self.position[0] - self.bounds_rect.center[0]) / abs(self.position[0] - self.bounds_rect.center[0])
            self.velocity = 0


    def update_shield(self, damage_taken):
        if damage_taken > 0:
            self.shield -= damage_taken

        else:
            if self.shield < self.max_shield and pygame.time.get_ticks() - self.last_regen_time > self.shield_regen_time:
                self.shield += 1
                self.last_regen_time = pygame.time.get_ticks()

        if self.shield <= 0:
            self.exists = False

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot_time > self.reload:
            self.shooting = True
            self.last_shot_time = pygame.time.get_ticks()

    def render(self, screen):
        if self.tilt < 0:
            self.tilt = max(-12, self.tilt - 1.8 * self.acceleration - 0.05 * self.tilt)
        else:
            self.tilt = min(12, self.tilt - 1.8 * self.acceleration - 0.05 * self.tilt)

        screen.blit(pygame.transform.rotate(self.scaled_image, self.tilt), self.rect) 

        screen.blit(self.shield_img, (10, 10))
        for i in range(1, self.max_shield + 1):
            if i < self.shield + 1:
                screen.blit(self.shield_bar_img, (42 + 16 * i, 10))
            else:
                screen.blit(self.lost_shield_bar_img, (42 + 16 * i, 10))

    def game_tick(self, acceleration, damage_taken, shooting, screen):
        self.shooting = False

        self.acceleration = acceleration

        self.rect = self.scaled_image.get_rect(center = self.position)

        self.update_motion()

        self.update_shield(damage_taken)

        if shooting:
            self.shoot()

        self.render(screen)


class Enemy(Entity):
    def __init__(self, position, velocity, bounds_rect, damage, shield, max_shield, shield_regen_time, shot_probability, dimensions, image):
        super().__init__(position, bounds_rect, damage, dimensions, image)
        
        self.initial_position = copy(position)

        self.velocity = velocity

        self.shield = shield
        self.max_shield = max_shield
        self.shield_regen_time = shield_regen_time
        self.last_shield_regen = 0

        self.shot_probability = shot_probability

    def update_motion(self, gamma):
        if abs(self.initial_position[0] - self.position[0]) < 60:
            self.position[0] += + self.velocity / gamma

        else:
            self.velocity *= -1
            self.position[0] += self.velocity

    def update_shield(self, damage_taken, gamma):
        if damage_taken > 0:
            self.shield -= damage_taken

        else:
            if self.shield < self.max_shield and pygame.time.get_ticks() - self.last_shield_regen > self.shield_regen_time * round(gamma):
                self.shield += 1

                self.last_shield_regen = pygame.time.get_ticks()

        if self.shield <= 0:
            self.exists = False

    def shoot(self, gamma):
        if random.random() < self.shot_probability / gamma:
            self.shooting = True

    def render(self, screen):
        screen.blit(self.relativistic_image, self.rect)

    def game_tick(self, damage_taken, screen, gamma):
        self.shooting = False

        self.relativistic_dimensions = [round(self.dimensions[0] / gamma), self.dimensions[1]]

        self.relativistic_image = pygame.transform.scale(self.image, self.relativistic_dimensions)

        self.rect.center = self.position

        self.update_motion(gamma)

        self.update_shield(damage_taken, gamma)

        self.shoot(gamma)

        self.render(screen)


class Projectile(Entity):
    def __init__(self, position, bounds_rect, velocity, damage, dimensions, image):
        super().__init__(position, bounds_rect, damage, dimensions, image)

        self.velocity = velocity

    def update_motion(self, gamma):
        self.position[1] += round(self.velocity / gamma)

        if not self.in_bounds():
            self.exists = False

    def render(self, screen):
        screen.blit(self.relativistic_image, self.rect)

    def game_tick(self, screen, gamma):
        self.relativistic_dimensions = [round(self.dimensions[0] / gamma), self.dimensions[1]]

        self.relativistic_image = pygame.transform.scale(self.image, self.relativistic_dimensions)

        self.rect.center = self.position

        self.update_motion(gamma)

        self.render(screen)


class Button:
    def __init__(self, position, dimensions, text, font, clicked_image, unclicked_image, onclick_function):
        self.position = position

        self.dimensions = dimensions

        self.text = font.render(text, True, (4, 217, 255))

        self.text_rect = self.text.get_rect()
        self.text_rect.center = position

        self.clicked_image = clicked_image
        self.unclicked_image = unclicked_image

        self.scaled_clicked_image = pygame.transform.scale(self.clicked_image, self.dimensions)
        self.scaled_unclicked_image = pygame.transform.scale(self.unclicked_image, self.dimensions)

        self.image_rect = self.scaled_clicked_image.get_rect(center = self.position)

        self.onclick_function = onclick_function

    def render(self, screen, depressed):
        if depressed:
            screen.blit(self.scaled_clicked_image, self.image_rect)

        else:
            screen.blit(self.scaled_unclicked_image, self.image_rect)

        screen.blit(self.text, self.text_rect)

    def game_tick(self, screen, depressed, clicked):
        self.render(screen, depressed)

        if clicked:
            self.onclick_function()


class Game:
    def __init__(self, screen, screen_dimensions, player_img, enemy_img, strong_enemy_img, player_projectile_img, enemy_projectile_img, bg_img, clicked_button_img, unclicked_button_img, player_dimensions, enemy_dimensions, projectile_dimensions, button_dimensions):
        self.screen = screen

        self.screen_dimensions = screen_dimensions

        self.player_img = player_img
        self.enemy_img = enemy_img
        self.strong_enemy_img = strong_enemy_img
        self.player_projectile_img = player_projectile_img
        self.enemy_projectile_img = enemy_projectile_img
        self.bg_img = bg_img
        self.clicked_button_img = clicked_button_img
        self.unclicked_button_img = unclicked_button_img

        self.font_small = pygame.font.Font('assets/orbitron.ttf', 16)
        self.font_medium = pygame.font.Font('assets/orbitron.ttf', 25)
        self.font_big = pygame.font.Font('assets/orbitron.ttf', 48)

        self.player_dimensions = player_dimensions
        self.enemy_dimensions = enemy_dimensions
        self.projectile_dimensions = projectile_dimensions
        self.button_dimensions = button_dimensions

        self.restart_button = Button((self.screen_dimensions[0] // 2 - (self.button_dimensions[0] + 10), self.screen_dimensions[1] // 2 - (self.button_dimensions[1] + 30)), self.button_dimensions, 'RESTART GAME', self.font_medium, self.clicked_button_img, self.unclicked_button_img, self.restart)
        self.retry_button = Button((self.screen_dimensions[0] // 2 + (self.button_dimensions[0] + 10), self.screen_dimensions[1] // 2 - (self.button_dimensions[1] + 30)), self.button_dimensions, 'RETRY LEVEL', self.font_medium, self.clicked_button_img, self.unclicked_button_img, self.start_level)
        self.proceed_button = Button((self.screen_dimensions[0] // 2, self.screen_dimensions[1] // 2 + 150), self.button_dimensions, 'PROCEED', self.font_medium, self.clicked_button_img, self.unclicked_button_img, self.start_level)
        
        self.easy_button = Button((self.screen_dimensions[0] // 2 - (self.button_dimensions[0] - 30), self.screen_dimensions[1] // 2 + (self.button_dimensions[1] - 20)), self.button_dimensions, 'EASY', self.font_medium, self.clicked_button_img, self.unclicked_button_img, self.start_level)
        self.medium_button = Button((self.screen_dimensions[0] // 2 + (self.button_dimensions[0] - 30), self.screen_dimensions[1] // 2 + (self.button_dimensions[1] - 20)), self.button_dimensions, 'MEDIUM', self.font_medium, self.clicked_button_img, self.unclicked_button_img, self.start_level)
        self.hard_button = Button((self.screen_dimensions[0] // 2 - (self.button_dimensions[0] - 30), self.screen_dimensions[1] // 2 + (self.button_dimensions[1] + 110)), self.button_dimensions, 'HARD', self.font_medium, self.clicked_button_img, self.unclicked_button_img, self.start_level)
        self.yikuan_button  = Button((self.screen_dimensions[0] // 2 + (self.button_dimensions[0] - 30), self.screen_dimensions[1] // 2 + (self.button_dimensions[1] + 110)), self.button_dimensions, 'YIKUAN', self.font_medium, self.clicked_button_img, self.unclicked_button_img, self.start_level)

        self.restart_button_depressed = False
        self.retry_button_depressed = False
        self.proceed_button_depressed = False

        self.easy_button_depressed = False
        self.medium_button_depressed = False
        self.hard_button_depressed = False
        self.yikuan_button_depressed = False

        self.bounds_rect = bg_img.get_rect(center = (self.screen_dimensions[0] // 2, self.screen_dimensions[1] // 2))

        self.level = 0

        self.enemy_rows = 0

        self.intro_done = False

    def restart(self):
        self.level = 0
        self.enemy_rows = 0

        self.start_level()

    def start_level(self):
        self.level += 1

        self.restart_button_depressed = False
        self.retry_button_depressed = False
        self.proceed_button_depressed = False

        self.keys_down = {'K_LEFT': False, 'K_RIGHT': False, 'K_SPACE': False}
        
        player_inputs = {'position': [self.screen_dimensions[0] // 2, self.screen_dimensions[1] - 100], 'bounds_rect': self.bounds_rect, 'max_velocity': 9, 'drag_constant': 0.01, 'damage': 3, 'reload': 600, 'shield': 12 - self.difficulty * 2, 'max_shield': 12 - self.difficulty * 2, 'shield_regen_time': self.difficulty * 1000, 'dimensions': self.player_dimensions, 'image': pygame.image.load('assets/ship.png')}
        self.player = Player(**player_inputs)
        self.player_projectiles = []

        if self.level < 6 and self.level % 2:
            self.enemy_rows += 1

        self.enemies = []
        for i in range(self.enemy_rows):
            enemy_shield = 3
            enemy_img = self.enemy_img

            if self.level // 2 - i:
                enemy_shield = 5
                enemy_img = self.strong_enemy_img
            
            for j in range(10):
                enemy_inputs = {'position': [j * (self.enemy_dimensions[0] + 40) + (self.screen_dimensions[0] - 10 * (self.enemy_dimensions[0] + 40)) // 2 + 40, self.screen_dimensions[1] // 2 - (self.enemy_dimensions[1] + 20) * i], 'velocity': self.difficulty / 1.5, 'bounds_rect': self.bounds_rect, 'damage': 3, 'shield': enemy_shield, 'max_shield': enemy_shield, 'shield_regen_time': (4 - self.difficulty / 2) * 1000, 'damage': 3, 'shot_probability': 0.0033 + self.difficulty / 2000, 'dimensions': [50, 50], 'image': enemy_img}
                self.enemies.append(Enemy(**enemy_inputs))

        self.enemy_projectiles = []

    def intro_screen(self):
        easy_button_clicked = False
        medium_button_clicked = False
        hard_button_clicked = False
        yikuan_button_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.easy_button.image_rect.collidepoint(pos):
                    self.easy_button_depressed = True

                elif self.medium_button.image_rect.collidepoint(pos):
                    self.medium_button_depressed = True

                elif self.hard_button.image_rect.collidepoint(pos):
                    self.hard_button_depressed = True

                elif self.yikuan_button.image_rect.collidepoint(pos):
                    self.yikuan_button_depressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.easy_button_depressed = False
                self.medium_button_depressed = False
                self.hard_button_depressed = False
                self.yikuan_button_depressed = False

                pos = pygame.mouse.get_pos()

                if self.easy_button.image_rect.collidepoint(pos):
                    self.intro_done = True
                    easy_button_clicked = True
                    self.difficulty = 1

                elif self.medium_button.image_rect.collidepoint(pos):
                    self.intro_done = True
                    medium_button_clicked = True
                    self.difficulty = 2

                elif self.hard_button.image_rect.collidepoint(pos):
                    self.intro_done = True
                    hard_button_clicked = True
                    self.difficulty = 3

                elif self.yikuan_button.image_rect.collidepoint(pos):
                    self.intro_done = True
                    yikuan_button_clicked = True
                    self.difficulty = 5

        instructions_text1 = self.font_small.render('USE ARROW KEYS TO MOVE. USE SPACE TO SHOOT. RED ALIENS ARE STRONGER AND CAN REGAIN HEALTH', True, (4, 217, 255))
        instructions_rect1 = instructions_text1.get_rect()
        instructions_rect1.center = (self.screen_dimensions[0] // 2, self.screen_dimensions[1] // 2 - 150)

        instructions_text2 = self.font_small.render('THE FASTER YOU MOVE, THE SLOWER AND THINNER EVERYTHING ELSE GETS.', True, (4, 217, 255))
        instructions_rect2 = instructions_text2.get_rect()
        instructions_rect2.center = (self.screen_dimensions[0] // 2, self.screen_dimensions[1] // 2 - 100)
            
        instructions_text3 = self.font_big.render('CHOOSE YOUR LEVEL TO START.', True, (4, 217, 255))
        instructions_rect3 = instructions_text3.get_rect()
        instructions_rect3.center = (self.screen_dimensions[0] // 2, self.screen_dimensions[1] // 2 - 40)

        screen.blit(bg_img, self.bounds_rect)
        screen.blit(instructions_text1, instructions_rect1)
        screen.blit(instructions_text2, instructions_rect2)
        screen.blit(instructions_text3, instructions_rect3)

        self.easy_button.game_tick(screen, self.easy_button_depressed, easy_button_clicked)
        self.medium_button.game_tick(screen, self.medium_button_depressed, medium_button_clicked)
        self.hard_button.game_tick(screen, self.hard_button_depressed, hard_button_clicked)
        self.yikuan_button.game_tick(screen, self.yikuan_button_depressed, yikuan_button_clicked)

    def level_beat_screen(self):
        self.player.exists = False
        end_text = self.font_big.render('YOU BEAT LEVEL ' + str(self.level), True, (4, 217, 255))
        end_text_rect = end_text.get_rect(center = (self.screen_dimensions[0] // 2, self.screen_dimensions[1] // 2)) 

        proceed_button_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.proceed_button.image_rect.collidepoint(pos):
                    self.proceed_button_depressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.proceed_button_depressed = False

                pos = pygame.mouse.get_pos()

                if self.proceed_button.image_rect.collidepoint(pos):
                    proceed_button_clicked = True

        self.screen.blit(self.bg_img, self.bounds_rect)

        self.proceed_button.game_tick(self.screen, self.proceed_button_depressed, proceed_button_clicked)

        self.screen.blit(end_text, end_text_rect)  

    def death_screen(self):
        end_text = self.font_big.render('YOU DIED ON LEVEL ' + str(self.level), True, (4, 217, 255))
        end_text_rect = end_text.get_rect(center = (self.screen_dimensions[0] // 2, self.screen_dimensions[1] // 2)) 

        restart_button_clicked = False
        retry_button_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.restart_button.image_rect.collidepoint(pos):
                    self.restart_button_depressed = True

                elif self.retry_button.image_rect.collidepoint(pos):
                    self.retry_button_depressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.restart_button_depressed = False
                self.retry_button_depressed = False

                pos = pygame.mouse.get_pos()

                if self.restart_button.image_rect.collidepoint(pos):
                    restart_button_clicked = True

                elif self.retry_button.image_rect.collidepoint(pos):
                    if self.level % 2:
                        self.enemy_rows -= 1

                    self.level -= 1

                    retry_button_clicked = True

        self.screen.blit(self.bg_img, self.bounds_rect)

        self.restart_button.game_tick(self.screen, self.restart_button_depressed, restart_button_clicked)
        self.retry_button.game_tick(self.screen, self.retry_button_depressed, retry_button_clicked)

        self.screen.blit(end_text, end_text_rect)    

    def game_tick(self):
        self.screen.blit(self.bg_img, (0, 0))

        player_updates = {'acceleration': 0, 'damage_taken': 0, 'shooting': False, 'screen': self.screen}
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.keys_down['K_LEFT'] = True

                elif event.key == pygame.K_RIGHT:
                    self.keys_down['K_RIGHT'] = True

                elif event.key == pygame.K_SPACE:
                    self.keys_down['K_SPACE'] = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.keys_down['K_LEFT'] = False

                elif event.key == pygame.K_RIGHT:
                    self.keys_down['K_RIGHT'] = False

                elif event.key == pygame.K_SPACE:
                    self.keys_down['K_SPACE'] = False

        if self.keys_down['K_LEFT']:
            player_updates['acceleration'] -= 0.22

        if self.keys_down['K_RIGHT']:
            player_updates['acceleration'] += 0.22

        if self.keys_down['K_SPACE']:
            player_updates['shooting'] = True

        self.enemies = [enemy for enemy in self.enemies if enemy.exists]
        self.player_projectiles = [projectile for projectile in self.player_projectiles if projectile.exists]

        for enemy in self.enemies:
            enemy_velocity = 1
            combined_velocity = relativity.combined_velocity_parallel(enemy_velocity / 10, self.player.velocity / 10)
            gamma = relativity.gamma(combined_velocity)

            enemy_updates = {'damage_taken': 0, 'screen': self.screen, 'gamma': gamma}

            for projectile in self.player_projectiles:
                if enemy.is_hit(projectile.rect):
                    enemy_updates['damage_taken'] = projectile.damage
                    projectile.exists = False

            enemy.game_tick(**enemy_updates)

            if enemy.shooting: 
                self.enemy_projectiles.append(Projectile(copy(enemy.position), self.bounds_rect, 3, enemy.damage, self.projectile_dimensions, self.enemy_projectile_img))

        for projectile in self.player_projectiles:
                combined_velocity = relativity.combined_velocity_perpendicular(projectile.velocity / 10, self.player.velocity / 10)
                gamma = relativity.gamma(combined_velocity)

                projectile.game_tick(self.screen, gamma)

        self.enemy_projectiles = [projectile for projectile in self.enemy_projectiles if projectile.exists]

        for projectile in self.enemy_projectiles:
            if self.player.is_hit(projectile.rect):
                player_updates['damage_taken'] = projectile.damage
                projectile.exists = False

            combined_velocity = relativity.combined_velocity_perpendicular(projectile.velocity / 10, self.player.velocity / 10)
            gamma = relativity.gamma(combined_velocity)
            projectile.game_tick(self.screen, gamma)

        self.player.game_tick(**player_updates)

        title = self.font_medium.render('Relativistic Space Invaders', True, (4, 217, 255))
        screen.blit(title, (610, 10))

        credit = self.font_small.render('Jaden Mu', True, (4, 217, 255))
        screen.blit(credit, (900, 40))

        level_text = self.font_small.render('LEVEL: ' + str(self.level), True, (4, 217, 255))
        screen.blit(level_text, (20, 60))

        if self.difficulty == 1:
            difficulty = 'EASY'

        elif self.difficulty == 2:
            difficulty = 'MEDIUM'

        elif self.difficulty == 3:
            difficulty = 'HARD'

        else:
            difficulty = 'YIKUAN'

        difficulty_text = self.font_small.render('DIFFICULTY: ' + difficulty, True, (4, 217, 255))
        screen.blit(difficulty_text, (120, 60))

        if self.player.shooting:
            self.player_projectiles.append(Projectile(copy(self.player.position), self.bounds_rect, -3, self.player.damage, self.projectile_dimensions, self.player_projectile_img))
            


if __name__ == '__main__':
    pygame.init()

    screen_dimensions = (1000, 600)

    screen = pygame.display.set_mode(screen_dimensions)

    pygame.display.set_caption('Relativistic Space Invaders')

    clock = pygame.time.Clock()

    player_img = pygame.image.load('assets/ship.png')
    enemy_img = pygame.image.load('assets/alien.png')
    strong_enemy_img = pygame.image.load('assets/strong_alien.png')
    player_projectile_img = pygame.image.load('assets/projectile_player.png')
    enemy_projectile_img = pygame.image.load('assets/projectile_enemy.png')
    bg_img = pygame.transform.scale(pygame.image.load('assets/bg.png'), screen_dimensions)
    clicked_button_img = pygame.image.load('assets/clicked_button.png')
    unclicked_button_img = pygame.image.load('assets/unclicked_button.png')

    game = Game(screen, screen_dimensions, player_img, enemy_img, strong_enemy_img, player_projectile_img, enemy_projectile_img, bg_img, clicked_button_img, unclicked_button_img, [100, 70], [50, 50], [18, 18], [300, 100])

    while True:
        clock.tick(31)

        if not game.intro_done:
            game.intro_screen()

        elif not len(game.enemies):
            game.level_beat_screen()

        elif game.player.exists:
            game.game_tick()

        else:
            game.death_screen()

        pygame.display.update()

    pygame.quit()





    

    

    
