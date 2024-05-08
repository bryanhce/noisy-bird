import pygame, sys, time, math, numpy
from settings import *
from sprites import BG, Ground, Bird, Obstacle

class Game:
    def __init__(self):

        # set up the game       
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Noisy Bird')
        self.clock = pygame.time.Clock()
        # status of the game
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('./graphics/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.bird = Bird(self.all_sprites, self.scale_factor / 1.7)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400) # runs every 1.4 sec

        # text
        self.font = pygame.font.Font('./graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # menu
        self.menu_surface = pygame.image.load('./graphics/Tap.png').convert_alpha()
        self.menu_surface = pygame.transform.scale(self.menu_surface, pygame.math.Vector2(self.menu_surface.get_size()) / 4)
        self.menu_rect = self.menu_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # sounds
        pygame.mixer.init()
        pygame.mixer.music.load('./sound/background.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)

    def get_microphone_input(self):
            return pygame.sndarray.array(self.microphone)

    def collision(self):
        if (pygame.sprite.spritecollide(self.bird, self.collision_sprites, False, pygame.sprite.collide_mask) 
        or self.bird.rect.top <= 0):
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.bird.kill()
    
    def display_score(self):
        y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 3)
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 10
            y = WINDOW_HEIGHT / 10

        score_surface = self.font.render(str(self.score), True, 'black')
        score_rect = score_surface.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surface, score_rect)

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.bird.jump()
                    else:
                        self.bird = Bird(self.all_sprites, self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                
                if event.type == self.obstacle_timer and self.active:
                    # multiply scale factor by 1.1 or 1.2 to make mountains taller
                    # and therefore game harder
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor)

            # game logic
            self.display_surface.fill((0, 0, 0))
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collision()
            else:
                self.display_surface.blit(self.menu_surface, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAME_RATE)

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()