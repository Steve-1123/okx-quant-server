from flask import Flask, jsonify
from application.sma_strategy.sma_strategy import back_test

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Quant Trading System"})

@app.route('/test')
def test():
    result, buy_log, sell_log = back_test()
    print(result)
    print(buy_log)
    print(sell_log)
    return {}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
