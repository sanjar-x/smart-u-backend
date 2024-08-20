#!/bin/bash

PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")
cd "$PROJECT_ROOT"
echo "Перешел в директорию: $PROJECT_ROOT" | tee -a script.log

if [ -d "build" ]; then
    echo "Найдена директория build. Удаляю..." | tee -a script.log
    rm -rf build
    echo "Директория build удалена." | tee -a script.log
else
    echo "Директория build не найдена. Нечего удалять." | tee -a script.log
fi