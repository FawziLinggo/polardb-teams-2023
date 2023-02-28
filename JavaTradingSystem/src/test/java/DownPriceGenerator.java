public class DownPriceGenerator implements PriceGenerator {
    private double volatility;

    public DownPriceGenerator(double volatility) {
        this.volatility = volatility;
    }

    public double nextPrice(double currentPrice) {
        double delta = volatility * currentPrice * Math.random();
        return currentPrice - delta;
    }
}
