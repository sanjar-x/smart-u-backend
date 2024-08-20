#!/bin/bash

PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")

cd "$PROJECT_ROOT"

cd build
./main

# Возвращение в исходную директорию
cd "$PROJECT_ROOT"
