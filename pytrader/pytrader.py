#!/usr/bin/env python

import sqlite3, readline, rlcompleter
import rpy2.robjects as robjects
import rpy2.rlike.container as rlc
from rpy2.robjects.packages import importr

TTR = importr("TTR")

DATABASE = "/home/irocha/pytrader/data/symbols.db"
SYMBOL = "UOLL4"

class Trader:
    def __init__(self, database, symbol, start=None, end=None, limit=0):
        self.database = database
        self.symbol = symbol
        self.start = start
        self.end = end
        self.limit = limit
        self.frames = self.createFrames()

    def getData(self, sql, params):
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        cur.execute(sql, params)
        rows = [row for row in cur]
        cur.close()
        con.close()
        return rows

    def getSymbols(self):
        sql, params = None, None
        if (self.start == None and self.end == None):
            sql = "SELECT D, O, H, L, C, V FROM symbols WHERE S = ? ORDER BY D"
            params = [self.symbol]
        elif (self.end == None):
            sql = "SELECT D, O, H, L, C, V FROM symbols WHERE S = ? AND D >= ? ORDER BY D"
            params = [self.symbol, self.start]
        else:
            sql = "SELECT D, O, H, L, C, V FROM symbols WHERE S = ? AND D BETWEEN ? AND ? ORDER BY D"
            params = [self.symbol, self.start, self.end]
        if self.limit != None and self.limit > 1:
            sql = sql + " LIMIT %d" % self.limit
        return self.getData(sql, params)

    def createFrames(self):
        symbols = self.getSymbols()
        dates = [v[0] for v in symbols]
        data1 = rlc.OrdDict([('Open', robjects.FloatVector([v[1] for v in symbols])),
                             ('Volume', robjects.FloatVector([v[5] for v in symbols]))])
        data2 = rlc.OrdDict([('High', robjects.FloatVector([v[2] for v in symbols])),
                             ('Low', robjects.FloatVector([v[3] for v in symbols])),
                             ('Close', robjects.FloatVector([v[4] for v in symbols]))])
        return (dates, robjects.DataFrame(data1), robjects.DataFrame(data2))

    def frames(self):
        return self.frames

    def get(self, tag):
        n = tag.capitalize()
        f = self.frames
        return f[0] if n == "Date" else (f[1] if n in ["Open", "Volume"] else f[2]).rx2(n)

    def Date(self):
        return self.get("Date")

    def Open(self):
        return self.get("Open")

    def High(self):
        return self.get("High")

    def Low(self):
        return self.get("Low")

    def Volume(self):
        return self.get("Volume")

    def Close(self):
        return self.get("Close")

    # Simple moving average
    # http://en.wikipedia.org/wiki/Exponential_moving_average#Simple_moving_average
    def SMA(self, tag, n):
        return TTR.SMA(self.get(tag), n)

    # Exponential moving average
    # http://en.wikipedia.org/wiki/Exponential_moving_average#Exponential_moving_average
    def EMA(self, tag, n):
        return TTR.EMA(self.get(tag), n)

    # Average True Range
    # http://en.wikipedia.org/wiki/Average_True_Range
    def ATR(self, n):
        return TTR.ATR(self.frames[2], n).rx(True, 2)

    # Stochastic Oscillator 20/80
    # http://en.wikipedia.org/wiki/Stochastic_oscillator
    # http://www.investopedia.com/terms/s/stochasticoscillator.asp
    # stoch(HLC, nFastK=14, nFastD=3, nSlowD=3)
    def Stoch(self, nFastK=14, nFastD=3, nSlowD=3):
        return TTR.stoch(self.frames[2], nFastK, nFastD, nSlowD).rx(True, 1)

    # Relative Strength Index
    # http://en.wikipedia.org/wiki/Relative_Strength_Index
    # http://www.investopedia.com/articles/technical/071601.asp
    # The 30/70 on our scale represents the oversold/overbought positions
    def RSI(self, tag, n):
        return TTR.RSI(self.get(tag), n)

    # Average Directional Index
    # http://en.wikipedia.org/wiki/Average_Directional_Index
    # http://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp
    # 00 -  25  Absent or Weak Trend
    # 25 -  50  Strong Trend
    # 50 -  75  Very Strong Trend
    # 75 - 100  Extremely Strong Trend
    def ADX(self, n):
        return TTR.ADX(self.frames[2], n)

    # STARC Bands
    # http://www.investopedia.com/terms/s/starc.asp
    # Best alternative to Bollinger Bands
    def STARCBands(self, tag, n, factor=1.0):
        atr = self.ATR(n)
        ma = self.EMA(tag, n)
        up, dn = [], []
        for i in range(len(sma)):
            up.append((ma[i] + (atr[i] * factor)) if atr[i] > 0 else atr[i])
            dn.append((ma[i] - (atr[i] * factor)) if atr[i] > 0 else atr[i])
        return (atr, ma, dn, up)

    # Bollinger Bands
    # http://en.wikipedia.org/wiki/Bollinger_bands
    # http://www.investopedia.com/articles/technical/102201.asp
    # http://www.investopedia.com/articles/trading/05/022205.asp
    def BBands(self, n, maType="SMA", sd=2):
        bbands = TTR.BBands(self.frames[2], n, maType, sd)
        return (bbands.rx(True, 1), bbands.rx(True, 2), bbands.rx(True, 3))


