import pandas as pd
import numpy as np
import datetime 
import MetaTrader5 as mt5
import time

#Library to generate technical indicators
import talib
from talib import RSI, EMA

symbol = "EURUSD"
lot = 0.02 

# Get the Data
mt5.initialize()
symbol_info=mt5.symbol_info("EURUSD")
            
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M1, 0, 1000)
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')         

while True:



    #Signal Processing

    # close = np.array(rates_frame['close'])
    # rsi_ind = RSI(close, timeperiod = 14)
    
    
    # last_rsi = rsi_ind[-1]
    price = mt5.symbol_info_tick(symbol).ask

    close = np.array(rates_frame["close"])
    rates_frame["rsi"] = RSI(close, timeperiod = 14)
    rates_frame["rsi_roll_mean"] = rates_frame["rsi"].rolling(10).mean()
    rates_frame["rsi_roll_std"] = rates_frame["rsi"].rolling(10).std()
    rates_frame["custom signal"] = np.where(rates_frame["rsi"] > 2*rates_frame["rsi_roll_std"], "Sell",
    np.where(rates_frame["rsi"] < 2*rates_frame["rsi_roll_std"], "Buy", ""))
    
    #Decission Taking and Send Order

    if rates_frame["rsi"] > 2*rates_frame["rsi_roll_std"]  :
        request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot,
                    "type": mt5.ORDER_TYPE_SELL,
                    "sl": price - 0.002,
                    "tp": price + 0.005,
                    "deviation": rates_frame["rsi_roll_std"],
                    "magic": 202003,
                    "comment": "InUpBot MrEurUsd",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC}
        print('Se ejecutó una compra por 0.01')
        mt5.order_send(request)
        print('time: ', datetime.now())
        #print('last_close: ', last_close)
        # print('sma: ', sma)
        print('signal: ', "Sell")
        print(symbol)
        print("position is opened. ")
        print('-------\n')
        continue
                
                
    if rates_frame["rsi"] < 2*rates_frame["rsi_roll_std"] :
        request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "sl": price + 0.002,
                "tp": price - 0.005,
                "deviation": rates_frame["rsi_roll_std"],
                "magic": 202003,
                "comment": "InUpBot Lancero",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC}
        print('Se ejecutó una venta por 0.01')
        mt5.order_send(request)
        print('time: ', datetime.now())
        #print('last_close: ', last_close)
        # print('sma: ', sma)
        print('signal: ', "Buy")
        print(symbol)
        print("position is opened. ")
        print('-------\n')
    else:
        print('-------\n')
        print("position is opened. ")
        print('Waiting for Market Signal')
        print('-------\n')
    
