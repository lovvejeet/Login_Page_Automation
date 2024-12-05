from driver_setup import setup_driver
from login_test import run_login_test
from academic_tests import run_academic_tests
from network_logs import check_failed_api_calls
from utils.file_operations import initialize_csv

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def main():
    csv_file_path = "Failed_API_Logs.csv"
    initialize_csv(csv_file_path)

    driver = setup_driver()

    try:
        if run_login_test(driver, EMAIL, PASSWORD):
            run_academic_tests(driver)
            check_failed_api_calls(driver, csv_file_path)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()