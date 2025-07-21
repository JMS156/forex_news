from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

# === SETUP CHROME ===
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-data-dir=/tmp/chrome-user-data')  # Avoid session conflict

driver = webdriver.Chrome(options=options)

# === LOAD TODAY'S FOREX FACTORY PAGE ===
today_url = f"https://www.forexfactory.com/calendar?day={datetime.today().strftime('%b%d.%Y').lower()}"
print(f"\n📡 Loading: {today_url}")
driver.get(today_url)
time.sleep(6)

# Scroll to force load
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# === FETCH NEWS ROWS ===
rows = driver.find_elements(By.CLASS_NAME, "calendar__row")

print("\n📰 TODAY'S FOREX NEWS:\n")
for row in rows:
    try:
        time_ = row.find_element(By.CLASS_NAME, "calendar__time").text.strip()
        currency = row.find_element(By.CLASS_NAME, "calendar__currency").text.strip()
        title = row.find_element(By.CLASS_NAME, "calendar__event-title").text.strip()
        impact = row.find_element(By.CLASS_NAME, "impact").get_attribute("title").strip()

        print(f"{time_:>7} | {currency:<3} | {title:<40} | Impact: {impact}")
    except:
        continue

driver.quit()

