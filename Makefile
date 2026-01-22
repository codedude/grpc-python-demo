# Path from where the command is called
PB_SRC_FILES= pb/sub/sub_demo.proto pb/demo.proto

# [python|grpc|pyi]_out: relative to -I
# -I xxx: includes paths
# -Ix=y: y files will be place in package x
#	It also change the import path in .proto files
build_pb:
	@echo "Compiling proto files..."
	@python -m grpc_tools.protoc --fatal_warnings \
		-Ipb/generated=./pb -I googleapis\
		--python_out=./ \
		--grpc_python_out=./ \
		--pyi_out=./ \
		$(PB_SRC_FILES)
	@echo "... done!"

.PHONY: start_server, start_client, build_pb, pb_demo, type_demo

start_server:
	@echo "Starting server..."
	@PYTHONPATH=./:$(PYTHONPATH) python server/server.py

start_client:
	@echo "Starting client..."
	@PYTHONPATH=./:$(PYTHONPATH) python client/client.py $(ARGS)
	@echo "... done!"

pb_demo:
	@PYTHONPATH=./:$(PYTHONPATH) python pb_demo.py

type_demo:
	@PYTHONPATH=./:$(PYTHONPATH) python type_demo.py
