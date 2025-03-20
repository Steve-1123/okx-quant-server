import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class OKXConfig:
    SECRET_KEY = os.getenv('OKX_SECRET_KEY', 'default-secret-key')
    API_KEY = os.getenv('OKX_API_KEY')
    PASSPHRASE = os.getenv('OKX_PASSPHRASE')
    FLAG=os.getenv('OKX_SIMULATED_FLAG')