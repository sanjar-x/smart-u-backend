#!/bin/bash


PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")

cd "$PROJECT_ROOT"

if [ -d "build" ]; then
    rm -rf build
fi

mkdir -p build
cd build

cmake ..

make

cd "$PROJECT_ROOT"
