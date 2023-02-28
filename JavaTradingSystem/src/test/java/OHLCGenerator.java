public class OHLCGenerator {
    public static void main(String[] args) {
        double initialPrice = 100.0;
        double volatility = 0.1;
        int numDays = 100;
        double minPrice = 100.0;
        double maxPrice = 200.0;

        // Generate the price data using a while loop
        double[] prices = new double[100];
        prices[0] = initialPrice;
        PriceGenerator generator = new UpPriceGenerator(volatility);
        int i = 1;
        while (i < numDays) {
            double price = generator.nextPrice(prices[i-1]);
            if (price > maxPrice) {
                generator = new DownPriceGenerator(volatility);
            } else if (price < minPrice) {
                generator = new UpPriceGenerator(volatility);
            }
            prices[i] = price;
            i++;
        }

        // Calculate the OHLC values for each day
        for (int j = 0; j < numDays; j += 5) {
            double open = prices[j];
            double high = open;
            double low = open;
            double close = prices[j + 4];
            for (int k = j + 1; k < j + 5; k++) {
                if (prices[k] > high) {
                    high = prices[k];
                }
                if (prices[k] < low) {
                    low = prices[k];
                }
            }
            System.out.printf("Day %d: O=%.2f, H=%.2f, L=%.2f, C=%.2f\n", (j/5)+1, open, high, low, close);
        }
    }
}
