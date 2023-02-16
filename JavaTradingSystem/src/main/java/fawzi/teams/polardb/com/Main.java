package fawzi.teams.polardb.com;

import fawzi.teams.polardb.com.model.TradingJson;
import fawzi.teams.polardb.com.properties.CheckProperties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.json.JSONObject;

import java.io.IOException;
import java.sql.Date;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
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
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssZ");

                String Symbol = (String) data.getJSONArray("Perusahaan").get((int) (Math.random()*((data.getJSONArray("Perusahaan").length()-1)+1)+0));
                float Open = (float) (Math.random()*(max_harga-min_harga+1)+min_harga);
                float High = (float) (Math.random()*(max_harga-min_harga+1)+min_harga);
                float Low = (float) (Math.random()*(max_harga-min_harga+1)+min_harga);
                float Close = (float) (Math.random()*(max_harga-min_harga+1)+min_harga);
                String Time = sdf.format(new Date(System.currentTimeMillis()));

                TradingJson tradingJson = new TradingJson(Symbol, Open, High, Low, Close, Time);
                if (tradingJson.close < tradingJson.high){
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