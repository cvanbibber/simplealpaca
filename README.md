# SimpleAlpaca

A simple but comprehensive Alpaca trading API, designed to provide a clean and easy-to-use interface for interacting with the Alpaca API.

## Installation

```bash
pip install simplealpaca
```

## Usage

First, initialize the `SimpleAlpaca` client with your API keys. You can either pass them as arguments or set them as environment variables (`APCA_API_KEY_ID` and `APCA_API_SECRET_KEY`).

```python
from simplealpaca import SimpleAlpaca

# Initialize the client
client = SimpleAlpaca(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")
```

### Account Management

Get your account details, including portfolio size, cash, daily change, and buying power.

```python
account_details = client.get_account_details()
print(account_details)
```

### Positions

Retrieve a list of your current open positions.

```python
positions = client.get_positions()
print(positions)
```

### Trading

Place an order for a stock or crypto asset. The `place_order` method supports various order types, including market, limit, stop, stop-limit, and trailing stop orders.

```python
# Place a market order
market_order = client.place_order(
    symbol="AAPL",
    qty=1,
    side="buy",
    order_type="market",
    time_in_force="gtc"
)
print(market_order)

# Place a limit order
limit_order = client.place_order(
    symbol="AAPL",
    qty=1,
    side="buy",
    order_type="limit",
    time_in_force="gtc",
    limit_price=100.00
)
print(limit_order)
```

### Order Management

Retrieve a list of your orders (open, closed, or all) and cancel open orders.

```python
# Get all open orders
open_orders = client.get_orders()
print(open_orders)

# Cancel an order by its ID
cancellation_status = client.cancel_order_by_id(open_orders[0].id)
print(cancellation_status)
```

### Position Management

Close an open position.

```python
# Close a position
close_status = client.close_position("AAPL")
print(close_status)
```

### Market Data

Fetch historical market data for stocks and cryptocurrencies.

```python
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

# Get daily stock bars for the last week
end_date = datetime.now()
start_date = end_date - timedelta(days=7)
stock_bars = client.get_stock_bars("SPY", TimeFrame.Day, start_date, end_date)
print(stock_bars)

# Get hourly crypto bars for the last 24 hours
end_date = datetime.now()
start_date = end_date - timedelta(days=1)
crypto_bars = client.get_crypto_bars("BTC/USD", TimeFrame.Hour, start_date, end_date)
print(crypto_bars)
```

If you attempt to place a buy order that exceeds your buying power, the API will handle the error by placing an order with the maximum available buying power (only for market orders).
