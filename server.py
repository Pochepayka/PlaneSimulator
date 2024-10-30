import socket
import math
import json
HOST = '192.168.0.106'  # IP-адрес сервера
PORT = 65432  # Порт для подключения


def handle_client_request(conn, addr):
    print(f"Подключение от {addr}")
    params=[]
    # Получение данных от клиента
    data = conn.recv(1024)
    try:
        response = json.loads(data.decode())
        params = response[0]
        cordsFirst = response[1]
        print(f"Получено: {params} и {cordsFirst}")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Ошибка при обработке ответа: {e}")

    #print("Получено:", data)
    #params = [int(x) for x in data.decode().split(',')]

    # Формирование ответа
    cord = [[0,0,0],[100,100,100]]

    if int(params[1]) == 1:
        cord = [[int(params[2]), int(params[4]), int(params[5])],
                [int(params[3]), int(params[4]),
                 int(params[5]) - int(params[0]) * (int(params[3]) - int(params[2]))]]
    if int(params[1]) == 2:
        cord = [[int(params[2]), int(params[4]), int(params[5])],
                [int(params[3]), int(params[4]) + math.sqrt(((int(params[0])**2)/2)) * (int(params[3]) - int(params[2])),
                 int(params[5]) - math.sqrt(((int(params[0])**2)/2)) * (int(params[3]) - int(params[2]))]]
    if int(params[1]) == 3:
        cord = [[int(params[2]), int(params[4]), int(params[5])],
                [int(params[3]), int(params[4]) + int(params[0])* (int(params[3]) - int(params[2])),
                 int(params[5])]]
    if int(params[1]) == 4:
        cord = [[int(params[2]), int(params[4]), int(params[5])],
                [int(params[3]), int(params[4]) + math.sqrt(((int(params[0])**2)/2)) * (int(params[3]) - int(params[2])),
                 int(params[5]) + math.sqrt(((int(params[0])**2)/2)) * (int(params[3]) - int(params[2]))]]
    if int(params[1]) == 5:
        cord = [[int(params[2]), int(params[4]), int(params[5])],
                [int(params[3]), int(params[4]),
                 int(params[5]) + int(params[0]) * (int(params[3]) - int(params[2]))]]
    if int(params[1]) == 6:
        cord = [[int(params[2]), int(params[4]), int(params[5])],
                [int(params[3]), int(params[4]) - math.sqrt(((int(params[0])**2)/2)) * (int(params[3]) - int(params[2])),
                 int(params[5]) + math.sqrt(((int(params[0])**2)/2)) * (int(params[3]) - int(params[2]))]]
    if int(params[1]) == 7:
        cord = [[int(params[2]), int(params[4]), int(params[5])],
                [int(params[3]), int(params[4]) - (int(params[0])) * (int(params[3]) - int(params[2])),
                 int(params[5])]]
    if int(params[1]) == 8:
        cord = [[int(params[2]), int(params[4]), int(params[5])],
                [int(params[3]), int(params[4]) - math.sqrt(((int(params[0])**2)/2)) * (int(params[3]) - int(params[2])),
                 int(params[5]) - math.sqrt(((int(params[0])**2)/2)) * (int(params[3]) - int(params[2]))]]

    #response = str(cord).replace('[', '').replace(']', '').replace('\'', '')
    response = cord


    # Отправка ответа клиенту
    #conn.sendall(response.encode())
    conn.sendall(json.dumps(response).encode())
    print(f"Отправлено: {response}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            HOST = get_local_ip()
            s.bind((HOST, PORT))
            s.listen()
            print(f"Сервер запущен и ожидает подключений на {HOST}:{PORT}")

            while True:
                conn, addr = s.accept()
                handle_client_request(conn, addr)
        except OSError as e:
            print(f"Ошибка: {e}")

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

if __name__ == "__main__":
    start_server()