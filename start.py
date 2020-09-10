# [Python pygame Game] 4 Beats
# made by "PrintedLove"
# https://printed.tistory.com/
# This game was created with reference to ParkJuneWoo(korca0220)'s [Finding-the-Rabbit]
#-*-coding: utf-8
import pygame as pg
import os, time, random

TITLE = "4 Beats"       ### default setting
WIDTH = 640
HEIGHT = 480
FPS = 60
DEFAULT_FONT = "NotoSansCJKkr-Regular.otf"

WHITE = (238, 238, 238)     ### color setting
BLACK = (32, 36, 32)
RED = (246, 36, 74)
BLUE = (32, 105, 246)

class Game:
    def __init__(self): ########################## Game Start
        pg.init()
        pg.mixer.init()     #sound mixer
        pg.display.set_caption(TITLE)       #title name
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))      #screen size
        self.screen_mode = 0    #screen mode (0: logo, 1: logo2, 2: main, 3: stage select, 10: play)
        self.screen_value = [-450, 0, 0, 0]       #screen management value
        self.clock = pg.time.Clock()        #FPS timer
        self.start_tick = 0     #game timer
        self.running = True     #game initialize Boolean value
        self.language_mode = 0         #0: english, 1: korean, 2~: custom
        self.song_select = 1    #select song
        self.load_date()        #data loading

    def load_date(self): ########################## Data Loading
        self.dir = os.path.dirname(__file__)
        
        ### font
        self.fnt_dir = os.path.join(self.dir, 'font')
        self.gameFont = os.path.join(self.fnt_dir, DEFAULT_FONT)
        language_file = open(os.path.join(self.fnt_dir, 'language.ini'), "r", encoding = 'UTF-8')
        language_lists = language_file.read().split('\n')
        language_file.close()
        self.language_list = [n.split("_") for n in language_lists]
        
        ### image
        self.img_dir = os.path.join(self.dir, 'image')
        pg.display.set_icon(pg.image.load(os.path.join(self.img_dir, 'icon.png')))      #set icon
        self.spr_printed = pg.image.load(os.path.join(self.img_dir, 'printed.png'))
        self.spr_logoback = pg.image.load(os.path.join(self.img_dir, 'logoback.png'))
        self.spr_logo = pg.image.load(os.path.join(self.img_dir, 'logo.png'))
        
        ### sound
        self.snd_dir = os.path.join(self.dir, 'sound')
        self.bg_main = os.path.join(self.snd_dir, 'bg_main.ogg')
        self.sound_click = pg.mixer.Sound(os.path.join(self.snd_dir, 'click.ogg'))
        self.sound_drum1 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum1.ogg'))
        self.sound_drum2 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum2.ogg'))
        self.sound_drum3 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum3.ogg'))
        self.sound_drum4 = pg.mixer.Sound(os.path.join(self.snd_dir, 'drum4.ogg'))

        ### song
        self.sng_dir = os.path.join(self.dir, 'song')
        music_type = ["ogg", "mp3", "wav"]
        self.song_list = [i.split('.')[0] for i in os.listdir(self.sng_dir) if i.split('.')[-1] in music_type]
        self.song_num = len(self.song_list)

    def new(self):      ########################## Game Initialize
        self.circle_rot = 0     #circle rotation value
        self.circle_dir = 0     #circle direction value
        self.textbox_show = 0       #textbox show Boolean value
        self.textbox_text = ""      #textbox text
        self.all_sprites = pg.sprite.Group()        #sprite group
        self.effects = pg.sprite.Group()
        self.bars = pg.sprite.Group()
        self.start_tick = pg.time.get_ticks()   #playtime timer
        pg.mixer.music.load(self.bg_main)       #bgm
        self.run()      #gameloop start
        
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
        
        for event in pg.event.get():                        ### Event Check
            if event.type == pg.QUIT:       #exit
                if self.playing:
                    self.playing, self.running = False, False 
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
        
        if self.screen_mode == 0:           ### Logo Screen1
            self.screen_value[0] += 5

            if self.screen_value[0] == 300:
                self.screen_value[0] = 0
                self.screen_mode = 1
                pg.mixer.music.play(loops = -1)    
        elif self.screen_mode == 1:             ### Logo Screen2          
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
        elif self.screen_mode == 2:                     ### Main Screen
            if self.screen_value[2] == 0:
                if self.screen_value[0] < 255:
                    self.screen_value[0] += 17
                else:
                    for i in range(4):                  #mouse cursor check
                        if mouse_move and mouse_coord[0] > 400 and mouse_coord[0] < 560 and mouse_coord[1] > 105 + i*70 and mouse_coord[1] < 155 + i*70:
                            self.screen_value[1] = i + 1

                    if (key_click == 273 or mouse_click == 4) and self.screen_value[1] > 1:     #key up check
                        self.screen_value[1] -= 1
                    elif (key_click == 274 or mouse_click == 5) and self.screen_value[1] < 4:   #key down check
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
                            self.language_mode = self.language_mode + 1 if self.language_mode < len(self.language_list) - 1 else 0
                            self.gameFont = os.path.join(self.fnt_dir, self.load_language(1)) if self.load_language(1) != "ERROR" else DEFAULT_FONT 
            elif self.screen_value[2] == 1:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= 17
                else:
                    self.screen_mode = 3
                    self.screen_value[1] = 0
                    self.screen_value[2] = 0
            elif self.screen_value[2] == 2:
                if mouse_click == 1 or key_click != 0:
                    self.screen_value[2] = 0
            elif self.screen_value[2] == 3:
                if self.screen_value[0] > 0:
                    self.screen_value[0] -= 17
                else:
                    self.playing, self.running = False, False
        elif self.screen_mode == 3:                     ### Song Select Screen
            if self.screen_value[0] < 255:
                self.screen_value[0] += 5

            if (key_click == 273 or mouse_click == 4) and self.song_select > 1:     #key up check
                self.song_select -= 1
                self.screen_value[0] -= 20
            elif (key_click == 274 or mouse_click == 5) and self.song_select < self.song_num:   #key down check
                self.song_select += 1
                self.screen_value[0] -= 20
        
    def draw(self):     ########################## Game Loop - Draw
        self.all_sprites.draw(self.screen)
        self.background = pg.Surface((WIDTH, HEIGHT))           #white background
        self.background = self.background.convert()
        self.background.fill(WHITE)
        self.screen.blit(self.background, (0,0))
        self.draw_screen(self.screen_mode)                      #draw screen
        self.draw_textbox()         #draw textbox(warnning, error message)
        pg.display.update()

    def draw_screen(self, mode):                    # Draw Screen
        screen_alpha = self.screen_value[0]
        
        if mode == 0:       #logo screen1
            screen_alpha = 255 - min(max(self.screen_value[0], 0), 255)
            self.spr_printed.set_alpha(screen_alpha)
            self.screen.blit(self.spr_printed, (93, 200))
        elif mode == 1:     #logo screen2
            self.spr_logoback.set_alpha(screen_alpha) if self.screen_value[3] == 0 else self.spr_logoback.set_alpha(255)
            spr_logoRescale = pg.transform.scale(self.spr_logo, (301 + self.screen_value[1], 306 + self.screen_value[1]))
            spr_logoRescale.set_alpha(screen_alpha)
            self.screen.blit(self.spr_logoback, (0, 0))
            self.screen.blit(spr_logoRescale, (320 - round(self.screen_value[1] / 2), 40 - round(self.screen_value[1] / 2)))
        elif mode == 2:     #main screen
            select_index = [True if self.screen_value[1] == i + 1 else False for i in range(4)]
            
            if self.screen_value[2] == 0:
                self.spr_logoback.set_alpha(255)
                self.screen.blit(self.spr_logoback, (0, 0))
            else:
                self.spr_logoback.set_alpha(screen_alpha)
                logoback_coord = 0 if self.screen_value[2] == 2 else round(screen_alpha - 255) / 10
                self.screen.blit(self.spr_logoback, (logoback_coord, 0))
                
            if self.screen_value[2] == 2:
                help_surface = pg.Surface((WIDTH - 60, HEIGHT - 60))
                help_surface.fill(WHITE)
                help_surface.set_alpha(200)                  
                self.screen.blit(help_surface, pg.Rect(30, 30, 0, 0))
                self.draw_text("- " + self.load_language(5) + " -", 36, BLACK, 320, 50, 255)
                self.draw_text(self.load_language(7), 16, BLACK, 320, 150)
                self.draw_text(self.load_language(8), 16, BLACK, 320, 220)
                self.draw_text(self.load_language(9), 16, BLACK, 320, 290)
            else:
                self.draw_text(self.load_language(2), 36, BLACK, 480, 105, screen_alpha, select_index[0])
                self.draw_text(self.load_language(3), 36, BLACK, 480, 175, screen_alpha, select_index[1])
                self.draw_text(self.load_language(4), 36, BLACK, 480, 245, screen_alpha, select_index[2])
                self.draw_text(self.load_language(0), 24, BLACK, 480, 315, screen_alpha, select_index[3])
        elif mode == 3:     #song select screen
            surface = pg.Surface((WIDTH, HEIGHT))
            surface.fill(WHITE)
            pg.draw.circle(surface, BLACK, (750, round(HEIGHT / 2)), 770, 1)
            pg.draw.circle(surface, BLACK, (750, round(HEIGHT / 2)), 460, 1)
            pg.draw.circle(surface, BLACK, (750, round(HEIGHT / 2)), 200, 1)
            pg.draw.circle(surface, RED, (750, round(HEIGHT / 2)), 470, 1)
            pg.draw.circle(surface, BLUE, (750, round(HEIGHT / 2)), 450, 1)
            surface.set_alpha(max(screen_alpha - 200, 0))
            self.screen.blit(surface, (0,0))
            
            if self.song_select > 2:
                self.draw_text(self.song_list[self.song_select - 3], 16, BLACK, 180, HEIGHT / 2 - 140, max(screen_alpha - 220, 0))
                
            if self.song_select > 1:
                self.draw_text(self.song_list[self.song_select - 2], 18, BLACK, 170, HEIGHT / 2 - 80, max(screen_alpha - 180, 0))
                self.draw_text("△", 24, BLACK, 190, HEIGHT / 2 -210, screen_alpha)
                #△▽▲▼
            self.draw_text(self.song_list[self.song_select - 1], 20, BLACK, 160, HEIGHT / 2 - 20, screen_alpha)

            if self.song_select < self.song_num:
                self.draw_text(self.song_list[self.song_select], 18, BLACK, 170, HEIGHT / 2 + 40, max(screen_alpha - 180, 0))
                self.draw_text("▽", 24, BLACK, 190, HEIGHT / 2 + 150, screen_alpha)

            if self.song_select < self.song_num - 1:
                self.draw_text(self.song_list[self.song_select + 1], 16, BLACK, 180, HEIGHT / 2 + 100, max(screen_alpha - 220, 0))

            self.draw_text("★★★☆☆", 32, BLACK, 430, HEIGHT / 2 - 100, screen_alpha)
            self.draw_text(self.load_language(2), 32, BLACK, 425, HEIGHT / 2 + 20, screen_alpha)
            self.draw_text(self.load_language(6), 32, BLACK, 450, HEIGHT / 2 + 80, screen_alpha)

    def load_language(self, index):
        try:
            return self.language_list[self.language_mode][index]
        except:
            return "ERROR"

    def draw_textbox(self):         
        if (self.textbox_show > 0 and not(self.textbox_show)):
            self.textbox_show -= 1
            self.draw_text(textbox_text, 36, RED, WIDTH / 2, HEIGHT / 2)
            
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
            surface = pg.Surface((len(text) * size, size + 20))
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
