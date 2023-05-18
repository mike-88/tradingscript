import yfinance as yf
import pandas as pd
import numpy as np

def dl_stock(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval)
    return pd.DataFrame(df)['Close'].tolist(), pd.DataFrame(df)['Close'].index.tolist()

def trade_stock(ticker, period, interval):
    df = pd.DataFrame(yf.download(tickers=ticker, period=period, interval=interval))

    TradeList = []
    ProfitList = []
    Balance = 1000
    VolumeList = []

    #Implemented Inc to prevent overlapping trades? Leads to error because index is out of range when the dataset stops. This is not the issue with the Closing price.
    Inc = 0

    TargetVar = 1.12
    MaxLength = 45

    Close = df['Adj Close']
    DfIndex = df.index
    CloseMAstop = df['Adj Close'].rolling(window=8).mean()
    CloseMA5 = df['Adj Close'].rolling(window=5).mean()
    CloseMA10 = df['Adj Close'].rolling(window=10).mean()
    CloseMA20 = df['Adj Close'].rolling(window=20).mean()
    Volume = df['Volume']
    VolumeMA20 = df['Volume'].rolling(window=20).mean()
    Open = df['Open']
    Low = df['Low']
    High = df['High']

    for i in range(len(df)):
        #i += Inc
        Inc = 0
        if i < len(df) - MaxLength:
            if Close[i-1] > CloseMA5[i-1] and \
                CloseMA5[i-1] > CloseMA10[i-1] and \
                CloseMA10[i-1] > CloseMA20[i-1] and \
                Volume[i-1] > VolumeMA20[i-1] and \
                Open[i] < Close[i-1] * 1.02 and \
                Close[i-1] > Open[i-1] and \
                Open[i-1] - Low[i-1] < Close[i-1] - Open[i-1]:

               ConsolHigh = max(High[i-20:i-1]) * 1.01
               ConsolLow = High[i-1] - 0.5 * (Close[i-1] - Open[i-1])
               Length = 0

               while Open[i] < ConsolHigh and \
                   Open[i] > ConsolLow and \
                   High[i] < ConsolHigh and \
                   Low[i] > ConsolLow and \
                    i < len(High) - 1:
                   i += 1
                   Inc += 1
                   Length += 1
               else:
                   if Open[i] > ConsolHigh and Open[i] < ConsolHigh * 1.03:
                       Buy = Open[i] #at price = Open[i]
                       Target = Open[i] * TargetVar
                       StopLoss = CloseMA5[i-1] * 0.99
                       #StopLoss = Open[i] * 0.97
                       while Low[i] > StopLoss and High[i] < Target and i < len(High) - 1 and Length < MaxLength:
                           if i < len(High) - 1:
                               i += 1
                               Inc += 1
                               Length += 1
                       else:
                           if Low[i] < StopLoss and i < len(High) - 1:
                               TradeList.append([ticker, DfIndex[i + Inc], round(Buy, 2), DfIndex[i + Inc + Length], round(StopLoss, 2), round((StopLoss / Buy) - 1, 2)])
                               ProfitList.append((StopLoss / Buy) - 1)
                               Balance = Balance * (StopLoss / Buy)
                           elif High[i] > Target and i < len(High) - 1:
                               TradeList.append([ticker, DfIndex[i + Inc], round(Buy, 2), DfIndex[i + Inc + Length], round(Target, 2), round((Target / Buy) - 1, 2)])
                               ProfitList.append((Target / Buy) - 1)
                               Balance = Balance * (Target / Buy)
                           else:
                               TradeList.append([ticker, DfIndex[i + Inc], round(Buy, 2), DfIndex[i + Inc + Length], round(Close[i], 2), round((Close[i] / Buy) - 1, 2)])
                               ProfitList.append((Close[i] / Buy) - 1)
                               Balance = Balance * (Close[i] / Buy)

                   elif Open[i] > ConsolHigh * 1.03:
                       Buy = 0

                   elif Open[i] < ConsolHigh and High[i] > ConsolHigh:
                       Buy = ConsolHigh  # at price = Open[i]
                       Target = ConsolHigh * TargetVar
                       StopLoss = CloseMA5[i-1] * 0.99
                       #StopLoss = ConsolHigh * 0.97
                       while Low[i] > StopLoss and High[i] < Target and i < len(High) - 1 and Length < MaxLength:
                           i += 1
                           Inc += 1
                           Length += 1
                       else:
                           if Low[i] < StopLoss:
                               TradeList.append([ticker, DfIndex[i + Inc], round(Buy, 2), DfIndex[i + Inc + Length], round(StopLoss, 2), round((StopLoss / Buy) - 1, 2)])
                               ProfitList.append((StopLoss / Buy) - 1)
                               Balance = Balance * (StopLoss / Buy)
                           elif High[i] > Target:
                               TradeList.append([ticker, DfIndex[i + Inc], round(Buy, 2), DfIndex[i + Inc + Length], round(Target, 2), round((Target / Buy) - 1, 2)])
                               ProfitList.append((Target / Buy) - 1)
                               Balance = Balance * (Target / Buy)
                           else:
                               TradeList.append([ticker, DfIndex[i + Inc], round(Buy, 2), DfIndex[i + Inc + Length], round(Close[i], 2), round((Close[i] / Buy) - 1, 2)])
                               ProfitList.append((Close[i] / Buy) - 1)
                               Balance = Balance * (Close[i] / Buy)
                   else:
                       Buy = 0
            else:
                pass
        else:
            pass
    return {"Total Trades": len(ProfitList), "Average Return": np.average(ProfitList), "Sum": np.sum(ProfitList), "Balance": Balance, "TradeList": TradeList}