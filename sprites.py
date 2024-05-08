import pygame
from settings import *
from random import randint, choice

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load('./graphics/background.png').convert()

        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))

        # create a surface twice as wide as the background image
        # to make it seem like a loop
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0 
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'
        ground_image = pygame.image.load('./graphics/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_image, pygame.math.Vector2(ground_image.get_size()) * scale_factor)

        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0 
        self.rect.x = round(self.pos.x)

class Bird(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        
        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 700
        self.direction = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # sound
        self.jump_sound = pygame.mixer.Sound('./sound/noise.wav')
        self.jump_sound.set_volume(0.5)

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(1):
            frame = pygame.image.load('./graphics/bird.png').convert_alpha()
            frame = pygame.transform.scale(frame, pygame.math.Vector2(frame.get_size()) / 7)
            self.frames.append(frame)

        # to render red airplane
        # for i in range(3):
        #     frame = pygame.image.load(f'./graphics/red{i}.png').convert_alpha()
        #     frame = pygame.transform.scale(frame, pygame.math.Vector2(frame.get_size()) * scale_factor)
        #     self.frames.append(frame)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jump_sound.play()
        self.direction = -400
    
    def animate(self, dt):
        self.frame_index += 7 * dt 
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotate_plane = pygame.transform.rotozoom(self.image, self.direction * 0.06, 1)
        self.image = rotate_plane
        self.mask = pygame.mask.from_surface(self.image)

        # alternative to rotate animation
        # if self.direction < 0:
        #     self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], 45)
        # else:
        #     self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -45)

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        orientation = choice(('down', 'up'))
        surface = pygame.image.load(f'./graphics/obstacles/{choice((0, 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)

        x = WINDOW_WIDTH + randint(40, 100)
        
        if orientation == 'down':
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop=(x, randint(-50, -10)))
        else:
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom=(x, y))
        
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= 0:
            self.kill()