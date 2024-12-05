import time
import os
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
LOGIN_URL = os.getenv("LOGIN_URL")


login_url = LOGIN_URL

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
        return True

    except Exception as e:
        print(f"Login Test case - Failed: {str(e)}")
        return False
