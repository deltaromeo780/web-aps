import socket
import json
from datetime import datetime

UDP_IP = 'localhost'
UDP_PORT = 5000
data = 'received_data.json'


def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    print(f'UDP server started on {UDP_IP} : {UDP_PORT}')

    try:
        while True:
            data, address = sock.recvfrom(1024)
            decoded_data = data.decode()
            print(f'Received: {decoded_data} from: {address}')
            sock.sendto(data, address)
            print(f'Send: {decoded_data} to: {address}')

            # Zapisujemy otrzymane dane do pliku JSON
            save_data_to_json(decoded_data)

    except KeyboardInterrupt:
        print(f'Shutdown server')
    finally:
        sock.close()


def save_data_to_json(data):
    try:
        # Otwieramy plik w trybie dołączania ('a' oznacza append)
        with open("Storage/data.json", 'a', encoding='utf-8') as file:
            timestamp = datetime.now().isoformat()
            # Tworzymy słownik z danymi i zapisujemy do pliku JSON
            json.dump({timestamp: data}, file, ensure_ascii=False)
            file.write('\n')
            # Dodajemy nową linię, aby oddzielić kolejne wpisy w pliku JSON
    except Exception as e:
        print(f'Błąd podczas zapisywania danych do pliku JSON: {e}')


if __name__ == '__main__':
    run_server(UDP_IP, UDP_PORT)



