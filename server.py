import socket
import threading
import pickle
import time
from config import *


# Игроки
players = {}
chatHistory = []
chatTime = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    players[addr] = (1400, 3800, None, '', '', '')  # Начальные координаты игрока
    #(x, y, name, chatSendMessage, vector, state)

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            players[addr] = pickle.loads(data)
            print(players)
            for info in players.values():
                if info[3] != '':
                    message = (info[2], info[3])
                    chatHistory.append(message)
                    chatTime.append(time.time())
                for timing in chatTime:
                    if time.time() - timing > 5:
                        ind = chatTime.index(timing)
                        chatHistory.pop(ind)
                        chatTime.pop(ind)

            broadcast((players, chatHistory), conn)

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    del players[addr]
    conn.close()

def broadcast(players, conn):
    for player in players:
        conn.sendall(pickle.dumps(players))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("[SERVER STARTED]")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
