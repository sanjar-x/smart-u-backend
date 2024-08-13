#!/bin/bash

# Определение пути к корневой директории проекта
PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")

# Переход в корневую директорию проекта
cd "$PROJECT_ROOT"

if [ -d "build" ]; then
    rm -rf build
fi

# Переход в директорию сборки
mkdir -p build
cd build

# Генерация файлов сборки с помощью CMake
cmake ..

# Компиляция проекта
make

# Возвращение в исходную директорию
cd "$PROJECT_ROOT"
