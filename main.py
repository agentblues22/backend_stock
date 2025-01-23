import requests
import pandas as pd
from fastapi import FastAPI
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf


app=FastAPI()

origins = [
    "http://localhost:5173",  # React app running on localhost
  # Another local app
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins, or use ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods: GET, POST, DELETE, etc.
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/company")
def output(comp: str):
 
    # Reading from json file
    data = json.load(open('sample.json', 'r'))
    symbol=data["Meta Data"]['2. Symbol']
    comp_name=yf.Ticker(symbol)
    company_name = comp_name.info['longName']
    company_description = comp_name.info.get("longBusinessSummary", "Description not found")
    logo_url = comp_name.info.get("logo_url", "Logo URL not found")

    refresh=data["Meta Data"]["3. Last Refreshed"]
    interval=data["Meta Data"]["4. Interval"]
    time_series = data["Time Series (5min)"]
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df.index)
    df = df.apply(pd.to_numeric)
    high=df["high"].tolist()
    closing=df["close"].tolist()
    openlist=df["open"].tolist()
    low=df["low"].tolist()
    varhigh=np.var(high)
    volume=df["volume"].tolist()
    varlow=np.var(low)
    varclose=np.var(closing)
    index_list = df.index.tolist()
    ##Advanced Metrics.
    ##Moving Averages over a period of 5.
    def moav(list,n):
        grouped_list = []
        for i in range(0, len(list), n):
            grouped_list.append(list[i:i + n])
        avg_list=[]
        for i in grouped_list:
            avg_list.append(np.average(i))
        return avg_list
    moving_average=moav(closing,5)
#################################################
## Volume weighted average price##
    out_array=np.multiply(closing,volume)
    sumout=np.sum(out_array)
    sumvol=np.sum(volume)
    VWA=sumout/sumvol
#######################################################################################

    def calculate_rsi(prices, period=14):
        delta = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    
        gains = [max(change, 0) for change in delta]
        losses = [-min(change, 0) for change in delta]
        
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        rsi = [None] * period  # RSI not defined for the first 'period' values
        for i in range(period, len(prices) - 1):
            current_gain = gains[i - 1]
            current_loss = losses[i - 1]
            
            avg_gain = (avg_gain * (period - 1) + current_gain) / period
            avg_loss = (avg_loss * (period - 1) + current_loss) / period
            
            # Avoid division by zero
            if avg_loss == 0:
                rs = float('inf')  # Strong upward trend
            else:
                rs = avg_gain / avg_loss
            
            rsi_value = 100 - (100 / (1 + rs))
            rsi.append(rsi_value)
    
    # Fill in None for RSI values before the 'period'
        rsi.extend([None] * (len(prices) - len(rsi)))
    
        return rsi
    RSI = calculate_rsi(closing, period=14)
################################################################################
    def calculate_roc(prices, n):
        roc = [None] * n  # Initial values can't be calculated, so None for the first 'n' values
    
        for i in range(n, len(prices)):
            # Calculate ROC for each value after 'n'
            roc_value = ((prices[i] - prices[i - n]) / prices[i - n]) * 100
            roc.append(roc_value)
        
        return roc
    ROC = calculate_roc(closing,5)

###############################################################################

    ind=[]
    for i in index_list:
        ind.append(str(i))

    return {
        "openlist":openlist,
        "highlist": high,
        "lowlist": low,
        "closelist":closing,
        "variance_high": varhigh,
        "variance_low":varlow,
        "variance_close":varclose,
        "index": ind,
        "volume":volume,
        "symbol":symbol,
        "Company":company_name,
        "Description":company_description,
        "Logo":logo_url,
        "Last refresh":refresh,
        "interval":interval,
        "moving Average":moving_average,
        "VWA":VWA,
        "RSI":RSI,
        "final":closing[0],
        "ROC":ROC,


    }


