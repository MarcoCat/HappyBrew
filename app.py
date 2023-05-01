import json

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    with open("menu.json") as f:
        menu = json.load(f)
    return render_template("index.html", menu=menu)


if __name__ == "__main__":
    app.run()
