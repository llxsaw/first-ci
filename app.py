from flask import Flask, render_template, request, jsonify
import json
import random
from datetime import datetime
import os

app = Flask(__name__)

QUOTES_FILE = 'quotes.json'


def load_quotes():
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, 'r', encoding="utf-8") as f:
            return json.load(f)
    return []


def save_quotes(quotes):
    with open(QUOTES_FILE, 'w', encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)


@app.route('/')
def home():
    quotes = load_quotes()
    if quotes:
        random_quote = random.choice(quotes)
    else:
        random_quote = {"text": "Пока нет цитат! Добавьте первую!", "author": "Система"}
    return render_template("index.html",
                           quote=random_quote,
                           time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), )


@app.route('/all')
def all_quotes():
    quotes = load_quotes()
    return render_template("all_quotes.html", quotes=quotes)


@app.route('/add', methods=['GET','POST'])
def add_quote():
    if request.method == 'POST':
        quote_text = request.form.get('text')
        author = request.form.get('author')

        if quote_text and author:
            new_quote = {
                "text": quote_text,
                "author": author,
                "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            quotes = load_quotes()
            quotes.append(new_quote)
            save_quotes(quotes)

            return render_template("add_quote.html",
                                   success=True,
                                   message="Цитата добавлена успешно",)

    return render_template("add_quote.html", success=False)


@app.route('/api/quote', methods=['GET'])
def api_random_quote():
    quotes = load_quotes()
    if quotes:
        return jsonify(random.choice(quotes))
    return jsonify({"text": "No Quotes Available", "author": "System"})


@app.route('/api/quote', methods=['POST'])
def api_add_quote():
    if request.is_json:
        data = request.get_json()
        quote_text = data.get('text')
        quote_author = data.get('author')
    else:
        quote_text = request.form.get('text')
        quote_author = request.form.get('author')

    if quote_text and quote_author:
        new_quote = {
            "text": quote_text,
            "author": quote_author,
            "date_added": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        quotes = load_quotes()
        quotes.append(new_quote)
        save_quotes(quotes)

        return jsonify({"status": "success", "message": "Quote added"})

    return jsonify({"status": "error", "message": "Missing text or author"}), 400


@app.route('/health')
def health():
    return {"status": "OK", "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
