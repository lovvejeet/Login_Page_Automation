from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC     

def run_quiz_tests(driver):
    try:
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


    except Exception as e:
        print(f"Error: {str(e)}")
        result = "FAILED"
        print(f"Academic Tests: {result}")      