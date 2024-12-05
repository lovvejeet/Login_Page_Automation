import time
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from quiz import run_quiz_tests
from pdf import run_pdf_tests

def log_with_timestamp(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

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

        # Wait to observe changes
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
        time.sleep(5)
        
        run_pdf_tests(driver)

        time.sleep(5)

        run_quiz_tests(driver)

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
    
    except Exception as e:
        print(f"Error: {str(e)}")
        result = "FAILED"
        print(f"Academic Tests: {result}")
