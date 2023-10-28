import logging
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from binance.client import Client
from pypfopt import EfficientFrontier, risk_models, expected_returns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Client()
client.RESPONSE_TIMEOUT = 20
prices = client.futures_symbol_ticker()

crypto_symbols = [price['symbol'] for price in prices if price['symbol'].endswith('USDT')]
stock_symbols = ["AAPL", "MSFT", "GOOGL"]
currency_symbols = ["EURUSD=X", "JPYUSD=X"]
commodity_symbols = ["GC=F", "CL=F"]


def fetch_crypto_data(symbol):
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=1440)
    closes = [float(entry[4]) for entry in klines]
    return symbol, closes


def fetch_yahoo_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period="1d", interval="1m", auto_adjust=True)
    return data['Close']


def fetch_data_by_market(symbols, market_type):
    if market_type == "crypto":
        price_data = {}
        expected_length = None

        with ThreadPoolExecutor(max_workers=3) as executor:
            for symbol, closes in executor.map(fetch_crypto_data, symbols):
                if expected_length is None:
                    expected_length = len(closes)
                elif expected_length != len(closes):
                    continue
                price_data[symbol] = closes

        return pd.DataFrame(price_data)
    elif market_type in ["stocks", "currency", "commodities"]:
        return pd.DataFrame({symbol: fetch_yahoo_data(symbol) for symbol in symbols})


def optimize_market_portfolio(symbols, market_type):
    df = fetch_data_by_market(symbols, market_type)

    mu = expected_returns.mean_historical_return(df)
    S = risk_models.CovarianceShrinkage(df).ledoit_wolf()

    ef = EfficientFrontier(mu, S, solver="ECOS")

    try:
        ef.max_sharpe()
    except ValueError:
        logger.warning(f"Unable to optimize for Sharpe ratio in {market_type}. No recommendations will be made.")
        return []

    cleaned_weights = ef.clean_weights()
    return [pair for pair, weight in cleaned_weights.items() if weight > 0]


if __name__ == "__main__":
    recommended_assets = {
        "crypto": optimize_market_portfolio(crypto_symbols, "crypto"),
        "stocks": optimize_market_portfolio(stock_symbols, "stocks"),
        "currency": optimize_market_portfolio(currency_symbols, "currency"),
        "commodities": optimize_market_portfolio(commodity_symbols, "commodities")
    }

    for market, assets in recommended_assets.items():
        if assets:
            for asset in assets:
                print(f"Recommendation ({market}): {asset}")
        else:
            print(f"No recommendations available for {market}.")
