# MIT License

# Copyright (c) 2025 BloraMc @ lystech.org

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import socket
import threading
import random
import string
import datetime

HOST = '0.0.0.0' # Do not modify that / Ne modifier pas çela
PORT = 12345 # Here add the port of you're server / Ici ajoutez le port de votre serveur

clients = {}
ids = {}
lock = threading.Lock()
LOG_FILE = 'proxy_server.log'

def log_event(event):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {event}\n')

def generate_id():
    return ''.join(random.choices(string.digits, k=6))

def handle_client(conn, addr):
    with lock:
        client_id = generate_id()
        while client_id in ids:
            client_id = generate_id()
        ids[client_id] = conn
        clients[conn] = client_id
    log_event(f'Client connected: {addr}, assigned ID: {client_id}')
    try:
        conn.sendall(f"YOUR_ID:{client_id}\n".encode())
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode().strip()
            log_event(f'Received from {client_id}: {msg}')
            if msg.startswith("SENDTO:"):
                try:
                    _, target_id, message = msg.split(':', 2)
                    with lock:
                        target_conn = ids.get(target_id)
                    if target_conn:
                        target_conn.sendall(f"FROM:{client_id}:{message}\n".encode())
                        log_event(f'Message relayed from {client_id} to {target_id}: {message}')
                    else:
                        conn.sendall(b"ERROR:ID_NOT_FOUND\n")
                        log_event(f'Failed delivery from {client_id} to {target_id}: ID_NOT_FOUND')
                except Exception as e:
                    conn.sendall(b"ERROR:INVALID_FORMAT\n")
                    log_event(f'Invalid format from {client_id}: {msg}')
            else:
                conn.sendall(b"ERROR:UNKNOWN_COMMAND\n")
                log_event(f'Unknown command from {client_id}: {msg}')
    finally:
        with lock:
            if conn in clients:
                log_event(f'Client disconnected: {clients[conn]}')
                del ids[clients[conn]]
                del clients[conn]
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Proxy server listening on {HOST}:{PORT}")
        log_event(f"Server started on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":

    main()
