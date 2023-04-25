## Problem

A client application connects to your application via a TCP socket and sends an arbitrary
number of protobuf-encoded, length-prefixed messages. Every message block consists of
an unsigned long (C type) denoting the length in bytes of the following serialized protobuf
container. The protobuf container is defined as:

```
syntax = "proto2";

message LogMessage {
  required string log_level = 1; // may contain the values DEBUG, INFO, WARNING or ERROR
  required string logger = 2; // Identifier where in the client
  application this message originated from
  required bytes mac = 3; // MAC address of the system running the
  client application
  optional string message = 4; // free-form log message
}
```

The client application may send multiple messages over a single TCP connection with
arbitrary long pauses in between. The client application may close the connection at any
time (even with partially transferred messages), or not at all. Your application has to receive
these messages from the client connections (up to 100 concurrent connections), convert the
messages into properly formatted log messages, and pass them to a logging system. For
demonstration purposes, sending the logs to stdout is fine.

A naive implementation of the client application may look like this:
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

```
sock.connect(('127.0.0.1', 15000))
lm = LogMessage()
lm.log_level = 'ERROR'
lm.logger = 'main'
lm.mac = bytes([0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff])
lm.message = 'test message'
payload = lm.SerializeToString()
sock.sendall(struct.pack('>L', len(payload)) + payload)
```

## How to run the solution

To make easier the dependencies management, poetry was add to the project, and to run the project provinding all the required dependencies, you have to run the following sequency of commands:

```
poetry shell # It activates the virtual env
poetry install --no-root # It install the dependencies in the venv
```

No you should be able to run the client and the server with the following command:

```
python <file_name>.py
```

## Notes



