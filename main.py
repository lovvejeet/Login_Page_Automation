from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import csv
import os
import time

csv_file_path = "Login_Automation_Sheet1.csv"
file_exists = os.path.exists(csv_file_path)

def write_header():
    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Time", "Date", "Username", "Password", "Test Scenario", "Result"])

def write_header():
    # Check if the file already exists
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Time", "Date", "Username", "Password", "Test Scenario", "Result"])

def write_to_csv(username, password, test_case, result):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    datestamp = time.strftime("%Y-%m-%d", time.localtime())

    write_header()  # Ensure the header is written only once

    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([timestamp, datestamp, username, password, test_case, result])

def run_test(driver, username, password, test_case):
    try:
        driver.maximize_window()
        driver.get("https://student.vistaslearning.com/login")
        time.sleep(2)
        username_field = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[1]/div/div/input')
        password_field = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[2]/div/div/input')

        username_field.send_keys(username)
        time.sleep(2)
        password_field.send_keys(password)
        time.sleep(2)

        login_button = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[3]/div/div/button')
        login_button.click()

        time.sleep(2)

        result = "PASSED"

        print(f"Test case - {test_case}: {result}")
        write_to_csv(username, password, test_case, result)

    except Exception as e:
        print(f"Test case - {test_case}: FAILED")
        print(f"Error: {str(e)}")

def main():
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    try:
        # Test scenarios
        run_test(driver, "ksk@v-learning.in", "Dream@$2023$", "Incorrect Username")
        run_test(driver, "ksk@v-learning.in", "Dream@$2023", "Incorrect Password")
        run_test(driver, "ksk", "Dream", "Invalid Credentials")
        run_test(driver, "ksk10@v-learning.in", "Dream@$2023$", "Successful Login")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
