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

    df_final = df_long.pivot( #Pivoting to have fuel types as columns but no aggregation
        index="Year",
        columns="Fuel",
        values="Value"
    ).reset_index()

    print(df_long.head())

    output_name = wide_files.replace(".csv", "-long.csv")
    df_final.to_csv(output_name, index=False) #saved to renamed csv
    return df_final

wide_files = ["electricity-generated.csv","share-electricity-generated.csv"]

gen_df = reshape("electricity-generated.csv")
#Altering column names for share sheet so they don't completely match electricity-generated
share_df = reshape("share-electricity-generated.csv")
share_df.columns = [
    col if col == "Year" else col + " (%)"
    for col in share_df.columns
]
share_df.to_csv("share-electricity-generated-long.csv", index=False) #Saving (%) column addition

combined_electrcity = pd.merge(gen_df, share_df, on="Year", how="inner") 
# Merge can be inner as you won't have missing years not in both datasets because of the nature of the datasets.

# Organising alphabetically for aesthetics to have share next to generation for each fuel type
cols = ["Year"] + sorted([col for col in combined_electrcity.columns if col != "Year"])
combined_electrcity = combined_electrcity[cols] 
combined_electrcity.columns = combined_electrcity.columns.str.replace(r"\s*\[.*?\]", "", regex=True) #removing notes

# #Data visualisation

# # Creating a new dataframe with aggregated years average shares of generation to visualise later:
# df = combined_electrcity.copy()
# df["Year"] = pd.to_numeric(df["Year"])  # Convert Year to numeric for comparisons
# percent_cols = [col for col in df.columns if '%' in col]
# df[percent_cols] = df[percent_cols].replace('%', '', regex=True).astype(float) # removing % sings

# # Define period of interest for aggregation
# periods = { 
#     "2020-2024": (2020, 2024),
#     "2010-2014": (2010, 2014),
#     "2005-2010": (2005, 2010),
#     "2000-2005": (2000, 2005),
# }

# avg_data = [] # New dataframe for grouped averages

# for label, (start, end) in periods.items(): #READ UNDERSTAND AND COMMENT THIS!!
#     subset = df[(df["Year"] >= start) & (df["Year"] <= end)]
    
#     means = subset[percent_cols].mean()
#     means["Period"] = label
    
#     avg_data.append(means)

# avg_df = pd.DataFrame(avg_data).set_index("Period")

# #Dropping columns that double count variables
# avg_df.drop(
#     columns=["Renewable generation share (%)",
#     "Total all generating companies (%)",
#     "Onshore wind (%)",
#     "Offshore wind (%)", 
#     "Renewable generation share (%)"], inplace=True)

# # # Plotting figures in interactive pie charts (plotly)

# all_labels = avg_df.columns
# avg_df = avg_df.sort_index() # Sort for chronological orderings in final visualisation.

# cmap = plt.get_cmap("tab20b") # Using constant colour palette between visualisations
# colors = [cmap(i) for i in range(len(avg_df.columns))]

# def rgba_to_hex(rgba): # Convert RGBA to Hexadecimal for Plotly recognition of colour palette
#     return '#%02x%02x%02x' % tuple(int(255*x) for x in rgba[:3])

# colors = [rgba_to_hex(c) for c in colors]
# color_map = {
#     label: colors[i % len(colors)]
#     for i, label in enumerate(avg_df.columns)
# }

# rows = 2
# cols = 2

# fig = make_subplots( #Creating visual with 4 pie charts all in one visual from years of interest chosen using subplots
#     rows=rows,
#     cols=cols,
#     specs=[[{'type':'domain'}]*cols for _ in range(rows)],
#     subplot_titles=avg_df.index
# )

# positions = [(1,1), (1,2), (2,1), (2,2)] #Ordering the images chronolgically from left to right.

# for (period, pos) in zip(avg_df.index, positions): #Looping through time periods
    
#     values = avg_df.loc[period]
    
#     fig.add_trace(
#         go.Pie(
#             labels=values.index,
#             values=values.values,
#             name=period,
#             textinfo='none',  # removes numbers on pie wedges
#             hovertemplate='%{label}: %{value:.2f}%', # interactive hover % display
#             marker=dict(
#                 colors=[color_map[label] for label in values.index] # consistent colors 
#             )
#         ),
#         row=pos[0], col=pos[1]
#     )

