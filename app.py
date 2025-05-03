from flask import Flask, render_template, request
from screenshot import take_screenshot
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    screenshot_rel_path = "temp/screenshots/screenshot.png"
    screenshot_path = os.path.join("static", screenshot_rel_path)
    screenshot_exists = False
    error = None
    comment = None

    if request.method == "POST":
        url = request.form["url"]
        selector = request.form["selector"]
        index = request.form["index"]

        if not index:
            index = 1

        success, comment = take_screenshot(url, selector, screenshot_path, index)
        if success:
            screenshot_exists = True
        else:
            error = "There was a problem saving the photo."

    return render_template(
        "index.html",
        screenshot=screenshot_rel_path if screenshot_exists else None,
        error=error,
        comment=comment,
    )


if __name__ == "__main__":
    os.makedirs("static/temp/screenshots", exist_ok=True)
    app.run(debug=True)
