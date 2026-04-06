import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function that reads, reshapes and renames files from wide to long formats for sheets in 5.6
def reshape (wide_files):
    df = pd.read_csv(wide_files) 
    
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")] # drop empty, unamed columns #EDIT THIS!!

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
print(combined_electrcity.head())

#Data visualisation
combined_electrcity['Year'] = pd.to_numeric(combined_electrcity['Year']) # Convert Year to numeric (from str) for plotting
combined_electrcity['Renewable generation share (%)'] = pd.to_numeric(
    combined_electrcity['Renewable generation share (%)']
    .astype(str)
    .str.rstrip('%') # Removing % for the plot
)
combined_electrcity['Total renewable generation'] = pd.to_numeric(
    combined_electrcity['Total renewable generation']
    .astype(str)
    .str.replace(',', '')
)

df = combined_electrcity.copy() # Only plotting these for now

df["Total renewable generation"] = (
    df["Total renewable generation"]
    .astype(str)
    .str.replace(",", "")
)
df["Total renewable generation"] = pd.to_numeric(df["Total renewable generation"])
df["Total wind"] = pd.to_numeric(df["Total wind"].astype(str).str.replace(",", ""))
df["Solar"] = pd.to_numeric(df["Solar"].astype(str).str.replace(",", "")) # WHAT DOEAS THIS ERRORS=COERCE DO? I THINK IT JUST MAKES ANYTHING THAT CAN'T BE CONVERTED TO NUMERIC A NAN, WHICH IS FINE FOR OUR PURPOSES AS WE CAN DROP THESE LATER IF NEEDED. THIS IS USEFUL BECAUSE OF THE POSSIBILITY OF MISSING OR MALFORMATTED DATA IN THE CSV FILES, AND IT PREVENTS THE CODE FROM BREAKING DUE TO CONVERSION ERRORS.

# Sort
df = df.sort_values("Year")


fig, ax = plt.subplots(figsize=(12, 6)) # Creating a wide figure for time series

# Data containers
x_renew = []
y_renew = []
x_wind = []
y_wind = []
x_solar = []
y_solar = []

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
ax.legend()

# --- ANIMATION FUNCTION ---
def update(frame):
    year = df["Year"].iloc[frame]
    renew_val = df["Total renewable generation"].iloc[frame]
    wind_val = df["Total wind"].iloc[frame]
    solar_val = df["Solar"].iloc[frame]

    if renew_val != 0: # Sets markers as none when value is zero so method only appears once producing energy
        x_renew.append(year)
        y_renew.append(renew_val)
    if wind_val >= 1000: # Using threshold as 1000 Gwhs before showing generation on the graph
        x_wind.append(year)
        y_wind.append(wind_val)
    if solar_val >= 1000:
        x_solar.append(year)
        y_solar.append(solar_val)

    line1.set_data(x_renew, y_renew)
    line2.set_data(x_wind, y_wind)
    line3.set_data(x_solar, y_solar)

    return line1, line2, line3

# --- CREATE ANIMATION ---
ani = FuncAnimation(
    fig,
    update,
    frames=len(df),
    interval=150,
    repeat=False
)

plt.tight_layout()
plt.show()

#Plot improvements:
#Keep legend on the  top left handside for the whole plot
# Show the value of each line as its increasing overtime

# Think about how you can  plot things better to better answer the question.