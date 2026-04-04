import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
df_trade.head()

df_trade_2024 = df_trade[df_trade['Year'] == 2024]

countries = df_trade_2024["Country"]
imports = -df_trade_2024["Imports"] # imports made negative for bi-directional chart
exports = df_trade_2024["Exports"]

#Using my favourite of the qualitative colormaps, but may later alter, to make all visualisations cohesive
colors = plt.cm.tab20b(np.linspace(0, 1, len(countries))) 

plt.figure(figsize=(10, 6))

plt.barh(countries, imports, color=colors, alpha=0.7, label='Imports')
plt.barh(countries, exports, color=colors, alpha=0.7, label='Exports')

#GO OVER THIS CODE PATCH!!
for idx in range(len(countries)):
    plt.text(imports.iloc[idx], idx, f"{abs(int(imports.iloc[idx])):,}", 
             va='center', ha='right', color='black', fontsize=6)
    plt.text(exports.iloc[idx], idx, f"{int(exports.iloc[idx]):,}", 
             va='center', ha='left', color='black', fontsize=6)
    
plt.title("Trade Balance by Country", fontsize=14)

# Add "Imports" and "Exports" text labels above chart
y_pos = -1.25  # slightly below the bottom bar
plt.text(min(imports), y_pos, "Imports", ha='left', fontsize=12)
plt.text(max(exports), y_pos, "Exports", ha='right', fontsize=12)


plt.axvline(0, color="black", linewidth=1) # Adding a vertical line at x=0

plt.grid(axis='x', linestyle='--', alpha=0.5) # trying with a small dotted grid line sstyle

plt.tight_layout()
plt.show()

#Improvements to graph!! 
# Smaller grid line intervals
   #Order by countries that appear first
