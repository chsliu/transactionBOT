#pip install yfinance

import yfinance as yf
import pandas as pd

global state
global data

state = False

total_selection = 3

def enableSelection(total_selection, weekno):

  global state
  global data
  
  state = True

  #每週須建立新的dict，或將舊的dict儲存檔案
  data = {}
  
  return "現在開始競賽！"

def disableSelection(weekno):
  state = False
  return "競賽結束！"

def selectStock(weekno, line_id, stock_symbol):
  global data
  global state
  stock_symbol = int(stock_symbol)
  line_id = str(line_id)

  if state == False:
    return "競賽尚未開始！"
  elif line_id == "無效":
    return "LineID無效！"
  
  stock_code = str(stock_symbol)+".TW"  #這裡以台積電為例
  stock_data = yf.Ticker(stock_code)  #下載股票資料
  hist = stock_data.history(period="5d")  #取得最近的股價資訊
  if hist.empty:
    return "股票代碼錯誤！"
  elif line_id not in data:
    data[line_id] = [stock_symbol]  #新增第一筆股票代碼(value)到line_id(key)
    return line_id+"成功新增股票"+str(stock_symbol)+"！"
  elif stock_symbol in data[line_id]:
    return line_id+"已經有股票"+str(stock_symbol)+"了！"
  elif len(data[line_id]) >= total_selection:
    remove_stockSymbol = data[line_id].pop(0)
    data[line_id].append(stock_symbol)
    return line_id+"的股票"+str(remove_stockSymbol)+"已被移除，並成功新增股票"+str(stock_symbol)+"了！"
  else:
    data[line_id].append(stock_symbol)  #新增一筆股票代碼(value)到line_id(key)
    return line_id+"成功新增股票"+str(stock_symbol)+"！"

def printSelection(weekno, line_id):
  global data
  line_id = str(line_id)

  message = "目前"+line_id+"競賽的股票為："
  
  if line_id not in data:
    return line_id+"還沒競賽過！"
  else:
    for i in range(0,len(data[line_id])):
      message += str(data[line_id][i])
      if i < len(data[line_id])-1:
        message += ","
    return message

def rank_stocks(data):
  all_stocks = []
  for player, stocks in data.items():
    all_stocks.extend(stocks)
  print(all_stocks)

  stock_performance = {}
  for stock in all_stocks:
    stock_code = str(stock) + ".TW"
    stock_data = yf.Ticker(stock_code)
    hist = stock_data.history(period="5d")
    if not hist.empty:
      growthRate = (hist['Close'].iloc[4]-hist['Open'].iloc[0])/hist['Open'].iloc[0]
      stock_performance[stock] = growthRate
  print(stock_performance)

  ranked_stocks = sorted(stock_performance, key=stock_performance.get, reverse=True)
  ranked_performance = sorted(stock_performance.values(), reverse=True)

  return ranked_stocks, ranked_performance

def selectWinningStock(weekno, num_winners):
  global data
  global state

  if state == False:
    return "競賽尚未開始！"

  ranked_stocks,ranked_performance = rank_stocks(data)
  winning_stocks = ranked_stocks[:num_winners]

  message = ""

  for i in range(0,len(winning_stocks)):
    message += "第"+str(i+1)+"名為："
    value_to_find = winning_stocks[i]
    for key in data.items():
      for values in key:
        if isinstance(values, list) == True:
          for stock in values:
            if stock == value_to_find:
              message += str(key[0])+"、"
    message = message[:-1]
    message += "的"+str(winning_stocks[i])+"（成長率為"+str(round(ranked_performance[i]*100,2))+"%）"
    message += "\n"
  return message