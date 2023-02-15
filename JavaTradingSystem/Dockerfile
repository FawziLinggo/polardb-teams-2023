FROM openjdk:17-alpine
RUN apk add --no-cache --upgrade bash
COPY target/*.jar /app.jar
COPY /home/adi/fawzi_linggo/pythonProject/pythonProject/polardb-teams-2023/All-Config/config-socket-server.properties /config-socket-server.properties


# Run the multiple jars file
CMD ["/bin/sh", "-c", "java -cp app.jar fawzi.teams.polardb.com.socket.StockServer & java -cp app.jar fawzi.teams.polardb.com.socket.StockServer & java -cp app.jar fawzi.teams.polardb.com.socket.StockServer"]