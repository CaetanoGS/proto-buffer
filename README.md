# Protocol Buffers

Protocol buffers are Google’s language-neutral, platform-neutral, extensible mechanism for serializing structured data. It is possible to define how you want your data to be structured once, then you can use special generated source code to easily write and read your structured data to and from a variety of data streams and using a variety of languages.

## Protocol Buffer Compiler Installation

To install the compiler, please check the follow link where the instructions are provided: https://grpc.io/docs/protoc-installation/

## How generate the _pb2.py file

To generate the _pb2.py file based on the .proto structure, the follow command is required:

```
protoc -I=. --python_out=. ./<PROTO_FILE_NAME>.proto
```

After it a file called <PROTO_FILE_NAME>_pb2.py must be generated, and from it the structured created can be imported.

## Pros comparing with JSON

* Faster than JSON
* Protofbuf tends to be faster at integer encoding than JSON
* Protobuf is great when you exchange high volumes of the same type of message and when performance matters

## Cons comparing with JSON

* JSON is useful when you want data to be human readable
* If your server side application is written in JavaScript, JSON makes most sense
* Limited support for complex data types

# Problem

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

## Requirements

To run the provided solution, there are to requirements, these requirements are:

* Python ^3.11 (https://www.python.org/downloads/)
* Poetry ^1.4.0 (https://python-poetry.org/docs/#installation)

## Explained dependencies

* protobuf ^4.22.3 --> Enables Protocol Buffers
* tqdm = "^4.65.0" --> Used to have a load bar to follow the progress
* black ^23.3.0 --> Used to format the python files


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

### Server results

```
Client ('192.168.2.32', 55906) is connected
Received Message -> Logger:[main] Log Level: [1] Message: fc692875-da0f-418b-b859-3cb9e7f6ef7e MAC: (5d837dcc4804)
Client ('192.168.2.32', 55907) is connected
Received Message -> Logger:[main] Log Level: [1] Message: 9965f0da-60c3-4e19-b022-c0679b3b4853 MAC: (c8d9b451697f)
Client ('192.168.2.32', 55908) is connected
Received Message -> Logger:[main] Log Level: [1] Message: 0cbe3eb4-5c2c-4361-9c6b-acdcbcbce139 MAC: (aa8374a7809f)
Client ('192.168.2.32', 55909) is connected
Received Message -> Logger:[main] Log Level: [1] Message: 5e90e147-07ab-4f1d-b70f-ce5c4414c684 MAC: (2777d64b2748)
```

### Client results

```
Sending messages to Gustavos-Air:15005
100%|█████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:56<00:00,  1.78it/s]
```



