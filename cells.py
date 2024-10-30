import pygame
from const import *
class Cells():
    def __init__(self,sc):
        self.condition = 1 #масштаб клетки (не реализован)
        self.screen = sc
        self.x = 15
        self.y = 18
        self.w =1242
        self.h = 571
        self.fontNormal = pygame.font.SysFont(font_name, 12, bold=True)
        self.textCollor = (230,100,75)
    def Draw(self):
        """ Рисуем клетку и подписи координат """
        self.screen.blit(cels, (self.x, self.y))  # клетка
        for i in range(0,self.condition * self.w, 100):
            Surface = self.fontNormal.render(str(i), True, self.textCollor)
            Rect = Surface.get_rect(topleft=(self.x + i - 10, self.y + 10), size=(20, 20))
            self.screen.blit(Surface, Rect)
        for i in range(0,self.condition * self.h, 100):
            Surface = self.fontNormal.render(str(i), True, self.textCollor)
            Rect = Surface.get_rect(topleft=(self.x + 10, self.y + i - 10), size=(20, 20))
            self.screen.blit(Surface, Rect)
            #print(i,self.x + i - 10,self.y + self.h - 50)
    #def ChangeCB(self,mosPos):
    #    if self.x <= mosPos[0] <= self.x + self.w and self.y <= mosPos[1] <= self.y + self.h:
    #        self.condition = not(self.condition)
