package fawzi.teams.polardb.com.socket;

import fawzi.teams.polardb.com.model.TradingJson;
import fawzi.teams.polardb.com.properties.CheckProperties;
import org.apache.log4j.Logger;
import org.json.JSONObject;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.sql.Date;
import java.sql.Timestamp;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.util.Properties;
public class StockServer {
    final static Logger logger = Logger.getLogger(StockServer.class.getName());

    public static void main(String[] args) {
        try {
//        ParameterTool params = ParameterTool.fromArgs(args);
//        Properties props = new CheckProperties(params.getRequired("config.socket.path")).build();
            // from file
            Properties props = new CheckProperties("/home/adi/fawzi_linggo/pythonProject/pythonProject/polardb-teams-2023/All-Config/config-socket-server.properties").build();
            JSONObject data = new JSONObject((String) props.get("data"));
            int min_harga = Integer.parseInt((String) props.get("min_harga"));
            int max_harga = Integer.parseInt((String) props.get("max_harga"));
            int random_delay = Integer.parseInt((String) props.get("delay.max.ms"));
            int port = Integer.parseInt((String) props.get("port"));

            ServerSocket ss = new ServerSocket(port);
            System.out.println("Server started on port " + port);
            
            DecimalFormat df = new DecimalFormat();
            df.setMaximumFractionDigits(2);

        while (true){
            Socket s = ss.accept();
            logger.info("Client Connected");
            PrintWriter pr = new PrintWriter(s.getOutputStream());
            BufferedWriter bufferedWriter = new BufferedWriter(pr);
            while (true){
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssZ");
                String time = sdf.format(new Date(System.currentTimeMillis()));

                String Symbol = (String) data.getJSONArray("Perusahaan").get((int) (Math.random()*((data.getJSONArray("Perusahaan").length()-1)+1)+0));
                float Open = (float) (Math.random()*(max_harga-min_harga+1)+min_harga);
                float High = (float) (Math.random()*(max_harga-min_harga+1)+min_harga);
                float Low = (float) (Math.random()*(max_harga-min_harga+1)+min_harga);
                float Close = (float) (Math.random()*(max_harga-min_harga+1)+min_harga);
                String Time = sdf.format(new Date(System.currentTimeMillis()));
                Open = Float.parseFloat(df.format(Open));
                High = Float.parseFloat(df.format(High));
                Low = Float.parseFloat(df.format(Low));
                Close = Float.parseFloat(df.format(Close));


                TradingJson tradingJson = new TradingJson(Symbol, Open, High, Low, Close, time);
                try {
                    if (tradingJson.close < tradingJson.high){
                    bufferedWriter.write(String.valueOf(tradingJson));
                    logger.info(tradingJson);
                    bufferedWriter.newLine();
                    bufferedWriter.flush();
                    Thread.sleep((long) (Math.random()*(random_delay +1)+0));
                }
                if(!s.isConnected()){
                    logger.info("Client Disconnect");
                    break;
                }
                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}