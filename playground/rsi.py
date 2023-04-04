import MetaTrader5 as mt5  # install using 'pip install MetaTrader5'
import pandas as pd  # install using 'pip install pandas'
from datetime import datetime
import time
import talib

# function to send a market order
def market_order(symbol, volume, order_type, **kwargs):
    tick = mt5.symbol_info_tick(symbol)

    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": DEVIATION,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)
    print(order_result)

    return order_result


# function to close an order based on ticket id
def close_order(ticket):
    positions = mt5.positions_get()

    for pos in positions:
        tick = mt5.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 represents buy, 1 represents sell - inverting order_type to close the position
        price_dict = {0: tick.ask, 1: tick.bid}

        if pos.ticket == ticket:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": type_dict[pos.type],
                "price": price_dict[pos.type],
                "deviation": DEVIATION,
                "magic": 100,
                "comment": "python close order",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            order_result = mt5.order_send(request)
            print(order_result)

            return order_result

    return 'Ticket does not exist'


# function to get the exposure of a symbol
def get_exposure(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()

        return exposure


# function to look for trading signals
def signal(symbol, timeframe, rsi_period, rsi_buy_threshold, rsi_sell_threshold):
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 1, rsi_period)
    bars_df = pd.DataFrame(bars)

    close = bars_df.close.values
    rsi = talib.RSI(close, timeperiod=rsi_period)

    last_close = close[-1]
    last_rsi = rsi[-1]

    direction = 'flat'
    if last_rsi >= rsi_buy_threshold:
        direction = 'buy'
    elif last_rsi <= rsi_sell_threshold:
        direction = 'sell'

    return last_close, last_rsi, direction



if __name__ == '__main__':

    # strategy parameters
    SYMBOL = "EURUSD"
    VOLUME = 1.0
    TIMEFRAME = mt5.TIMEFRAME_M1
    SMA_PERIOD = 10
    DEVIATION = 20
    RSI_PERIOD = 14

    mt5.initialize()

    while True:
        # calculating account exposure
        exposure = get_exposure(SYMBOL)

        # calculating last candle close and simple moving average and RSI, and checking for trading signal
        last_close = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 1, 1)[0][4]
        sma = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, SMA_PERIOD)['close'].mean()
        rsi = talib.RSI(mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, RSI_PERIOD)['close'], timeperiod=RSI_PERIOD)
        direction = 'buy' if (last_close > sma) and (rsi[-1] < 30) else 'sell' if (last_close < sma) and (rsi[-1] > 70) else None

        # trading logic
        if direction == 'buy':
            # if we have a BUY signal, close all short positions
            for pos in mt5.positions_get():
                if pos.type == 1:  # pos.type == 1 represent a sell order
                    close_order(pos.ticket)

            # if there are no open positions, open a new long position
            if not mt5.positions_total():
                market_order(SYMBOL, VOLUME, direction)

        elif direction == 'sell':
            # if we have a SELL signal, close all short positions
            for pos in mt5.positions_get():
                if pos.type == 0:  # pos.type == 0 represent a buy order
                    close_order(pos.ticket)

            # if there are no open positions, open a new short position
            if not mt5.positions_total():
                market_order(SYMBOL, VOLUME, direction)

        print('time: ', datetime.now())
        print('exposure: ', exposure)
        print('last_close: ', last_close)
        print('sma: ', sma)
        print('rsi: ', rsi[-1])
        print('signal: ', direction)
        print(SYMBOL)
        print("position is opened. ")
        print('-------\n')

        # update every 1 second
        time.sleep(1)