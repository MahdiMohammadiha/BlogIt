from flask import Flask, render_template, render_template_string
from report_exporter import main as report_exporter_main
from batch_runner import main as batch_runner_main
from tools.utils import JalaliDate
from tools.filekit import is_file_empty, load_config


app = Flask(__name__)


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
    report_exporter_main()
    batch_runner_main()

    pretty_jdate = str(JalaliDate().pretty())
    iso_jdate = str(JalaliDate().iso())

    golden_notification = not is_file_empty(
        f"templates/reports/{iso_jdate}/livetse_golden_notification_report.html"
    )

    blog_media_path = load_config("blog_media_path.json")
    tsetmc_index_report = load_config(
        f"templates/reports/{iso_jdate}/tsetmc_index_report.json"
    )

    return render_template(
        "blog.min.html",
        iso_jdate=iso_jdate,
        pretty_jdate=pretty_jdate,
        golden_notification=golden_notification,
        tsetmc_index_report=tsetmc_index_report,
        **blog_media_path,
    )


if __name__ == "__main__":
    app.run(debug=True)
