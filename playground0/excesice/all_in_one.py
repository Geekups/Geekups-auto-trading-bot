import talib as ta
import pandas as pd
import matplotlib.pyplot as mp
import numpy as np
import eikon

#This function uses the TA-Lib SMA function to calculate the Simple Moving Average
#using the Close price for two periods 
#which you will note later are 14 for the short period and 200 for the long period.
#As you will see later, the period interval itself can vary 
#e.g minute, daily, monthly, hourly - so for example, calculate SMA for 14 days and 200 days.
def SMA(close,sPeriod,lPeriod):
    shortSMA = ta.SMA(close,sPeriod)
    longSMA = ta.SMA(close,lPeriod)
    smaSell = ((shortSMA <= longSMA) & (shortSMA.shift(1) >= longSMA.shift(1)))
    smaBuy = ((shortSMA >= longSMA) & (shortSMA.shift(1) <= longSMA.shift(1)))
    return smaSell,smaBuy,shortSMA,longSMA
