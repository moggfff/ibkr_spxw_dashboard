# -*- coding: utf-8 -*-
import pandas as pd
import yfinance as yf

def rsi(series: pd.Series, period: int = 14):
    delta = series.diff()
    up = delta.clip(lower=0).ewm(alpha=1/period, adjust=False).mean()
    down = -delta.clip(upper=0).ewm(alpha=1/period, adjust=False).mean()
    rs = up / (down + 1e-9)
    return 100 - (100 / (1 + rs))

def macd(series: pd.Series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def analyze_equity(symbol: str, cfg: dict):
    try:
        hist = yf.download(symbol, period="3mo", interval="1d", progress=False)
        if hist.empty: return {"symbol":symbol, "ok":False, "msg":"no data"}
        close = hist["Close"]
        r = rsi(close, cfg["analysis"]["rsi_period"]).iloc[-1]
        macd_line, signal_line, histo = macd(close, cfg["analysis"]["macd_fast"],
                                             cfg["analysis"]["macd_slow"],
                                             cfg["analysis"]["macd_signal"])
        cross_up = macd_line.iloc[-2] < signal_line.iloc[-2] and macd_line.iloc[-1] > signal_line.iloc[-1]
        cross_dn = macd_line.iloc[-2] > signal_line.iloc[-2] and macd_line.iloc[-1] < signal_line.iloc[-1]
        signal = "NEUTRAL"
        if r < cfg["analysis"]["rsi_oversold"] or cross_up:
            signal = "BUY"
        elif r > cfg["analysis"]["rsi_overbought"] or cross_dn:
            signal = "SELL"
        return {"symbol":symbol, "ok":True, "rsi":float(r), "macd_cross_up":cross_up, "macd_cross_dn":cross_dn, "signal":signal}
    except Exception as e:
        return {"symbol":symbol, "ok":False, "msg":str(e)}

def spxw_filter(row: pd.Series, cfg: dict) -> bool:
    try:
        d = abs(float(row.get("delta", 0)))
        return cfg["analysis"]["delta_min"] <= d <= cfg["analysis"]["delta_max"]
    except:
        return True
