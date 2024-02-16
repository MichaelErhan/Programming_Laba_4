import socket
import select
import threading

history_file = open("history.txt", "a", encoding="cp1251")

HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

server_socket.listen(5)

sockets_list = [server_socket]
clients = {}

print("Сервер включен. Ожидание подключений...")
def handle_message(sender, message):
    # Пересылка сообщения всем клиентам в чате
    for client_socket in clients:
        if client_socket != sender:
            client_socket.send(message)
            history_file.write(message.decode("utf-8") + "\n")
    history_file.flush()

def handle_client(client_socket):
    user = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    if user is False:
        return

    clients[client_socket] = user

    print(f'Подключен новый клиент: {user}, порт: {client_socket.getpeername()[1]}')
    handle_message(client_socket, f'{user} присоединил(ась/ся) к чату!'.encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE)
            if message:
                user = clients[client_socket]
                message_with_user = f'{user}: {message.decode("utf-8")}'.encode('utf-8')
                message_with_user_str = message_with_user.decode("utf-8")
                history_file.write(message_with_user_str + "\n")
                history_file.flush()
                handle_message(client_socket, message_with_user)
            else:
                user = clients[client_socket]
                print(f'Клиент {user} отключился от чата')
                handle_message(client_socket, f'{user} покинул чат'.encode('utf-8'))
                break
        except Exception as e:
            print(f'Ошибка взаимодействия с клиентом {user}: {e}')
            break

    client_socket.close()
    del clients[client_socket]

def start_server():
    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                client_thread.start()

            else:
                pass

start_server()

history_file.close()