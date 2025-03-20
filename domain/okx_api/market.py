import okx.MarketData as MarketData
from utils import OKXConfig

class OKXMarketAPI:
    def __init__(self):
        flag = OKXConfig.FLAG
        self._okx_market_api = MarketData.MarketAPI(flag=flag)
    
    def get_ticker(self, inst_id: str):
        return self._okx_market_api.get_ticker(instId=inst_id)

