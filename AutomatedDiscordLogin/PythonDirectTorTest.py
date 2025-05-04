from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

def human_delay(min_time=1, max_time=5):
    delay = random.uniform(min_time, max_time)
    time.sleep(delay)
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
options.set_preference("general.useragent.locale", "en-US") 
options.set_preference("startup.homepage_welcome_url", "about:blank")
options.set_preference("startup.homepage_welcome_url.additional", "about:blank")
options.set_preference("browser.startup.homepage", "about:blank")
options.set_preference("browser.shell.checkDefaultBrowser", False)
options.set_preference("browser.warnOnQuit", False)
options.set_preference("geo.enabled", False)  # Disable location services
# Launch the browser
service = Service(GECKODRIVER_PATH)
driver = webdriver.Firefox(service=service, options=options)

# Make sure Tor is running
#change_tor_ip()

time.sleep(5)  # Wait for page to load
# Open Tor Browser
driver.get("about:blank")

time.sleep(5)  # Wait for page to load

# Wait until the "Connect" button is visible and then click it
try:
    # Wait for the connect button to be available
    connect_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Connect')]"))
    )
    connect_button.click()

    # Wait for Tor to connect (check for an element that appears after connection, like the "Connected" message or similar)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Connected')]"))
    )

    print("Successfully connected to Tor!")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Cleanup
    driver.quit()

# Check IP via a Tor-detecting site
driver.get("https://check.torproject.org/")

# Optional: print title to verify success
#print(driver.title)

# Cleanup
# driver.quit()