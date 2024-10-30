from const import *
from chackbox import ChackBox
from slider import Slider
from plus import Plus
from goToServer import GoServer
from cells import Cells
import pygame
#-------------oткрытие окна игры--------------
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Plane Simulate")
input_text=""
#-------------инициализация-------------------

fontBold = pygame.font.SysFont(font_name, 35, bold=True)
fontNormal = pygame.font.SysFont(font_name, 30, bold=True)
fontNormalNoBold = pygame.font.SysFont(font_name, 30, )

SettingSurface = fontBold.render("Настройки", True, textCollor)
SettingRect = SettingSurface.get_rect(topleft=(1520, 800), size=(35, 180))

ColorSurface = fontNormal.render("Цвет", True, textCollor)
ColorRect = SettingSurface.get_rect(topleft=(1360, 860), size=(35, 180))

PlainSurface = fontNormal.render("Самолет", True, textCollor)
PlainRect = SettingSurface.get_rect(topleft=(1360, 930), size=(35, 180))

PunctirSurface = fontNormal.render("Пунктир", True, textCollor)
PunctirRect = SettingSurface.get_rect(topleft=(1360, 1000), size=(35, 180))

ConnectSurface = fontNormal.render("Пересечение", True, textCollor)
ConnectRect = SettingSurface.get_rect(topleft=(1680, 860), size=(35, 180))

InfoSurface = fontNormal.render("Доп. инф-я", True, textCollor)
InfoRect = SettingSurface.get_rect(topleft=(1680, 930), size=(35, 180))

NoiseSurface = fontNormal.render("Сетка", True, textCollor)
NoiseRect = SettingSurface.get_rect(topleft=(1680, 1000), size=(35, 180))

CB1 = ChackBox(1285, 850, screen)
CB2 = ChackBox(1285, 920, screen)
CB3 = ChackBox(1285, 990, screen)
CB4 = ChackBox(1600, 850, screen)
CB5 = ChackBox(1600, 920, screen)
CB6 = ChackBox(1600, 990, screen)

listCB = [CB1.condition,CB2.condition,CB3.condition,CB4.condition,CB5.condition,CB6.condition]
listParam = [[]]
ListCord = []
ListConect = []
cordFirst = []

maxT = openT

Slider = Slider(screen)

Plus = Plus(screen)

Cell = Cells(screen)

"""настройка звука"""
#pygame.mixer.music.load(os.path.join(BASE, "media/music/main.mp3"))
#pygame.mixer.music.set_volume(0.2)
#pygame.mixer.music.play(-1)

#click = pygame.mixer.Sound(os.path.join(BASE, "media/music/click.mp3"))
#click.set_volume(0.2)

