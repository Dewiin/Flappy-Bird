import pygame
from random import choice

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0
        bird_upflap = pygame.image.load("Bird/bird-upflap.png").convert_alpha()
        bird_midflap = pygame.image.load("Bird/bird-midflap.png").convert_alpha()
        bird_downflap = pygame.image.load("Bird/bird-downflap.png").convert_alpha()
        self.bird_flap = [bird_upflap, bird_midflap, bird_downflap]

        self.flap_frame = 0
        self.image = self.bird_flap[self.flap_frame]
        self.rect = self.image.get_rect(center = (150, 400))

    def jump(self):
        self.gravity = -17

    def animation_state(self):
        self.flap_frame += 0.1
        if(self.flap_frame >= len(self.bird_flap)): self.flap_frame = 0
        self.image = self.bird_flap[int(self.flap_frame)]
        self.image = pygame.transform.rotozoom(self.image, 0, 1.2)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

    def update(self):
        self.animation_state()
        self.apply_gravity()

def background_scroll(scrollVal):
    for i in range(0, bg_tiles):
        screen.blit(bg_night, (bg_night.get_width()*i + scrollVal, 0))
    for j in range(0, base_tiles):
        screen.blit(base, (base.get_width() * j + scrollVal, 640))

def game_start():
    background_scroll(scroll)
    screen.blit(start_screen, start_rect)

def game_over():
    background_scroll(scroll)
    screen.blit(game_over_screen, game_over_rect)

def collisions():
    if bird.sprite.rect.y <= 0:
        bird.sprite.rect.y = 0
    if bird.sprite.rect.y >= 630:
        bird.sprite.rect.y = 400
        bird.sprite.gravity = 0
        return False
    return True

def display_score():
    score = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = flappy_font.render(f"{score}", False, "white")
    score_surface = pygame.transform.scale2x(score_surface)
    score_rect = score_surface.get_rect(center = (SCREEN_WIDTH/2, 100))
    screen.blit(score_surface, score_rect)


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 750
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
score = 0
start_time = 0

#Groups
bird = pygame.sprite.GroupSingle()
bird.add(Bird())

#Font
flappy_font = pygame.font.Font("Font/FlappyFont.ttf", 50)

#Backgrounds
bg_night = pygame.image.load("Background/background-night.png").convert_alpha()
bg_night = pygame.transform.rotozoom(bg_night, 0, 1.5)
bg_tiles = int((SCREEN_WIDTH/bg_night.get_width()) + 2)

#Base
base = pygame.image.load("Background/base.png"). convert_alpha()
base_tiles = int((SCREEN_WIDTH/base.get_width()) + 2)

#Start screen
start_screen = pygame.image.load("Background/start.png").convert_alpha()
start_screen = pygame.transform.rotozoom(start_screen, 0, 1.5)
start_rect = start_screen.get_rect(center = (350, 300))

#Game over screen
game_over_screen = pygame.image.load("Background/gameover.png").convert_alpha()
game_over_rect = game_over_screen.get_rect(center = (350, 200))

run = True
game_active = False
scroll = 0

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.sprite.jump()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.sprite.jump()
                game_active = True

    if game_active:
        #Background 
        background_scroll(scroll)
        scroll -= 3
        if abs(scroll) > bg_night.get_width(): scroll = 0

        #Score
        score = display_score()

        #Bird
        bird.draw(screen)
        bird.update()

        #Running condition
        game_active = collisions()
    
    else:
        if score == 0:
            game_start()
            scroll -= 3
            if abs(scroll) > bg_night.get_width(): scroll = 0
        else:
            game_over()
            start_time = int(pygame.time.get_ticks()/1000)
            scroll -= 3
            if abs(scroll) > bg_night.get_width(): scroll = 0

    pygame.display.update()