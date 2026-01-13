# Absolute path from Makefile
PB_SRC_DIR=./
# Relative path to PB_SRC_DIR
PB_DST_DIR=./
# Absolute path of .proto files
PB_SRC_FILES= $(PB_SRC_DIR)/pb/hello.proto

build_pb:
	python -m grpc_tools.protoc --fatal_warnings \
		--proto_path=$(PB_SRC_DIR) \
		--python_out=$(PB_DST_DIR) \
		--grpc_python_out=$(PB_DST_DIR) \
		--pyi_out=$(PB_DST_DIR) \
		$(PB_SRC_FILES)

start_server:
	PYTHONPATH=./:$(PYTHONPATH) python server/server.py

start_client:
	PYTHONPATH=./:$(PYTHONPATH) python client/client.py
