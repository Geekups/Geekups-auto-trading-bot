import pandas as pd
import numpy as np
import datetime 
import MetaTrader5 as mt5
import time

#Library to generate technical indicators
import talib
from talib import RSI, EMA


while True:
    symbol = "EURUSD"
    lot = 0.02 

    # Get the Data
    mt5.initialize()
            
    symbol_info=mt5.symbol_info("EURUSD")
            
    rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M1, 0, 1000)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

    #Signal Processing

    close = np.array(rates_frame['close'])
    rsi_ind = RSI(close, timeperiod = 14)
    array_length = len(rsi_ind)
    last_element = rsi_ind[- 1]
    last_rsi = last_element
    array_length3 = len(close)
    last_element3 = close[-1]
    last_price = last_element3
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20

    #Decission Taking and Send Order

    if last_rsi>70  :
        request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot,
                    "type": mt5.ORDER_TYPE_SELL,
                    "sl": price - 0.002,
                    "tp": price + 0.005,
                    "deviation": deviation,
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
                
                
    if 30>last_rsi :
        request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "sl": price + 0.002,
                "tp": price - 0.005,
                "deviation": deviation,
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
    
