import socket
import struct
import logmessage_pb2 as LogMessage

# https://www.freecodecamp.org/news/googles-protocol-buffers-in-python/


def send_message(message):
    payload = message.SerializeToString()
    length_bytes = struct.pack(">L", len(payload))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("127.0.0.1", 15005))
        sock.sendall(length_bytes)
        sock.sendall(payload)
        sock.shutdown(socket.SHUT_RDWR)


def main():
    lm = LogMessage.LogMessage()
    lm.log_level = 3
    lm.logger = "main"
    lm.mac = bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF])
    lm.message = "test message"
    send_message(lm)


if __name__ == "__main__":
    main()
