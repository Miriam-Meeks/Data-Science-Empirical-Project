import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np 
import plotly.express as px # for interactive visuals of changing energy generation shares over time.
from plotly.subplots import make_subplots # for merging interactive visuals looped
import plotly.graph_objects as go
import os

# Function that reads, reshapes and renames files from wide to long formats for sheets in 5.6
def reshape (wide_files):
    df = pd.read_csv(wide_files) 
    
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")] # drop empty, unamed columns

    df.columns = df.columns.str.strip() #removing white space from all columns
    df["Fuel"] = df["Fuel"].astype(str).str.strip()
    df["Generation type"] = df["Generation type"].astype(str).str.strip()

    df = df[df["Generation type"] == "All generating companies"] # interested in total generated output
    df = df.drop(columns=["Generation type"]) 

    df_long = df.melt( 
        id_vars=["Fuel"],    
        var_name="Year",     
        value_name="Value"
    )

    df_long["Fuel"] = df_long["Fuel"].str.replace(r"\s*\[.*?\]", "", regex=True) #removing notes after Fuel type

    df_final = df_long.pivot( #Pivoting to have fuel types as columns but no aggregation (NOT pivot_table)
        index="Year",
        columns="Fuel",
        values="Value"
    ).reset_index()

    #print(df_long.head())

    output_name = wide_files.replace(".csv", "-long.csv")
    df_final.to_csv(output_name, index=False) #saved to renamed csv
    return df_final

wide_files = ["csv-raw/electricity-generated.csv","csv-raw/share-electricity-generated.csv"]

gen_df = reshape("csv-raw/electricity-generated.csv") # Passing csv through re-shape function
gen_df.to_csv("csv-reshaped/electricity-generated-long.csv", index=False)
#Altering column names for share sheet so they don't completely match electricity-generated
share_df = reshape("csv-raw/share-electricity-generated.csv")
share_df.columns = [
    col if col == "Year" else col + " (%)"
    for col in share_df.columns
]
share_df.to_csv("csv-reshaped/share-electricity-generated-long.csv", index=False) #Saving (%) column addition

#Aggregation: merging reshaped dataframes
combined_electrcity = pd.merge(gen_df, share_df, on="Year", how="inner") 

# Merge can be inner as you won't have missing years not in both datasets because of the nature of the datasets.

# Organising alphabetically for aesthetics to have share next to generation for each fuel type
cols = ["Year"] + sorted([col for col in combined_electrcity.columns if col != "Year"])
combined_electrcity = combined_electrcity[cols] 
combined_electrcity.columns = combined_electrcity.columns.str.replace(r"\s*\[.*?\]", "", regex=True) #removing notes
#print(combined_electrcity.head())

#Average Energy generation shares across time visualisation
# Creating a new dataframe with aggregated years average shares of generation to visualise later:
'''Initially tried using share (%) columns but aggregated this did not work as shares averaged gives
 a disproportionate pie chart so second try shown below, summing and averaging absolute values to give
 representative pie charts'''
#Note pie charts do not have to add to 100 because of transfers
df = combined_electrcity.copy()
df.columns = df.columns.str.strip() # Removing white space from columns
df["Year"] = pd.to_numeric(df["Year"])  # Convert Year to numeric for comparisons
df = df.loc[:, ~df.columns.str.contains("%")] # Removing % share columns

#Dropping columns like total wind to avoid double counting so pies add to 100
cols_to_drop = [
    "Total all generating companies",
    "Total fossil fuel generation",
    "Total low carbon generation",
    "Total renewable generation",
    "Total wind"
]

df.drop(columns=cols_to_drop, inplace=True) 

for col in df.columns: # Converting to numeric for plotting
    if col != "Year":
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col])


# Define period of interest for aggregation
periods = { 
    "2020-2024": (2020, 2024),
    "2010-2014": (2010, 2014),
    "2005-2010": (2005, 2010),
    "2000-2005": (2000, 2005),
}

fuel_cols = [col for col in df.columns if col != "Year"]

share_data = [] # Computing shares for each fuel for pies

