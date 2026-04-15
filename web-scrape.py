from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# --- Setup Selenium ---
options = Options()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)
driver.get("https://grid.iamkate.com/")

time.sleep(5)

actions = ActionChains(driver)

# --- Trigger tooltip ONCE ---
element = driver.find_element(By.CSS_SELECTOR, "svg")
actions.move_to_element(element).perform()
time.sleep(1)

# --- Get full page text ---
text = driver.find_element(By.TAG_NAME, "body").text
driver.quit()


# =========================
# 🔍 Extract TOP-LEVEL values (FIRST occurrence only)
# =========================

def extract_first(pattern):
    match = re.search(pattern, text)
    return float(match.group(1)) if match else None

demand = extract_first(r"Demand\s+([\d\.]+)GW")
generation = extract_first(r"Generation\s+([\d\.]+)GW")
transfers = extract_first(r"Transfers\s+([\d\.]+)GW")


# =========================
# 🔍 Extract ONLY FIRST dataset (before "Past day")
# =========================

main_section = text.split("Past day")[0]

lines = main_section.split("\n")

data = {}

for line in lines:
    match = re.match(r"([A-Za-z\s]+)\s+([\d\.]+)\s+([\d\.]+)", line)
    
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


print("\nCLEAN DATA (CURRENT):")
for k, v in data.items():
    print(k, v)


# =========================
# 🎨 Use tab20b colormap
# =========================

cmap = plt.get_cmap("tab20b")
colors = [cmap(i) for i in range(len(data))]


# =========================
# 📊 Plot interactive pie (Plotly)
# =========================

labels = list(data.keys())
values = list(data.values())

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    name="",  # 👈 this removes "trace 0"
    #hovertemplate="<b>%{label}</b><br>%{value} GW<br>%{percent}<extra></extra>",
    hovertemplate="<b>%{label}</b><br>%{value:.2f} GW<br>%{percent:.1%}<extra></extra>",
    marker=dict(colors=[f"rgba({int(r*255)},{int(g*255)},{int(b*255)},1)" for r,g,b,_ in colors]),
    textinfo='label'
)])

# --- Add annotation (below chart) ---
fig.update_layout(
    title="UK Energy Generation Mix (Live Today)",
    annotations=[
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

fig.write_html("Visualisations/scraped-generation-mix.html") 

fig.show()