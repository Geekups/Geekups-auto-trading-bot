import pandas as pd
import numpy as np
import talib as ta
import MetaTrader5 as mt5
from datetime import datetime

def get_rates_frame(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 1000)
    rates_frame = pd.DataFrame(rates)
    return rates_frame

def signal(rates_frame):
    rates_frame["time"]=pd.to_datetime(rates_frame["time"], unit="s")
    close = np.array(rates_frame["close"])
    rates_frame["rsi"] = RSI(close, timeperiod = 14)
    rates_frame["rsi_roll_mean"] = rates_frame["rsi"].rolling(10).mean()
    rates_frame["rsi_roll_std"] = rates_frame["rsi"].rolling(10).std()
    rates_frame["custom signal"] = np.where(rates_frame["rsi"] > 2*rates_frame["rsi_roll_std"], "Sell",
    np.where(rates_frame["rsi"] < 2*rates_frame["rsi_roll_std"], "Buy", ""))
    
    return rates_frame["custom signal"]
def RSI(close,timePeriod):
    rsi = ta.RSI(close,timePeriod)
    rsiSell = (rsi>70) #& (rsi.shift(1)<=70)
    rsiBuy = (rsi<30) #& (rsi.shift(1)>=30)
    return rsiSell,rsiBuy, rsi

if __name__ == '__main__':
    mt5.initialize()
    SYMBOL = "EURUSD"
    while True:
        rates_frame = get_rates_frame(SYMBOL)
        rates_frame["time"]=pd.to_datetime(rates_frame["time"], unit="s")
        close = np.array(rates_frame["close"])
        rates_frame["rsi"] = RSI(close, timePeriod = 14)
        rates_frame["rsi_roll_mean"] = rates_frame["rsi"].rolling(10).mean()
        rates_frame["rsi_roll_std"] = rates_frame["rsi"].rolling(10).std()
        rates_frame["custom signal"] = np.where(rates_frame["rsi"] > 2*rates_frame["rsi_roll_std"], "Sell",
        np.where(rates_frame["rsi"] < 2*rates_frame["rsi_roll_std"], "Buy", ""))
        n = rates_frame["custom signal"]
        close = np.array(rates_frame["close"])
        rsiSell, rsiBuy, rsi = RSI(close=close, timePeriod = 14)
       

        # directions = signal(rates_frame)
        # for direction in directions.values :
        #     print('time: ', datetime.now())
        #     #print('last_close: ', last_close)
        #     # print('sma: ', sma)
        #     print('signal: ', direction)
        #     print(SYMBOL)
        #     #print("position is opened. ")
        #     print('-------\n')

