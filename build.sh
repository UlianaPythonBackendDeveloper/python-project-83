#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

make install

# Автоматически применяем структуру базы данных при каждой сборке
psql -a -d $DATABASE_URL -f database.sql