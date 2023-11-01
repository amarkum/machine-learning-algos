import concurrent.futures
import pandas as pd
from binance.client import Client
from pypfopt import EfficientFrontier, risk_models, expected_returns
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Client()
client.RESPONSE_TIMEOUT = 20

prices = client.futures_symbol_ticker()
symbols = [price['symbol'] for price in prices if price['symbol'].endswith('USDT')]

def fetch_symbol_data(symbol):
    try:
        klines = client.futures_klines(symbol=symbol, interval='1m', limit=1440)
        closes = [float(entry[4]) for entry in klines]
        return symbol, closes
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return symbol, []

def recommend_pairs(df, interval):
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.CovarianceShrinkage(df).ledoit_wolf()
    ef = EfficientFrontier(mu, S, solver="ECOS")

    try:
        ef.max_sharpe()
    except ValueError:
        logger.warning(f"Unable to optimize for Sharpe ratio for {interval}. No recommendations will be made.")
        return []

    cleaned_weights = ef.clean_weights()
    recommended_pairs = [pair for pair, weight in cleaned_weights.items() if weight > 0]
    return recommended_pairs

if __name__ == "__main__":
    price_data = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_symbol = {executor.submit(fetch_symbol_data, symbol): symbol for symbol in symbols}
        for future in concurrent.futures.as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                _, closes = future.result()
                if len(closes) == 1440:
                    price_data[symbol] = closes
                else:
                    logger.info(f"Discarding {symbol} due to incomplete data")
            except Exception as e:
                logger.error(f"Error processing data for {symbol}: {str(e)}")

    if not price_data:
        logger.error("No valid price data retrieved.")
    else:
        df_24h = pd.DataFrame(price_data)
        df_12h = df_24h.tail(720)  # Last 12 hours
        df_1h = df_24h.tail(60)    # Last 1 hour

        recommendations = defaultdict(lambda: {"weight": 0, "intervals": []})
        intervals = [("24h", df_24h), ("12h", df_12h), ("1h", df_1h)]
        for interval, df in intervals:
            recommended_pairs = recommend_pairs(df, interval)
            for pair in recommended_pairs:
                recommendations[pair]["weight"] += 1
                recommendations[pair]["intervals"].append(interval)

        if recommendations:
            sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1]["weight"], reverse=True)
            recommendations_to_print = []

            for pair, data in sorted_recommendations:
                output = f"Symbol: {pair} | Weight: {data['weight']} | Intervals: {', '.join(data['intervals'])}"
                print(output)

                if data["weight"] > 1:
                    recommendations_to_print.append(pair)

            if recommendations_to_print:
                print("\nBuy Recommendations:")
                for rec in recommendations_to_print:
                    print(f"Recommendation: {rec}")
            else:
                print("No recommendations with weight greater than 1 available.")
        else:
            print("No recommendations available.")
