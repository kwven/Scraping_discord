# Scraping_discord

This project provides tools for scraping data from Discord servers using both API requests and web automation.

## Components
- `scraping_api.py`: Uses the Discord API to fetch server member counts, online presence, and the last 15 messages from a channel. Requires environment variables for authentication.
- `scraping_web.py`: Uses Selenium to automate Discord web login and scrape messages, saving them to a CSV file. Also uses environment variables for credentials and configuration.

## Requirements
- Python 3.x
- `requests`, `python-dotenv`, `selenium`, `webdriver-manager`

## Environment Variables
The following environment variables are required for proper configuration:

- `EMAIL`: Your Discord account email address. Used for web automation login.
- `PASSWORD`: Your Discord account password. Used for web automation login.
- `ACCESS_TOKEN`: Your Discord API token. Used for API requests. Obtain this from the Discord Developer Portal by creating an application and generating a bot token.
- `SERVER_ID`: The ID of the Discord server you want to scrape. You can get this by enabling Developer Mode in Discord, right-clicking the server icon, and selecting "Copy Server ID".
- `CHANNEL_ID`: The ID of the Discord channel to fetch messages from. Enable Developer Mode, right-click the channel, and select "Copy Channel ID".

Create a `.env` file in the project root with these variables:
```env
EMAIL=your_email
PASSWORD=your_password
ACCESS_TOKEN=your_token
SERVER_ID=your_server_id
CHANNEL_ID=your_channel_id
```

## Setup
1. Install dependencies:
   ```bash
   pip install requests python-dotenv selenium webdriver-manager
   ```
2. Create a `.env` file with your Discord credentials and tokens as described above.

## Usage
- To fetch data via API, run:
  ```bash
  python scraping_api.py
  ```
- To scrape messages via web automation, run:
  ```bash
  python scraping_web.py
  ```