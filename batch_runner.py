import json
import os
from screenshot import take_screenshot


JOBS_FILE = "jobs.json"


if not os.path.exists(JOBS_FILE):
    print(f"❌ Error: Jobs file '{JOBS_FILE}' not found.")
    exit(1)

with open(JOBS_FILE, "r", encoding="utf-8") as f:
    try:
        jobs = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Error: Jobs file '{JOBS_FILE}' is not a valid JSON file.")
        exit(1)

success_count = 0
failure_count = 0

for i, job in enumerate(jobs, 1):
    url = job.get("url")
    selector = job.get("selector")
    output_paths = job.get("output_paths", ["static/temp/screenshots/unnamed.png"])
    indexes = job.get("indexes", [1])
    login_required = job.get("login_required", False)
    scroll_into_view = job.get("scroll_into_view", False)
    pre_actions = job.get("pre_actions", [])

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
        scroll_into_view=scroll_into_view,
        pre_actions=pre_actions
    )

    for success, message in result:
        status = "✅ Success" if success else "❌ Failed"
        print(f"{status}: {message}")
        if success:
            success_count += 1
        else:
            failure_count += 1
    print("\n")

print(f"✅ Total Success: {success_count}")
print(f"❌ Total Failures: {failure_count}")
