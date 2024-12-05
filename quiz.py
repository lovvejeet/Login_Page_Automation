from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def wait_for_element(driver, by, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

def run_quiz_tests(driver):
    try:
        # Wait for the quiz to start and click the "Take Quiz" button
        quiz_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "el-button") and contains(., "Take Quiz")]'))
        )
        driver.execute_script("arguments[0].click();", quiz_button)
        print("Clicked 'Take Quiz' button")
        time.sleep(2)

        # Scroll to the bottom of the page to make the "Next" button visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Wait for quiz to load and get the total number of questions
        question_progress = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "question-progress"))
        )

        # Count the number of questions (circle-buttons)
        question_buttons = question_progress.find_elements(By.CLASS_NAME, "circle-button")
        total_questions = len(question_buttons)
        print(f"Total number of questions: {total_questions}")

        # Loop through each question
        for i in range(total_questions):
            print(f"Processing question {i + 1} of {total_questions}")

            # Wait for the question card to load
            question_card = wait_for_element(driver, By.CLASS_NAME, "el-carousel__item.is-active")

            # Handle selecting an option from the radio group
            radio_group = question_card.find_element(By.CLASS_NAME, "el-radio-group.options")
            radio_buttons = radio_group.find_elements(By.XPATH, './label[@role="radio"]')

            # Example: Select the first unselected radio button
            for radio_button in radio_buttons:
                if not radio_button.get_attribute("aria-checked") == "true":  # if not already checked
                    radio_button.click()
                    print(f"Selected a radio button for question {i + 1}")
                    break

            time.sleep(2)

            # Now click the "Next" or "Submit" button based on the last question
            try:
                if i + 1 == total_questions:  # If it's the last question, click Submit
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "el-button") and contains(., "Submit")]'))
                    )
                    submit_button.click()
                    print("Submitted the quiz")
                else:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "el-button") and contains(., "Next")]'))
                    )
                    next_button.click()
                    print(f"Navigated to question {i + 2} of {total_questions}")

                    # Wait for the next question to load before interacting
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "el-carousel__item.is-active"))
                    )
                    print(f"Next question {i + 2} loaded")

                time.sleep(2)  # Wait for the next question to settle

            except Exception as e:
                print(f"Error navigating to question {i + 1}: {str(e)}")
                break  # Exit the loop on error

        # Close the quiz or perform further actions if needed
        time.sleep(5)
        academic_chapter_quiz_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/span'))
        )
        academic_chapter_quiz_close.click()
        print("Closed Academic Chapter Quiz")
        time.sleep(2)

    except Exception as e:
        print(f"Error: {str(e)}")
        result = "FAILED"
        print(f"Academic Tests: {result}")
