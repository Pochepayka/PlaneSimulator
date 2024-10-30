import pygame
from const import *
from inputbox import InputBox
class Bort():
    def __init__(self,x,y,i,sc):
        self.condition = i #номер борта в массиве
        self.screen = sc
        self.x = x
        self.y = y
        self.w = 60
        self.h = 60
        self.color = bortsColor
        self.textBorts = ["Борт1 (основной)","Борт2","Борт3","Борт4","Борт5","Борт6","Борт7","Борт8"]
        self.textParam = ["V =", "P =", "Tн =", "Tк =", "Xн =", "Yн ="]
        self.active = True #флаг, True=изменяются параметры, False=параметры обработаны и неизменны
        self.fontBold = pygame.font.SysFont(font_name, 24, bold=True)
        self.fontNormal = pygame.font.SysFont(font_name, 20, bold=True)

        self.inputText = "0"
        self.IBs = [InputBox(self.x+100,self.y+45,self.screen),InputBox(self.x+190,self.y+45,self.screen),
                    InputBox(self.x+280,self.y+45,self.screen),InputBox(self.x+370,self.y+45,self.screen),
                    InputBox(self.x+460,self.y+45,self.screen),InputBox(self.x+550,self.y+45,self.screen)]
                    #список inputboxs конкретного борта

    def Draw(self):
        """ Пририсовываем конкретный борт """
        pygame.draw.rect(self.screen, mainCollor, (1285, self.y, 596, 81), border_radius=borderRad)  #борт
        pygame.draw.circle(self.screen, self.color[self.condition-1], (self.x+30, self.y+40), 15) #цвет борта

        self.Surface = self.fontBold.render(self.textBorts[self.condition-1], True, textCollor)
        self.Rect = self.Surface.get_rect(topleft=(self.x + 66, self.y +10), size=(35, 180))
        self.screen.blit(self.Surface, self.Rect)

        for i in range (len(self.textParam)):
            self.SurfaceI = self.fontNormal.render(self.textParam[i], True, textCollor)
            self.RectI = self.SurfaceI.get_rect(topleft=(self.x + 60 + 90*i, self.y +50), size=(30, 45))
            self.screen.blit(self.SurfaceI, self.RectI)

        for ib in self.IBs:
            ib.Draw() #рисуем inputboxs

    def StopChange(self):
        """ Сбрасывает состояние inputboxs в не активное """
        for ib in self.IBs:
            ib.OffChenged()

    def Change(self,mosPos):
        """ Обновляет данные введенных значений в inputbox """
        for ib in self.IBs:
            if ib.Change(mosPos):
                self.StopChange()
                text = ib.OnChenged()
                return text
        return

    def UnActive(self):
        """ Останавливает возможность изменение параметров борта """
        for ib in self.IBs:
            ib.UnActive()





