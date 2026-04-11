import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation # for creating animation
import os #for saving video animation

df = pd.read_csv("net-imports.csv")

df = df.drop(columns=["Total Imports (to UK)",
    "Total Exports (from UK)",
    "Net imports (to UK)"
]) #Removing columns of no interest currently

#reshape trade balance sheet to plot trade balance over time
df_long = df.melt(
    id_vars=["Year"],
    var_name="Type",
    value_name="Value"
)

#Using regex to extract
df_long["Variable"] = df_long["Type"].str.extract(r"^(Imports|Exports|Net imports)")
df_long["Country"] = df_long["Type"].str.extract(r"\((.*?)\)") # Extracts countries trading in type column

df_long["Country"] = (
    df_long["Country"]
    .str.replace(r"\s*\[.*?\]", "", regex=True) # remove notes in column
    #.str.replace('Wales','UK') # Replacing NI and Wales with UK so that the formatting works with the pivot
    .str.replace("Northern Ireland", "UK")
    .str.replace("Wales", "UK")
    .str.replace(" to UK", "") # remove "to UK"
    .str.replace("UK to ", "")
    .str.strip() # cleans whitespace and standardises
)

# Drop rows where NaN in Variable, i.e. removing transfers within UK columns
df_long = df_long.dropna(subset=['Variable'])

# Converting value to numeric, removing commas only to allow for summing in the pivot
df_long["Value"] = (
    df_long["Value"]
    .astype(str)
    .str.replace(',', '') # Removing commas from values to make them numeric
)   
df_long["Value"] = pd.to_numeric(df_long["Value"]) # Converting to numeric

#Removing rows of NaN in value column so the later sum in pivot works (as Nan seems to mess this up)
    #Previously had trouble using pivot and pivot tables because of this summing/ counting with Nan with the repeat of Ireland to UK.
df_long = df_long.dropna(subset=["Value"]) # Key for pivot table to reshape correclty

#Using a pivot table to group and reshape the data
df_final = df_long.pivot_table(
    index=["Year", "Country"],
    columns="Variable",
    values="Value",
    aggfunc="sum"   # best choice for trade data acccording to AI
).reset_index()

print(df_final.head())
df_final.to_csv("net-imports-long.csv", index=False)


#Data Viualsiation
df_trade = pd.read_csv("net-imports-long.csv")
df_trade = df_trade[(df_trade["Year"] >= 2017) & (df_trade["Year"] <= 2024)] # To show years that we have trade data for more countries
df_trade["Total"] = df_trade["Imports"] + df_trade["Exports"]
#WORTH TRYING TO ORDER BY COUNTRIES WITH THE LARGEST NUMBER OF OCCURRENCES IN THE DATASET!! THEN HAVING ALL DATES!!!

country_order = ( # Ordering countries by highest overall trade (imports + exports) for the animation
    df_trade.groupby("Country")["Total"]
    .mean()
    .sort_values(ascending=True)   # smallest at bottom, largest at top
    .index
)

# Create a stable color mapping for each country across frames
all_countries = list(country_order)
country_colors = {
    country: plt.cm.tab20b(i / max(len(all_countries) - 1, 1)) # Chosen color pallette
    for i, country in enumerate(all_countries)
}

frames = df_trade["Year"].unique()

# Using ax to allow for animation
max_import = (df_trade["Imports"].max()+ 2000) # Adding import buffer for clear visualisation
max_export = df_trade["Exports"].max()
x_limit = max(max_import, max_export)
fig, ax = plt.subplots(figsize=(12, 6))

def animate(frame):
    ax.clear()
    df_trade_frame = df_trade[df_trade['Year'] == frame]

    df_trade_frame["Country"] = pd.Categorical(
        df_trade_frame["Country"],
        categories=country_order,
        ordered=True
    )
    df_trade_frame = df_trade_frame.sort_values("Country") # Applying country order

    countries = df_trade_frame["Country"]
    imports = -df_trade_frame["Imports"]  # imports made negative for bi-directional chart
    exports = df_trade_frame["Exports"]

    # Use the same color for each country in every frame
    colors = [country_colors[c] for c in countries]

    ax.barh(countries, imports, color=colors, alpha=0.7, label='Imports')
    ax.barh(countries, exports, color=colors, alpha=0.7, label='Exports')

    ax.set_xlim(-x_limit, x_limit)

    # GO OVER THIS CODE PATCH!!
    for idx in range(len(countries)):
        ax.text(imports.iloc[idx], idx, f"{abs(int(imports.iloc[idx])):,}", 
                va='center', ha='right', color='black', fontsize=6)
        ax.text(exports.iloc[idx], idx, f"{int(exports.iloc[idx]):,}", 
                va='center', ha='left', color='black', fontsize=6)
        
    ax.set_title(f"Trade Balance by Country - {frame}", fontsize=14)

    #Add "Imports" and "Exports" text labels above chart
    y_pos = -1  # safely below bars
    ax.text(-x_limit, y_pos, "Imports", ha='left', fontsize=12)
    ax.text(x_limit, y_pos, "Exports", ha='right', fontsize=12)

    ax.axvline(0, color="black", linewidth=1)  # Adding a vertical line at x=0

    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.minorticks_on()
    ax.grid(axis='x', which='minor', linestyle=':', linewidth=0.3, alpha=0.3)

trade_animation = animation.FuncAnimation(fig, animate, frames=frames, interval=500, repeat=True)

save_path = 'C:\\Users\\mm147\\Empirical-Project\\Data-Science-Empirical-Project\\Visualisations'
if not os.path.exists(save_path):
    os.makedirs(save_path)
completed_video = os.path.join(save_path, 'trade_balance_animation.gif')
trade_animation.save(completed_video, writer="pillow", fps=2)

plt.show()

# Animation improvements
#Export and Import labels are still moving around a bit?? - Is it worth interpolating (more interested in all countries staying in the visualisations, and the orderings.)