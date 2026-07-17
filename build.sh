#!/usr/bin/env bash

# Скачиваем uv и активируем его окружение в контейнере Render
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости глобально в систему Render
make install