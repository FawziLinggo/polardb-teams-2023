package fawzi.teams.polardb.com.socket;

import com.fasterxml.jackson.dataformat.avro.AvroMapper;
import com.fasterxml.jackson.dataformat.avro.AvroSchema;
import fawzi.teams.polardb.com.model.TradingAvro;
import fawzi.teams.polardb.com.properties.CheckProperties;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.generic.GenericRecordBuilder;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Properties;
import java.util.logging.Logger;

public class StockClient {

    final static Logger logger = Logger.getLogger(StockClient.class.getName());
    public static void main(String[] args) throws IOException{
//        ParameterTool params = ParameterTool.fromArgs(args);
//        Properties props = new NindaProperties(params.getRequired("config.socket.path")).build();

        Properties props = new CheckProperties("/home/adi/fawzi_linggo/pythonProject/pythonProject/polardb-teams-2023/All-Config/config-socket-server.properties").build();

        // Initialize target topics
        String topics = (String) props.get("topic.name");
        String hostname = (String) props.get("hostname");
        int port = Integer.parseInt((String) props.get("port"));
        // Init kafka connection
//        Producer<String, String> producer = new KafkaProducer<>(props);

        try {

            // Schema Generation For Our Customer Class
            final AvroMapper avroMapper = new AvroMapper();
            final AvroSchema schema = avroMapper.schemaFor(TradingAvro.class);
            System.out.println(schema.getAvroSchema().toString(true));
            final Producer<String, GenericRecord> producer = new KafkaProducer<>(props);

            Socket s = new Socket(hostname, port);
            logger.info(String.format("Server Conncet add IP " + hostname + " port " + port));

            InputStreamReader in = new InputStreamReader(s.getInputStream());
            BufferedReader bf = new BufferedReader(in);


//            while (true){
//
//                String str = bf.readLine();
//                JSONObject message = new JSONObject(str);
//
//                GenericRecordBuilder recordBuilder = new GenericRecordBuilder(schema.getAvroSchema());
//                recordBuilder.set("symbol", message.getString("Symbol"));
//                recordBuilder.set("open", message.getFloat("Open"));
//                recordBuilder.set("high", message.getFloat("High"));
//                recordBuilder.set("low", message.getFloat("Low"));
//                recordBuilder.set("close", message.getFloat("Close"));
//                recordBuilder.set("timestamp", message.getLong("timestamp"));
//                final GenericRecord genericRecord = recordBuilder.build();
//                System.out.println(genericRecord);
//
//                ProducerRecord<String, GenericRecord> record = new ProducerRecord<>(topics,
//                        message.getString("Symbol").toString(),
//                        genericRecord);
//                producer.send(record);
//                logger.info(String.format("Send Message to Topic " + topics ));
////
//            }

        } catch (IOException e) {
            logger.warning("Server Close : " + e.getMessage());
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }
    }
}
