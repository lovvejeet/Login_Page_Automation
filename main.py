import json
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Environment variables and constants
login_url = "https://preprod.v-learning.in/login" 
csv_file_path = "Failed_API_Logs.csv"

# Function to write failed API calls to CSV
def write_failed_api_to_csv(url, status_code):
    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), url, status_code])

# Setup WebDriver with performance logging enabled
def setup_driver():
    chromedriver_autoinstaller.install()
    
    # Create Chrome options
    options = Options()
    
    # Enable performance logging
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    
    # Enable performance logs
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    # Use Service to manage the ChromeDriver instance
    service = Service()

    # Create the Chrome driver with options
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Analyze network logs for failed API calls
def check_failed_api_calls(driver):
    print("Checking network logs for failed API calls...")
    logs = driver.get_log("performance")
    failed_apis = []

    for entry in logs:
        log = json.loads(entry["message"])["message"]

        if log["method"] == "Network.responseReceived":
            response = log["params"]["response"]
            url = response.get("url", "")
            status_code = response.get("status", 0)

            # Log failed API calls (HTTP 4xx or 5xx)
            if 400 <= status_code < 600:
                failed_apis.append({"url": url, "status_code": status_code})
                # Write failed API calls to CSV immediately
                write_failed_api_to_csv(url, status_code)

    if failed_apis:
        print("Failed API calls detected:")
        for api in failed_apis:
            print(f"URL: {api['url']}, Status Code: {api['status_code']}")
    else:
        print("No failed API calls detected.")

def run_login_test(driver, username, password):
    try:
        driver.maximize_window()
        driver.get(login_url)
        time.sleep(2)

        username_field = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[1]/div/div/input')
        password_field = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[2]/div/div/input')
        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[3]/div/div/button')
        login_button.click()
        time.sleep(5)

        print("Login Test case - Successful Login: PASSED")
        return True  # Successful login

    except Exception as e:
        print(f"Login Test case - Failed: {str(e)}")
        return False

# Academic Test Function
def run_academic_tests(driver):
    try:
        # Navigate to Academic section
        academic = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div[3]/div/a[2]'))
        )
        academic.click()
        print("Clicked on Academic")

        # Select a subject and a chapter
        academic_subject = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]'))
        )
        academic_subject.click()
        print("Clicked on Academic Subject")

        academic_subject_chapter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'chapter-rows'))
        )
        academic_subject_chapter.click()
        print("Clicked on Academic Subject Chapter")

        # Wait for iframe and switch context [video player]
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[name^='vdoFrame']"))
        )
        driver.switch_to.frame(iframe)
        print("Switched to video iframe.")

        # Wait for the video element to be ready
        video_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        print("Video player located.")

        # Wait until the video duration is available and valid
        for _ in range(10):  # Retry up to 10 times
            video_duration = driver.execute_script(
                """
                let video = document.querySelector('video');
                if (video && video.duration > 0) {
                    return video.duration;
                }
                return null;
                """
            )
            if video_duration:
                break
            print("Waiting for valid video duration...")
            time.sleep(1)

        if video_duration and isinstance(video_duration, (int, float)):
            print(f"Video duration: {video_duration:.2f} seconds")
        else:
            print("Failed to retrieve valid video duration.")
            return False

        # Play the video
        driver.execute_script("document.querySelector('video').play();")
        print("Started playing the video.")

        # Wait for a few seconds to ensure playback
        time.sleep(5)

        # Forward the video by 10 seconds
        driver.execute_script(
            """
            let video = document.querySelector('video');
            if (video) {
                video.currentTime = Math.min(video.currentTime + 10, video.duration);
            }
            """
        )
        print("Forwarded the video by 10 seconds.")
        time.sleep(5)

        # Verify if the video is still playing
        is_playing = driver.execute_script(
            """
            let video = document.querySelector('video');
            return video && !video.paused && !video.ended && video.readyState > 2;
            """
        )
        if is_playing:
            print("Video is confirmed to be playing.")
        else:
            print("Video is not playing.")

        # Switch back to the main content
        driver.switch_to.default_content()
        print("Switched back to main content.")

        return True

    except Exception as e:
        print(f"Academic Tests FAILED: {str(e)}")
        return False


# Main function
def main():
    # Create or write CSV header 
    if not os.path.exists(csv_file_path):  # Check if the file exists
        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Timestamp", "URL", "Status Code"])  # Write header row

    driver = setup_driver()

    try:
        if run_login_test(driver, "ksk10@v-learning.in", "Dream@$1224$"):
            run_academic_tests(driver)
            check_failed_api_calls(driver) 

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