for label, (start, end) in periods.items():
    subset = df[(df["Year"] >= start) & (df["Year"] <= end)] # Within time period for aggregation
    
    # Sum generation over period to find %
    totals = subset[fuel_cols].sum()
    
    # Convert to % to plot in representative pie charts 
    shares = totals / totals.sum() * 100
    
    shares["Period"] = label
    share_data.append(shares)

avg_df = pd.DataFrame(share_data).set_index("Period")
avg_df = avg_df.sort_index()
fuel_order = [ # Making a fuel order to be shown consistently in each pie chart
    "Coal",
    "Gas",
    "Oil",
    "Nuclear",
    "Hydro (natural flow)",
    "Onshore wind",
    "Offshore wind",
    "Solar",
    "Thermal renewables",
    "Other fuels",
    "Energy storage"
]

# Keep only columns that exist
fuel_order = [f for f in fuel_order if f in avg_df.columns]

# Each pie chart will no have the same fuel order for each year, changes should be easier to see.
avg_df = avg_df[fuel_order] 

#print("Row sums (should be ~100):") #Verifies sums to 100
#print(avg_df.sum(axis=1))

# Plotting figures in interactive pie charts (plotly)
cmap = plt.get_cmap("tab20b") #tab20b is the consistent colour palette between visualisations
colors = [cmap(i) for i in range(len(avg_df.columns))]

def rgba_to_hex(rgba): #Convert RGBA to Hexadecimal for Plotly recognition of colour palette
    return '#%02x%02x%02x' % tuple(int(255*x) for x in rgba[:3])

colors = [rgba_to_hex(c) for c in colors]

color_map = {
    label: colors[i % len(colors)]
    for i, label in enumerate(avg_df.columns)
}

# Subplot grid
rows, cols = 2, 2

fig = make_subplots( #Creating visual with 4 pie charts all in one visual from years of interest chosen using subplots
    rows=rows,
    cols=cols,
    specs=[[{'type':'domain'}]*cols for _ in range(rows)],
    subplot_titles=avg_df.index
)

positions = [(1,1), (1,2), (2,1), (2,2)] # Ordering pie charts chronologically by years aggregated

for (period, pos) in zip(avg_df.index, positions): #Looping through time periods
    values = avg_df.loc[period]
    
    fig.add_trace( # Making interactive pie chart with hover feature, with Plotly.
        go.Pie(
            labels=values.index,
            values=values.values,
            name=period,
            textinfo='none',
            hovertemplate='%{label}: %{value:.2f}%',
            marker=dict(
                colors=[color_map[label] for label in values.index]
            )
        ),
        row=pos[0], col=pos[1]
    )

fig.update_layout( # Adding title and legend
    title_text="Average Energy Generation Shares Across Time Periods",
    showlegend=True
)

fig.write_html("Visualisations/combined_energy_pie_charts.html") # Saved as an interactive html in visualisations
#fig.show()


# Line graph animation of renewable energy generation over time
df = combined_electrcity.copy() # Only plotting these for now
df["Year"] = pd.to_numeric(df["Year"])  # Convert Year to numeric for plotting and animation

df["Total renewable generation"] = ( #Removing commas in dataframe with spaces
    df["Total renewable generation"]
    .astype(str)
    .str.replace(",", "")
)

# Converting to numeric for plotting and later data manipulation
df["Total renewable generation"] = pd.to_numeric(df["Total renewable generation"])
df["Total wind"] = pd.to_numeric(df["Total wind"].astype(str).str.replace(",", ""))
df["Solar"] = pd.to_numeric(df["Solar"].astype(str).str.replace(",", "")) 

# Sorting values for visualisation
df = df.sort_values("Year")

fig, ax = plt.subplots(figsize=(12, 6)) # Creating a wide figure for time series

# Creating Data containers for each frame
x_renew, y_renew = [], []
x_wind, y_wind = [], []
x_solar, y_solar = [], []

# Lines (thin + x markers)
line1, = ax.plot([], [], marker='x', linewidth=1, label="Renewables (GWh)")
line2, = ax.plot([], [], marker='x', linewidth=1, label="Wind")
line3, = ax.plot([], [], marker='x', linewidth=1, label="Solar") #Looking at wind and solar generation

# Axis settings
ax.set_xlim(1995, 2025)
ax.set_ylim(0, (df["Total renewable generation"].max()+10000)) # Adding extra space on y-axis for clarity

