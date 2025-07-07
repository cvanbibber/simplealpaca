import os

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import (
    MarketOrderRequest,
    LimitOrderRequest,
    StopOrderRequest,
    StopLimitOrderRequest,
    TrailingStopOrderRequest,
    GetOrdersRequest,
)
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType, QueryOrderStatus
from alpaca.common.exceptions import APIError
from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame


class SimpleAlpaca:
    def __init__(self, api_key=None, secret_key=None, paper=True):
        self.api_key = api_key or os.getenv("APCA_API_KEY_ID")
        self.secret_key = secret_key or os.getenv("APCA_API_SECRET_KEY")
        self.paper = paper
        self.trading_client = TradingClient(self.api_key, self.secret_key, paper=self.paper)
        self.crypto_client = CryptoHistoricalDataClient()
        self.stock_client = StockHistoricalDataClient(self.api_key, self.secret_key)


    def get_account_details(self):
        account = self.trading_client.get_account()
        return {
            "portfolio_size": float(account.portfolio_value),
            "cash": float(account.cash),
            "daily_change": float(account.equity) - float(account.last_equity),
            "buying_power": float(account.buying_power),
        }

    def get_positions(self):
        positions = self.trading_client.get_all_positions()
        return [
            {
                "symbol": pos.symbol,
                "qty": float(pos.qty),
                "avg_entry_price": float(pos.avg_entry_price),
                "current_price": float(pos.current_price),
                "market_value": float(pos.market_value),
                "unrealized_pl": float(pos.unrealized_pl),
            }
            for pos in positions
        ]

    def place_order(
        self,
        symbol,
        qty,
        side,
        order_type,
        time_in_force,
        limit_price=None,
        stop_price=None,
        trail_price=None,
        trail_percent=None,
    ):
        try:
            if order_type == "market":
                order_data = MarketOrderRequest(
                    symbol=symbol, qty=qty, side=side, time_in_force=time_in_force
                )
            elif order_type == "limit":
                order_data = LimitOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    time_in_force=time_in_force,
                    limit_price=limit_price,
                )
            elif order_type == "stop":
                order_data = StopOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    time_in_force=time_in_force,
                    stop_price=stop_price,
                )
            elif order_type == "stop_limit":
                order_data = StopLimitOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    time_in_force=time_in_force,
                    limit_price=limit_price,
                    stop_price=stop_price,
                )
            elif order_type == "trailing_stop":
                order_data = TrailingStopOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    time_in_force=time_in_force,
                    trail_price=trail_price,
                    trail_percent=trail_percent,
                )
            else:
                raise ValueError("Invalid order type")

            return self.trading_client.submit_order(order_data)
        except APIError as e:
            if "insufficient" in str(e) and side == "buy":
                account_details = self.get_account_details()
                buying_power = account_details["buying_power"]
                
                # This is a simplified example. A more robust implementation would be needed.
                # It does not account for the price of the asset.
                print(f"Insufficient funds. Placing order with available buying power: {buying_power}")
                if order_type == "market":
                    order_data = MarketOrderRequest(
                        symbol=symbol, notional=buying_power, side=side, time_in_force=time_in_force
                    )
                    return self.trading_client.submit_order(order_data)
            raise e

    def get_orders(self, status=QueryOrderStatus.OPEN, symbols=None):
        request_params = GetOrdersRequest(status=status, symbols=symbols)
        return self.trading_client.get_orders(filter=request_params)

    def cancel_order_by_id(self, order_id):
        return self.trading_client.cancel_order_by_id(order_id)

    def close_position(self, symbol):
        return self.trading_client.close_position(symbol)

    def get_stock_bars(self, symbols, timeframe, start, end=None):
        request_params = StockBarsRequest(
            symbol_or_symbols=symbols, timeframe=timeframe, start=start, end=end
        )
        return self.stock_client.get_stock_bars(request_params)

    def get_crypto_bars(self, symbols, timeframe, start, end=None):
        request_params = CryptoBarsRequest(
            symbol_or_symbols=symbols, timeframe=timeframe, start=start, end=end
        )
        return self.crypto_client.get_crypto_bars(request_params)
