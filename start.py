# [Python pygame Game] 4 Beats
# made by "PrintedLove"
# https://printed.tistory.com/

# This game was created with reference to ParkJuneWoo(korca0220)'s [Finding-the-Rabbit]

import pygame as pg
import time
import os
from sprites import *

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
        pg.display.set_icon(pg.image.load(os.path.join(os.path.join(os.path.dirname(__file__), 'image'), 'icon.png')))
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))      #screen size
        
        self.clock = pg.time.Clock()        #FPS timer
        self.running = True     #game initialize Boolean value
        self.screen_mode = 0    #screen mode (0: logo, 1: main, 2: help, 3:stage select, 10: play)
        self.load_date()        #data loading

    def load_date(self): ########################## Data Loading
        self.dir = os.path.dirname(__file__)
        
        ### font
        self.gameFont = os.path.join(os.path.join(self.dir, 'font'), FONT_NAME)
        
        ### image
        self.img_dir = os.path.join(self.dir, 'image')
        
        pg.display.set_icon(pg.image.load(os.path.join(self.img_dir, 'icon.png')))      #set icon
        self.spr_logoback = pg.image.load(os.path.join(self.img_dir, 'logoback.png'))
        self.spr_logo = pg.image.load(os.path.join(self.img_dir, 'logo.png'))
        self.spr_button_logo = pg.image.load(os.path.join(self.img_dir, 'button_logo.png'))
        self.spr_buttonEffect_logo = pg.image.load(os.path.join(self.img_dir, 'buttonEffect_logo.png'))

        ### background music
        self.snd_dir = os.path.join(self.dir, 'sound')
        
        #self.sound_bg_main = pg.mixer.Sound(os.path.join(self.snd_dir, 'bg_main.ogg'))
        
    def new(self):      ########################## Game Initialize
        ### value initialize
        self.stage = 1;     #stage
        self.circle_rot = 0;     #circle rotation value
        self.circle_dir = 0;     #circle direction value

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
        pg.mixer.music.play(loops = -1)

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
        
    def draw(self):     ########################## Game Loop - Draw
        self.all_sprites.draw(self.screen)

        self.spr_logo.set_alpha(50)
        self.screen.blit(self.spr_logoback, (0, 0))
        self.screen.blit(self.spr_logo, (320, 40))
        
        pg.display.update()

    def draw_text(self, text, size, color, x, y):   # Draw Text
        font = pg.font.Font(self.gameFont, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

game = Game()

while game.running:
    game.new()
            
pg.quit()
