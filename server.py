import socket
import threading


class Server:
    def __init__(self, header, port, format='utf-8', disconnect_message="!DISCONNECT"):
        self._header = header
        self._port = port
        self._host = socket.gethostbyname(socket.gethostname())
        self._addr = (self._host, self._port)
        self._format = format
        self._disconnect_message = disconnect_message
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(self._addr)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(self._header).decode(self._format)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self._format)
                if msg == self._disconnect_message:
                    connected = False

                print(f"[{addr}] {msg}")
                conn.send(f"Msg received '{msg}'".encode(self._format))

        conn.close()

    def run(self):
        self._server.listen()
        print(f"[LISTENING] Server is listening on {self._host}")
        while True:
            conn, addr = self._server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


