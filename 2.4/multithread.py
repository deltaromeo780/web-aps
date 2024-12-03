import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
import json
from datetime import datetime
import threading

# Adres i port dla serwera HTTP
HTTP_HOST = 'localhost'
HTTP_PORT = 3000

# Adres i port dla serwera UDP
UDP_HOST = 'localhost'
UDP_PORT = 5000


class HttpHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = "localhost", 5000
        sock.sendto(data, server)
        sock.close()

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run_http_server(host, port):
    server_class = HTTPServer
    handler_class = HttpHandler
    server_address = (host, port)
    http = server_class(server_address, handler_class)
    print(f'HTTP server started on {host}:{port}')
    http.serve_forever()


def run_udp_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    print(f'UDP server started on {ip}:{port}')

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
    # Uruchamianie serwera HTTP w oddzielnym wątku
    http_thread = threading.Thread(target=run_http_server, args=(HTTP_HOST, HTTP_PORT))
    http_thread.start()

    # Uruchamianie serwera UDP w oddzielnym wątku
    udp_thread = threading.Thread(target=run_udp_server, args=(UDP_HOST, UDP_PORT))
    udp_thread.start()

    try:
        # Czekanie na zakończenie obu wątków
        http_thread.join()
        udp_thread.join()
    except KeyboardInterrupt:
        print("Zakończono program z powodu przerwania klawiatury.")