# R language (test):
# library(quantmod)
# trader <- read.csv(file="/home/irocha/pytrader/data/UOLL4.csv", header=FALSE)
# names(trader) <- c("Date", "Open", "High", "Low", "Close", "Volume", "A")
# EMA(trader[5], 7)[1:14]
# hlc = data.frame(trader[3], trader[4], trader[5])
# names(hlc) <- c("High", "Low", "Close")
# ATR(hlc, 7)[,2][1:14]
# BBands(hlc, 7)[1:14]
# ADX(hlc, 7)[1:14]
# RSI(hlc[3], 7)[1:14]
# stoch(hlc, 7)[1:14]
# ohlc = data.frame(trader[2], trader[3], trader[4], trader[5])
# names(ohlc) <- c("Open", "High", "Low", "Close")
# data <- xts(ohlc, order.by=as.Date(trader[,1], "%Y-%m-%d"))
# candleChart(data,multi.col=TRUE,theme="white")

FORMAT = 10
FORMAT_FMT = "{:%s} " % FORMAT

FIELDS = ["Date", "Open", "High", "Low", "Close",
          "EMA", "SMA", "ATR", "STARC(dn)", "STARC(up)",
          "ADX(%)", "Stoch", "RSI(%)",
          "BB(dn)", "BB(ma)", "BB(up)"]
NF = len(FIELDS)

def f(x):
    return ("%%%d.4f" % FORMAT) % x

def tr():
    print("-" * (FORMAT * NF) + "-" * NF)
    
    
if __name__ == '__main__':
    # for development/debug (python -i pytrader.py)
    rc = rlcompleter
    readline.parse_and_bind("tab: complete")

    limit = 21
    periods = 7

    trader = Trader(DATABASE, SYMBOL, None, None, limit)

    ema = trader.EMA("Close", periods)
    sma = trader.SMA("Close", periods)
    env = trader.STARCBands("Close", periods)
    stk = trader.Stoch(periods)
    rsi = trader.RSI("Close", periods)
    adx = trader.ADX(periods)
    bba = trader.BBands(periods)

    n = len(ema)
    
    print("%s: Summary of %d items [%d useful data]" % (SYMBOL, n, n - periods))
    tr()
    
    fmt = (FORMAT_FMT * NF).rstrip()
    print(" ".join([t.rjust(FORMAT) for t in FIELDS]))
    tr()
    
    i = periods
    while i < n:
        print(fmt.format(trader.Date()[i],
                         f(trader.Open()[i]), f(trader.High()[i]), f(trader.Low()[i]), f(trader.Close()[i]),
                         f(ema[i]), f(sma[i]),
                         f(env[0][i]), f(env[2][i]), f(env[3][i]),
                         f(adx[i]), f(stk[i]), f(rsi[i]),
                         f(bba[0][i]), f(bba[1][i]), f(bba[2][i])))
        i += 1
