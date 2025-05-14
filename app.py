from flask import Flask


app = Flask(__name__)


@app.route("/blog", methods=["GET"])
def blog():
    return "This is blog page."


if __name__ == "__main__":
    app.run(debug=True)
