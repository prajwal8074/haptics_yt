import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import random

# --- Configuration ---
USER_PROFILE_PATH = "/home/prajwal/haptics_yt/chromium"
USER_PROFILE = "Profile 4"

# --- Main Script ---
chrome_options = Options()
# Profile configuration
chrome_options.add_argument(f"user-data-dir={USER_PROFILE_PATH}")
chrome_options.add_argument(f"profile-directory={USER_PROFILE}")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
        service=Service(executable_path="/home/prajwal/chromedriver-linux64/chromedriver"),
        options=chrome_options
    )

try:
    # 1. Navigate to YouTube
    driver.get("https://studio.youtube.com/channel/UCWyx3tAp-yDk6VmX8Ak4Z6Q/videos/short?filter=%5B%7B%22name%22%3A%22VISIBILITY%22%2C%22value%22%3A%5B%22PUBLIC%22%5D%7D%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D") # Corrected URL

    driver.execute_script("window.open('https://www.tiktok.com/tiktokstudio/content');")

    WebDriverWait(driver, 3600).until(EC.number_of_windows_to_be(0))

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()