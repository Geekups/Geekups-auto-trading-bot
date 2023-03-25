import pandas as pd
import numpy as np
from talib import RSI
import MetaTrader5 as mt5
from datetime import datetime
import matplotlib.pyplot as plt 
symbol = "EURUSD"
lot = 0.02 
5
# Get the Data
# mt5.initialize( login = name, server = serv, password = key, path = path)
mt5.initialize()
while True:
    symbol_info=mt5.symbol_info("EURUSD")
        
    rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M1, 0, 1000)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

    #Create signal

    close = np.array(rates_frame['close'])

    #Create the RSI indicator
    rates_frame['rsi'] = RSI(close, timeperiod = 14)

    #Create the Rolling mean
    rates_frame['rsi_roll_mean'] = rates_frame['rsi'].rolling(10).mean()

    #Create the Rolling std
    rates_frame['rsi_roll_std'] = rates_frame['rsi'].rolling(10).std()

    #Create the custom signal
    rates_frame['custom signal'] = np.where(rates_frame['rsi'] > 2*rates_frame['rsi_roll_std'], 'Sell',
        np.where(rates_frame['rsi'] < 2*rates_frame['rsi_roll_std'], 'Buy', '')
    )
    
    print('time: ', datetime.now())    #print('exposure: ', exposure)
   
    #print('signal: ', direction)
    print("symbo_info",symbol_info)
    print("position is opened. ")
    print('-------\n')