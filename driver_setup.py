import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_driver():
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver
