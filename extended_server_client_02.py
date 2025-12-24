import socket

HOST = '127.0.0.1'
PORT = 12345


if __name__ == '__main__':

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            print(f'Подключено к серверу {HOST}:{PORT}')
            print('Для выхода введите "exit"')
            print('Для выключения сервера введите "shutdown"')
            print('-' * 40)

            while True:
                try:
                    try:
                        prompt = sock.recv(1024, socket.MSG_PEEK)
                        if prompt:
                            data_bytes_received = sock.recv(1024)
                            print(data_bytes_received.decode('utf-8'), end='')
                    except BlockingIOError:
                        pass

                    data_to_send = input()

                    data_bytes_send = data_to_send.encode('utf-8')
                    sock.sendall(data_bytes_send)

                    if data_to_send.lower() == 'exit':
                        print('Отключение от сервера...')
                        break

                    data_bytes_received = sock.recv(1024)

                    if not data_bytes_received:
                        print('Сервер закрыл соединение')
                        break

                    data_received = data_bytes_received.decode('utf-8')
                    print('Получено от сервера:', data_received)

                except KeyboardInterrupt:
                    print('\nПрервано пользователем')
                    sock.sendall(b'exit')
                    break

                except ConnectionResetError:
                    print('Соединение разорвано сервером')
                    break

                except ConnectionAbortedError:
                    print('Соединение прервано')
                    break

                except Exception as e:
                    print(f'Ошибка: {e}')
                    break

    except ConnectionRefusedError:
        print(f'Не удалось подключиться к серверу {HOST}:{PORT}')
        print('Убедитесь, что сервер запущен')

    except Exception as e:
        print(f'Неожиданная ошибка: {e}')