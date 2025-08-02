# 🤖 YouTube Shorts Automation Suite

This project is a suite of scripts designed to automate the creation and uploading of short-form videos. It works by combining a base set of video clips with a library of audio tracks, generating numerous unique video variations, and then systematically uploading them to YouTube.

## Demo


https://github.com/user-attachments/assets/36f1b4a8-603b-4b75-9105-8c2706c821c6



## ✨ Features

-   **Batch Video Generation**: Automatically combines every video in the `videos` folder with every audio track in the `audios` folder.
-   **Hardware Accelerated Encoding**: Utilizes `ffmpeg` with VA-API for fast, hardware-accelerated video processing on compatible Linux systems.
-   **Professional Touches**: Adds a fade-to-black transition at the end of the main clip before appending a custom `outro.mp4`.
-   **Automated Uploading**: Uses Selenium to automate the entire YouTube upload process, from file selection to setting the title, description, tags, and publishing.
-   **Content Randomization**: The `upload.py` script selects a random video from the generated files for each run, ensuring varied upload order.
-   **Self-Cleaning**: Automatically deletes video files from the `outputs` directory after they are successfully uploaded to save disk space.
-   **Helper Scripts**: Includes a script to pre-process and standardize source videos (`convert.sh`) and another to quickly check channel stats (`stats.py`).

***

## ⚙️ How It Works (Workflow)

The process is broken down into four main stages:

1.  **Prepare Source Videos**: Use the `convert.sh` script to process your raw video clips. This script converts them to a standard MP4 format, removes any existing audio, and renames them sequentially (e.g., `video001.mp4`).
2.  **Stage Media Files**:
    * Place your prepared, audio-less video clips into the `/videos` directory.
    * Place your sound clips (MP3, WAV, etc.) into the `/audios` directory.
    * Ensure your custom `outro.mp4` is in the root directory.
3.  **Generate Videos**: Run the `./generate.sh` script. It will create every possible video-audio combination, add the fade and outro, and save the final files to the `/outputs` directory.
   - **Sample Generated Videos**:

https://github.com/user-attachments/assets/98045056-9b18-45ce-883c-a39c6a69bbdb

https://github.com/user-attachments/assets/5619a634-8fd5-4a47-8e89-2d8b08e6a7e3

4.  **Upload to YouTube**: Run the `python3 upload.py` script. It will:
    * Pick a random video from `/outputs`.
    * Open a Chrome browser with your specified user profile.
    * Upload the video and fill in the metadata you configured in the script.
    * Delete the local video file after the upload is confirmed.

***

## 🚀 Setup and Installation

### Prerequisites

-   A **Linux-based OS** (the scripts are written for a bash environment).
-   **Intel GPU** that supports VA-API for hardware acceleration (for `generate.sh`).
-   **Python 3.8+** and `pip`.
-   `ffmpeg`: The core for all video processing.
-   `wmctrl`: A utility to manage windows (used by `upload.py` to hide the browser).
-   A dedicated **Google Chrome / Chromium** browser profile for YouTube.
-   **ChromeDriver** matching your Chrome/Chromium version.

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/prajwal8074/haptics_yt.git
    cd haptics_yt
    ```

2.  **Install system dependencies** (example for Debian/Ubuntu):
    ```bash
    sudo apt-get update && sudo apt-get install ffmpeg wmctrl
    ```

3.  **Set up Python environment and install packages:**
    run:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Download ChromeDriver**:
    * Make sure you have Google Chrome or Chromium installed.
    * Download the corresponding version of ChromeDriver from the official site.
    * Place the executable in a known location (e.g., `/home/user/drivers/chromedriver`) and make it executable (`chmod +x`).

### Configuration

Before running the scripts, you must configure the variables within them.

#### 1. `generate.sh`
This script handles video creation.
```bash
# Verify the path to your VAAPI rendering device
HW_ACCEL_DEVICE="/dev/dri/renderD128"
```

#### 2. `upload.py`
This script handles the upload automation. **This requires the most setup.**
```python
# --- Configuration ---
# Path to your Chrome/Chromium user data directory
USER_PROFILE_PATH = "/home/prajwal/haptics_yt/chromium"
# The specific profile directory name (e.g., "Profile 4" or "Default")
USER_PROFILE = "Profile 4"

# Metadata for your uploads
VIDEO_TITLE = "Vibration ASMR Ringtone (Github in channel info) #ASMR #Ringtones"
VIDEO_DESCRIPTION = ""
VIDEO_TAGS = "Haptic Ringtones, Custom Ringtones, ... " # Comma-separated tags

# --- Main Script ---
# Update this to the absolute path of your downloaded chromedriver
driver = webdriver.Chrome(
        service=Service(executable_path="/home/prajwal/chromedriver-linux64/chromedriver"),
        options=chrome_options
    )
```
You will also need to update the `stats.py` script with the same `USER_PROFILE_PATH`, `USER_PROFILE`, and `chromedriver` path.

***

## Usage

Follow the workflow steps:

1.  **Prepare videos**. Navigate to a folder containing your raw source videos and run the conversion script.
    ```bash
    ./convert.sh
    ```
    Move the resulting files from the `converted_videos_no_audio` folder into this project's `videos` directory.

2.  **Generate all video combinations**. From the project's root directory, run:
    ```bash
    ./generate.sh
    ```
    Monitor progress and check `ffmpeg.log` for any errors.

3.  **Upload a video**. To upload one random video, run:
    ```bash
    source venv/bin/activate
    python3 upload.py
    ```
    You can run this script multiple times or set it up as a cron job to upload periodically.

4.  **Check your stats**. To quickly open your YouTube and TikTok studio pages:
    ```bash
    source venv/bin/activate
    python3 stats.py
    ```

***

## ⚠️ Important Notes

-   **UI Changes**: The `upload.py` script relies on Selenium to navigate the YouTube Studio web UI. If YouTube changes its website structure, the `XPATH`, `ID`, or `NAME` selectors in the script may break and will need to be updated.
-   **Hardware Dependency**: The `generate.sh` script is hard-coded to use Intel VA-API for hardware acceleration. If you have an NVIDIA (`nvenc`) or AMD (`amf`) GPU, you will need to significantly modify the `ffmpeg` command in the script.

