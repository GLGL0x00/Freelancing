import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter import filedialog
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
def upload_file():
    # Open file dialog to select Excel file
    file_path = filedialog.askopenfilename(
        title="Select an Excel file",
        filetypes=[("Excel files", "*.xlsx *.xls")] #("All files", "*.*")
    )
    
    if file_path:  # If a file is selected
        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file_path)
            
            # Display the first few rows in the console
            print("Excel file successfully loaded! Here are the first 5 rows:")
            print(df.head())
        except Exception as e:
            print(f"Error reading the Excel file: {e}")
    else:
        print("No file was selected.")

    return file_path

def get_chrome_driver():
    try:
        # Check if Chrome WebDriver exists in PATH
        driver_path = ChromeDriverManager().install()
        print(f"Using WebDriver from {driver_path}")
        # Try to initialize the driver
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)
        return driver
    except WebDriverException as e:
        print("Error initializing WebDriver:", e)
        print("Installing Chrome WebDriver...")
        # Automatically install the WebDriver using webdriver_manager
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)
        return driver

if __name__ == "__main__":

    # Load Excel data
    student_file_path = upload_file()
    data = pd.read_excel(student_file_path)

    try:
        driver = get_chrome_driver()
        print("WebDriver initialized successfully!")
        driver.get("")  # Replace with your form's URL
    except Exception as e:
            print(f"Failed to set up WebDriver: {e}")

    # Loop through each student's data
    for index, row in data.iterrows():
        # Locate form fields and fill them
        # input text
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[1]/div[2]/div/span/input').send_keys(row['Student Email'])
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/span/input').send_keys(row['Teacher Code'])

        # list of weeks
        dropdown_trigger = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/div/div'))  # Replace with the actual class or locator of the dropdown trigger
        )
        dropdown_trigger.click()

        driver.find_element(By.XPATH, f'//div[@role="option" and @aria-posinset="{row["Week"]}"]').click()

        # single choice from 1 to 5
        #student interaction level
        driver.find_element(By.XPATH, f'//div[@aria-labelledby="QuestionId_r60105d5c443d4547bb455e5cbceba3dd QuestionInfo_r60105d5c443d4547bb455e5cbceba3dd"]//input[@type="radio" and @value="{row["Interaction Level"]}"]').click()
        #level of commitment
        driver.find_element(By.XPATH, f'//div[@aria-labelledby="QuestionId_r3424766a67a14130a6a83d62a9bab8c4 QuestionInfo_r3424766a67a14130a6a83d62a9bab8c4"]//input[@type="radio" and @value={row["Committment Level"]}]').click()
        #single choice (Commited, troublemaker, absent)
        driver.find_element(By.XPATH, f'//input[@type="radio" and @value="{row["Student behaviour"]}"]').click()

        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[7]/div[2]/div/span/input').send_keys(row["Feedback"])
        
        # Submit the form
        driver.find_element(By.XPATH, '//*[@id="form-main-content1"]/div/div/div[2]/div[3]/div/button').click()
        print(index, "-", row['Student Email'])
        # Wait a few seconds before processing the next student
        time.sleep(5)

        driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[5]/span').click()

    driver.quit()
