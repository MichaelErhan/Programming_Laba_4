import socket
import threading

HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

username = input('Введите ваше имя: \n')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(username.encode('utf-8'))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            print(message)
        except Exception as e:
            print(f'Ошибка при получении сообщений: {e}\n')
            client_socket.close()
            break

def send_message():
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()