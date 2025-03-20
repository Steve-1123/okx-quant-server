from flask import Flask, jsonify
from domain import OKXAccountAPI

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Quant Trading System"})

@app.route('/instruments/<inst_type>')
def instruments(inst_type: str):
    okx_account_api = OKXAccountAPI()
    return okx_account_api.instruments(inst_type=inst_type)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