ax.set_xlabel("Year")
ax.set_ylabel("Energy Generation (GWh)")
ax.set_title("Renewable Energy Trends Over Time")

ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
ax.legend(loc="upper left")

#Adding text labels to the plot points for the visualisation
text_renew = ax.text(0, 0, "", fontsize=9)
text_wind = ax.text(0, 0, "", fontsize=9)
text_solar = ax.text(0, 0, "", fontsize=9)

offset = 500  # vertical offset for readability

def update(frame): # Creating function to loop through frames fro animation
    current_df = df.iloc[:frame + 1]

    # Apply your conditions
    renew_data = current_df[current_df["Total renewable generation"] != 0]
    wind_data = current_df[current_df["Total wind"] >= 1000] # Using threshold as 1000 Gwhs before showing generation on the graph (otherwise too small)
    solar_data = current_df[current_df["Solar"] >= 1000]

    # Update lines each frame
    line1.set_data(renew_data["Year"], renew_data["Total renewable generation"])
    line2.set_data(wind_data["Year"], wind_data["Total wind"])
    line3.set_data(solar_data["Year"], solar_data["Solar"])

    # Updating text labels with if statement for latest updated points:
    if not renew_data.empty: # Sets markers as none when data is empty/0 so renewable only appears once producing enough energy
        x, y = renew_data["Year"].iloc[-1], renew_data["Total renewable generation"].iloc[-1]
        text_renew.set_position((x, y + offset))
        text_renew.set_text(f"{y:,.0f}")

    if not wind_data.empty:
        x, y = wind_data["Year"].iloc[-1], wind_data["Total wind"].iloc[-1]
        text_wind.set_position((x, y + offset))
        text_wind.set_text(f"{y:,.0f}")

    if not solar_data.empty:
        x, y = solar_data["Year"].iloc[-1], solar_data["Solar"].iloc[-1]
        text_solar.set_position((x, y + offset))
        text_solar.set_text(f"{y:,.0f}")

    return line1, line2, line3, text_renew, text_wind, text_solar #Draw each line and label each frame, if requirements met (return)

#Animation created, with 300ms between each frame
ani1 = FuncAnimation(
    fig,
    update,
    frames=len(df),
    interval=300,
    repeat=False
)

plt.tight_layout()

output_folder = r"C:\\Users\\mm147\\Empirical-Project\\Data-Science-Empirical-Project\\Visualisations" 
os.makedirs(output_folder, exist_ok=True)

gif_path = os.path.join(output_folder, "annual-renewable-generation.gif") # Saving to Visualisations folder as gif
ani1.save(gif_path, writer=PillowWriter(fps=10))

#New dataset
#Importing and using a monthly dataset to briefly look at smaller, seasonal variations
monthly_gen = pd.read_csv("csv-raw/monthly-energy-generation.csv") # new dataset
monthly_gen = monthly_gen.loc[:, ~monthly_gen.columns.str.contains("^Unnamed")] # drop empty, unnamed columns

monthly_gen.columns = monthly_gen.columns.str.replace(r"\s*\[.*?\]", "", regex=True) # removing notes

df_monthly = monthly_gen[["Month", "Total electricity supplied by MPPs", "Total wind", "Solar"]]
print(df_monthly.head())

#Repeat make of the line graph animation for monthly data generation of MPPs to see cyclical nature.
df = df_monthly.copy()

# Clean Month values and convert to datetime (repeated process for before, look to previous comments)
df["Month"] = (
    df["Month"]
    .astype(str)
    .str.replace(r"\s*\[.*?\]", "", regex=True)
    .str.strip()
)
df["Month"] = pd.to_datetime(df["Month"], format="%B %Y")

# Ensure numeric
df["Total electricity supplied by MPPs"] = pd.to_numeric(
    df["Total electricity supplied by MPPs"]
)
df["Total wind"] = pd.to_numeric(df["Total wind"])
df["Solar"] = pd.to_numeric(df["Solar"])

# Sort by time
df = df.sort_values("Month")

fig, ax = plt.subplots(figsize=(12, 6)) #Standard dimensions fixed

