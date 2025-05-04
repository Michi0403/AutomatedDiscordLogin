from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import csv
import time
import random

def human_delay(min_time=1, max_time=5):
    delay = random.uniform(min_time, max_time)
    time.sleep(delay)

def open_discord_sessions(csv_file):
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                email = row['username'].strip()
                password = row['password'].strip()

                print(f"[INFO] Launching browser for: {email}")
                # Debug: Print the raw credentials to check encoding or hidden characters
                print(f"[DEBUG] Attempting login with:")
                print(f"  Username: '{email}' (len={len(email)})")
                print(f"  Password: '{password}' (len={len(password)})")
                # Chrome incognito session
                chrome_options = Options()
                chrome_options.add_argument("--incognito")
                chrome_options.add_argument("--start-maximized")

                driver = webdriver.Chrome(options=chrome_options)
                driver.get("https://discord.com/login")

                time.sleep(3)  # Wait for page to load

                # Fill in email
                email_field = driver.find_element(By.NAME, "email")
                email_field.send_keys(email)
                human_delay()
                # Fill in password
                password_field = driver.find_element(By.NAME, "password")
                password_field.send_keys(password)
                human_delay()
                password_field.send_keys(Keys.RETURN)  # Press Enter to log in
                human_delay()
                print(f"[INFO] Login attempted for {email}")
                time.sleep(10)  # Let the session load before moving on

    except FileNotFoundError:
        print(f"[ERROR] File '{csv_file}' not found.")
    except Exception as e:
        print(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    open_discord_sessions("accounts.csv")