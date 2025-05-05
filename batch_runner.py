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
    indexes = job.get("indexes")
    login_required = job.get("login_required")

    if not all([url, selector, output_path]):
        print(f"❌ Job #{i}: Invalid job definition.")
        continue

    print(f"🔍 Job #{i}: Taking screenshot from {url} ...")
    result = take_screenshot(url, selector, output_path, indexes, login_required)
    print(f"{result}\n")
