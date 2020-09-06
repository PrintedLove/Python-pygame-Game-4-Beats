# [Python pygame Game] 4 Beats
# made by "PrintedLove"
# https://printed.tistory.com/

# This game was created with reference to ParkJuneWoo(korca0220)'s [Finding-the-Rabbit]

import pygame as pg
import os, time, random

### default setting
TITLE = "4 Beats"
WIDTH = 640
HEIGHT = 480
FPS = 60
FONT_NAME = 'HeirofLightRegular.ttf'

### color setting
WHITE = (238, 238, 238)
BLACK = (32, 36, 32)
RED = (246, 36, 74)
BLUE = (32, 105, 246)

class Game:
    def __init__(self): ########################## Game Start
        pg.init()
        pg.mixer.init()     #sound mixer
        pg.display.set_caption(TITLE)       #title name
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))      #screen size
        self.clock = pg.time.Clock()        #FPS timer
        self.running = True     #game initialize Boolean value
        self.screen_mode = 0    #screen mode (0: logo, 1: logo2, 2: main, 3: help, 4:stage select, 10: play)
        self.screen_value = [0, 0, 0, 0]       #screen management value
        self.load_date()        #data loading

    def load_date(self): ########################## Data Loading
        self.dir = os.path.dirname(__file__)
        
        ### font
        self.gameFont = os.path.join(os.path.join(self.dir, 'font'), FONT_NAME)
        
        ### image
        self.img_dir = os.path.join(self.dir, 'image')
        pg.display.set_icon(pg.image.load(os.path.join(self.img_dir, 'icon.png')))      #set icon
        self.spr_printed = pg.image.load(os.path.join(self.img_dir, 'printed.png'))
        self.spr_logoback = pg.image.load(os.path.join(self.img_dir, 'logoback.png'))
        self.spr_logo = pg.image.load(os.path.join(self.img_dir, 'logo.png'))
        
        ### background music
        self.snd_dir = os.path.join(self.dir, 'sound')
        self.sound_click = pg.mixer.Sound(os.path.join(self.snd_dir, 'click.ogg'))
        self.sound_drum1 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum1.ogg'))
        self.sound_drum2 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum2.ogg'))
        self.sound_drum3 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum3.ogg'))
        self.sound_drum4 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum4.ogg'))
        
    def new(self):      ########################## Game Initialize
        ### value initialize
        self.stage = -1;         #stage
        self.circle_rot = 0;    #circle rotation value
        self.circle_dir = 0;    #circle direction value

        ### sprite group
        self.all_sprites = pg.sprite.Group()
        self.effects = pg.sprite.Group()
        self.bars = pg.sprite.Group()

        ### playtime timer
        self.start_tick = pg.time.get_ticks()
        
        ### bgm
        pg.mixer.music.load(os.path.join(self.snd_dir, 'bg_main.ogg'))

        ### gameloop start
        self.run()
        
    def run(self):      ########################## Game Loop
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        pg.mixer.music.fadeout(600)
    
    def update(self):   ########################## Game Loop - Update
        self.all_sprites.update()       #screen update
        self.second = ((pg.time.get_ticks() - self.start_tick) / 1000)      #play time calculation
        
    def events(self):   ########################## Game Loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:       #exit
                if self.playing:
                    self.playing = False
                    self.running = False
                    
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:         #RIGHT key
                    self.sound_drum1.play()

                elif event.key == pg.K_LEFT:         #LEFT key
                    self.sound_drum2.play()

                elif event.key == pg.K_UP:         #UP key
                    self.sound_drum3.play()

                elif event.key == pg.K_DOWN:         #DOWN key
                    self.sound_drum4.play()

            elif event.type == pg.MOUSEBUTTONDOWN:      #mouse click
                if self.screen_mode < 4:
                    self.sound_click.play()

                if self.screen_mode == 1 and self.screen_value[0] == 255:
                    self.screen_value[3] = 1

        if self.screen_mode == 0:       #logo screen1
            self.screen_value[0] += 1

            if self.screen_value[0] > 90:
                self.screen_value[1] += 5

            if self.screen_value[1] == 300:
                self.screen_value[0] = 1
                self.screen_value[1] = 0
                self.screen_mode = 1
                pg.mixer.music.play(loops = -1)
                
        elif self.screen_mode == 1:       #logo screen2
            if self.screen_value[3] == 0:
                if self.screen_value[0] < 255:
                    self.screen_value[0] += 2
            else:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= 5
                else:
                    self.screen_mode = 2
                    self.screen_value[1] = 0
                    self.screen_value[2] = 0
                    self.screen_value[3] = 0

            if self.screen_value[1] > -10:
                self.screen_value[1] -= 1
            else:
                if self.screen_value[2] == 0:
                    self.screen_value[1] = random.randrange(0, 10)
                    self.screen_value[2] = random.randrange(5, 30)
                else:
                    self.screen_value[2] -= 1

        elif self.screen_mode == 2:       #logo screen2
            if self.screen_value[0] < 255:
                self.screen_value[0] += 5
        
    def draw(self):     ########################## Game Loop - Draw
        self.all_sprites.draw(self.screen)

        pg.draw.rect(self.screen, WHITE, [0, 0, 640, 480], 0)       #white background
        self.draw_screen(self.screen_mode)                      #draw screen
        
        pg.display.update()

    def draw_screen(self, mode):        # Draw Screen
        if mode == 0:       #logo screen1
            screen_alpha = 255 - min(self.screen_value[1], 255)
            self.spr_printed.set_alpha(screen_alpha)
            self.screen.blit(self.spr_printed, (93, 200))
        
        elif mode == 1:     #logo screen2
            screen_alpha = min(self.screen_value[0], 255)
            
            if self.screen_value[3] == 0:
                self.spr_logoback.set_alpha(screen_alpha)
            else:
                self.spr_logoback.set_alpha(255)
                
            spr_logoRescale = pg.transform.scale(self.spr_logo, (301 + self.screen_value[1], 306 + self.screen_value[1]))
            spr_logoRescale.set_alpha(screen_alpha)
            self.screen.blit(self.spr_logoback, (0, 0))
            self.screen.blit(spr_logoRescale, (320 - round(self.screen_value[1] / 2), 40 - round(self.screen_value[1] / 2)))
            
        elif mode == 2:     #main screen
            screen_alpha = min(self.screen_value[0], 255)
            self.screen.blit(self.spr_logoback, (0, 0))
            self.draw_text("START", 36, BLACK, 480, 105, screen_alpha)
            self.draw_text("HELP", 36, BLACK, 480, 175, screen_alpha)
            self.draw_text("LANG(EN)", 36, BLACK, 480, 245, screen_alpha)
            self.draw_text("EXIT", 36, BLACK, 480, 315, screen_alpha)

    def draw_text(self, text, size, color, x, y, alpha):   # Draw Text
        font = pg.font.Font(self.gameFont, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        text_surface.set_alpha(alpha)
        self.screen.blit(text_surface, text_rect)

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        
        return image

game = Game()

while game.running:
    game.new()
            
pg.quit()
