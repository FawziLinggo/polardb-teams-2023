package fawzi.teams.polardb.com.model;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.sql.Date;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;

public class TradingJson {

    public String symbol;
    public float open;
    public float high;
    public float low;
    public float close;
    public String time;

    public TradingJson(String symbol, float open, float high, float low, float close, String time) {
        this.symbol = symbol;
        this.open = open;
        this.high = high;
        this.low = low;
        this.close = close;
        this.time = time;
    }

    public String toString(){
        Gson gson = new GsonBuilder().create();
        return gson.toJson(this);
    }

}
