# This is a Python Code for the extraction of rainfall data table from
# a website using selenuim and BeautifulSoup Tools

# Importing all the required Libraries
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Define the start and end date range
start_date = date(2023, 1, 14)
end_date = date(2023, 1, 14)

# Define the location and URL template
location = "secunderabad"
url_template = "https://www.wunderground.com/history/daily/in/{location}/VOHY/date/{year}-{month}-{day}"

# To extract the table from the website we need to load the website, the website was taking time to
# load the data. For the code has to wait for some time to load the data. After loading the dataset,
# it searches for the table collects and stores in a .csv file.
# In the below code, entire code is in while loop, if there is any error inside the while 'try' will 
# throw to 'except' part and saves that. And runs again the loop till it satisfies. If 'except' part
# executes the 'k' value increases by 1 and 'if' condition will not execute.
# The code structure follows
# while (..)..:
#   try:
#       while (..):
#           ...
#           for (..):
#               for (..):
#           if (..):
#   except:
#       with (..):
#           if (..):
#   if (..):
#       with (..):
#           if (..):

bool_ = True
while start_date <= end_date:
    k, n = 1, 1
    try:
        # Create an empty list to store the table data
        data = []

        # Loop through the dates
        delta = timedelta(days=1)
        while start_date <= end_date:
            # Format the date in the required format
            date_str = start_date.strftime("%Y-%m-%d")
            year_str = start_date.strftime("%Y")
            month_str = start_date.strftime("%m")
            day_str = start_date.strftime("%d")

            # Construct the URL
            url = url_template.format(location=location, year=year_str, month=month_str, day=day_str)

            # Navigate to the URL
            driver.get(url)

            # Wait for the table to load
            wait = WebDriverWait(driver, 15)
            table = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".mat-table.cdk-table.mat-sort.ng-star-inserted")))

            # Parse the web page content as HTML using BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find the table element by its tag and class
            table = soup.find("table", class_="mat-table cdk-table mat-sort ng-star-inserted")

            # Loop through the table rows
            for row in table.find_all("tr"):
                # Create an empty list to store the row data
                row_data = []
                # Loop through the row cells
                for cell in row.find_all("td"):
                    # Append the cell text to the row data list
                    row_data.append(cell.text.strip())
                # Append the row data list to the table data list
                if len(row_data) > 0:
                    # Add the date to the row data list
                    row_data.insert(0, date_str)
                    data.append(row_data)

            # Increment the date by 1 day
            start_date += delta
    except:
        # Save the data to a CSV file
        with open("data_web_scrap.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            if bool_:
                writer.writerow(
                    ["Date", "Time", "Temperature", "Dew Point", "Humidity", "Wind", "Wind Speed", "Wind Gust", "Pressure",
                     "Precipitation", "Condition"])
                bool_ = False
            # Write the data rows
            writer.writerows(data)
            k += 1

    # This will be executed only if above 'except' block is not executed
    if k == n:
        # Save the data to a CSV file
        with open("data_web_scrap.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            if bool_:
                writer.writerow(
                    ["Date", "Time", "Temperature", "Dew Point", "Humidity", "Wind", "Wind Speed", "Wind Gust",
                     "Pressure",
                     "Precipitation", "Condition"])
                bool_ = False
            # Write the data rows
            writer.writerows(data)
        start_date += delta



# Close the Chrome driver
driver.quit()
