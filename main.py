# content from kids can code: http://kidscancode.org/blog/
# https://web.microsoftstream.com/video/b1bdbe8e-edc6-47a8-a2f9-c1aaf1b7930f

'''
Innovation:
powerup that increases jump to reach crown
bounce pads to help get to powerup
more platforms
'''

# import libraries and modules
# from platform import platform
from sre_constants import JUMP
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

import os

# set up asset folders here
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

vec = pg.math.Vector2

# initial game settings 
WIDTH = 1200 # determines width of screen
HEIGHT = 800 # determines height of screen
FPS = 30

# initial player settings
PLAYER_GRAV = 1.5 # determines how strong gravity is if any
PLAYER_FRIC = 0.1 # determines how much friction
SCORE = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (244, 255, 0)

# defines the function that visually draws text
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

def colorbyte():
    return random.randint(0,255)

# sprites...
# player class
class Player(Sprite): # make class for player
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert() # loads image of bellarmine bell
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumppower = 20
    def controls(self): # left and right controls
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -2.5
        if keys[pg.K_d]:
            self.acc.x = 2.5
    def jump(self): # jumping contols and mechanics
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -self.jumppower # sets y-velocity to variable so it can be changed unlike a set numerical velocity
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos


# platforms class
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# mobs class
class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'crown.png')).convert() # loads image of crown
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self): # position of mob
        self.rect.y = 45
        self.rect.x = 670

# powerups class
class pwrup(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'powerup.png')).convert() # loads image of powerup
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# bounce pads class
class bounce_pad(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'bouncepads.png')).convert() # loads image of bounce pad
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# create groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()
pwrups = pg.sprite.Group()
bounce_pads = pg.sprite.Group()

# instantiate classes
player = Player()
plat = Platform(-7000, 765, 14000, 35)
plat1 = Platform(900, 700, 100, 35)
plat2 = Platform(650, 600, 100, 35)
plat3 = Platform(280, 500, 100, 35)
plat4 = Platform(50, 388, 100, 35)
plat5 = Platform(250, 170, 100, 35)
plat6 = Platform(650, 100, 100, 35)
pwrupplat = Platform(900, 400, 100, 35)
pwrup1 = pwrup(924, 353, 52, 50)
bounce1 = bounce_pad(1075, 720, 82, 50)


for i in range(1): # determines number of mobs and their color
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 62, 50, (colorbyte(),colorbyte(),colorbyte()))
    all_sprites.add(m)
    mobs.add(m)
    print(m)

# add player to all sprites group
all_sprites.add(player, pwrup1, bounce1)
pwrups.add(pwrup1)
all_plats.add(plat, plat1, plat2, plat3, plat4, plat5, plat6, pwrupplat)
bounce_pads.add(bounce1)

# add platform to all sprites group
all_sprites.add(plat)
all_sprites.add(plat1)
all_sprites.add(plat2)
all_sprites.add(plat3)
all_sprites.add(plat4)
all_sprites.add(plat5)
all_sprites.add(plat6)
all_sprites.add(pwrupplat)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    # when player hits the platforms, they go to the top of it and stay on it without falling through
    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        player.pos.y = hits[0].rect.top
        player.vel.y = 0

    # powerup that increases jump height when hits
    for p in pwrups:
        poweruphit = pg.sprite.spritecollide(player, pwrups, True)
        if poweruphit:
            print("I got a powerup!")
            player.jumppower += 6
    
    # when the player hits the bounce pad, it auto jumps
    for b in bounce_pads:
        bouncepadhit = pg.sprite.spritecollide(player, bounce_pads, False)
        if bouncepadhit:
            print("I've hit a bounce pad!")
            player.rect.x += 1
            hits = pg.sprite.spritecollide(player, all_plats, False)
            player.rect.x += -1
            if hits:
                player.vel.y = -40
    
    # when the player hits a mob, score increases by 1
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        SCORE += 1

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()

    # ends game and prints you've won when the player reaches the mob and touches it because the score = 1
    if SCORE == 1:
        print("You've won!")
        break
        
    # update all sprites
    all_sprites.update()

    # draw the background screen
    screen.fill(BLACK)
    # draw text
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    # draw all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()