# [Python pygame Game] 4 Beats
# made by "PrintedLove"
# https://printed.tistory.com/

import pygame as pg
import random
import time
import os
from sprites import *

TITLE = "4 Beats"
WIDTH = 640
HEIGHT = 480
FPS = 60
FONT_NAME = 'neodgm.ttf'

class Game:
    def __init__(self): ########################## 게임 시작
        pg.init()
        pg.mixer.init()     #사운드 믹서
        pg.display.set_caption(TITLE)       #타이틀 이름
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))      #화면 사이즈 세팅
        self.clock = pg.time.Clock()        #FPS 설정용 타이머
        self.running = True     #게임 실행 Boolean 값
        self.selecting = True       #메뉴 선택 Boolean 값
        self.load_date()        #데이터 로딩 함수 실행

    def load_date(self): ########################## 파일 로딩
        self.dir = os.path.dirname(__file__)
        
        ### 폰트
        self.gameFont = os.path.join(os.path.join(self.dir, 'font'), FONT_NAME)
        
        ### 이미지
        self.img_dir = os.path.join(self.dir, 'image')
        
        self.spr_logoback = Spritesheet(os.path.join(self.img_dir, 'logoback.png'))
        self.spr_logo = Spritesheet(os.path.join(self.img_dir, 'logo.png'))
        self.spr_button_logo = Spritesheet(os.path.join(self.img_dir, 'button_logo.png'))
        self.spr_buttonEffect_logo = Spritesheet(os.path.join(self.img_dir, 'buttonEffect_logo.png'))

        ### 배경음악, 효과음
        self.snd_dir = os.path.join(self.dir, 'sound')
        
        self.sound_bg_main = pg.mixer.Sound(os.path.join(self.snd_dir, 'theaudioway.ogg'))
        
    def new(self):      ########################## 게임 초기화
        ###변수 초기화
        self.score = 0;     #점수
        self.stage = 1;     #스테이지
        self.circle_rot = 0;     #중심 회전값

        ### 스프라이트 그룹
        self.all_sprites = pg.sprite.Group()
        self.effects = pg.sprite.Group()
        self.bars = pg.sprite.Group()

        ### 플레이 타임 타이머
        self.start_tick = pg.time.get_ticks()
        
        ### 배경 음악 실행
        pg.mixer.music.load(self.sound_bg_main)

        ### 점수값 로드
        with open(os.path.join(self.dir, 'highscore.txt'), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        ### 게임 루프 실행
        self.run()
        
    def run(self):      ########################## 게임 루프
        pg.mixer.music.play(loops = -1)
        
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        pg.mixer.music.fadeout(600)
    
    def update(self):   ########################## 게임 루프 - 업데이트
        self.all_sprites.update()       #화면 업데이트
        self.second = ((pg.time.get_ticks() - self.start_tick) / 1000)      #플레이 타임 계산
        
    def events(self):   ########################## 게임 루프 - 이벤트
        for event in pg.event.get():
            if event.type == pg.QUIT:       #종료
                self.start = False
                
                if self.playing:
                    self.playing = False
                    self.running = False
        
    def draw(self):     ########################## 게임 루프 - 드로우
        self.all_sprites.draw(self.screen)

        self.screen.blit(self.spr_logoback, (0, 0))
        
        pg.display.update()

g = Game()

while g.start:
    #g.show_start_screen()
    
    while g.running:
        g.new()
            
pg.quit()
