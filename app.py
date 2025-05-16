from flask import Flask, redirect, url_for, render_template
from jdatetime import date
from report_exporter import livetse_market_report
import json


app = Flask(__name__)


def load_config(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    return redirect(url_for("blog"))


@app.route("/blog")
def blog():
    livetse_market_report()

    blog_media_path = load_config("blog_media_path.json")

    today = date.today()
    jalali_date = today.strftime("%d %B %Y")

    return render_template("blog.html", jalali_date=jalali_date, **blog_media_path)


if __name__ == "__main__":
    app.run(debug=True)
