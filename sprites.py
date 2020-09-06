import pygame as pg
import random
import time
import os

"""
class Circle(pg.sprite.Sprite):

class Shot(pg.sprite.Sprite):

class Effect(pg.sprite.Sprite):

"""

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    #불러온 이미지(self.spritesheet)를  (0,0)에 불러오며, 이미지의(x,y)부터 (width, height)까지 자르겠다.
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        
        return image

