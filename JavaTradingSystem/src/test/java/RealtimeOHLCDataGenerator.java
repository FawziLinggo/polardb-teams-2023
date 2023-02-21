import java.util.Random;

public class RealtimeOHLCDataGenerator {
    private double open = 100.0; // starting value
    private double high = 100.0;
    private double low = Double.MAX_VALUE; // set initial low value to a very high value
    private double close = 100.0;
    private Random random = new Random();

    public void updateData() {
        // generate a random change value between -5 and 5
        double change = random.nextDouble() * 30.0 - 5.0;

        // update the OHLC values
        close = close + change;
        if (close > high) {
            high = close;
        }
        if (close < low) {
            low = close;
        }
        open = close - random.nextDouble() * 5.0;
        if (open < low) {
            low = open;
        }
        if (open > high) {
            high = open;
        }
    }

    public double getOpen() {
        return open;
    }

    public double getHigh() {
        return high;
    }

    public double getLow() {
        return low;
    }

    public double getClose() {
        return close;
    }

    public static void main(String[] args) throws InterruptedException {
        RealtimeOHLCDataGenerator generator = new RealtimeOHLCDataGenerator();
        while (true) {
            generator.updateData();
            System.out.printf("OHLC Data: %.2f %.2f %.2f %.2f \n" , generator.getOpen(),generator.getHigh(), generator.getLow(),generator.getClose());
            Thread.sleep(1000); // wait 1 second
        }
    }
}
