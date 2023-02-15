compile:
	@echo
	@echo "Compiling..."
	mvn clean compile assembly:single

StockServer:
	@echo
	@echo "Starting StockServer..."
	java -cp target/StockServer-1.0-SNAPSHOT-jar-with-dependencies.jar fawzi.teams.polardb.com.socket.StockServer

StockClient:
	@echo
	@echo "Starting StockClient..."
	java -cp target/StockServer-1.0-SNAPSHOT-jar-with-dependencies.jar fawzi.teams.polardb.com.socket.StockClient