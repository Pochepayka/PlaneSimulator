import os
import pygame
import sys
import math


HOST = '192.168.0.106'  # IP-адрес сервера
PORT = 65432  # Порт для подключения


# Основные цвета
mainCollor = (219, 235, 252)  # Основной цвет, вероятно, для фона или основных элементов
dopCollor = (192, 211, 231)  # Дополнительный цвет, возможно, для дополнительных элементов или подсветки
dopCollorAlfa = (192, 211, 231,200)  # Дополнительный цвет, возможно, для дополнительных элементов или подсветки
borderCollor = (174, 193, 213)  # Цвет для границ или разделителей
errorCollor = (250, 50, 50)  # Цвет для ошибок или проблемных состояний
textCollor = (73, 81, 90)  # Цвет для текстовых элементов
activeCollor = (20, 40, 150)  # Цвет для активных или выбранных состояний
ellsCollor = (120, 178, 252)  # Цвет для некоторых специфических элементов, возможно, связанных с эллипсами или другими фигурами

# Список для хранения цветов авиа-бортов
bortsColor = [(255,0,0),(255,255,0),(0,255,0),(0,0,255),(0,255,255),(255,0,255),(255,100,50),(50,100,150)]

# Максимальные координаты
xMax = 1237
yMax = 563
pMax = 9

# Параметры связи
conectEps = 10  # Максимальное расстояние между двумя точками, чтобы считать их связанными

# Параметры отображения
FPS = 30  # Целевая частота кадров в секунду

# Другие параметры
openT = 100  # Начальное или стандартное "открытое время" для некоторой функциональности
stepCord = 1  # Шаг изменения координат

# Размеры окна
screen_width = 1920
screen_height = 1080

# Параметры линий
lineWidht = 5  # Ширина линий
lineGap = 5  # Расстояние между штрихами линий
lineDash = 5  # Длина штрихов линий

# Параметры границ
borderRad = 10  # Радиус скругления границ

# Получаем путь к текущей директории
current_dir = os.path.dirname(__file__)

# Указываем путь к папке media относительно текущей директории
media_dir = os.path.join(current_dir, 'media')

#BASE = 'C:/Users/vovap/PycharmProjects/practic/media/'

# Загрузка медиафайлов
map = pygame.image.load(os.path.join(media_dir, "map.png"))
cels = pygame.image.load(os.path.join(media_dir, "map (1).png"))
plus = pygame.image.load(os.path.join(media_dir, "plus.png"))
plain = pygame.image.load(os.path.join(media_dir, "plane (1).png"))
main = pygame.image.load(os.path.join(media_dir, "main.png"))
conect = pygame.image.load(os.path.join(media_dir, "conect.png"))
chackbox = pygame.image.load(os.path.join(media_dir, "CheckboxFalse.png"))
true = pygame.image.load(os.path.join(media_dir, "True.png"))

# Шрифт по умолчанию
font_name = "Arial"



def DashedLine(screen, start_pos, end_pos, line_color, line_width=2, dash_length=10, gap_length=5):
    """
    Рисует пунктирную линию на заданном экране.

    Параметры:
    screen (pygame.Surface): Экран, на котором будет нарисована линия.
    start_pos (tuple): Координаты начальной точки линии (x, y).
    end_pos (tuple): Координаты конечной точки линии (x, y).
    line_color (tuple): Цвет линии в формате RGB (r, g, b).
    line_width (int): Ширина линии (по умолчанию 2).
    dash_length (int): Длина штриха (по умолчанию 10).
    gap_length (int): Длина промежутка между штрихами (по умолчанию 5).
    """
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = max(abs(dx), abs(dy))
    try:
        dx = dx / distance
        dy = dy / distance
    except:
        dx=0
        dy=0

    x, y = start_pos
    count = 0
    while distance >= 0.5:
        if count % 2 == 0:
            pygame.draw.line(screen, line_color, (x, y), (x + dx * dash_length, y + dy * dash_length), line_width)
        x += dx * (dash_length + gap_length)
        y += dy * (dash_length + gap_length)
        distance -= dash_length + gap_length
        count += 1

def InterpolatePoints(mas,step,mT):
    """
    Интерполирует точки между соседними элементами в списке `mas`.

    Параметры:
    mas (list of list of float): Входной список, содержащий элементы вида `[t, x, y]`, где `t` - время, `x` и `y` - координаты.
    step (int): Шаг интерполяции. Определяет, через сколько единиц времени будут вычисляться промежуточные точки.
    mT (float): Максимальное время, до которого нужно интерполировать точки.

    Возвращает:
    list of list of float: Новый список, в котором каждый элемент содержит интерполированные значения `[t, x, y]`.
    """
    masRes = []

    for i in range(len(mas) - 1):

        t1 = mas[i][0]
        x1, y1 = mas[i][1:]
        t2 = mas[i+1][0]
        x2, y2 = mas[i+1][1:]
        if t1!=t2:
            num_steps = (t2 - t1) // step
            for j in range(num_steps + 1):
                t = t1 + j * step
                x = x1 + int((x2 - x1) * j / num_steps)
                y = y1 + int((y2 - y1) * j / num_steps)
                masRes.append([t, x, y])

        if i == len(mas) - 2 and mas[i+1][0]<mT:
            for j in range (mas[i+1][0]+step,mT+1,step):
                masRes.append([j, x, y])
    return masRes


def FindMaxInColumn(matrix, column_index):
    """
    Находит максимальное значение в указанном столбце двумерного массива.

    Параметры:
    matrix (list of lists): Двумерный массив, в котором нужно найти максимальное значение.
    column_index (int): Индекс столбца, в котором нужно найти максимальное значение.

    Возвращает:
    int: Максимальное значение в указанном столбце.
    """
    max_value = matrix[0][column_index]

    for row in matrix:
        if row[column_index] > max_value:
            max_value = row[column_index]

    return max_value

def ChackConect(list):
    """
    Находит точки пересечения между соседними элементами в списке `list`.

    Параметры:
    list (list of list of list of float): Входной список, содержащий вложенные списки вида `[[t, x, y], [t, x, y], ...]`.

    Возвращает:
    list of list of float: Новый список, в котором каждый элемент содержит время `t`, координаты `x` и `y` точки пересечения, а также расстояние `d` между точками.
    """
    res=[]
    i=0
    for j in range(i+1,len(list)):
        res.append([])
        for k in range(len(list[i])):
            for m in range(len(list[j])):
                if list[i][k][0]==list[j][m][0]:
                    x1 = list[i][k][1]
                    y1 = list[i][k][2]
                    x2 = list[j][m][1]
                    y2 = list[j][m][2]
                    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    res[j-1].append([list[i][k][0],list[i][k][1],list[i][k][2],d])
                #if list[i][k] == list[j][m]:
                #    res.append(list[i][k])
    #print(res)
    return res



def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(),border_radius=borderRad)
    surface.blit(shape_surf, rect)

