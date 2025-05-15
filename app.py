from flask import Flask, redirect, url_for, render_template
from jdatetime import date
from report_exporter import livetse_market_report


app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("blog"))


@app.route("/blog")
def blog():
    livetse_market_report()

    today = date.today()
    jalali_date = today.strftime("%d %B %Y")

    return render_template("blog.html", jalali_date=jalali_date)


if __name__ == "__main__":
    app.run(debug=True)
