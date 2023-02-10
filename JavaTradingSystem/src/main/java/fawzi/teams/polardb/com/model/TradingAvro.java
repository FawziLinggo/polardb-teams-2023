package fawzi.teams.polardb.com.model;

public class TradingAvro {
    private String Symbol;
    private float Open;
    private float High;
    private float Low;
    private float Close;
    private long timestamp;

    public TradingAvro(final String Symbol, float Open, float High,
                       float Low, float Close, long timestamp ) {
        this.Symbol = Symbol;
        this.Open = Open;
        this.High = High;
        this.Low = Low;
        this.Close = Close;
        this.timestamp = timestamp;
    }
    // Create Setter and Getter
    public String getSymbol() {
        return Symbol;
    }
    public void setSymbol(String symbol) {
        Symbol = symbol;
    }
    public float getOpen() {
        return Open;
    }
    public void setOpen(float open) {
        Open = open;
    }
    public float getHigh() {
        return High;
    }
    public void setHigh(float high) {
        High = high;
    }
    public float getLow() {
        return Low;
    }
    public void setLow(float low) {
        Low = low;
    }
    public float getClose() {
        return Close;
    }
    public void setClose(float close) {
        Close = close;
    }
    public long getTimestamp() {
        return timestamp;
    }
    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

}
