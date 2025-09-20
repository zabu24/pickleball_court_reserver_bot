import time as t
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import traceback
import schedule

EMAIL = "xxx" // enter account creds
PASSWORD = "xxx" 
CLUB_ID = "36"  # Fairfax
SPORT = "Pickleball%3A+Indoor"
DURATION = "90"
TIME_WINDOW = [
    "10:00 PM", "9:30 PM", "9:00 PM", "8:30 PM", "8:00 PM",
    "7:30 PM", "7:00 PM", "6:30 PM", "6:00 PM", "5:30 PM", "5:00 PM"
]
MAX_DAYS_AHEAD = 10  

def get_target_date(offset):
    target_day = dt.date.today() + dt.timedelta(days=offset)
    return target_day.strftime("%Y-%m-%d")

def perform_login(driver):
    try:
        print("Waiting for login form...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username, Email, or Member ID']"))
        )
        username = driver.find_element(By.XPATH, "//input[@placeholder='Username, Email, or Member ID']")
        password = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        login_button = driver.find_element(By.XPATH, "//button[contains(., 'Log In')]")

        username.send_keys(EMAIL)
        password.send_keys(PASSWORD)
        login_button.click()
        print("Submitted login form.")

        WebDriverWait(driver, 15).until(
            lambda d: "login" not in d.current_url.lower()
        )
        print("Logged in and redirected.")
    except Exception as e:
        print("Login failed.")
        traceback.print_exc()

def click_waiver_checkbox(driver):
    print("Attempting to click waiver checkbox...")
    try:
        waiver_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "acceptwaiver"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", waiver_checkbox)
        t.sleep(1)
        if not waiver_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", waiver_checkbox)
            print("Accepted reservation waiver.")
    except Exception as e:
        print("No waiver checkbox found or clickable.")
        traceback.print_exc()

def reserve_court():
    for day_offset in range(1, MAX_DAYS_AHEAD + 1):
        target_date = get_target_date(day_offset)
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Trying {target_date}...")
        RESERVATION_URL = f"https://my.lifetime.life/clubs/va/fairfax/resource-booking.html?sport={SPORT}&clubId={CLUB_ID}&date={target_date}&startTime=-1&duration={DURATION}&hideModal=true"

        options = Options()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            print("Navigating to reservation page...")
            driver.get(RESERVATION_URL)
            t.sleep(2)

            print("Checking for cookie banner...")
            try:
                cookie_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All')]"))
                )
                cookie_btn.click()
                print("Accepted cookies.")
            except:
                print("No cookie banner found.")

            print("🔍 Scanning for available time blocks...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            t.sleep(2)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "timeslot"))
            )
            all_slots = driver.find_elements(By.CLASS_NAME, "timeslot")

            preferred_slot = None
            slot_time = None
            for preferred_time in TIME_WINDOW:
                for slot in all_slots:
                    if preferred_time in slot.text:
                        preferred_slot = slot
                        slot_time = preferred_time
                        break
                if preferred_slot:
                    break

            if not preferred_slot and all_slots:
                preferred_slot = all_slots[0]
                slot_time = preferred_slot.text.split("\n")[0]

            if preferred_slot:
                driver.execute_script("arguments[0].click();", preferred_slot)
                print(f"Clicked slot for {slot_time}")
                t.sleep(2)

                if "login" in driver.current_url.lower():
                    print("Redirected to login screen after time selection. Logging in...")
                    perform_login(driver)
                    print("Waiting for reservation UI...")
                    WebDriverWait(driver, 15).until_not(lambda d: "login" in d.current_url.lower())

                click_waiver_checkbox(driver)

                print("🎯 Waiting for reservation panel to load...")
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "reservation-summary"))
                    )
                except:
                    print("Reservation summary panel may not have loaded.")

                print("Clicking Finish button...")
                try:
                    finish_btn = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Finish')]"))
                    )
                    finish_btn.click()
                    print(f"Reservation completed for {target_date} at {slot_time}")
                    t.sleep(5)
                    return  # Success, exit the function
                except Exception as e:
                    print("Couldn't find or click Finish button.")
                    traceback.print_exc()
            else:
                print("No time slots available.")

        except Exception as e:
            print("Error occurred:")
            traceback.print_exc()
        finally:
            print("Quitting browser.")
            with open("page_snapshot.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
                print("Saved page_snapshot.html for inspection.")
            driver.quit()

# Run immediately for testing
#reserve_court()

#    Schedule for weekdays at 9:00 AM
schedule.every().monday.at("09:00").do(reserve_court)
schedule.every().tuesday.at("09:00").do(reserve_court)
schedule.every().wednesday.at("09:00").do(reserve_court)
schedule.every().thursday.at("09:00").do(reserve_court)
schedule.every().friday.at("09:00").do(reserve_court)

print("Scheduler running. Waiting for 9:00 AM on weekdays to reserve your court...")
while True:
    schedule.run_pending()
    t.sleep(10)
