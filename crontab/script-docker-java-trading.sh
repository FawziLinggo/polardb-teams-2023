#!/bin/bash

# Menjalankan container Docker
docker run -d --network host --name stockswizard-polardb-trading-system stockswizard-polardb/trading-system:latest
# Tunggu selama 5 menit
sleep 5m

# Menghentikan container Docker
# shellcheck disable=SC2046
docker stop $(docker ps -q --filter stockswizard-polardb/trading-system:latest)