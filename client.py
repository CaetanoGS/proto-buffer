from ast import List
import random
import socket
import struct
import time
from tqdm import tqdm
import logmessage_pb2 as LogMessage
from random import randint
import uuid

from server import NUMBER_OF_CLIENTS_TO_TEST, PORT

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]


class SocketClient:
    def __init__(self, host: str, port: int, keep_connection_flag: bool):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keep_connection_flag = keep_connection_flag

    def connect(self) -> None:
        self.client_socket.connect((self.host, self.port))

    def disconnect(self) -> None:
        self.client_socket.close()

    def send_message(self, message: LogMessage.LogMessage) -> None:
        payload = message.SerializeToString()
        length_bytes = struct.pack(">L", len(payload))
        try:
            self.client_socket.sendall(length_bytes)
            self.client_socket.sendall(payload)

            if not self.keep_connection_flag:
                self.disconnect()

            # Uncomment the following if to close connection randomly

            if random.random() < 0.1:
                self.disconnect()

        except ConnectionRefusedError:
            print(f"Connection to {self.host}:{self.port} refused.")
        except BrokenPipeError:
            print(f"Connection to {self.host}:{self.port} broken.")
        except Exception as e:
            print(f"Error while sending message: {e}")
            self.disconnect()


def create_random_message() -> LogMessage.LogMessage:
    lm = LogMessage.LogMessage()
    lm.log_level = LogMessage.LogLevel.Value(
        LOG_LEVELS[randint(0, len(LOG_LEVELS) - 1)]
    )
    lm.logger = "main"
    lm.mac = bytes([randint(0, 255) for _ in range(6)])
    lm.message = str(uuid.uuid4())
    return lm


def main() -> None:
    clients: List[SocketClient] = []
    for _ in range(NUMBER_OF_CLIENTS_TO_TEST):
        client = SocketClient(socket.gethostname(), PORT, True)
        client.connect()
        clients.append(client)

    print(f"Sending messages to {socket.gethostname()}:{PORT}")

    for client in tqdm(clients):
        client.send_message(create_random_message())
        time.sleep(random.uniform(0.001, 1))

        # To Enable Random client disconnection, please uncomment the following condition

        if random.random() < 0.05:
            client.disconnect()


if __name__ == "__main__":
    main()
