import time
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import csv

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD=os.getenv("PASSWORD")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SERVER_ID = os.getenv("SERVER_ID")

# Initialize the Chrome driver correctly
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# Function to save messages to CSV
def save_messages_to_csv(messages, filename="discord_messages.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Message Content", "Author", "Timestamp"])
        for msg in messages:
            writer.writerow([msg["content"], msg["author"], msg["timestamp"]])
    print(f"Messages saved to {filename}")

 # Navigate to Discord login page
driver.get("https://discord.com/login")
# Wait for the login page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "email"))
)
# Enter email
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(EMAIL)
# Enter password
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(PASSWORD)
# Click login button
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_button.click()
print("Logging in to Discord...")
 # Wait for login to complete and Discord to load
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='sidebar']")),
    message="Timed out waiting for Discord to load after login"
)
print("Successfully logged in!")
# Navigate to the specific channel
channel_url = f"https://discord.com/channels/{SERVER_ID}/{CHANNEL_ID}"
driver.get(channel_url)
# Wait for messages to load
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='message']")),
    message="Timed out waiting for messages to load"
)
print("Messages loaded. Starting to scrape...")
time.sleep(3)
# Function to scroll up to load more messages
def scroll_for_messages(max_scrolls=20, messages_per_scroll=50):
    # Find the scrollable message container
    message_container = driver.find_element(By.CSS_SELECTOR, '[class*="scroller__36d07"]')
    
    # Initialize variables
    total_messages = []
    scroll_count = 0
    last_message_count = 0
    
    print("Starting to scroll and collect messages...")
    
    while scroll_count < max_scrolls:
        message_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='message']")
        current_messages = []
        for msg_element in message_elements:
            try:
                # Extract message content
                content_element = msg_element.find_element(By.CSS_SELECTOR, "[class*='messageContent']")
                content = content_element.text
                # Extract author
                author_element = msg_element.find_element(By.CSS_SELECTOR, "[class*='username']")
                author = author_element.text
                # Extract time posted
                timestamp_element = msg_element.find_element(By.CSS_SELECTOR, "time")
                timestamp = timestamp_element.get_attribute("datetime")
                clean_ts = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
                msg_id = f"{author}_{clean_ts}"
                current_messages.append({
                    "content": content,
                    "author": author,
                    "timestamp": clean_ts,
                    "id": msg_id
                })
            except Exception as e:
                print(f"Error extracting message data: {e}")
        # Check if we've reached the end 
        if len(total_messages) == last_message_count:
            print("No new messages found after scrolling. Reached the end or rate limited.")
            break
        last_message_count = len(total_messages)
        
        # Scroll up to load more messages
        driver.execute_script("arguments[0].scrollTop = 0;", message_container)
        # Wait for new messages to load
        time.sleep(2)
        scroll_count += 1
        # If we've collected enough messages, stop scrolling
        if len(total_messages) >= max_scrolls * messages_per_scroll:
            print(f"Collected {len(total_messages)} messages, stopping scrolling")
            break
    return total_messages
