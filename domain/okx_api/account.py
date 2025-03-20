import okx.Account as Account
from utils import OKXConfig

class OKXAccountAPI:
    def __init__(self):
        flag = OKXConfig.FLAG
        self._okx_account_api = Account.AccountAPI(api_key=OKXConfig.API_KEY, api_secret_key=OKXConfig.SECRET_KEY, passphrase=OKXConfig.PASSPHRASE, flag=flag)
    
    def instruments(self, inst_type: str):
        return self._okx_account_api.get_instruments(instType=inst_type)