import pygame
from const import *
class Slider():
    def __init__(self,sc):
        self.condition = 30 #значение slider
        self.screen = sc
        self.min = 0
        self.max = 100
        self.posPoint = 350 #позиция точки ролика
        self.x = 89
        self.y = 944
        self.h = 30
        self.w = 1121
        self.fontNormal = pygame.font.SysFont(font_name, 35, bold=True)
    def Draw(self):
        """ Рисуем слайдер, ролик и значения времени и ось координат для графиков """

        pygame.draw.rect(self.screen, dopCollor, (89, 944, 1121, 20),
                         border_radius=borderRad)  # слайдер
        pygame.draw.rect(self.screen, borderCollor, (89, 944, 1121, 20), 5,
                         border_radius=borderRad)  # слайдер
        pygame.draw.circle(self.screen, ellsCollor, (self.posPoint, 954), 20)  # точка
        pygame.draw.circle(self.screen, borderCollor, (self.posPoint, 954), 20, 2)  # точка

        self.Surface1 = self.fontNormal.render("0", True, textCollor)
        self.Rect1 = self.Surface1.get_rect(topleft=(self.x-14, self.y - 45), size=(20, 20))
        self.screen.blit(self.Surface1, self.Rect1)

        self.Surface2 = self.fontNormal.render(str(self.max), True, textCollor)
        self.Rect2 = self.Surface2.get_rect(topleft=(self.x + self.w - 25, self.y - 45), size=(50, 20))
        self.screen.blit(self.Surface2, self.Rect2)

        self.Surface3 = self.fontNormal.render(str(self.condition), True, textCollor)
        self.Rect3 = self.Surface3.get_rect(topleft=(self.posPoint -15, self.y + 25), size=(50, 20))
        self.screen.blit(self.Surface3, self.Rect3)


        """Ось координат графика"""
        #0Y
        pygame.draw.line(self.screen, borderCollor, (self.x, 610),
                         (self.x, 880), 5)
        pygame.draw.line(self.screen, borderCollor, (self.x, 600),
                         (self.x-10, 610), 5)
        pygame.draw.line(self.screen, borderCollor, (self.x, 600),
                         (self.x+10, 610), 5)
        #подпись оси y
        self.Surface4 = self.fontNormal.render(str(1000), True, textCollor)
        self.Rect4 = self.Surface4.get_rect(topleft=(self.x - 75, 610), size=(50, 20))
        self.screen.blit(self.Surface4, self.Rect4)
        pygame.draw.line(self.screen, borderCollor, (self.x-10, 630),
                         (self.x+10, 630), 5)

        #0X
        pygame.draw.line(self.screen, borderCollor, (self.x, 880),
                         (self.x + self.w+20, 880), 5)
        pygame.draw.line(self.screen, borderCollor, (self.x + self.w +30, 880),
                         (self.x + self.w+20, 870), 5)
        pygame.draw.line(self.screen, borderCollor, (self.x + self.w +30, 880),
                         (self.x + self.w+20, 890), 5)

        pygame.draw.line(self.screen, borderCollor, (self.x+self.w, 880+10),
                         (self.x+self.w, 880-10), 5)

    def Change(self,mosPos):
        """ При нажатии на слайдер меняем положение ролика и значение состояния времени """

        if self.x <= mosPos[0] <= self.x + self.w and self.y <= mosPos[1] <= self.y + self.h:
            self.posPoint = mosPos[0]
            self.condition = int((self.posPoint-79)*self.max/self.w)
            #print("T:",self.condition)

    def ImportMaxT(self,T):
        """ Обновляем максимальное значение времени """
        self.max = T