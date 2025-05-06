import json
import os
from screenshot import take_screenshot

JOBS_FILE = "jobs.json"

with open(JOBS_FILE, "r", encoding="utf-8") as f:
    jobs = json.load(f)

for i, job in enumerate(jobs, 1):
    url = job.get("url")
    selector = job.get("selector")
    output_paths = job.get("output_paths", ["static/temp/screenshots/unnamed.png"])
    indexes = job.get("indexes", [1])
    login_required = job.get("login_required", False)

    if not all([url, selector, output_paths]):
        print(f"❌ Job #{i}: Invalid job definition.")
        continue

    print(f"🔍 Job #{i}: Taking screenshot from {url} ...")
    result = take_screenshot(
        url,
        selector,
        output_paths=output_paths,
        indexes=indexes,
        login_required=login_required,
    )

    for success, message in result:
        status = "✅ Success" if success else "❌ Failed"
        print(f"{status}: {message}")
    print("\n")
