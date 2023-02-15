package fawzi.teams.polardb.com.socket;

import com.fasterxml.jackson.dataformat.avro.AvroMapper;
import com.fasterxml.jackson.dataformat.avro.AvroSchema;
import fawzi.teams.polardb.com.model.TradingAvro;
import fawzi.teams.polardb.com.properties.CheckProperties;
import org.apache.avro.generic.GenericRecord;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.json.JSONException;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Properties;
import java.util.logging.Logger;

public class StockClientNoSSL {

    final static Logger logger = Logger.getLogger(StockClientNoSSL.class.getName());
    public static void main(String[] args) throws IOException{
//        ParameterTool params = ParameterTool.fromArgs(args);
//        Properties props = new NindaProperties(params.getRequired("config.socket.path")).build();

        Properties props = new CheckProperties("/home/adi/fawzi_linggo/pythonProject/pythonProject/polardb-teams-2023/All-Config/config-socket-server.properties").build();

        // Initialize target topics
        String topics = (String) props.get("topic.name");
        String hostname = (String) props.get("hostname");
        int port = Integer.parseInt((String) props.get("port"));


        try {
            final Producer<String, String> producer = new KafkaProducer<>(props);

            Socket s = new Socket(hostname, port);
            logger.info(String.format("Server Conncet add IP " + hostname + " port " + port));

            InputStreamReader in = new InputStreamReader(s.getInputStream());
            BufferedReader bf = new BufferedReader(in);

            // produce to topic kafka
            while (true){
                String str = bf.readLine();
                // producer to kafka topic
                producer.send(new ProducerRecord<>(topics, str));
                producer.flush();
                logger.info("Send to Kafka : " + str);
            }




        } catch (IOException e) {
            logger.warning("Server Close : " + e.getMessage());
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }
    }
}
