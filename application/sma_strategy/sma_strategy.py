import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from domain import OKXMarketAPI

class SMACrossStrategy:
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
        self.position = 0.0
        self.balance = 100000  # 初始资金
        self.position_log = []

    def get_historical_data(self):
        okx_market_client = OKXMarketAPI()

        start_time = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_ts = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
        end_ts = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))) * 1000

        try:
            resp = okx_market_client.get_history_candlesticks(inst_id="ETH-USDT", before=str(start_ts), after=str(end_ts), bar="1D", limit="100")
            if not resp["code"] == '0':
                raise ValueError(f"API 请求失败: {resp['msg']}")
            
            data = resp["data"]
        except Exception as e:
            print("获取数据时发生错误:", str(e))
            return []
        
        # 将数据转换为 DataFrame
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "volCcy", "volCcyQuote", "confirm"])
    
        # 转换时间戳为可读格式并设置索引
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("datetime", inplace=True)
    
        return df

    def calculate_indicators(self, df):
        """计算短期和长期均线"""
        df['sma_short'] = df['close'].rolling(window=self.short_window, min_periods=1).mean()
        df['sma_long'] = df['close'].rolling(window=self.long_window, min_periods=1).mean()
        return df

    def generate_signal(self, indicators, current_price):
        if indicators["sma_short"] > indicators["sma_long"]:
            return "buy"
        elif indicators["sma_short"] < indicators["sma Long"]:
            return "sell"
        else:
            return None

#     def execute_trade(self, signal, price):
#         fee = 0.001
#         if signal == "buy":
#             max_buy = self.balance * (1 - fee) / price
#             self.position += max_buy
#             self.balance -= max_buy * price * (1 + fee)
#         elif signal == "sell":
#             proceeds = self.position * price * (1 - fee)
#             self.balance += proceeds
#             self.position = 0.0

#     def update_position(self, current_price):
#         return self.position * current_price + self.balance

def back_test():
    sma_strategy = SMACrossStrategy()
    df = sma_strategy.get_historical_data()
    new_df = sma_strategy.calculate_indicators(df)
    buy_signals = []
    sell_signals = []
    fee_rate = 0.0005

    for i in range(1, len(new_df)):
        current_row = df.iloc[i]
        previous_row = df.iloc[i-1]
        
        # 计算信号（基于上一日的均线位置）
        if (previous_row['sma_short'] > previous_row['sma_long']) and \
           (sma_strategy.position == 0):
            # 均线上穿时买入
            buy_price = float(current_row['close'])
            sma_strategy.position = sma_strategy.balance // buy_price
            cost = buy_price * sma_strategy.position * (1 + fee_rate)
            sma_strategy.position_log.append( ('buy', current_row.name, buy_price, sma_strategy.position) )
            sma_strategy.balance -= cost
            buy_signals.append(i)
        
        elif (previous_row['sma_short'] < previous_row['sma_long']) and \
             (sma_strategy.position > 0):
            # 均线下穿时卖出
            sell_price = float(current_row['close'])
            proceeds = sell_price * sma_strategy.position * (1 - fee_rate)
            sma_strategy.position_log.append( ('sell', current_row.name, sell_price, sma_strategy.position) )
            sma_strategy.balance += proceeds
            sma_strategy.position = 0
            sell_signals.append(i)
 
        # 记录持仓价值（每天更新）
        df.loc[current_row.name, 'equity'] = sma_strategy.balance + float(current_row['close'])*sma_strategy.position
 
    # 补全最后一天的收益计算
    if sma_strategy.position > 0:
        final_value = float(df.iloc[-1]['close']) * sma_strategy.position
        df['equity'].iloc[-1] = sma_strategy.balance + final_value

    print(sma_strategy.position_log)
        
    return df, buy_signals, sell_signals
