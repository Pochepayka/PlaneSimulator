import pygame
from const import *
from bort import Bort
class Plus():
    def __init__(self,sc):
        self.condition = 1 #кол-во прорисованных бортов
        self.screen = sc
        self.delta = 91
        self.x = 1567
        self.y = 50+91
        self.h = 50
        self.w = 50
        self.borts = [Bort(1285,33,1,self.screen)] #массив бортов
        self.uncorrect =False #флаг корректности параметров борта
        self.listParam=[] #данные всех бортов
        self.lastListParam=[] #данные последнего борта
        self.errorParam = [False,False,False,False,False,False] #флаги ошибок в корректности параметра True=ошибка
        self.oversteck =False #флаг переполнения количества бортов True=переполнение

    def Draw(self):
        """Прорисовывыем плюс и все доступные борта"""

        if (self.condition<8) and self.oversteck==False:
            self.screen.blit(plus, (self.x, self.y))  # плюс
        for el in self.borts:
            el.Draw()

    def Change(self,mosPos):
        """ Проверяем нажатие плюса и в случае корректных параметров борта и отсутствие переполнения
            добавляем новый борт и отправляем данные на сервер для создания траектории по параметрам борта"""

        if self.condition>0:
            self.CheckCorrect()

        if (self.x <= mosPos[0] <= self.x + self.w and self.y <= mosPos[1] <= self.y + self.h) and self.condition<8 :
            #плюс нажат и нет переполнения

            if self.uncorrect==False:# or self.condition==0:
                #параметры корректны

                self.y +=self.delta
                if len(self.borts) >= 1: #существует хотябы 1 борт
                    self.borts[len(self.borts) - 1].UnActive()
                if self.condition<7: #не последний борт
                    self.condition += 1
                    newBort = Bort(1285,33+self.delta*(self.condition-1),self.condition,self.screen)
                    self.borts.append(newBort)

                else: #последний борт
                    self.oversteck = True

                for i in range(6): #обнуление флагов ошибки
                    self.borts[self.condition-2].IBs[i].error = False

                if self.lastListParam!=[]: #список не пуст
                    self.listParam.append(self.lastListParam)

                if self.condition != 1: # не нулевой борт (пока без параметров)
                    return(self.lastListParam)#GoServer(self.lastListParam))

            else: #параметры некорректны
                for i in range(6):
                    self.borts[self.condition - 1].IBs[i].changed = False
                    if self.errorParam[i]:
                        self.borts[self.condition-1].IBs[i].error = True
                    else:
                        self.borts[self.condition-1].IBs[i].error = False
            return([[]])
                #self.CheckCorrect()




    def NewText (self,newText):
        """
        Обновляет текст для всех связанных элементов.

        Параметры:
        newText (str): Новый текст, который нужно установить.

        Возвращает:
        str: Обновленный текст.
        """

        newText = str(self.toInt(newText))[:4]
        for bort in self.borts:
           for ib in bort.IBs:
               ib.NewText(newText)
        return newText


    def toInt(self,string):
        """
        Преобразует строку в целое число.

        Параметры:
        string (str): Входная строка.

        Возвращает:
        int: Преобразованное целое число.
        """

        nums=[0]
        try:
            for i in string:
                try:
                    nums.append(int(i))
                except:
                    print()
        except:
            print()
        res = ""
        for num in nums:
            res = res + str(num)
        return int(res)

    def CheckCorrect(self):
        """
       Проверяет корректность параметров и обновляет флаги ошибок.

       Возвращает:
       bool: True, если параметры не корректны, False - если нет ошибки.
       """

        self.UpdateListParam()
        self.uncorrect = False
        self.errorParam = [False,False,False,False,False,False]
        if self.lastListParam[0] ==0:
            self.errorParam[0] = True
        if self.lastListParam[1] ==0 or self.lastListParam[1] > pMax:
            self.errorParam[1] = True
        if self.lastListParam[1] >9 and self.condition == 1:
            self.errorParam[1] = True
        if self.lastListParam[2] <0:
            self.errorParam[2] = True
        if self.lastListParam[3] <=self.lastListParam[2]:
            self.errorParam[3] = True
        if self.lastListParam[4] <0 or self.lastListParam[4] > xMax:
            self.errorParam[4] = True
        if self.lastListParam[5] <0 or self.lastListParam[5] > yMax:
            self.errorParam[5] = True

        for i in range(6):
            self.uncorrect = self.uncorrect or self.errorParam[i]

    def UpdateListParam(self):
        """Обновляет список параметров из связанных элементов"""
        self.lastListParam = []
        bort = self.borts[self.condition - 1]
        for ib in bort.IBs:
            self.lastListParam.append(int(ib.inputText))


