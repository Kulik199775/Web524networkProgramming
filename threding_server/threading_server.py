import socket
import threading

HOST = '127.0.0.1'
PORT = 12346

server_running = True
client_counter = 0
lock = threading.Lock()


def handle_client(client_sock, client_addr, client_id):
    global server_running

    print(f'Клиент #{client_id} подключен: {client_addr}')

    try:
        while True:
            client_sock.send(b'Enter your message: ')
            data = client_sock.recv(1024).decode('utf-8').strip()

            if not data:
                print(f'Клиент #{client_id} отключился')
                break

            if data == '':
                continue

            print(f'Клиент #{client_id} написал: {data}')

            if data.lower() == 'exit':
                print(f'Клиент #{client_id} отключается')
                client_sock.send(b'Goodbye!\n')
                break

            elif data.lower() == 'shutdown':
                print(f'Клиент #{client_id} выключает сервер')
                client_sock.send(b'The server is shutting down...\n')

                with lock:
                    server_running = False

                continue

            else:
                response = f'Вы сказали: {data}\n'
                client_sock.send(response.encode('utf-8'))

    except (ConnectionResetError, ConnectionAbortedError):
        print(f'Клиент #{client_id} разорвал соединение')

    except Exception as e:
        print(f'Ошибка с клиентом #{client_id}: {e}')

    finally:
        client_sock.close()
        print(f'Клиент #{client_id} отключен')


if __name__ == '__main__':

    print(f'Многопоточный сервер запущен на {HOST}:{PORT}')
    print('Ожидание подключений...')

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_sock.bind((HOST, PORT))
        server_sock.listen(5)

        while server_running:
            try:
                client_socket, client_address = server_sock.accept()

                with lock:
                    client_counter += 1
                    current_id = client_counter

                print(f'Новый клиент #{current_id}')

                thread = threading.Thread(target=handle_client,args=(client_socket, client_address, current_id))
                thread.daemon = True
                thread.start()

            except KeyboardInterrupt:
                print('\nСервер остановлен пользователем')
                break

            except Exception as e:
                if server_running:
                    print(f'Ошибка при принятии подключения: {e}')

    except Exception as e:
        print(f'Не удалось запустить сервер: {e}')

    finally:
        server_sock.close()
        print('Сервер выключен')