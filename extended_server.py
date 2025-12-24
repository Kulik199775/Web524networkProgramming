import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server_state = {"running": True}
server_lock = threading.Lock()


def handle_client(client_sock, client_addr, server_state_ref):
    print(f'Подключен клиент: {client_addr}')

    try:
        while True:
            try:
                client_sock.send(b'Type the message to send: ')
                data = client_sock.recv(1024).decode('utf-8').strip()

                if not data:
                    print(f'Клиент {client_addr} отключился')
                    break

                print(f'Получено от {client_addr}: {data}')

                if data.lower() == 'exit':
                    print(f'Клиент {client_addr} запросил отключение')
                    client_sock.send(b'Goodbye! Connection closed.\n')
                    break

                elif data.lower() == 'shutdown':
                    print(f'Клиент {client_addr} запросил выключение сервера')
                    client_sock.send(b'Server shutdown initiated.\n')

                    with server_lock:
                        server_state_ref["running"] = False

                    client_sock.send(b'Server is shutting down...\n')
                    break

                elif data.lower() == 'add':
                    response = 'Command "add" received. Sending response...\n'
                    client_sock.send(response.encode('utf-8'))
                    client_sock.send(b'Data after "add" command\n')

                else:
                    response = f'Echo: {data}\n'
                    client_sock.send(response.encode('utf-8'))

            except ConnectionResetError:
                print(f'Клиент {client_addr} разорвал соединение')
                break

            except ConnectionAbortedError:
                print(f'Соединение с {client_addr} прервано')
                break

            except Exception as ex:
                print(f'Ошибка с клиентом {client_addr}: {ex}')
                break

    finally:
        client_sock.close()
        print(f'Соединение с {client_addr} закрыто')


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server.bind((HOST, PORT))
            server.listen(5)
            print(f'Сервер запущен на {HOST}:{PORT}')
            print(f'Ожидание подключения...')

            while server_state["running"]:
                try:
                    server.settimeout(1.0)
                    try:
                        client_sock, client_addr = server.accept()
                        print(f'Принято подключение от {client_addr}')

                        client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr, server_state))
                        client_thread.daemon = True
                        client_thread.start()

                    except socket.timeout:
                        continue

                except KeyboardInterrupt:
                    print(f'\nСервер остановлен пользователем')
                    with server_lock:
                        server_state["running"] = False
                    break

                except OSError as OSex:
                    if server_state["running"]:
                        print(f'Ошибка сервера: {OSex}')

                except Exception as ex:
                    print(f'Неожиданная ошибка: {ex}')
                    break

        except Exception as e:
            print(f'Не удалось запустить сервер: {e}')

        finally:
            print(f'Сервер завершил работу')
