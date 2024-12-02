from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import chromedriver_autoinstaller
import csv
import os
import time

load_dotenv()

# Access environment variables
login_url = os.getenv("LOGIN_URL", "https://preprod.v-learning.in/login")
csv_file_path = os.getenv("CSV_FILE_PATH", "Login_Automation_Sheet1.csv")

# Ensure the CSV header is written only once
def write_header():
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Time", "Date", "Username", "Password", "Test Scenario", "Result"])

# Write test results to CSV file
def write_to_csv(username, password, test_case, result):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    datestamp = time.strftime("%Y-%m-%d", time.localtime())

    write_header()  # Ensure header is written only once

    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([timestamp, datestamp, username, password, test_case, result])

# Run login tests
def run_login_test(driver, username, password, test_case):
    try:
        driver.maximize_window()
        driver.get("https://preprod.v-learning.in/login")
        time.sleep(2)
        
        username_field = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[1]/div/div/input')
        password_field = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[2]/div/div/input')
        username_field.send_keys(username)
        time.sleep(2)
        password_field.send_keys(password)
        time.sleep(2)

        login_button = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div[3]/div/div[1]/form/div[3]/div/div/button')
        login_button.click()
        time.sleep(5)

        result = "PASSED"
        print(f"Login Test case - {test_case}: {result}")
        write_to_csv(username, password, test_case, result)

        return True  # Successful login

    except Exception as e:
        print(f"Login Test case - {test_case}: FAILED")
        print(f"Error: {str(e)}")
        write_to_csv(username, password, test_case, "FAILED")
        return False

# Run Academic tests after successful login
def run_academic_tests(driver):
    try:
         # Click the academic
        academic = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div[3]/div/a[2]'))
        )
        academic.click()
        print("Clicked on Academic")
        time.sleep(5)

        # Wait until the subjects list is visible
        subjects_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "subjects-list"))
        )

        # Find all subjects under the 'subjects-list' class
        subject_items = subjects_list.find_elements(By.XPATH, './*')  # This will return child elements
        
        # Print the number of subjects found
        print(f"Number of Academic subjects found: {len(subject_items)}")
        
        # Click on the first subject (adjust the index or XPath for other subjects if needed)
        academic_subject = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]'))
        )
        academic_subject.click()
        print("Clicked on Academic subject")
        
        # Wait for the chapter list to be visible after clicking the subject
        chapter_list_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "chapter-list-area"))
        )
        
        # Find all chapter elements within the chapter-list-area (adjust the XPath if needed)
        chapters = chapter_list_area.find_elements(By.XPATH, './*')  # This will return child elements
        
        # Print the number of chapters found
        print(f"Number of chapters found: {len(chapters)}")
        
        # print the name of each chapter (if it has a name inside a specific tag, e.g., <div class="chapter-name">)
        # for chapter in chapters:
        #     chapter_name = chapter.text  # Extract the chapter name
        #     print(f"Chapter: {chapter_name}")

        # Click the academic subject chapter 
        academic_subject_chapter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'chapter-rows'))
        )
        academic_subject_chapter.click()
        print("Clicked on Academic Subject Chapter")

        # Wait for iframe and switch context
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[name^='vdoFrame']"))
        )
        driver.switch_to.frame(iframe)
        print("Switched to video iframe.")

        # Wait until the video is playing
        max_wait_time = 30  # Maximum time to wait for the video to start playing
        wait_interval = 2   # Interval between checks
        is_playing = False
        elapsed_time = 0

        while elapsed_time < max_wait_time:
            is_playing = driver.execute_script(
                """
                let video = document.querySelector('video');
                return video && !video.paused && !video.ended && video.readyState > 2;
                """
            )
            if is_playing:
                print("Video is playing.")
                break
            time.sleep(wait_interval)
            elapsed_time += wait_interval
            print("Waiting for video to start playing...")

        if not is_playing:
            print("Video did not start playing within the allotted time.")

        # Switch back to the main content
        driver.switch_to.default_content()
        print("Switched back to main content.")

        return is_playing

        # Click the academic subject chapter pdf
        academic_pdf_chapter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/button[3]'))
        )
        academic_pdf_chapter.click()
        print("Clicked on Academic Subject PDF Chapter")
        time.sleep(5)

        # Click the academic subject chapter pdf close button
        academic_pdf_chapter_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div/div[6]/div/div[1]/button/i'))
        )
        academic_pdf_chapter_close.click()
        print("Closed Academic PDF Chapter")
        time.sleep(5)

        # Click the academic subject chapter quiz
        academic_chapter_quiz = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/button[2]'))
        )
        academic_chapter_quiz.click()
        print("Clicked on Academic Subject Chapter Quiz")
        time.sleep(5)
        
        # Click the academic subject chapter quiz close button
        academic_chapter_quiz_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/span'))
        )
        academic_chapter_quiz_close.click()
        print("Closed Academic Chapter Quiz")
        time.sleep(5)

        # Click the academic subject back chapter 
        academic_back_chapter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/span'))
        )
        academic_back_chapter.click()
        print("Clicked on Academic Back Chapter")
        time.sleep(5)

        # Click the academic back button
        academic_back = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/span'))
        )
        academic_back.click()
        print("Clicked on Academic Back Button")
        time.sleep(5)


        result = "PASSED"
        print(f"Academic Tests: {result}")
        write_to_csv("N/A", "N/A", "Academic Tests", result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        write_to_csv("N/A", "N/A", "Academic Tests", "FAILED")

# Run Building Legends tests after successful login


# Main function to run all tests
def main():
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    try:
        # Login tests
        # run_login_test(driver, "ksk@v-learning.in", "Dream@$2023$", "Incorrect Username")
        # run_login_test(driver, "ksk10@v-learning.in", "Dream@$2023", "Incorrect Password")
        # run_login_test(driver, "ksk", "Dream", "Invalid Credentials")
        if run_login_test(driver, "ksk10@v-learning.in", "Vista@$1024$", "Successful Login"):
            # Run tests if login is successful
            run_academic_tests(driver)
            # Run Building Legends tests
            # run_building_legends_tests(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
