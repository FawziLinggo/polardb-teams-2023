FROM openjdk:17-alpine
RUN apk add --no-cache --upgrade bash
COPY target/*.jar /apps.jar
RUN ls

COPY config-socket-server.properties /config-socket-server.properties


# Run the multiple jars file
CMD ["/bin/sh", "-c", "java -cp apps.jar fawzi.teams.polardb.com.socket.StockServer & sleep 3 & java -cp apps.jar fawzi.teams.polardb.com.socket.StockClientNoSSL"]