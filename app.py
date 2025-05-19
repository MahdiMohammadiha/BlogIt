from flask import Flask, redirect, url_for, render_template, render_template_string
from jdatetime import date
from report_exporter import (
    livetse_market_report,
    livetse_golden_notification_report,
    is_file_empty,
)
from batch_runner import main
import json


app = Flask(__name__)


def load_config(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    html = """
        <form action="{{ url_for('blog') }}">
            <button type="submit">Blog</button>
        </form>
    """
    return render_template_string(html)


@app.route("/blog")
def blog():
    livetse_market_report()
    livetse_golden_notification_report()
    main()

    gold_notification = not is_file_empty("templates/golden_notification_report.html")

    blog_media_path = load_config("blog_media_path.json")

    today = date.today()
    jalali_date = today.strftime("%d %B %Y")

    return render_template(
        "blog.html",
        jalali_date=jalali_date,
        gold_notification=gold_notification,
        **blog_media_path
    )


if __name__ == "__main__":
    app.run(debug=True)
