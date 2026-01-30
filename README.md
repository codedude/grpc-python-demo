# gRPC in Python demo

> You can find the presentation here: [Google presentation link](https://docs.google.com/presentation/d/1DCvhPxhlxRVahnn6mqAFa_IhStlg-rSn6Gfp6Hj6xYg/edit?usp=sharing)

## Installation

```bash
git clone https://github.com/codedude/grpc-python-demo.git
cd grpc-python-demo
# Get googleapis submodule
git submodule update --init
# Install python dependencies (you should be in a pyenv)
pip install -r requirements.txt
# Compile protobuf files first
make build_pb
# Start server in an other terminal
make start_server&
# Start client
make start_client ARGS="simple"
```

## TODO

### gRPC

- Server interceptor
- Mock server
https://stackoverflow.com/questions/44718078/how-to-write-a-grpc-python-unittest
https://pypi.org/project/pytest-grpc/

### Protocol Buffers

- code examples in presentation
