# AutomatedDiscordLogin

Simple Example how to log in to different discord accounts with help of Selenium and Python.

pip install -r requirements.txt
create based on example_accounts.csv an accounts.csv file.
Passwords and special signs need to be quoted or escaped in a way python3 csv expects it.

I thought it's more easy to use TAB as delimiter /t
            reader = csv.DictReader(file, delimiter='\t')

is you want to change that change that line like to ; , or whatever you want and the csv file accordingly.

For use with Tor

You need Geckodriver (for Tor Firefox) 
https://github.com/mozilla/geckodriver/releases/tag/v0.36.0
https://github.com/mozilla/geckodriver
You need Tor Firefox

Place paths and so on accordingly.

The Tor Project is not useless but sadly discord blocks most of Tors IP's due to misuse.

TOR_PATH = "./torbrowser/Tor Browser/Browser/firefox.exe"  # Adjust for your OS
GECKODRIVER_PATH = "./geckodriver.exe"  # Adjust as needed

place Toe and Geckodriver accordingly or changes pathes and so on.

On Linux ofc use the linux executeable and changes the python script accordingly.