import pygame
from const import *
class ChackBox():
    def __init__(self,x,y,sc):
        self.condition = True #флаг, True=галочка, False=отсутствие галочки
        self.screen = sc
        self.x = x
        self.y = y
        self.w = 60
        self.h = 60
    def Draw(self):
        """ Рисуем CB """
        self.screen.blit(chackbox, (self.x, self.y))  # бокc
        if self.condition:
            self.screen.blit(true, (self.x, self.y))  # галочка
    def ChangeCB(self,mosPos):
        """ При нажатии меняем значение CB """
        if self.x <= mosPos[0] <= self.x + self.w and self.y <= mosPos[1] <= self.y + self.h:
            self.condition = not(self.condition)
