import json
from utils.file_operations import write_failed_api_to_csv

def check_failed_api_calls(driver, csv_file_path):
    print("Checking network logs for failed API calls...")
    logs = driver.get_log("performance")
    for entry in logs:
        log = json.loads(entry["message"])["message"]

        if log["method"] == "Network.responseReceived":
            response = log["params"]["response"]
            url = response.get("url", "")
            status_code = response.get("status", 0)

            if 400 <= status_code < 600:
                write_failed_api_to_csv(csv_file_path, url, status_code)
                print(f"Failed API: URL={url}, Status Code={status_code}")
