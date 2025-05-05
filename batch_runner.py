import json
import os
from screenshot import take_screenshot

JOBS_FILE = "jobs.json"

with open(JOBS_FILE, "r", encoding="utf-8") as f:
    jobs = json.load(f)

for i, job in enumerate(jobs, 1):
    url = job.get("url")
    selector = job.get("selector")
    output_path = job.get("output_path")
    index = job.get("index", 1)
    login_required = job.get("login_required", False)

    if not all([url, selector, output_path]):
        print(f"❌ Job #{i}: Invalid job definition.")
        continue

    print(f"🔍 Job #{i}: Taking screenshot from {url} ...")
    success, comment = take_screenshot(url, selector, output_path, index=index, login_required=login_required)
    print(f"{'✅' if success else '❌'} {comment}\n")
