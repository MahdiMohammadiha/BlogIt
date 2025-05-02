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

    if request.method == "POST":
        url = request.form["url"]
        selector = request.form["selector"]

        success = take_screenshot(url, selector, screenshot_path)
        if success:
            screenshot_exists = True
        else:
            error = "نتوانستم عنصر مورد نظر را پیدا کنم یا مشکلی در ذخیره‌سازی عکس وجود داشت."

    return render_template(
        "index.html",
        screenshot=screenshot_rel_path if screenshot_exists else None,
        error=error,
    )


if __name__ == "__main__":
    os.makedirs("static/temp/screenshots", exist_ok=True)
    app.run(debug=True)
