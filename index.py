#pip install yfinance

import yfinance as yf

# 輸入你想查詢的股票代碼，台股代碼後面需要加上 ".TW"
stock_code = '2330.TW'  # 這裡以台積電為例

# 下載股票資料
stock_data = yf.Ticker(stock_code)

# 取得最近的股價資訊
hist = stock_data.history(period="5d")

# 顯示結果
print(hist)

print(hist['Open'].iloc[0])
print(hist['Open'].iloc[1])
print(hist['Open'].iloc[2])
print(hist['Open'].iloc[3])
print(hist['Open'].iloc[4])