# fig.update_layout(
#     title_text="Energy Generation Shares Across Time Periods",
#     showlegend=True
# )
# fig.write_html("combined_energy_pie_charts.html") # Saved as an interactive html
# fig.show()

# # ### Save to the visualisations folder in the Git repo






# # Line graph animation of renewable energy generation over time
df = combined_electrcity.copy() # Only plotting these for now
df["Year"] = pd.to_numeric(df["Year"])  # Convert Year to numeric for plotting and animation

df["Total renewable generation"] = (
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

# Data containers # WHAT EXACTLY IS THIS??
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
ax.set_ylabel("Value") #CHANGE Y-AXIS TO UNIT!!
ax.set_title("Renewable Energy Trends Over Time")

ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
ax.legend(loc="upper left")

#Adding text labels to the plot points for the visualisation
text_renew = ax.text(0, 0, "", fontsize=9)
text_wind = ax.text(0, 0, "", fontsize=9)
text_solar = ax.text(0, 0, "", fontsize=9)

offset = 500  # vertical offset for readability

def update(frame):
    current_df = df.iloc[:frame + 1]

    # Apply your conditions
    renew_data = current_df[current_df["Total renewable generation"] != 0]
    wind_data = current_df[current_df["Total wind"] >= 1000] # Using threshold as 1000 Gwhs before showing generation on the graph
    solar_data = current_df[current_df["Solar"] >= 1000]

    # Update lines
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

    return line1, line2, line3, text_renew, text_wind, text_solar

ani1 = FuncAnimation(
    fig,
    update,
    frames=len(df),
    interval=400,
    repeat=False
)

plt.tight_layout()

output_folder = r"C:\\Users\\mm147\\Empirical-Project\\Data-Science-Empirical-Project\\Visualisations" 
os.makedirs(output_folder, exist_ok=True)

gif_path = os.path.join(output_folder, "annual_renewable_generation.gif")
ani1.save(gif_path, writer=PillowWriter(fps=10))


#Repeat make of the line graph animation for monthly data generation of MPPs to see cyclical nature.
monthly_gen = pd.read_csv("monthly-energy-generation.csv") # new dataset
monthly_gen = monthly_gen.loc[:, ~monthly_gen.columns.str.contains("^Unnamed")] # drop empty, unnamed columns

monthly_gen.columns = monthly_gen.columns.str.replace(r"\s*\[.*?\]", "", regex=True) # removing notes

df_monthly = monthly_gen[["Month", "Total electricity supplied by MPPs", "Total wind", "Solar"]]
print(df_monthly.head())

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

fig, ax = plt.subplots(figsize=(12, 6))

line1, = ax.plot([], [], marker='x', linewidth=1, label="Total Electricity (MPPs)")
line2, = ax.plot([], [], marker='x', linewidth=1, label="Wind")
line3, = ax.plot([], [], marker='x', linewidth=1, label="Solar")

ax.set_xlim(df["Month"].min(), df["Month"].max())
ax.set_ylim(0, df["Total electricity supplied by MPPs"].max() * 1.1)

ax.set_xlabel("Year")
ax.set_ylabel("Electricity (GWh)")
ax.set_title("Monthly Electricity Generation Trends")

ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
ax.legend(loc="upper left")

text_main = ax.text(0, 0, "", fontsize=9)
text_wind = ax.text(0, 0, "", fontsize=9)
text_solar = ax.text(0, 0, "", fontsize=9)

offset = df["Total electricity supplied by MPPs"].max() * 0.02

def update(frame):
    current_df = df.iloc[:frame + 1]

    main_data = current_df.dropna(subset=["Total electricity supplied by MPPs"])
    wind_data = current_df[current_df["Total wind"].notna()]
    solar_data = current_df[current_df["Solar"].notna()]

    # Update lines
    line1.set_data(main_data["Month"], main_data["Total electricity supplied by MPPs"])
    line2.set_data(wind_data["Month"], wind_data["Total wind"])
    line3.set_data(solar_data["Month"], solar_data["Solar"])

    # --- Labels ---
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

ani2 = FuncAnimation(
    fig,
    update,
    frames=len(df),
    interval=100,
    repeat=False
)

plt.tight_layout()

os.makedirs(output_folder, exist_ok=True)
gif_path = os.path.join(output_folder, "monthly-mpps-renewable-generation.gif")
ani2.save(gif_path, writer=PillowWriter(fps=10))