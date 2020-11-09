import pygame, sys
import random
import os
                                   
WIDTH = 1500
HEIGHT = 1000
FPS = 30
GROUND = HEIGHT - 30
SLOW = 3
FAST = 8

#CONSTANTS - PHYSICS
PLAYER_ACC = 1.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 1.1
vec = pygame.math.Vector2

#DEFINE COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (48, 227, 255)

#ASSET FOLDERS
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

#DRAW TEXT
font_name = pygame.font.match_font("arial")
def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

#BACKGROUND
#background = pygame.image.load(os.path.join(img_folder, "space.png")).convert()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "character_robot_idle.png")).convert()
        self.image = pygame.transform.scale(self.image, (75, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.pos = vec(10, GROUND - 60)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet)
            #bullets.add(bullet)

        
    def update(self):
        
        self.image.set_colorkey(BLACK)

        self.acc = vec(0, PLAYER_GRAV)
        
        #RETURNS A LIST, keystate, OF ALL PRESSED KEYS
        keystate = pygame.key.get_pressed()

        #CHECKS TO SEE WHICH KEYS WERE IN THE LIST (A.K.A PRESSED)
        if keystate[pygame.K_RIGHT]:
            self.acc.x += PLAYER_ACC
        if keystate[pygame.K_LEFT]:
            self.acc.x += -PLAYER_ACC
        if keystate[pygame.K_UP]:
            self.rect.y += -5
        if keystate[pygame.K_DOWN]:
            self.rect.y += 5
        if self.vel.y == 0 and keystate[pygame.K_UP]:
            self.vel.y = -21
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_jump_left.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)
            if self.vel.x > 1:
                self.image = pygame.image.load(os.path.join(img_folder, "character_robot_jump.png")).convert()
                self.image = pygame.transform.scale(self.image, (75, 100))
                self.image.set_colorkey(BLACK)

        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
                
        #ANIMATIONS

                #Fall
        if self.vel.y > 0 and self.vel.x > 0:
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_fall.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)

                #Fall left
        if self.vel.y > 0 and self.vel.x < 0:
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_fall_left.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)

                #Idle
        if self.vel.y == 0: #and self.acc.x == 0:
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_idle.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)
            
                #Duck
        if keystate[pygame.K_DOWN]:
            if self.vel.y == 0 and self.acc.x == 0:
                self.image = pygame.image.load(os.path.join(img_folder, "character_robot_duck.png")).convert()
                self.image = pygame.transform.scale(self.image, (75, 100))
                self.image.set_colorkey(BLACK)
                
                #Slide
        if keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT] and self.vel.y == 0:
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_down.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)
            
                #Slide Left
        if keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT] and self.vel.y == 0:
            self.image = pygame.image.load(os.path.join(img_folder, "character_robot_down_left.png")).convert()
            self.image = pygame.transform.scale(self.image, (75, 100))
            self.image.set_colorkey(BLACK)

        #if keystate[pygame.K_RIGHT] and self.vel.y == 0:
            #running_images = pygame.image.load(os.path.join(img_folder, ["character_robot_run0.png", "character_robot_run1.png", "character_robot_run2.png"]).convert()
            #self.image = running_images
            #self.image = pygame.transform.scale(self.image, (75, 100))
            #self.image.set_colorkey(WHITE)   

        #APPLY FRICTION IN THE X DIRECTION
        self.acc.x += self.vel.x * PLAYER_FRICTION

        #EQUATIONS OF MOTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #WRAP AROUND THE SIDES OF THE SCREEN
        if self.pos.x > WIDTH - 30:
            self.pos.x = WIDTH - 30
        if self.pos.x < 0 + 30:
            self.pos.x = 0 + 30

        #SIMULATE THE GROUND
        if self.pos.y > GROUND:
            self.pos.y = GROUND + 1
            self.vel.y = 0

        #SET THE NEW PLAYER POSITION BASED ON ABOVE
        self.rect.midbottom = self.pos
            

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "UfoGrey.png")).convert()
        self.image = pygame.transform.scale(self.image, (150, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 500
        self.rect.y = 850

    def update(self):

        self.rect.x += -5

        if self.rect.right < 0:
            self.rect.left = WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "laserRed.png")).convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 20

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()

    
#INITIALIZE VARIABLES
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

#ADD BACKGROUND
bkgr_image = pygame.image.load(os.path.join(img_folder, "space.png")).convert()
background = pygame.transform.scale(bkgr_image, (WIDTH, HEIGHT))
background_rect = background.get_rect()

#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
player = Player()
platform = Platform()
all_sprites.add(player, platform)

# GAME LOOP:
#   Process Events
#   Update
#   Draw
running = True
while running:

    clock.tick(FPS)

    #PROCESS EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # UPDATE
    all_sprites.update()

    # DRAW
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "PLATFORMER", 24, 10, 10)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()



