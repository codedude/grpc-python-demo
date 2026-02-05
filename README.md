# gRPC in Python demo

> You can find the presentation here: [Google presentation link](https://docs.google.com/presentation/d/1DCvhPxhlxRVahnn6mqAFa_IhStlg-rSn6Gfp6Hj6xYg/edit?usp=sharing)

## Installation

```bash
# Clone the project
git clone https://github.com/codedude/grpc-python-demo.git
cd grpc-python-demo
# Get googleapis and protobuf submodules
git submodule update --init
```

```bash
# Create a venv
python -m venv /path/to/venv
source /path/to/venv/bin/activate
```

```bash
# Install and build the project
pip install -r requirements.txt
# Compile protobuf files first
make build_pb
# Start server in an other terminal
make start_server&
# Start client
make start_client ARGS="simple -mode=normal"
# Start client mock without server
make start_client ARGS="simple -mode=mock"
```

## Usefull links

- [gRPC website](https://grpc.io/)
- [Protocol Buffers website](https://protobuf.dev/)
