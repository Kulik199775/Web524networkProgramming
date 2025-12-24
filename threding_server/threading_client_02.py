import socket

HOST = '127.0.0.1'
PORT = 12346


if __name__ == '__main__':

    print('Клиент запущен')
    print('Команды: exit - выход, shutdown - выключить сервер')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print('Подключено к серверу')

        while True:
            prompt = sock.recv(1024).decode('utf-8')
            print(prompt, end='')

            message = input()
            sock.send(message.encode('utf-8'))

            if message.lower() == 'exit':
                print('Выход...')
                break

            response = sock.recv(1024).decode('utf-8')
            print('Ответ:', response)

    except ConnectionResetError:
        print('Сервер отключился')
        print('Process finished with exit code 0')

    except ConnectionRefusedError:
        print('Не удалось подключиться')

    except KeyboardInterrupt:
        print('\nВыход')

    finally:
        try:
            sock.close()
        except:
            pass