import pygame
from const import *
class InputBox():
    def __init__(self,x,y,sc):
        self.condition = True #флаг доступности IB True=возможно активировать, False=невозможно активировать
        self.changed = False #флаг активированного IB True=активный
        self.error = False #флаг некорректного значения True=ошибка
        self.screen = sc
        self.x = x
        self.y = y
        self.w = 45
        self.h = 30
        self.backColor = dopCollor
        self.textColor = textCollor
        self.fontBold = pygame.font.SysFont(font_name, 24, bold=True)
        self.fontNormal = pygame.font.SysFont(font_name, 20, bold=True)

        self.inputText = "0"
    def Draw(self):
        """ Рисуем IB, его обводку и текст в нем"""
        if self.condition:
            self.backColor = dopCollor
            if self.changed:
                self.textColor = activeCollor
            else:
                self.textColor = textCollor
        else:
            self.backColor = mainCollor
            self.textColor = textCollor

        pygame.draw.rect(self.screen, self.backColor, (self.x, self.y, self.w, self.h), border_radius=borderRad)
        if self.error:
            pygame.draw.rect(self.screen, errorCollor, (self.x, self.y, self.w, self.h), 3, border_radius=borderRad)
        if self.changed:
            pygame.draw.rect(self.screen, borderCollor, (self.x, self.y, self.w, self.h), 3, border_radius=borderRad)

        text_surface = self.fontNormal.render(self.inputText, True, self.textColor)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (self.x + 5, self.y + self.h // 2)
        self.screen.blit(text_surface, text_rect)

    def Change(self,mosPos):
        """ При нажатии на IB активируем его и меняем содержимое"""
        if self.x <= mosPos[0] <= self.x + self.w and self.y <= mosPos[1] <= self.y + self.h and self.condition:
            text = self.OnChenged()
            return True
        return False

    def UnActive(self):
        """ Блокируем IB делаем его недоступным """
        self.condition = False
        self.OffChenged()

    def OffChenged(self):
        """  Дизактивируем IB """
        self.changed = False

    def OnChenged(self):
        """  Aктивируем IB """
        self.changed = True
        return self.inputText

    def NewText(self,newText):
        """ Меняем содержимое IB """
        if self.changed:
            self.inputText = newText
