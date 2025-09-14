from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return f"Hello DevOps World! Current time is {datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}"


@app.route('/health')
def health():
    return {"status": "OK"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
