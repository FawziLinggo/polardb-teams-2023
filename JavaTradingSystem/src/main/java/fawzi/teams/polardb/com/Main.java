package fawzi.teams.polardb.com;

import fawzi.teams.polardb.com.model.TradingJson;
import fawzi.teams.polardb.com.properties.CheckProperties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.json.JSONObject;

import java.io.IOException;
import java.sql.Timestamp;
import java.time.Instant;
import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class Main {

        public static void main(String[] args) throws IOException, InterruptedException, ExecutionException {
            Properties props = new CheckProperties("/home/adi/fawzi_linggo/pythonProject/pythonProject/polardb-teams-2023/All-Config/config-socket-server.properties").build();

            JSONObject data = new JSONObject((String) props.get("data"));

            int min_harga = Integer.parseInt((String) props.get("min_harga"));
            int max_harga = Integer.parseInt((String) props.get("max_harga"));
            int random_delay = Integer.parseInt((String) props.get("delay.max.ms"));

    KafkaProducer<String,String> producer = new KafkaProducer<String, String>(props);
            for (int i = 0; i < 1000; i++){
                String Symbol = (String) data.getJSONArray("Perusahaan").get((int) (Math.random()*((data.getJSONArray("Perusahaan").length()-1)+1)+0));
                TradingJson tradingJson = new TradingJson(Symbol ,(float) (Math.random()*(max_harga-min_harga+1)+min_harga),
                (float) (Math.random()*(max_harga-min_harga+1)+min_harga),
                (float) (Math.random()*(max_harga-min_harga+1)+min_harga),
                (float) (Math.random()*(max_harga-min_harga+1)+min_harga),
                Timestamp.from(Instant.now()).getTime());
                if (tradingJson.Close < tradingJson.High){
                    System.out.println(tradingJson);
                    // producer callback to kafka topic
                    ProducerRecord<String, String> record = new ProducerRecord<>("TradingSystemOrder", tradingJson.toString());
                    producer.send(record).get();
                    Thread.sleep((long) (Math.random()*(random_delay +1)+0));
                }
                else {
                    System.out.println("Close is higher than High");
                }
            }
            producer.flush();
            producer.close();


            }

}