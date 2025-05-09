#!/bin/bash

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PARENT_DIR="$(dirname "$CURRENT_DIR")"
source $PARENT_DIR/logging_lib.sh
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"  # Has to be run again

log_info "Building the wafl interface..."

# Not writing this to wafl-temp, since it needs to be in the same dir as
# the entrypoint for supervisor to find it.
CPP_OUT_DIR=$CURRENT_DIR/cpp-out
mkdir -p $CPP_OUT_DIR

g++ -o $CPP_OUT_DIR/prepare_wasm_input.out $CURRENT_DIR/prepare_wasm_input.cpp $CURRENT_DIR/utils.cpp
g++ -o $CPP_OUT_DIR/getFileSize.out $CURRENT_DIR/getFileSize.cpp $CURRENT_DIR/utils.cpp
g++ -o $CPP_OUT_DIR/wait_for_server.out $CURRENT_DIR/wait_for_server.cpp $CURRENT_DIR/utils.cpp $CURRENT_DIR/socket_client.cpp
g++ -o $CPP_OUT_DIR/run_client.out $CURRENT_DIR/run_client.cpp $CURRENT_DIR/socket_client.cpp $CURRENT_DIR/utils.cpp
g++ -o $CPP_OUT_DIR/interface.out $CURRENT_DIR/interface.cpp $CURRENT_DIR/socket_client.cpp $CURRENT_DIR/utils.cpp

chmod +x $CPP_OUT_DIR/*.out

log_info "Finished building the wafl interface..."
