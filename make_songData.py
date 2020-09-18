#-*-coding: utf-8

import pygame as pg
import os, time, math

TITLE = "4 Beats - Make Song Data"       ### default setting
WIDTH = 640
HEIGHT = 480
FPS = 60
DEFAULT_FONT = "NotoSansCJKkr-Regular.otf"

WHITE = (238, 238, 238)     ### color setting
BLACK = (32, 36, 32)
RED = (246, 36, 74)
BLUE = (32, 105, 246)
ALPHA_MAX = 255

class Game:
    def __init__(self): ########################## Game Start
        pg.init()
        pg.mixer.init()     #sound mixer
        pg.display.set_caption(TITLE)       #title name
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))      #screen size
        self.clock = pg.time.Clock()        #FPS timer
        self.start_tick = 0     #game timer
        self.running = True     #game initialize Boolean value
        self.load_date()        #data loading
        self.new()

    def load_date(self): ########################## Data Loading
        self.dir = os.path.dirname(__file__)

        ### font
        self.fnt_dir = os.path.join(self.dir, 'font')
        self.gameFont = os.path.join(self.fnt_dir, DEFAULT_FONT)
        
        ### image
        self.img_dir = os.path.join(self.dir, 'image')
        pg.display.set_icon(pg.image.load(os.path.join(self.img_dir, 'icon.png')))      #set icon
        self.spr_circle = pg.image.load(os.path.join(self.img_dir, 'circle.png'))

    def new(self):      ########################## Game Initialize
        self.circle_dir = 1     #circle direction value (benchmark: white / down, right, up, left  == 1, 2, 3, 4)
        self.circle_rot = 0     #circle rotation value
        self.click_circle = 0
        self.color_list = ('W', 'B', 'D', 'R')
        self.mode_list = ('D', 'R', 'U', 'L')
        self.shot_text = ['W', 'D', 'D']
        self.line_coord = [round(WIDTH/2), HEIGHT]
        self.circle_coord = [round(WIDTH/2), round(HEIGHT/2 + 50)]
        
    def run(self):      ########################## Game Loop
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            pg.display.flip()
        
    def events(self):   ########################## Game Loop - Events
        mouse_coord = pg.mouse.get_pos()    #mouse coord value
        mouse_move = False      #mouse move Boolean value
        mouse_click = 0         #mouse click value (1: left, 2: scroll, 3: right, 4: scroll up, 5: scroll down)
        key_click = 0           #key value (275: right, 276: left, 273: up, 274: down, 13: enter)
        
        for event in pg.event.get():                        ### Event Check
            if event.type == pg.QUIT:       #exit
                if self.playing:
                    self.playing, self.running = False, False 
            elif event.type == pg.KEYDOWN:      #keyboard check
                key_click = event.key
            elif event.type == pg.MOUSEMOTION:
                if event.rel[0] != 0 or event.rel[1] != 0:    #mousemove
                    mouse_move = True
            elif event.type == pg.MOUSEBUTTONDOWN:      #mouse click
                mouse_click = event.button

        if mouse_click == 1:
            touch_s = self.screen_touchX(mouse_coord)
            self.shot_text[1] = self.mode_list[touch_s]
            self.shot_text[0] = self.color_list[touch_s - self.circle_dir + 1]

            if touch_s == 0:
                self.circle_coord = [round(WIDTH/2), round(HEIGHT/2 + 50)]
            elif touch_s == 1:
                self.circle_coord = [round(WIDTH/2 + 50), round(HEIGHT/2)]
            elif touch_s == 2:
                self.circle_coord = [round(WIDTH/2), round(HEIGHT/2 - 50)]
            else:
                self.circle_coord = [round(WIDTH/2 - 50), round(HEIGHT/2)]
                
            print(self.shot_text[0] + self.shot_text[1] + self.shot_text[2])

        if mouse_click == 3:
            touch_s = self.screen_touchX(mouse_coord)
            self.shot_text[2] = self.mode_list[touch_s]

            if touch_s == 0:
                self.line_coord = [round(WIDTH/2), HEIGHT]
            elif touch_s == 1:
                self.line_coord = [WIDTH , round(HEIGHT/2)]
            elif touch_s == 2:
                self.line_coord = [round(WIDTH/2), 0]
            else:
                self.line_coord = [0, round(HEIGHT/2)]

            print(self.shot_text[0] + self.shot_text[1] + self.shot_text[2])
                
        if key_click == 276:              #key check
            self.circle_dir += 1
        elif key_click == 275:
            self.circle_dir -= 1

        if self.circle_dir > 4:         #circle direction management
            self.circle_dir = 1
        elif self.circle_dir < 1:
            self.circle_dir = 4

        rotToDir = (self.circle_dir - 1) * 90       #circle rotation management
        
        if self.circle_rot != rotToDir:
            if self.circle_rot >= rotToDir:
                if self.circle_rot >= 270 and rotToDir == 0:
                    self.circle_rot += 15
                else:
                    self.circle_rot -= 15
            else:
                if self.circle_rot == 0 and rotToDir == 270:
                    self.circle_rot = 345
                else:
                    self.circle_rot += 15
                
        if self.circle_rot < 0:         
            self.circle_rot = 345
        elif self.circle_rot > 345:
            self.circle_rot = 0
                        
    def draw(self):     ########################## Game Loop - Draw
        self.background = pg.Surface((WIDTH, HEIGHT))           #white background
        self.background = self.background.convert()
        self.background.fill(WHITE)
        self.screen.blit(self.background, (0,0))
        self.draw_screen()                      #draw screen
        pg.display.update()

    def draw_screen(self):                    # Draw Screen
        surface = pg.Surface((WIDTH, HEIGHT))
        surface.fill(WHITE)
        pg.draw.line(surface, BLACK, (round(WIDTH / 2), round(HEIGHT / 2)), self.line_coord, 5)
        pg.draw.circle(surface, BLACK, self.circle_coord, 30, 5)
        self.screen.blit(surface, (0,0))
        self.draw_sprite(((WIDTH - 99) / 2, (HEIGHT - 99) / 2), self.spr_circle, self.circle_rot)
        self.draw_text(self.shot_text[0] + self.shot_text[1] + self.shot_text[2], 36, BLACK, WIDTH / 2 + 150, HEIGHT / 2 + 150)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.gameFont, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (round(x), round(y))
        self.screen.blit(text_surface, text_rect)
            
    def draw_sprite(self, coord, spr, rot):
        rotated_spr = pg.transform.rotate(spr, rot)
        self.screen.blit(rotated_spr, (round(coord[0] + spr.get_width() / 2 - rotated_spr.get_width() / 2), round(coord[1] + spr.get_height() / 2 - rotated_spr.get_height() / 2)))
        
    def screen_touchX(self, mouse_coord):       # screen touch by X
        dy = mouse_coord[1] - HEIGHT/2
        dx = mouse_coord[0] - WIDTH/2

        if dx == 0:
            dx = 1

        if dy == 0:
            dy = 1
            
        angle = math.atan(dy / dx) * (180 / math.pi)
        
        if dx < 0:
            angle += 180
        else:
            if dy < 0:
                angle += 360
        
        screen_dir = int(angle // 45)
        
        if screen_dir in [1, 2]:
            return 0    # Down
        elif screen_dir in [3, 4]:
            return 3    # left
        elif screen_dir in [5, 6]:
            return 2    # Up
        else:
            return 1    # Right
  
game = Game()

while game.running:
    game.run()
    
pg.quit()
