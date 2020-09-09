# [Python pygame Game] 4 Beats
# made by "PrintedLove"
# https://printed.tistory.com/
# This game was created with reference to ParkJuneWoo(korca0220)'s [Finding-the-Rabbit]

#-*-coding: utf-8

import pygame as pg
import os, time, random

### default setting
TITLE = "4 Beats"
WIDTH = 640
HEIGHT = 480
FPS = 60

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
        self.screen_mode = 0    #screen mode (0: logo, 1: logo2, 2: main, 3: stage select, 10: play)
        self.screen_value = [0, 0, 0, 0]       #screen management value
        self.language_mode = 0         #0: english, 1: korean, 2~: custom
        self.load_date()        #data loading

    def load_date(self): ########################## Data Loading
        self.dir = os.path.dirname(__file__)
        
        ### font
        self.fnt_dir = os.path.join(self.dir, 'font')
        self.gameFont = os.path.join(self.fnt_dir, "NotoSansCJKkr-Regular.otf")
        language_file = open(os.path.join(self.fnt_dir, 'language.ini'), "r", encoding = 'UTF-8')
        language_lists = language_file.read().split('\n')
        self.language_list = list()
        self.language_list = [n.split("_") for n in language_lists]
        language_file.close()
        
        ### image
        self.img_dir = os.path.join(self.dir, 'image')
        pg.display.set_icon(pg.image.load(os.path.join(self.img_dir, 'icon.png')))      #set icon
        self.spr_printed = pg.image.load(os.path.join(self.img_dir, 'printed.png'))
        self.spr_logoback = pg.image.load(os.path.join(self.img_dir, 'logoback.png'))
        self.spr_logo = pg.image.load(os.path.join(self.img_dir, 'logo.png'))
        
        ### music
        self.snd_dir = os.path.join(self.dir, 'sound')
        self.bg_main = os.path.join(self.snd_dir, 'bg_main.ogg')
        self.sound_click = pg.mixer.Sound(os.path.join(self.snd_dir, 'click.ogg'))
        self.sound_drum1 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum1.ogg'))
        self.sound_drum2 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum2.ogg'))
        self.sound_drum3 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum3.ogg'))
        self.sound_drum4 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum4.ogg'))

        ### song
        self.song_dir = os.path.join(self.dir, 'song')
        file_list = os.listdir(self.song_dir)
        song_lists = list()
        song_data = list()
        
        for song in file_list:
            let = song.split('.')[-1]
            
            if (let == "ogg" or let == "mp3" or let == "wav"):
                songs = os.path.join(self.song_dir, song)
                song_lists.append(songs)
            elif(let == "ini"):
                data = os.path.join(self.song_dir, song)
                song_data.append(data)

        self.song_list = [song_lists, song_data]
        
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
        pg.mixer.music.load(self.bg_main)

        ### gameloop start
        self.run()
        
    def run(self):      ########################## Game Loop
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            pg.display.flip()

        pg.mixer.music.fadeout(600)
    
    def update(self):   ########################## Game Loop - Update
        self.all_sprites.update()       #screen update
        self.second = ((pg.time.get_ticks() - self.start_tick) / 1000)      #play time calculation
        
    def events(self):   ########################## Game Loop - Events
        mouse_coord = pg.mouse.get_pos()    #mouse coord value
        mouse_move = False      #mouse move Boolean value
        mouse_click = 0         #mouse click value (1: left, 2: scroll, 3: right, 4: scroll up, 5: scroll down)
        key_click = 0           #key value (275: right, 276: left, 273: up, 274: down, 13: enter)

        ### Event Check
        for event in pg.event.get():
            if event.type == pg.QUIT:       #exit
                if self.playing:
                    self.playing = False
                    self.running = False
                 
            elif event.type == pg.KEYDOWN:      #keyboard check
                key_click = event.key

                if self.screen_mode < 4:
                    self.sound_click.play()

            elif event.type == pg.MOUSEMOTION:
                if event.rel[0] != 0 or event.rel[1] != 0:    #mousemove
                    mouse_move = True
                    
            elif event.type == pg.MOUSEBUTTONDOWN:      #mouse click
                mouse_click = event.button

                if self.screen_mode < 4:
                    self.sound_click.play()
                    
        ### Logo Screen1
        if self.screen_mode == 0:
            self.screen_value[0] += 1

            if self.screen_value[0] > 90:
                self.screen_value[1] += 5

            if self.screen_value[1] == 300:
                self.screen_value[0] = 0
                self.screen_value[1] = 0
                self.screen_mode = 1
                pg.mixer.music.play(loops = -1)
                
        ### Logo Screen2     
        elif self.screen_mode == 1:                
            if self.screen_value[3] == 0:
                if self.screen_value[0] < 255:
                    self.screen_value[0] += 5
                else:
                    if mouse_click == 1 or key_click != 0:
                        self.screen_value[3] = 1
            else:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= 17
                else:
                    self.screen_mode = 2
                    self.screen_value[1] = 2
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
                    
        ### Main Screen
        elif self.screen_mode == 2:
            if self.screen_value[2] == 0:
                if self.screen_value[0] < 255:
                    self.screen_value[0] += 17
                else:
                    for i in range(4):      #mouse cursor check
                        if mouse_move and mouse_coord[0] > 400 and mouse_coord[0] < 560 and mouse_coord[1] > 105 + i*70 and mouse_coord[1] < 155 + i*70:
                            self.screen_value[1] = i + 1

                    if (key_click == 273 or mouse_click == 4) and self.screen_value[1] > 1:     #key up check
                        self.screen_value[1] -= 1

                    if (key_click == 274 or mouse_click == 5) and self.screen_value[1] < 4:   #key down check
                        self.screen_value[1] += 1

                    if (mouse_click == 1 or key_click == 13):      #click or key enter check
                        if self.screen_value[1] == 1:       #START
                            self.screen_value[2] = 1
                        elif self.screen_value[1] == 2:     #HELP
                            self.screen_value[0] = 85
                            self.screen_value[2] = 2
                        elif self.screen_value[1] == 3:     #EXIT
                            self.screen_value[2] = 3
                        else:                               #Languague
                            if self.language_mode < len(self.language_list) - 1:
                                self.language_mode += 1
                            else:
                                self.language_mode = 0

                            self.gameFont = os.path.join(self.fnt_dir, self.language_list[self.language_mode][1])
                        
            elif self.screen_value[2] == 1:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= 17
                else:
                    self.screen_mode = 3
                    self.screen_value[1] = 0
                    self.screen_value[2] = 0

            elif self.screen_value[2] == 2:
                if (mouse_click == 1 or key_click != 0):
                    self.screen_value[2] = 0

            elif self.screen_value[2] == 3:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= 17
                else:
                    self.playing = False
                    self.running = False

        ### Stage Select Screen
        elif self.screen_mode == 3:
            if self.screen_value[1] == 0:
                if self.screen_value[0] < 255:
                    self.screen_value[0] += 5
        
    def draw(self):     ########################## Game Loop - Draw
        self.all_sprites.draw(self.screen)

        self.background = pg.Surface((WIDTH, HEIGHT))
        self.background = self.background.convert()
        self.background.fill(WHITE)
        self.screen.blit(self.background, (0,0))
        self.draw_screen(self.screen_mode)                      #draw screen
        
        pg.display.update()

    def draw_screen(self, mode):        # Draw Screen
        if mode == 0:       #logo screen1
            screen_alpha = 255 - min(self.screen_value[1], 255)
            self.spr_printed.set_alpha(screen_alpha)
            self.screen.blit(self.spr_printed, (93, 200))
        
        elif mode == 1:     #logo screen2
            screen_alpha = self.screen_value[0]
            
            if self.screen_value[3] == 0:
                self.spr_logoback.set_alpha(screen_alpha)
            else:
                self.spr_logoback.set_alpha(255)
                
            spr_logoRescale = pg.transform.scale(self.spr_logo, (301 + self.screen_value[1], 306 + self.screen_value[1]))
            spr_logoRescale.set_alpha(screen_alpha)
            self.screen.blit(self.spr_logoback, (0, 0))
            self.screen.blit(spr_logoRescale, (320 - round(self.screen_value[1] / 2), 40 - round(self.screen_value[1] / 2)))
            
        elif mode == 2:     #main screen
            screen_alpha = self.screen_value[0]
            select_index = [False, False, False, False]
            
            if self.screen_value[2] == 0:
                self.spr_logoback.set_alpha(255)
                self.screen.blit(self.spr_logoback, (0, 0))
            else:
                self.spr_logoback.set_alpha(screen_alpha)
                
                if self.screen_value[2] == 2:
                    self.screen.blit(self.spr_logoback, (0, 0))
                else:
                    self.screen.blit(self.spr_logoback, (round((screen_alpha - 255) / 10), 0))
            
            for i in range(4):
                if i + 1 == self.screen_value[1]:
                    select_index[i] = True
                
            if self.screen_value[2] == 2:
                help_surface = pg.Surface((WIDTH - 60, HEIGHT - 60))
                help_surface.fill(WHITE)
                help_surface.set_alpha(200)                  
                self.screen.blit(help_surface, pg.Rect(30, 30, 0, 0))

                self.draw_text("- " + self.language_list[self.language_mode][5] + " -", 36, BLACK, 320, 50, 255)
                self.draw_text(self.language_list[self.language_mode][6], 16, BLACK, 320, 150)
                self.draw_text(self.language_list[self.language_mode][7], 16, BLACK, 320, 220)
                self.draw_text(self.language_list[self.language_mode][8], 16, BLACK, 320, 290)
            else:
                self.draw_text(self.language_list[self.language_mode][2], 36, BLACK, 480, 105, screen_alpha, select_index[0])
                self.draw_text(self.language_list[self.language_mode][3], 36, BLACK, 480, 175, screen_alpha, select_index[1])
                self.draw_text(self.language_list[self.language_mode][4], 36, BLACK, 480, 245, screen_alpha, select_index[2])
                self.draw_text(self.language_list[self.language_mode][0], 24, BLACK, 480, 315, screen_alpha, select_index[3])
  
        elif mode == 3:     #stage select screen
            screen_alpha = self.screen_value[0]

            song_na
            for song in self.song_list:
                

                
            self.draw_text(self.language_list[self.language_mode][2], 36, BLACK, 480, 105, screen_alpha, select_index[0])
            self.draw_text(self.language_list[self.language_mode][3], 36, BLACK, 480, 175, screen_alpha, select_index[1])
            self.draw_text(self.language_list[self.language_mode][4], 36, BLACK, 480, 245, screen_alpha, select_index[2])
            
    def draw_text(self, text, size, color, x, y, alpha = 255, boldunderline = False):   # Draw Text
        font = pg.font.Font(self.gameFont, size)
        font.set_underline(boldunderline)
        font.set_bold(boldunderline)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
            
        if (alpha == 255):
            self.screen.blit(text_surface, text_rect)
        else:
            surface = pg.Surface((len(text) * (size + 20), size + 20))
            surface.fill(WHITE)
            surface.blit(text_surface, pg.Rect(0, 0, 10, 10))
            surface.set_alpha(alpha)
            self.screen.blit(surface, text_rect)

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
