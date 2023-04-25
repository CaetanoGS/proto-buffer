import asyncio
import struct
import logmessage_pb2 as LogMessage


async def handle_connection(reader, writer):
    while True:
        length_bytes = await reader.readexactly(4)
        length = struct.unpack(">L", length_bytes)[0]
        message_bytes = await reader.readexactly(length)
        message = LogMessage.LogMessage.FromString(message_bytes)
        log_message = f"[{message.logger}] [{message.log_level}] {message.message} ({message.mac.hex()})"
        print(log_message)


async def main():
    server = await asyncio.start_server(handle_connection, "127.0.0.1", 15005)
    async with server:
        await server.serve_forever()


asyncio.run(main())