running = True
while running: #основной цикл программы
    pygame.time.Clock().tick(FPS)

    pygame.draw.rect(screen, mainCollor, (0, 0, screen_width, screen_height))  #подложка

    screen.blit(map, (15, 18))  #карта

    if listCB[5]:
        Cell.Draw() #клетка

    k = 0
    for bortCords in ListCord: #проход по всем бортам
        l = -1
        for i in range(len(bortCords) - 1): #проход по всем координатам точек

            if bortCords[i][0] <= Slider.condition - stepCord:  # and bortCords[i][1]<xMax and bortCords[i][2]<yMax:
                #координата раньше чем ограничивающая отметка времени
                color = (0, 0, 0)
                if listCB[0]: #цвет включен
                    color = Plus.borts[0].color[k]
                else: #цвет выключен
                    color = textCollor
                if listCB[2]: #пунктир включен
                    DashedLine(screen, (bortCords[i][1], bortCords[i][2]), (bortCords[i + 1][1], bortCords[i + 1][2]),
                               color, lineWidht, lineDash, lineGap)
                else: #пунктир выключен
                    pygame.draw.line(screen, color, (bortCords[i][1], bortCords[i][2]),
                                     (bortCords[i + 1][1], bortCords[i + 1][2]), lineWidht)
                l = i
        if listCB[1] and l>-1:# and bortCords[len(bortCords) - 1][1] < xMax and bortCords[len(bortCords) - 1][2] < yMax:
            #самолет включен и нарисовано хоть что-то из траетории
            screen.blit(plain, (bortCords[l+1][1] - 15, bortCords[l+1][2] - 15))
        k += 1


    if len(ListCord)>1 :
        ListConect = ChackConect(ListCord)
        for i in range(len(ListConect)):
            for j in range(len(ListConect[i])):
                if j+1 < len(ListConect[i]):
                    if ListConect[i][j+1][0]<=Slider.condition and ListConect[i][j+1][3] < conectEps and listCB[3]:
                        #пересечение включено, пересечение было до отметки ограничения времени,
                        #борты на растоянии меньше conectEps в одно и тоже время
                        screen.blit(conect, (ListConect[i][j][1]-15, ListConect[i][j][2]-15)) #пересечение


    if listCB[4]: #доп инф-я включена

        draw_rect_alpha(screen, (dopCollorAlfa), (848, 279, 410, 310) )#доп область
        pygame.draw.rect(screen, borderCollor, (848, 279, 410, 310), 1, border_radius=borderRad)  # обводка


        DopSurface = fontNormal.render("Доп. инф-я", True, textCollor)
        DopRect = DopSurface.get_rect(topleft=(989, 280), size=(35, 110))
        screen.blit(DopSurface, DopRect)

        """Вывод инф-и о параметре P"""
        DopSurface3 = fontNormalNoBold.render("""P=1: y = ct; P=2: y = -xt;""",True, textCollor)
        DopRect3 = DopSurface.get_rect(topleft=(865+50, 325), size=(35, 110))
        screen.blit(DopSurface3, DopRect3)

        DopSurface4 = fontNormalNoBold.render("""P=3: x = ct; P=4: y= xt;""",True, textCollor)
        DopRect4 = DopSurface.get_rect(topleft=(865+50, 355), size=(35, 110))
        screen.blit(DopSurface4, DopRect4)

        DopSurface5 = fontNormalNoBold.render("""P=5: y = -ct; P=6: -y = xt;""",True, textCollor)
        DopRect5 = DopSurface.get_rect(topleft=(865+50, 385), size=(35, 110))
        screen.blit(DopSurface5, DopRect5)

        DopSurface6 = fontNormalNoBold.render("""P=7: x = -ct; P=8: -y = -xt;""",True, textCollor)
        DopRect6 = DopSurface.get_rect(topleft=(865+50, 415), size=(35, 110))
        screen.blit(DopSurface6, DopRect6)

        DopSurface7 = fontNormalNoBold.render("""P=9: разворот;""",True, textCollor)
        DopRect7 = DopSurface.get_rect(topleft=(865+50, 445), size=(35, 110))
        screen.blit(DopSurface7, DopRect7)

        DopSurface8 = fontNormalNoBold.render("""P=10: наведение.""",True, textCollor)
        DopRect8 = DopSurface.get_rect(topleft=(865+50, 475), size=(35, 110))
        screen.blit(DopSurface8, DopRect8)

        """Вывод информации о органичениях по параметрам"""
        DopSurface1 = fontNormalNoBold.render(f"Огр-я: V > 0; 0 < P < {pMax}; Tк > Tн;", True, textCollor)
        DopRect1 = DopSurface.get_rect(topleft=(865, 523), size=(75, 355))
        screen.blit(DopSurface1, DopRect1)

        DopSurface2 = fontNormalNoBold.render(f"0 <= Xн < {xMax}; 0 <= Xк < {yMax}.", True, textCollor)
        DopRect2 = DopSurface.get_rect(topleft=(865, 553), size=(75, 355))
        screen.blit(DopSurface2, DopRect2)

    screen.blit(main, (0, 0))  #фон


    if len(ListCord) > 1:
        ListConect = ChackConect(ListCord)
        for i in range(len(ListConect)):

            """параметры для рисования графика"""
            x = 89
            y = 880
            MaxD = 1000
            deltaY = 250 / max(100, MaxD)
            deltaX = Slider.w / Slider.max
            color = Plus.borts[0].color[i + 1]

            for j in range(len(ListConect[i])):
                if j + 1 < len(ListConect[i]):
                    if MaxD>ListConect[i][j][3]:
                        # рисуем графики
                        pygame.draw.line(screen, color, (x+(ListConect[i][j][0])*deltaX, y-ListConect[i][j][3]*deltaY),
                                         (x+(ListConect[i][j+1][0])*deltaX, y-ListConect[i][j+1][3]*deltaY), lineWidht)


    pygame.draw.rect(screen, dopCollor, (1271, 18, 630, 1045), border_radius = borderRad) #правая область
    pygame.draw.rect(screen, borderCollor, (1271, 18, 630, 1045), 1, border_radius = borderRad) #обводка

    """ Рисуем chackboxs """
    CB1.Draw()
    CB2.Draw()
    CB3.Draw()
    CB4.Draw()
    CB5.Draw()
    CB6.Draw()

    """ Рисуем текст для chackboxs """
    screen.blit(SettingSurface, SettingRect)
    screen.blit(ColorSurface, ColorRect)
    screen.blit(PlainSurface, PlainRect)
    screen.blit(PunctirSurface, PunctirRect)
    screen.blit(ConnectSurface, ConnectRect)
    screen.blit(InfoSurface, InfoRect)
    screen.blit(NoiseSurface, NoiseRect)

    Slider.Draw() #слайдер

    Plus.Draw() #плюс

    pygame.display.flip() #переворот экрана



    """ Отслеживание событий (нажатий мыши и кнопок) """
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #крест (закрытие окна)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN: #нажатие ПКМ
            CB1.ChangeCB(event.pos)
            CB2.ChangeCB(event.pos)
            CB3.ChangeCB(event.pos)
            CB4.ChangeCB(event.pos)
            CB5.ChangeCB(event.pos)
            CB6.ChangeCB(event.pos)
            listCB = [CB1.condition, CB2.condition, CB3.condition, CB4.condition, CB5.condition, CB6.condition]

            Slider.Change(event.pos)

            newParamBort = Plus.Change(event.pos)

            if newParamBort != [[]] and newParamBort != None:

                listParam = Plus.listParam

                try:
                    maxT = FindMaxInColumn(listParam, 3)
                except:
                    print("maxT", maxT)

                Slider.ImportMaxT(maxT)
                Slider.Change([Slider.posPoint, Slider.y + 5])

                if ListCord ==[]:
                    newListCord = GoServer(newParamBort)
                    cordFirst = newListCord
                else:
                    newListCord = GoServer(newParamBort,cordFirst)

                ListCord.append(newListCord)

                for i in range(len(ListCord)):
                    ListCord[i]=InterpolatePoints(ListCord[i],stepCord,maxT)

            for bort in Plus.borts:
                input_text = bort.Change(event.pos)


        elif event.type == pygame.KEYDOWN: #нажатие кнопок клавиатуры
            if event.key == pygame.K_RETURN:
                input_text = Plus.NewText(input_text)
                for bort in Plus.borts:
                    bort.StopChange()
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
                input_text = Plus.NewText(input_text)
            else:
                try:
                    input_text += str(event.unicode)
                except:
                    print()
                input_text = Plus.NewText(input_text)


#------------end running------------------
pygame.quit()
print(listCB)
print(listParam)

