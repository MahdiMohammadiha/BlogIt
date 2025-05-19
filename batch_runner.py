import json
import os
from screenshot import take_screenshot
from image_tools import merge_images_with_gap


SCREENSHOT_JOBS_FILE = "screenshot_jobs.json"
IMAGE_JOBS_FILE = "image_jobs.json"


def run_screenshot_jobs():
    if not os.path.exists(SCREENSHOT_JOBS_FILE):
        print(f"No screenshot jobs found.")
        return 0, 0

    try:
        with open(SCREENSHOT_JOBS_FILE, "r", encoding="utf-8") as f:
            jobs = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: '{SCREENSHOT_JOBS_FILE}' is not a valid JSON file.")
        return 0, 0

    success_count = 0
    failure_count = 0

    for i, job in enumerate(jobs, 1):
        url = job.get("url")
        selector = job.get("selector")
        indexes = job.get("indexes", [1])
        output_paths = job.get("output_paths", ["static/temp/screenshots/unnamed.png"])
        delay = job.get("delay", 1)
        login_required = job.get("login_required", False)
        scroll_into_view = job.get("scroll_into_view", False)
        pre_actions = job.get("pre_actions", [])

        if not all([url, selector, output_paths]):
            print(f"Screenshot Job #{i}: Invalid job definition.")
            continue

        print(f"Screenshot Job #{i}: Taking screenshot from {url} ...")
        result = take_screenshot(
            url,
            selector,
            indexes=indexes,
            output_paths=output_paths,
            delay=delay,
            login_required=login_required,
            scroll_into_view=scroll_into_view,
            pre_actions=pre_actions,
        )

        for success, message in result:
            status = "Success" if success else "Failed"
            print(f"{status}: {message}")
            if success:
                success_count += 1
            else:
                failure_count += 1

        print()

    return success_count, failure_count


def run_image_jobs():
    if not os.path.exists(IMAGE_JOBS_FILE):
        print(f"No image merge jobs found.")
        return 0, 0

    try:
        with open(IMAGE_JOBS_FILE, "r", encoding="utf-8") as f:
            jobs = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: '{IMAGE_JOBS_FILE}' is not a valid JSON file.")
        return 0, 0

    success_count = 0
    failure_count = 0

    for i, job in enumerate(jobs, 1):
        try:
            merge_images_with_gap(
                img1_path=job["img1_path"],
                img2_path=job["img2_path"],
                direction=job["direction"],
                gap_size=job["gap_size"],
                gap_color=job["gap_color"],
                output_path=job["output_path"],
            )
            print(f"Image Merge Job #{i}: Saved to {job['output_path']}")
            success_count += 1
        except Exception as e:
            print(f"Image Merge Job #{i} failed: {type(e).__name__}: {e}")
            failure_count += 1

    return success_count, failure_count


def main():
    print("Running Screenshot Jobs...")
    s_success, s_failure = run_screenshot_jobs()

    print("Running Image Merge Jobs...")
    i_success, i_failure = run_image_jobs()

    total_success = s_success + i_success
    total_failure = s_failure + i_failure

    print("\nSummary:")
    print(f"\tTotal Success: {total_success}")
    print(f"\tTotal Failures: {total_failure}")


if __name__ == "__main__":
    main()
