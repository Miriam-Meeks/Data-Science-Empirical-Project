import time
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re

# # Web Scrape data off site iamkate to then save as in a pie chart form as a replica of the site.
# # Try and make this a loop daily/ when run will it change between days?

#ARIA-LABEL OPTION DIDNT WORK HERE FOR SCRAPING PIE CHARTS

# --- Setup ---
# options = Options()
# options.add_argument("--headless=new")

# driver = webdriver.Chrome(options=options)
# driver.get("https://grid.iamkate.com/")

# # --- Function to extract clean number ---
# def get_value(label):
#     elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{label}')]")

#     for el in elements:
#         parent = el.find_element(By.XPATH, "..")
#         text = parent.text

#         # Extract first number (handles decimals)
#         match = re.search(r"\d+\.?\d*", text)
#         if match:
#             return float(match.group())

#     return None

# # --- Extract data ---
# demand = get_value("Demand")
# generation = get_value("Generation")
# transfers = get_value("Transfers")
# nuclear = get_value("Nuclear")

# # --- Print results ---
# print("Demand:", demand)
# print("Generation:", generation)
# print("Transfers:", transfers)
# print("Nuclear:", nuclear)

# driver.quit()

# #Defining labels and values for a pie chart
# labels = ["Generation", "Transfers"]
# values = [generation, transfers]

# #Creating a pie chart with web scraped data to replicate the one on the site.
# plt.figure()
# plt.pie(values, labels=labels, autopct='%1.1f%%')
# plt.title(f"Demand: {demand} GW")

# # --- Save image ---
# plt.savefig("grid_pie_chart.png")

# print("Saved as grid_pie_chart.png")





# --- Setup ---
options = Options()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)
driver.get("https://grid.iamkate.com/")

time.sleep(5)

actions = ActionChains(driver)

# Try both SVG and canvas fallback
elements = driver.find_elements(By.CSS_SELECTOR, "svg path")

data = []

for el in elements:
    try:
        actions.move_to_element(el).perform()
        time.sleep(0.5)

        # Try to grab tooltip (common selectors)
        tooltips = driver.find_elements(By.CSS_SELECTOR, "div, span")

        for t in tooltips:
            text = t.text.strip()

            # Look for GW values in tooltip
            if "GW" in text and "%" in text:
                print("RAW TOOLTIP:", text)

                match = re.search(r"(.+?)\s+([\d\.]+)\s*GW.*?([\d\.]+)%", text)
                if match:
                    data.append({
                        "fuel": match.group(1),
                        "GW": float(match.group(2)),
                        "percent": float(match.group(3))
                    })

                break

    except Exception as e:
        continue

driver.quit()

print("\nParsed Data:")
for d in data:
    print(d)

#Scraped the correct things just need to plot into a pie chart the correct things.