line1, = ax.plot([], [], marker='x', linewidth=1, label="Total Electricity (MPPs)")
line2, = ax.plot([], [], marker='x', linewidth=1, label="Wind")
line3, = ax.plot([], [], marker='x', linewidth=1, label="Solar")

ax.set_xlim(df["Month"].min(), df["Month"].max()) # Setting limits
ax.set_ylim(0, df["Total electricity supplied by MPPs"].max() * 1.1)

ax.set_xlabel("Year")
ax.set_ylabel("Electricity (TWh)")
ax.set_title("Electricity supplied (net) by Major Power Producers (MPPs) monthly trends")

ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
ax.legend(loc="upper left")

text_main = ax.text(0, 0, "", fontsize=9)
text_wind = ax.text(0, 0, "", fontsize=9)
text_solar = ax.text(0, 0, "", fontsize=9)

offset = df["Total electricity supplied by MPPs"].max() * 0.02

def update(frame): # Creating frame animations
    current_df = df.iloc[:frame + 1]

    main_data = current_df.dropna(subset=["Total electricity supplied by MPPs"])
    wind_data = current_df[current_df["Total wind"].notna()]
    solar_data = current_df[current_df["Solar"].notna()] # Plotting non-empty values

    # Update lines
    line1.set_data(main_data["Month"], main_data["Total electricity supplied by MPPs"])
    line2.set_data(wind_data["Month"], wind_data["Total wind"])
    line3.set_data(solar_data["Month"], solar_data["Solar"])

    #Labels postioning and text setting
    if not main_data.empty:
        x, y = main_data["Month"].iloc[-1], main_data["Total electricity supplied by MPPs"].iloc[-1]
        text_main.set_position((x, y + offset))
        text_main.set_text(f"{y:.2f}")

    if not wind_data.empty:
        x, y = wind_data["Month"].iloc[-1], wind_data["Total wind"].iloc[-1]
        text_wind.set_position((x, y + offset))
        text_wind.set_text(f"{y:.2f}")

    if not solar_data.empty:
        x, y = solar_data["Month"].iloc[-1], solar_data["Solar"].iloc[-1]
        text_solar.set_position((x, y + offset))
        text_solar.set_text(f"{y:.2f}")

    return line1, line2, line3, text_main, text_wind, text_solar

#Animating monthly renewable generation
ani2 = FuncAnimation(
    fig,
    update,
    frames=len(df),
    interval=100,
    repeat=False
)

plt.tight_layout()

os.makedirs(output_folder, exist_ok=True)
gif_path = os.path.join(output_folder, "monthly-mpps-renewable-generation.gif") # Saving to Visualisation folder as gif
ani2.save(gif_path, writer=PillowWriter(fps=10))

#Interactive (hover) line graph for monthly wind generation over time
df = df_monthly.copy()
#print(df.head())

# Clean Month values and convert to datetime
df["Month"] = (
    df["Month"]
    .astype(str)
    .str.replace(r"\s*\[.*?\]", "", regex=True)
    .str.strip()
)
df["Month"] = pd.to_datetime(df["Month"], format="%B %Y", errors="coerce")

# Ensure numeric
df["Total wind"] = pd.to_numeric(df["Total wind"], errors="coerce")

# Drop rows where wind is NaN
df = df.dropna(subset=["Total wind"])

# Sort just in case
df = df.sort_values("Month")

# Create interactive plot with plotly express
fig = px.line(
    df,
    x="Month",
    y="Total wind",
    title="MPPs Monthly Wind Generation Over Time (UK)",
    markers=True
)

#Improving aesthetic
fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Wind Generation (TWh)",
    hovermode="x unified", # Best hover mode

    # White background
    plot_bgcolor="white",
    paper_bgcolor="white",

    # Gridlines
    xaxis=dict(
        showgrid=True,
        gridcolor="lightgrey",
        dtick="M12"  # major grid line for every year
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="lightgrey"
    )
)

# Cleaner hover labels
fig.update_traces(
    hovertemplate="Date: %{x|%b %Y}<br>Wind: %{y:.2f}<extra></extra>"
)

# Range slider for time series and for good user interactivity within the visualisation
fig.update_layout(
    xaxis_rangeslider_visible=True
)

fig.write_html("Visualisations/monthly-wind-generation.html") # Saved as html visualisation
#fig.show()