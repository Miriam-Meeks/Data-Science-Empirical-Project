from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#Selinium setup to scrape
options = Options()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)
driver.get("https://grid.iamkate.com/") #Identifying site page to scrape

time.sleep(5) # Adding a wait to mimic human behaviour (to avoid blocking)

actions = ActionChains(driver)

#Tried previously to extract SVG elements (aria labels) but this didn't work so instead extracting all visible text
element = driver.find_element(By.CSS_SELECTOR, "svg")
actions.move_to_element(element).perform()
time.sleep(1) # Wait for content to load

text = driver.find_element(By.TAG_NAME, "body").text #Extracting all visible text found and saving to text variable
driver.quit() # end the scrape

#Function to extract the first occurrence of a pattern and keep that. 
#This is because site hast past days generation after todays generation and so todays scraped values are replaced with the following yesterday's values.
def extract_first(pattern):
    match = re.search(pattern, text)
    return float(match.group(1)) if match else None

demand = extract_first(r"Demand\s+([\d\.]+)GW") # Removing value with regex from units to then put numerically into a pie chart
generation = extract_first(r"Generation\s+([\d\.]+)GW")
transfers = extract_first(r"Transfers\s+([\d\.]+)GW")

main_section = text.split("Past day")[0]

lines = main_section.split("\n")

data = {}

for line in lines:
    match = re.match(r"([A-Za-z\s]+)\s+([\d\.]+)\s+([\d\.]+)", line) #Regex matching
    
    if match:
        fuel = match.group(1).strip()
        gw = float(match.group(2))

        # Keep ONLY actual generation sources (no aggregates or transfers)
        if fuel not in [
            "Fossil fuels", "Renewables", "Other sources",
            "Belgium", "Denmark", "France", "Ireland",
            "Netherlands", "Norway",
            "Pumped storage", "Battery storage"
        ]:
            data[fuel] = gw


#print("\nCLEAN DATA (CURRENT):")

for k, v in data.items():
    print(k, v)

cmap = plt.get_cmap("tab20b") # Maintaining constant colourmap
colors = [cmap(i) for i in range(len(data))]

#Plotting pie chart to represent scraped data
labels = list(data.keys()) #Saving data in lists to be extracted later
values = list(data.values())

#Making sure the pie chart is interactive (hover)
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values, #Data used from the scrape
    name="", 
    hovertemplate="<b>%{label}</b><br>%{value:.2f} GW<br>%{percent:.1%}<extra></extra>", #Later edit to remove trace from the label during hover
    marker=dict(colors=[f"rgba({int(r*255)},{int(g*255)},{int(b*255)},1)" for r,g,b,_ in colors]),
    textinfo='label'
)])

fig.update_layout(
    title="UK Energy Generation Mix (Live Today)",
    annotations=[ # Adding demand, generation and transfers label below chart (from scrape)
        dict(
            text=f"Demand: {demand} GW | Generation: {generation} GW | Transfers: {transfers} GW",
            x=0.5,
            y=-0.1,
            showarrow=False,
            xref="paper",
            yref="paper"
        )
    ]
)

fig.write_html("site/Visualisations/scraped-generation-mix.html") #Saving as html in Visualisations

#fig.show()