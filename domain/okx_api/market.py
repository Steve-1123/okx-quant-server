import okx.MarketData as MarketData
from utils import OKXConfig

class OKXMarketAPI:
    def __init__(self):
        flag = OKXConfig.FLAG
        self._okx_market_api = MarketData.MarketAPI(flag=flag)
    
    def get_ticker(self, inst_id: str):
        return self._okx_market_api.get_ticker(instId=inst_id)
    
    def get_history_candlesticks(self, inst_id, before, after, bar, limit: str):
        return self._okx_market_api.get_history_candlesticks(instId=inst_id, before=before, after=after, bar=bar, limit=limit)
