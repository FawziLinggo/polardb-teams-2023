package fawzi.teams.polardb.com.model;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.sql.Timestamp;
public class TradingJson {

    public String Symbol;
    public float Open;
    public float High;
    public float Low;
    public float Close;
    public long timestamp;


    public TradingJson(String Symbol, float Open, float High,
                       float Low, float Close, long timestamp ) {
        this.Symbol = Symbol;
        this.Open = Open;
        this.High = High;
        this.Low = Low;
        this.Close = Close;
        this.timestamp = timestamp;
    }

    public String toString() {
        Gson gson = new GsonBuilder().setLenient().create();
        return gson.toJson(this);
    }
}
