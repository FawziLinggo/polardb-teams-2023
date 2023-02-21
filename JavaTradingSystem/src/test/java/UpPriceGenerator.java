public class UpPriceGenerator implements PriceGenerator {
    private double volatility;

    public UpPriceGenerator(double volatility) {
        this.volatility = volatility;
    }

    public double nextPrice(double currentPrice) {
        double delta = volatility * currentPrice * Math.random();
        return currentPrice + delta;
    }
}
