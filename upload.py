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
import subprocess

def get_random_file_path(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: The provided path '{folder_path}' is not a valid directory.")
        return None

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        print(f"The folder '{folder_path}' is empty or contains no files.")
        return None

    random_file_name = random.choice(files)
    return os.path.join(folder_path, random_file_name)

def put_window_behind(window_title_substring="Google Chrome"):
    """
    Attempts to move a Chrome window behind all other windows on Ubuntu using wmctrl.
    Assumes wmctrl is installed and the window title contains the substring.
    """
    try:
        # Find the window ID of the Chrome browser
        cmd = f"wmctrl -l | grep '{window_title_substring}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split('\n')
            # Look for the most recently opened Chrome window, usually the last one in the list
            # Or, if you are sure about the exact title.
            # A more robust way might involve filtering by the process ID if possible to get from Selenium.
            # For simplicity, taking the first match:
            window_id = lines[0].split(' ')[0] 
            
            print(f"Found Chrome window with ID: {window_id}")
            
            # Use wmctrl to set the window property to 'below'
            subprocess.run(f"wmctrl -i -r {window_id} -b add,below", shell=True)
            print(f"Moved window {window_id} behind other windows.")
        else:
            print(f"Could not find Chrome window with title containing '{window_title_substring}'.")
            print("wmctrl output:", result.stderr if result.stderr else result.stdout)
    except Exception as e:
        print(f"Error while trying to move window behind: {e}")

# --- Configuration ---
USER_PROFILE_PATH = "/home/prajwal/haptics_yt/chromium"
USER_PROFILE = "Profile 4"
VIDEO_PATH = get_random_file_path("/home/prajwal/haptics_yt/outputs")  # Path to your video file
VIDEO_TITLE = "Vibration ASMR Ringtone (Github in channel info) #ASMR #Ringtones"
VIDEO_DESCRIPTION = ""
# Optional: Add tags as a comma-separated string
VIDEO_TAGS = "Haptic Ringtones, Custom Ringtones, Music App, Haptics, Mobile App, Personalization, Ringtone Creator, Vibration App, Sound Design, Audio Customization, Tech Demo, Android App, iOS App, Unique Ringtones, Tactile Feedback, Immersive Audio, DIY Ringtones, ASMR, Haptic ASMR, Sensory Experience, Soothing Sounds"

# --- Main Script ---
chrome_options = Options()

# Profile configuration
chrome_options.add_argument(f"user-data-dir={USER_PROFILE_PATH}")
chrome_options.add_argument(f"profile-directory={USER_PROFILE}")
# chrome_options.add_argument("--start-minimized")
chrome_options.add_argument("window-size=1200,800")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
        service=Service(executable_path="/home/prajwal/chromedriver-linux64/chromedriver"),
        options=chrome_options
    )

try:
    # After the browser starts, immediately try to move it behind other windows
    put_window_behind(window_title_substring="New Tab - Chromium")

    # 1. Navigate to YouTube
    driver.get("http://youtube.com/") # Corrected URL

    # 2. Navigate to the upload page
    upload_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Create"]'))
    )
    upload_button.click()

    upload_video_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//yt-formatted-string[text()="Upload video"]'))
    )
    upload_video_link.click()

    # 3. Upload the video file
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )
    file_input.send_keys(VIDEO_PATH)
    print("Video file selected.")

    # 4. Fill in video details
    title_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="textbox"]'))
    )
    #title_input.send_keys(Keys.CONTROL + 'a')
    title_input.send_keys(Keys.BACKSPACE)
    # Clear existing title and enter new one
    # Assuming the input field has existing text that needs clearing
    title_input.send_keys(" "+VIDEO_TITLE)
    print("Video title entered.")

    description_input = driver.find_element(By.XPATH, '(//*[@id="textbox"])[2]')
    description_input.send_keys(VIDEO_DESCRIPTION)
    print("Video description entered.")

    # --- Handle "Made for Kids" section ---
    # Wait for the "Made for Kids" radio buttons to be present
    # You'll need to inspect the YouTube page to get the correct XPATHs for these elements.
    # The following are examples and might need adjustment.

    # Option 1: "No, it's not made for kids"
    not_made_for_kids_radio = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK")) # Common name attribute
        # Or By.XPATH, '//*[contains(text(), "No, it\'s not made for kids")]/ancestor::tp-yt-paper-radio-button'
        # Or By.ID, 'not-made-for-kids-radio-button' (if YouTube uses an ID)
    )
    not_made_for_kids_radio.click()
    print("Selected 'No, it's not made for kids'.")

    more_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Show advanced settings"]'))
    )
    more_button.click()
    print("Show more clicked.")

    # Wait for the checkbox to be clickable using its aria-label
    checkbox_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="checkbox" and @aria-label="Show how many viewers like this video"]'))
    )

    # Then, execute JavaScript to click it
    driver.execute_script("arguments[0].click();", checkbox_element)
    print("Clicked 'Hide Likes'.")

    # 5. Click 'Next' for video details
    next_button_details = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, "next-button"))
    )
    next_button_details.click()
    print("Clicked 'Next' for video details.")

    # If you wanted to select "Yes, it's made for kids"
    # made_for_kids_radio = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.NAME, "MADE_FOR_KIDS"))
    # )
    # made_for_kids_radio.click()
    # print("Selected 'Yes, it's made for kids'.")

    # 6. Click 'Next' for video elements (already in your script)
    next_button_elements = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, "next-button"))
    )
    next_button_elements.click()
    print("Clicked 'Next' for video elements.")

    # 7. Click 'Next' for checks (already in your script)
    next_button_checks = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, "next-button"))
    )
    next_button_checks.click()
    print("Clicked 'Next' for checks.")

    # Select visibility (e.g., 'Private', 'Unlisted', or 'Public')
    private_radio_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.NAME, "PUBLIC"))
    )
    private_radio_button.click()
    print("Selected 'Private' visibility.")

    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Publish"]'))
    )
    save_button.click()
    # Wait for the upload to finalize
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Upload complete")]'))
    )
    print("Video upload process completed.")

    time.sleep(5)

    print("Video successfully published to YouTube!")

    # driver.get("https://www.tiktok.com/tiktokstudio/upload?from=webapp") # Corrected URL
    # # 3. Upload the video file
    # file_input_tk = WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    # )
    # file_input_tk.send_keys(VIDEO_PATH)
    # print("Video file selected.")

    # description_textbox = WebDriverWait(driver, 15).until(
    #     EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and contains(@class, "public-DraftEditor-content")]'))
    # )
    # description_textbox.send_keys(Keys.BACKSPACE)
    # description_textbox.send_keys(" "+VIDEO_TITLE)
    # print("Video title entered.")

    # # Wait for the upload to finalize
    # WebDriverWait(driver, 300).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Uploaded")]'))
    # )
    # print("Video successfully uploaded!")

    # post_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//button[@data-e2e="post_video_button"]'))
    # )
    # post_button.click()
    # print("Video upload process completed.")

    # # Wait for the upload to finalize
    # WebDriverWait(driver, 300).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Video published")]'))
    # )
    # print("Video successfully published to Tiktok!")

    os.remove(VIDEO_PATH)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    time.sleep(2)