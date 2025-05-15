from flask import Flask, redirect, url_for, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("blog"))


@app.route("/blog")
def blog():
    return render_template("blog.html")


if __name__ == "__main__":
    app.run(debug=True)
