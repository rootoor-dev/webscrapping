# Source 
**Master Thesis :** `Prediction of football players’ position using Data Mining and Machine Learning techniques`   (https://thesis.unipd.it/retrieve/8224c2d2-200b-4e6d-a0e9-d2458dd5adf9/Gobbo_Alberto.pdf)[https://thesis.unipd.it/retrieve/8224c2d2-200b-4e6d-a0e9-d2458dd5adf9/Gobbo_Alberto.pdf] (Accessed at 30th December 2023, 08h00)

**NOTE** : Chatgpt has been used to help in copying and rewrtting by refactoring the code. For the original codes, please read the thesis.

# Website to scrape

This code allows to apply web scraping technique on the first web page from (https://sofifa.com/)[https://sofifa.com/].
In the code, this is variable `url = https://sofifa.com/`

# Purpose

The Python script is writting for web scraping FIFA 22 player data and manipulating the data. This script uses the BeautifulSoup library for web scraping and pandas for data manipulation. Here's a brief summary of the functions in the script:

## Functions of the code

`url = https://sofifa.com/`

1. **FirstPageWebScraping(url):**
   - Scrapes data from the first page of the specified URL.
   - Calls functions to catch table features' names and values.
   - Delays execution for 0.5 seconds.

2. **CatchFeaturesNames(table):**
   - Finds and appends feature names from the HTML table header.

3. **CatchFeaturesValues(table):**
   - Finds and appends feature values from the HTML table rows.

4. **NextPagesWebScraping(url, offset):**
   - Iteratively scrapes data from subsequent pages by incrementing the offset.
   - Calls a function to catch feature values.
   - Delays execution for 0.5 seconds.
   - Prints an error message if the request fails.

5. **ManipulateAndCleanData():**
   - Cleans and manipulates the scraped data.
   - Splits each row into cells.
   - Drops columns with "None" values.
   - Renames columns based on specific mappings.
   - Drops unnecessary columns.
   - Fixes typos or character errors in selected columns.
   - Removes spaces from values.
   - Removes rows with NaN values or empty cells.
   - Returns the cleaned dataset.

6. **GenerateCSVDataset(dataset):**
   - Writes the cleaned dataset to a CSV file named "FIFA22_Dataset.csv".

**Chatgpt Note**: The script seems to be well-organized, and the functions are appropriately named. It's important to ensure that you have the necessary dependencies installed (e.g., BeautifulSoup, requests, pandas) before running the script. Additionally, consider adding exception handling for potential errors during web requests and data manipulation.


### 1. `FirstPageWebScraping` Function:

```python
from bs4 import BeautifulSoup
import requests
import time

# url = https://sofifa.com/
def FirstPageWebScraping(url):
    if requests.get(f"{url}&offset=0").status_code == 200:
        page = requests.get(f"{url}&offset=0").text
        players_table = CatchWebPageTable(page)

        CatchFeaturesNames(players_table)
        CatchFeaturesValues(players_table)

        time.sleep(0.5)
    else:
        print(f"Error {requests.get('{url}&offset=0').status_code}")
```

### 2. `CatchFeaturesNames` Function:

```python
from bs4 import BeautifulSoup
import re

def CatchFeaturesNames(table):
    features_names = table.find_all("th")

    for row in features_names:
        cell = str(row)
        features_names_list.append(re.sub(re.compile('<.*?>'), '', cell))
```

### 3. `CatchFeaturesValues` Function:

```python
from bs4 import BeautifulSoup
import re
import pandas as pd

def CatchFeaturesValues(table):
    global results_features_values
    features_values = table.find_all("tr")

    for row in features_values:
        cells = re.sub(re.compile('Jun(.+?)</span>|<div class=\"tip\">(.+?)</span></div></div>'), '', str(row.find_all("td")))
        features_values_list.append(re.sub(re.compile('<.*?>'), '', cells))

    results_features_values = pd.DataFrame(features_values_list)
```

### 4. `NextPagesWebScraping` Function:

```python
from bs4 import BeautifulSoup
import requests
import time

# url = https://sofifa.com/
def NextPagesWebScraping(url, offset):
    current_offset = offset

    while requests.get(f"{url}&offset={current_offset}").status_code == 200 and current_offset <= 19980:
        page = requests.get(f"{url}&offset={current_offset}").text
        players_table = CatchWebPageTable(page)

        CatchFeaturesValues(players_table)

        current_offset += 60
        time.sleep(0.5)

        if requests.get(f"{url}&offset={current_offset}").status_code != 200:
            print(f"Error {requests.get('{url}&offset={current_offset}').status_code}")
        else:
            print("All players have been downloaded.")
```

### 5. `ManipulateAndCleanData` Function:

```python
from bs4 import BeautifulSoup
import re

def ManipulateAndCleanData():
    # Split each row to cells
    cleaned_dataset = results_features_values[0].str.split(',', expand=True)

    # Drop the last columns if it is full of "None" values
    if cleaned_dataset.shape[1] > 53:
        delete_last_n_columns = cleaned_dataset.shape[1] - 53
        for i in range(delete_last_n_columns):
            cleaned_dataset.drop(cleaned_dataset.columns[-1], inplace=True, axis=1)

    # Set column names using table headers
    cleaned_dataset.columns = features_names_list[0:len(features_names_list)]
    cleaned_dataset.rename(columns={'Height': 'Height_cm', 'Weight': 'Weight_kg', 'foot': 'Preferred_Foot',
                                    'BP': 'Best_Position', 'Heading Accuracy': 'Heading_Accuracy',
                                    'Short Passing': 'Short_Passing', 'FK Accuracy': 'Free_Kick_Accuracy',
                                    'Long Passing': 'Long_Passing', 'Ball Control': 'Ball_Control',
                                    'Sprint Speed': 'Sprint_Speed', 'Shot Power': 'Shot_Power',
                                    'Long Shots': 'Long_Shots', 'Marking': 'Defensive_Awareness',
                                    'Standing Tackle': 'Standing_Tackle', 'Sliding Tackle': 'Sliding_Tackle',
                                    'GK Diving': 'GK_Diving', 'GK Handling': 'GK_Handling',
                                    'GK Kicking': 'GK_Kicking', 'GK Positioning': 'GK_Positioning',
                                    'GK Reflexes': 'GK_Reflexes', 'W/F': 'Weak_Foot', 'SM': 'Skill_Moves',
                                    'A/W': 'Attacking_Work_Rate', 'D/W': 'Defensive_Work_Rate',
                                    'PAC': 'Pace_Diving', 'SHO': 'Shooting_Handling', 'PAS': 'Passing_Kicking',
                                    'DRI': 'Dribbling_Reflexes', 'DEF': 'Defending_Pace', 'PHY': 'Physical_Position'},
                           inplace=True)

    # Drop the first, "Team & Contract" and "Skill_Moves" columns because they are unmeaningful
    cleaned_dataset.drop(cleaned_dataset.columns[0], inplace=True, axis=1)
    cleaned_dataset.drop(columns=['Team & Contract'], inplace=True, axis=1)
    cleaned_dataset.drop(columns=['Skill_Moves'], inplace=True, axis=1)

    # Fix typos or character errors
    cleaned_dataset["Name"] = cleaned_dataset["Name"].str.replace(r"(\n|LW|ST|RW|LF|CF|RF|CAM|LM|CM|RM|CDM|LWB|LB|CB|RB|RWB|GK)", '', regex=True)
    cleaned_dataset["Name"] = cleaned_dataset["Name"].str.replace(r"[0-9\n]", '', regex=True)
    cleaned_dataset["Height_cm"] = cleaned_dataset["Height_cm"].str.replace(r"(\n| cm)", '', regex=True)
    cleaned_dataset["Weight_kg"] = cleaned_dataset["Weight_kg"].str.replace(" kg", '', regex=False)
    cleaned_dataset["Physical_Position"] = cleaned_dataset["Physical_Position"].str.replace("]", '', regex=False)

    for i in range(0, cleaned_dataset.shape[1]):
        cleaned_dataset.iloc[:, i] = cleaned_dataset.iloc[:, i].str.replace("N/A", '', regex=False)

    # Remove spaces
    for i in range(0, len(cleaned_dataset.columns)):
        cleaned_dataset.iloc[:, i] = cleaned_dataset.iloc[:, i].str.strip()

    # Remove every row which contains only NaN values or empty cells
    index_of_NaN_rows = []
    for i in range(0, cleaned_dataset.shape[0]):
        if cleaned_dataset.iloc[i, :].isnull().values.any() or cleaned_dataset.iloc[i, :].eq("").sum() > 0:
            index_of_NaN_rows.append(i)

    for i in range(0, len(index_of_NaN_rows)):
        cleaned_dataset.drop(labels=index_of_NaN_rows[i], inplace=True, axis=0)

    return cleaned_dataset
```

### 6. `GenerateCSVDataset` Function:

```python
def GenerateCSVDataset(dataset):
    dataset.to_csv("path/FIFA22_Dataset.csv", index=False, encoding="UTF-8", na_rep='NA', mode="a")
```

Note: The above code snippets assume that `CatchWebPageTable`, `features_names_list`, and `features_values_list` are defined and initialized appropriately elsewhere in your code. Additionally, make sure to handle import statements and any other dependencies.

# Complete code

Help rewriting using chatgpt because of problems encountered web copying the code from the document.

```python

from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd

class FIFAWebScraper:
    # url = https://sofifa.com/
    def __init__(self, url):
        self.url = url
        self.features_names_list = []
        self.features_values_list = []
        self.results_features_values = pd.DataFrame()

    def catch_web_page_table(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('table')
    return table


    def catch_features_names(self, table):
        features_names = table.find_all("th")
        for row in features_names:
            cell = str(row)
            self.features_names_list.append(re.sub(re.compile('<.*?>'), '', cell))

    def catch_features_values(self, table):
        features_values = table.find_all("tr")
        for row in features_values:
            cells = re.sub(re.compile('Jun(.+?)</span>|<div class=\"tip\">(.+?)</span></div></div>'), '', str(row.find_all("td")))
            self.features_values_list.append(re.sub(re.compile('<.*?>'), '', cells))

        self.results_features_values = pd.DataFrame(self.features_values_list)

    def first_page_web_scraping(self):
        if requests.get(f"{self.url}&offset=0").status_code == 200:
            page = requests.get(f"{self.url}&offset=0").text
            players_table = self.catch_web_page_table(page)

            self.catch_features_names(players_table)
            self.catch_features_values(players_table)

            time.sleep(0.5)
        else:
            print(f"Error {requests.get('{self.url}&offset=0').status_code}")

    def next_pages_web_scraping(self, offset):
        current_offset = offset

        while requests.get(f"{self.url}&offset={current_offset}").status_code == 200 and current_offset <= 19980:
            page = requests.get(f"{self.url}&offset={current_offset}").text
            players_table = self.catch_web_page_table(page)

            self.catch_features_values(players_table)

            current_offset += 60
            time.sleep(0.5)

            if requests.get(f"{self.url}&offset={current_offset}").status_code != 200:
                print(f"Error {requests.get('{self.url}&offset={current_offset}').status_code}")
            else:
                print("All players have been downloaded.")

    def ManipulateAndCleanData():
        # Split each row to cells
        cleaned_dataset = results_features_values[0].str.split(',', expand=True)

        # Drop the last columns if it is full of "None" values
        if cleaned_dataset.shape[1] > 53:
            delete_last_n_columns = cleaned_dataset.shape[1] - 53
            for i in range(delete_last_n_columns):
                cleaned_dataset.drop(cleaned_dataset.columns[-1], inplace=True, axis=1)

        # Set column names using table headers
        cleaned_dataset.columns = features_names_list[0:len(features_names_list)]
        cleaned_dataset.rename(columns={'Height': 'Height_cm', 'Weight': 'Weight_kg', 'foot': 'Preferred_Foot',
                                        'BP': 'Best_Position', 'Heading Accuracy': 'Heading_Accuracy',
                                        'Short Passing': 'Short_Passing', 'FK Accuracy': 'Free_Kick_Accuracy',
                                        'Long Passing': 'Long_Passing', 'Ball Control': 'Ball_Control',
                                        'Sprint Speed': 'Sprint_Speed', 'Shot Power': 'Shot_Power',
                                        'Long Shots': 'Long_Shots', 'Marking': 'Defensive_Awareness',
                                        'Standing Tackle': 'Standing_Tackle', 'Sliding Tackle': 'Sliding_Tackle',
                                        'GK Diving': 'GK_Diving', 'GK Handling': 'GK_Handling',
                                        'GK Kicking': 'GK_Kicking', 'GK Positioning': 'GK_Positioning',
                                        'GK Reflexes': 'GK_Reflexes', 'W/F': 'Weak_Foot', 'SM': 'Skill_Moves',
                                        'A/W': 'Attacking_Work_Rate', 'D/W': 'Defensive_Work_Rate',
                                        'PAC': 'Pace_Diving', 'SHO': 'Shooting_Handling', 'PAS': 'Passing_Kicking',
                                        'DRI': 'Dribbling_Reflexes', 'DEF': 'Defending_Pace', 'PHY': 'Physical_Position'},
                               inplace=True)

        # Drop the first, "Team & Contract" and "Skill_Moves" columns because they are unmeaningful
        cleaned_dataset.drop(cleaned_dataset.columns[0], inplace=True, axis=1)
        cleaned_dataset.drop(columns=['Team & Contract'], inplace=True, axis=1)
        cleaned_dataset.drop(columns=['Skill_Moves'], inplace=True, axis=1)

        # Fix typos or character errors
        cleaned_dataset["Name"] = cleaned_dataset["Name"].str.replace(r"(\n|LW|ST|RW|LF|CF|RF|CAM|LM|CM|RM|CDM|LWB|LB|CB|RB|RWB|GK)", '', regex=True)
        cleaned_dataset["Name"] = cleaned_dataset["Name"].str.replace(r"[0-9\n]", '', regex=True)
        cleaned_dataset["Height_cm"] = cleaned_dataset["Height_cm"].str.replace(r"(\n| cm)", '', regex=True)
        cleaned_dataset["Weight_kg"] = cleaned_dataset["Weight_kg"].str.replace(" kg", '', regex=False)
        cleaned_dataset["Physical_Position"] = cleaned_dataset["Physical_Position"].str.replace("]", '', regex=False)

        for i in range(0, cleaned_dataset.shape[1]):
            cleaned_dataset.iloc[:, i] = cleaned_dataset.iloc[:, i].str.replace("N/A", '', regex=False)

        # Remove spaces
        for i in range(0, len(cleaned_dataset.columns)):
            cleaned_dataset.iloc[:, i] = cleaned_dataset.iloc[:, i].str.strip()

        # Remove every row which contains only NaN values or empty cells
        index_of_NaN_rows = []
        for i in range(0, cleaned_dataset.shape[0]):
            if cleaned_dataset.iloc[i, :].isnull().values.any() or cleaned_dataset.iloc[i, :].eq("").sum() > 0:
                index_of_NaN_rows.append(i)

        for i in range(0, len(index_of_NaN_rows)):
            cleaned_dataset.drop(labels=index_of_NaN_rows[i], inplace=True, axis=0)

        return cleaned_dataset

    def generate_csv_dataset(self, dataset):
        dataset.to_csv("path/FIFA22_Dataset.csv", index=False, encoding="UTF-8", na_rep='NA', mode="a")
```
# Code-Refactoring

```python
from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd


class FIFAWebScraper:
    def __init__(self, url):
        self.url = url
        self.features_names_list = []
        self.features_values_list = []
        self.results_features_values = pd.DataFrame()

    def catch_web_page_table(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('table')
    return table


    def catch_features_names(self, table):
        features_names = table.find_all("th")
        for row in features_names:
            cell = str(row)
            self.features_names_list.append(re.sub(re.compile('<.*?>'), '', cell))

    def catch_features_values(self, table):
        features_values = table.find_all("tr")
        for row in features_values:
            cells = re.sub(
                re.compile('Jun(.+?)</span>|<div class=\"tip\">(.+?)</span></div></div>'), '', str(row.find_all("td")))
            self.features_values_list.append(re.sub(re.compile('<.*?>'), '', cells))

        self.results_features_values = pd.DataFrame(self.features_values_list)

    def first_page_web_scraping(self):
        if requests.get(f"{self.url}&offset=0").status_code == 200:
            page = requests.get(f"{self.url}&offset=0").text
            players_table = self.catch_web_page_table(page)

            self.catch_features_names(players_table)
            self.catch_features_values(players_table)

            time.sleep(0.5)
        else:
            print(f"Error {requests.get('{self.url}&offset=0').status_code}")

    def next_pages_web_scraping(self, offset):
        current_offset = offset

        while requests.get(f"{self.url}&offset={current_offset}").status_code == 200 and current_offset <= 19980:
            page = requests.get(f"{self.url}&offset={current_offset}").text
            players_table = self.catch_web_page_table(page)

            self.catch_features_values(players_table)

            current_offset += 60
            time.sleep(0.5)

            if requests.get(f"{self.url}&offset={current_offset}").status_code != 200:
                print(f"Error {requests.get('{self.url}&offset={current_offset}').status_code}")
            else:
                print("All players have been downloaded.")

    def manipulate_and_clean_data(self):
        # Split each row to cells
        cleaned_dataset = results_features_values[0].str.split(',', expand=True)

        # Drop the last columns if it is full of "None" values
        if cleaned_dataset.shape[1] > 53:
            delete_last_n_columns = cleaned_dataset.shape[1] - 53
            for i in range(delete_last_n_columns):
                cleaned_dataset.drop(cleaned_dataset.columns[-1], inplace=True, axis=1)

        # Set column names using table headers
        cleaned_dataset.columns = features_names_list[0:len(features_names_list)]
        cleaned_dataset.rename(columns={'Height': 'Height_cm', 'Weight': 'Weight_kg', 'foot': 'Preferred_Foot',
                                        'BP': 'Best_Position', 'Heading Accuracy': 'Heading_Accuracy',
                                        'Short Passing': 'Short_Passing', 'FK Accuracy': 'Free_Kick_Accuracy',
                                        'Long Passing': 'Long_Passing', 'Ball Control': 'Ball_Control',
                                        'Sprint Speed': 'Sprint_Speed', 'Shot Power': 'Shot_Power',
                                        'Long Shots': 'Long_Shots', 'Marking': 'Defensive_Awareness',
                                        'Standing Tackle': 'Standing_Tackle', 'Sliding Tackle': 'Sliding_Tackle',
                                        'GK Diving': 'GK_Diving', 'GK Handling': 'GK_Handling',
                                        'GK Kicking': 'GK_Kicking', 'GK Positioning': 'GK_Positioning',
                                        'GK Reflexes': 'GK_Reflexes', 'W/F': 'Weak_Foot', 'SM': 'Skill_Moves',
                                        'A/W': 'Attacking_Work_Rate', 'D/W': 'Defensive_Work_Rate',
                                        'PAC': 'Pace_Diving', 'SHO': 'Shooting_Handling', 'PAS': 'Passing_Kicking',
                                        'DRI': 'Dribbling_Reflexes', 'DEF': 'Defending_Pace', 'PHY': 'Physical_Position'},
                               inplace=True)

        # Drop the first, "Team & Contract" and "Skill_Moves" columns because they are unmeaningful
        cleaned_dataset.drop(cleaned_dataset.columns[0], inplace=True, axis=1)
        cleaned_dataset.drop(columns=['Team & Contract'], inplace=True, axis=1)
        cleaned_dataset.drop(columns=['Skill_Moves'], inplace=True, axis=1)

        # Fix typos or character errors
        cleaned_dataset["Name"] = cleaned_dataset["Name"].str.replace(r"(\n|LW|ST|RW|LF|CF|RF|CAM|LM|CM|RM|CDM|LWB|LB|CB|RB|RWB|GK)", '', regex=True)
        cleaned_dataset["Name"] = cleaned_dataset["Name"].str.replace(r"[0-9\n]", '', regex=True)
        cleaned_dataset["Height_cm"] = cleaned_dataset["Height_cm"].str.replace(r"(\n| cm)", '', regex=True)
        cleaned_dataset["Weight_kg"] = cleaned_dataset["Weight_kg"].str.replace(" kg", '', regex=False)
        cleaned_dataset["Physical_Position"] = cleaned_dataset["Physical_Position"].str.replace("]", '', regex=False)

        for i in range(0, cleaned_dataset.shape[1]):
            cleaned_dataset.iloc[:, i] = cleaned_dataset.iloc[:, i].str.replace("N/A", '', regex=False)

        # Remove spaces
        for i in range(0, len(cleaned_dataset.columns)):
            cleaned_dataset.iloc[:, i] = cleaned_dataset.iloc[:, i].str.strip()

        # Remove every row which contains only NaN values or empty cells
        index_of_NaN_rows = []
        for i in range(0, cleaned_dataset.shape[0]):
            if cleaned_dataset.iloc[i, :].isnull().values.any() or cleaned_dataset.iloc[i, :].eq("").sum() > 0:
                index_of_NaN_rows.append(i)

        for i in range(0, len(index_of_NaN_rows)):
            cleaned_dataset.drop(labels=index_of_NaN_rows[i], inplace=True, axis=0)

        return cleaned_dataset


    def generate_csv_dataset(self, dataset):
        dataset.to_csv("path/FIFA22_Dataset.csv", index=False, encoding="UTF-8", na_rep='NA', mode="a")


def main():
    # This code allows to apply web scraping technique on the first web page from https://sofifa.com/
    url = "https://sofifa.com/"
    scraper = FIFAWebScraper(url)

    scraper.first_page_web_scraping()
    scraper.next_pages_web_scraping(offset=0)

    cleaned_data = scraper.manipulate_and_clean_data()
    scraper.generate_csv_dataset(cleaned_data)


if __name__ == "__main__":
    main()
```

## Observations on the refactored code

**Structure and Functionality:**

- **Class Structure:** The code is well-organized into a class `FIFAWebScraper`, promoting modularity and reusability.
- **Web Scraping:**
    - It correctly fetches data from multiple pages using pagination.
    - It handles potential errors with HTTP status codes.
    - It extracts relevant information from the HTML structure.
- **Data Cleaning and Manipulation:**
    - It cleans and standardizes column names.
    - It removes unnecessary columns.
    - It fixes typos and character errors.
    - It handles missing values and empty cells.
- **CSV Generation:** It creates a CSV file with the cleaned data.

**Key Points:**

- **Ethical Considerations:** Respect the website's terms of service and rate limits to avoid overloading their servers.
- **Error Handling:** Consider more robust error handling for potential exceptions (e.g., network errors, HTML structure changes).
- **Data Validation:** Validate the scraped data to ensure accuracy and consistency.
- **Dynamic Content:** If the website uses JavaScript for dynamic content, explore libraries like Selenium or Playwright for browser automation.
- **Optimization:** Consider using vectorized string operations for potential performance improvements in data cleaning.

**Additional Considerations:**

- **Testing:** Implement unit tests to verify the code's functionality and handle potential changes in the website's structure.
- **Parameterization:** Make the code more adaptable by allowing users to specify the target URL and output file path.
- **Logging:** Add logging to track the scraping process and identify any errors or issues during execution.
