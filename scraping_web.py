import time
import os
#selenium to scrape the web page
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