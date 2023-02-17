1. build image 
```bash
docker build -t stockswizard-polardb/webscoket:latest .
```
2. run container    
```bash
docker run -d -p 8765:8765 --name stockswizard-polardb-webscoket stockswizard-polardb/webscoket:latest -e BOOTSTRAP_SERVERS="localhost:9092" -e TOPIC="TradingSystemOrderProduction" -e PORT_WS="8765"
```
3. check container
```bash
docker ps
```
4. check logs
```bash
docker logs stockswizard-polardb-webscoket
```
5. stop container
```bash
docker stop stockswizard-polardb-webscoket
```