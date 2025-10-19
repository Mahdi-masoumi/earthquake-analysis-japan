from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import pandas as pd
import datetime
import time


def run_emsc_scraper():
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.emsc.eu/Earthquake_information/")
    extracted_data = None
    wait = WebDriverWait(driver, 10)

    # accept cookies if there is a prompt
    try:
        cookie_btn = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "cookieButton")))
        cookie_btn.click()
    except:
        pass

    # fill out search form and submit
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#datemin"))).send_keys('2025-09-09')
    driver.find_element(By.CSS_SELECTOR, "#datemax").send_keys('2025-10-09')
    driver.find_element(By.CSS_SELECTOR, "#magmin").send_keys("1")
    driver.find_element(By.CSS_SELECTOR, "#latmin").send_keys("24")
    driver.find_element(By.CSS_SELECTOR, "#latmax").send_keys("46")
    driver.find_element(By.CSS_SELECTOR, "#lonmin").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "#lonmax").send_keys("146")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".subm input[type='submit']").click()

    # extract the data after the table has rendered

    def extract_data(driver):
        time.sleep(2)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".eqs tbody tr")))

        rows_data = []
        table_rows = driver.find_elements(By.CSS_SELECTOR, ".eqs tbody tr")

        for tr in table_rows:
            try:
                d_and_t_list = tr.find_element(
                    By.CSS_SELECTOR, ".tbdat").text.split()[:2]
                raw_date_and_time = d_and_t_list[0] + " " + d_and_t_list[1]

                row = {
                    "date_and_time": raw_date_and_time,
                    "latitude": tr.find_element(By.CSS_SELECTOR, ".tblat").text,
                    "longitude": tr.find_element(By.CSS_SELECTOR, ".tblon").text,
                    "depth": tr.find_element(By.CSS_SELECTOR, ".tbdep").text,
                    "magnitude": tr.find_element(By.CSS_SELECTOR, ".tbmag").text,
                    "region": tr.find_element(By.CSS_SELECTOR, ".tbreg").text
                }
                rows_data.append(row)
            except:
                continue

        return rows_data

    all_data = []
    while True:
        all_data.extend(extract_data(driver))
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, ".spes.spes1.pag")
            if next_btn.get_attribute("style") == "display: none;":
                break
            # click the next button
            driver.execute_script("arguments[0].click();", next_btn)

            old_first_row_text = driver.find_element(
                By.CSS_SELECTOR, ".eqs tbody tr .tbdat").text

            def has_page_updated(driver):
                current_first_row_text = driver.find_element(
                    By.CSS_SELECTOR, ".eqs tbody tr .tbdat").text
                return current_first_row_text != old_first_row_text

            wait.until(has_page_updated)

        except NoSuchElementException:
            break

    df = pd.DataFrame(all_data)
    df.to_csv("JAPAN_EMSC.csv")
    driver.quit()
