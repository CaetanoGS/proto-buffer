import socket
import struct
import logmessage_pb2 as LogMessage


PORT = 15005
NUMBER_OF_CLIENTS_TO_TEST = 10


class LogServer:
    def __init__(self, host: str, port: int, max_listeners_number: int):
        self.host = host
        self.port = port
        self.max_listeners_number = max_listeners_number
        self.server_socket: socket.socket

    def _handle_connection(self, conn):
        with conn:
            try:
                length_bytes = conn.recv(4)
                length = struct.unpack(">L", length_bytes)[0]
                message_bytes = conn.recv(length)
                message = LogMessage.LogMessage.FromString(message_bytes)
                log_message = f"Received Message -> Logger:[{message.logger}] Log Level: [{message.log_level}] Message: {message.message} MAC: ({message.mac.hex()})"
                print(log_message)
            except Exception as e:
                print(f"Error while handling response: {e}")

    def create_socket_connection(self) -> "LogServer":
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_listeners_number)
        return self

    def start(self):
        print(f"Listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Client {addr} is connected")
            self._handle_connection(conn)


if __name__ == "__main__":
    server = (
        LogServer(
            host=socket.gethostname(),
            port=PORT,
            max_listeners_number=NUMBER_OF_CLIENTS_TO_TEST,
        )
        .create_socket_connection()
        .start()
    )
