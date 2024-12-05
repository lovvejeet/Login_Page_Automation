


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def wait_for_element(driver, by, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

def run_pdf_tests(driver):
    try:
        # Click the academic subject chapter pdf
        academic_pdf_chapter = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "el-button") and contains(., "View PDF")]'))
        )
        academic_pdf_chapter.click()
        print("Clicked on 'View PDF' button")
        time.sleep(5)

        # Click the academic subject chapter pdf close button
        academic_pdf_chapter_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div/div[6]/div/div[1]/button/i'))
        )
        academic_pdf_chapter_close.click()
        print("Closed Academic PDF Chapter")
        time.sleep(5)

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Academic quiz Tests: FAILED")

