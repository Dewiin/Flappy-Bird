import pygame
from random import choice, randint

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
        flap.play()
        self.gravity = -16

    def animation_state(self):
        self.flap_frame += 0.1
        if(self.flap_frame >= len(self.bird_flap)): self.flap_frame = 0
        self.image = self.bird_flap[int(self.flap_frame)]
        #scale
        self.image = pygame.transform.rotozoom(self.image, 0, 1.3)
        #rotate
        self.image = pygame.transform.rotate(self.image, self.gravity * -1.5)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

    def update(self):
        self.animation_state()
        self.apply_gravity()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        super().__init__()
        self.pipe_gap = 270
        self.image = pygame.image.load("Background/pipe.png").convert_alpha()
        self.rect = self.image.get_rect()
        #pos 1 is top pipe, pos -1 is bottom pipe
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.pipe_gap/2)]
        if pos == -1:
            self.rect.topleft = [x, y + int(self.pipe_gap/2)]

    def update(self):
        self.image = pygame.transform.scale(self.image, (60, 400))
        self.rect.x -= scroll_speed
        if self.rect.x < -100: self.kill()

def background_scroll(scrollVal):
    for i in range(0, bg_tiles):
        screen.blit(bg_night, (bg_night.get_width()*i + scrollVal, 0))

def base_scroll(scrollVal):
    for j in range(0, base_tiles):
        screen.blit(base, (base.get_width() * j + scrollVal, 640))

def game_start():
    background_scroll(scroll)
    screen.blit(start_screen, start_rect)

def game_over():
    screen.blit(game_over_screen, game_over_rect)

def collisions():
    global died
    if bird.sprite.rect.y <= 0:
        bird.sprite.rect.y = 0
    if pygame.sprite.spritecollide(bird.sprite, pipe_group, False):
        hit.play()
        die.play()
        died = True
        bird.sprite.rect.y = 400
        bird.sprite.gravity = 0
        pipe_group.empty()
        return False
    if bird.sprite.rect.bottom >= 640:
        hit.play()
        die.play()
        died = True
        bird.sprite.rect.y = 400
        bird.sprite.gravity = 0
        pipe_group.empty()
        return False
    return True

def display_score():
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

#Groups
bird = pygame.sprite.GroupSingle()
bird.add(Bird())

pipe_group = pygame.sprite.Group()

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
restart_button = pygame.image.load("restart-button.png").convert_alpha()
restart_button = pygame.transform.scale(restart_button, (74,74))
restart_rect = restart_button.get_rect(center = (350,500))

#Sounds
point = pygame.mixer.Sound("Sound/point.wav")
die = pygame.mixer.Sound("Sound/audio_die.wav")
flap = pygame.mixer.Sound("Sound/wing.wav")
hit = pygame.mixer.Sound("Sound/hit.wav")

#Variables
run = True
game_active, flying, died = False, False, False
scroll, scroll_speed = 0, 3
pass_pipe = False

last_pipe = pygame.time.get_ticks()

while run:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.sprite.jump()
        else:   
            if died and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                died = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                bird.sprite.jump()
                game_active, flying = True, True

    if game_active and flying:

        scroll -= scroll_speed
        if abs(scroll) > bg_night.get_width(): scroll = 0

        #Background 
        background_scroll(scroll)

        #Pipes
        pipe_group.draw(screen)
        pipe_group.update()
        pipe_y_pos = randint(120,400)
        if current_time - last_pipe >= 2000:
            top_pipe = Pipe(SCREEN_WIDTH, pipe_y_pos, 1)
            bottom_pipe = Pipe(SCREEN_WIDTH, pipe_y_pos, -1)
            pipe_group.add(top_pipe)
            pipe_group.add(bottom_pipe)
            last_pipe = current_time 
            
        #Base
        base_scroll(scroll)

        #Bird
        bird.draw(screen)
        bird.update()

        #Score
        if len(pipe_group) > 0:
            if bird.sprite.rect.left > pipe_group.sprites()[0].rect.left\
                and bird.sprite.rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                point.play()
                pass_pipe = True
            if pass_pipe:
                if bird.sprite.rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        display_score()

        #Running condition
        game_active = collisions()
    
    else:
        if not died:
            game_start()
        else:
            flying = False
            game_over()

    pygame.display.update()