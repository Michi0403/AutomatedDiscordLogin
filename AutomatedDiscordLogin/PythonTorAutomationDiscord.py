from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stem import Signal
from stem.control import Controller
import tempfile
import os
import csv
import time
import random

TOR_PATH = "./torbrowser/Tor Browser/Browser/firefox.exe"  # Adjust for your OS
GECKODRIVER_PATH = "./geckodriver.exe"  # Adjust as needed

def human_delay(min_time=1, max_time=5):
    delay = random.uniform(min_time, max_time)
    time.sleep(delay)

def switch_to_main_tab(driver, original_window_handle):
    # Get all the window handles and switch to the original tab
    current_window_handles = driver.window_handles
    for handle in current_window_handles:
        if handle != original_window_handle:
            continue
        driver.switch_to.window(handle)
        break
def handle_alert(driver):
    try:
        # Switch to the alert and dismiss it
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print("Alert detected, dismissing it...")
        alert.dismiss()  # or alert.accept() to accept the alert
    except Exception as e:
        print(f"No alert detected: {e}")
        return
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

                # Path to geckodriver and Tor Browser's Firefox binary
                TOR_PATH = "./torbrowser/Tor Browser/Browser/firefox.exe"  # Adjust for your OS
                GECKODRIVER_PATH = "./geckodriver.exe"  # Adjust as needed

                # Create a temporary clean Firefox profile
                #temp_profile_dir = tempfile.mkdtemp()
                # Function to send a signal to Tor to get a new IP address
                #def change_tor_ip():
                #    with Controller.from_port(port=9051) as controller:
                #        controller.authenticate()
                #        controller.signal(Signal.NEWNYM)
                # Configure Firefox to use Tor's SOCKS proxy
                options = Options()
                options.binary_location = TOR_PATH
                options.headless = False  # Set to True for headless

                # Force Firefox to use a clean profile and override all defaults
                #options.set_preference("profile", temp_profile_dir)
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.socks", "127.0.0.1")
                options.set_preference("network.proxy.socks_port", 9050)  # or 9150 on some systems
                options.set_preference("network.proxy.socks_remote_dns", True)
                options.set_preference("permissions.default.image", 2)  # (optional) disables images
                options.set_preference("dom.ipc.processCount", 1)
                options.set_preference("network.http.use-cache", False)
                options.set_preference("intl.accept_languages", "en-US, en")
                options.set_preference("browser.startup.page", 0)  # Disable any startup page
                options.set_preference("intl.accept_languages", "en-US,en")  # Set language to English
                options.set_preference("intl.locale.requested", "en-US")  # Force English locale
                options.set_preference("toolkit.telemetry.reportingpolicy.firstRun", False)  # Disable telemetry
                options.set_preference("general.useragent.locale", "en-US") 
                options.set_preference("startup.homepage_welcome_url", "about:blank")
                options.set_preference("startup.homepage_welcome_url.additional", "about:blank")
                options.set_preference("browser.startup.homepage", "about:blank")
                options.set_preference("browser.shell.checkDefaultBrowser", False)
                options.set_preference("browser.warnOnQuit", False)
                options.set_preference("browser.newtab.url", "about:blank")  # Set new tab URL to blank
                options.set_preference("browser.download.useDownloadDir", True)  # Ensure downloads use the default directory
               
                options.set_preference("geo.enabled", False)  # Disable location services
                # Launch the browser
                service = Service(GECKODRIVER_PATH)
                driver = webdriver.Firefox(service=service, options=options)
                time.sleep(10) 
                # Make sure Tor is running
                #change_tor_ip()
                
                original_window_handle = driver.current_window_handle
                # Open Tor Browser
                #driver.get("about:blank")


                # Wait until the "Connect" button is visible and then click it
                try:
                    # Wait for the connect button to be available
                    connect_button = WebDriverWait(driver, 10).until(
                        #EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Connect')]"))
                        EC.element_to_be_clickable((By.ID, "connectButton"))
                    )
                    connect_button.click()
                    
                    human_delay()
                    # Wait for Tor to connect (check for an element that appears after connection, like the "Connected" message or similar)
                    #WebDriverWait(driver, 10).until(
                        #EC.presence_of_element_located((By.NAME, "connectButton"))
                    #)
                    time.sleep(3) 
                    print("Successfully connected to Tor!")

                except Exception as e:
                    print(f"An error occurred: {e}")
                handle_alert(driver)
                try:
                    time.sleep(3)  # Wait for page to load
                    driver.get("https://discord.com/login")
                    human_delay()
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
                except Exception as e:
                    print(f"An error occured in connection to Discord: {e}")
                #finally:
                    # Cleanup
                    #driver.quit()
    except FileNotFoundError:
        print(f"[ERROR] File '{csv_file}' not found.")
    except Exception as e:
        print(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    open_discord_sessions("accounts.csv")