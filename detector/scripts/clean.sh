#!/bin/bash

# Определение пути к корневой директории проекта
PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")

# Переход в корневую директорию проекта
cd "$PROJECT_ROOT"

# Удаление директории сборки
rm -rf build
