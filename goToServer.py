import pygame
import socket
import ast
import json
from const import *
def GoServer(params,cordFirst = []):
    """
    Отправляет данные на сервер, получает ответ и корректирует координаты.

    Параметры:
    params (list of float): Список параметров, включающий `V`, `P`, `T1`, `T2`, `X1`, `Y1`.

    Возвращает:
    list of list of float: Скорректированные координаты в виде списка вложенных списков `[[t, x, y], [t, x, y], ...]`.
    """
    cord = SendDataToServer(params,cordFirst)

    for i in range(len(cord)):
        cord[i][1] = 20 + cord[i][1]  # min(max(20,el[1]+20), 1240)
        cord[i][2] = 23 + cord[i][2]  # min(max(23,el[1]+23), 570)
    return cord


def SendDataToServer(params,cordFirst):
    """
    Отправляет данные на сервер и получает ответ.

    Параметры:
    params (list of float): параменты iго самолета
        V (float): Значение V.
        P (float): Значение P.
        T1 (float): Значение T1.
        T2 (float): Значение T2.
        X1 (float): Значение X1.
        Y1 (float): Значение Y1.

    cordFirst (list of list of float): Значение координат главного самолета.

    Возвращает:
    list of list of float: Ответ сервера в виде списка вложенных списков `[[t, x, y], [t, x, y], ...]`.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        HOST = GetLocalIp()

        print(HOST, PORT)
        s.connect((HOST, PORT))
        data = [params,cordFirst]
        #data = f"{V},{P},{T1},{T2},{X1},{Y1}"
        #s.sendall(data.encode())
        try:
            s.sendall(json.dumps(data).encode())
            print(f"Отправлено: {data}")
        except:
            print("Ошибка передачи на сервер")

        dataRes = s.recv(1024)

        #result = ast.literal_eval(dataRes.decode())
        #dataRes =b''
        #while True:
        #    chunk = s.recv(1024)
        #    if not chunk:
        #        break
        #    dataRes += chunk

        try:
            result = []
            response = json.loads(dataRes.decode())
            for item in response:
                result.append([item[0], item[1], item[2]])
            print(f"Получено: {result}")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Ошибка при обработке ответа: {e}")

        #print(f"Получено: {', '.join(map(str, result))}")
        return(result)

def GetLocalIp():
    """
    Получает локальный IP-адрес компьютера.

    Возвращает:
    str: Локальный IP-адрес компьютера.
    """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip