# #WORKING INTIAL:
# import pandas as pd

# df = pd.read_csv("net-imports.csv")

# df = df.drop(columns=["Total Imports (to UK)",
#     "Total Exports (from UK)",
#     "Net imports (to UK)"
#     ]) #Removing columns of no interest currently

# #reshape trade balance sheet to plot trade balance over time
# df_long = df.melt(
#     id_vars=["Year"],
#     var_name="Type",
#     value_name="Value"
# )
# #Using regex to extract
# df_long["Variable"] = df_long["Type"].str.extract(r"^(Imports|Exports|Net imports)")
# df_long["Country"] = df_long["Type"].str.extract(r"\((.*?)\)") # Extracts countries trading in type column
# df_long["Country"] = (
#     df_long["Country"]
#     .str.replace(r"\s*\[.*?\]", "", regex=True) # remove notes in column
#     .str.replace(" to UK", "", regex=False) # remove "to UK"
#     .str.replace("UK to ", "", regex=False)
#     .str.strip() # useful to clean whitespace and standardise
# )

# # Drop rows where NaN in Variable, i.e. removing transfers within UK columns
# df_long = df_long.dropna(subset=['Variable'])
# df_final = df_long.pivot(
#     index=["Year", "Country"],
#     columns="Variable",
#     values="Value",
# ).reset_index()

# print(df_final.head())
# df_final.to_csv("net-imports-long.csv", index=False)



# import pandas as pd 

# df = pd.read_csv("net-imports.csv")

# df = df.drop(columns=[
#     "Total Imports (to UK)",
#     "Total Exports (from UK)",
#     "Net imports (to UK)"
# ]) #Removing columns of no interest currently

# # reshape trade balance sheet to plot trade balance over time
# df_long = df.melt(
#     id_vars=["Year"],
#     var_name="Type",
#     value_name="Value"
# )

# # Using regex to extract
# df_long["Variable"] = df_long["Type"].str.extract(r"^(Imports|Exports|Net imports)")

# # Extract full flow (e.g. "France to UK")
# df_long["Flow"] = df_long["Type"].str.extract(r"\((.*?)\)")

# # Clean notes in flow
# df_long["Flow"] = df_long["Flow"].str.replace(r"\s*\[.*?\]", "", regex=True)

# # Split into From and To countries
# df_long[["From", "To"]] = df_long["Flow"].str.split(" to ", expand=True)

# # Identify the non-UK country
# df_long["Country"] = df_long.apply(
#     lambda x: x["To"] if x["From"] == "UK" else x["From"],
#     axis=1
# )

# # Drop rows where NaN in Variable, i.e. removing transfers within UK columns
# df_long = df_long.dropna(subset=['Variable'])

# # Convert values to numeric (important for clean pivot)
# df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")

# #Tried using a pivot but beause of the stacking and unstacking the import export to and from UK pivoting wasn't working, with lots of though and consulting LLMs this is what I came up with.
# df_final = df_long.pivot_table(
#     index=["Year", "Country"],
#     columns="Variable",
#     values="Value",
#     aggfunc="sum"   # best choice for trade data acccording to AI
# ).reset_index()

# print(df_final.head())

# df_final.to_csv("net-imports-long.csv", index=False)


# import pandas as pd

# df = pd.read_csv("net-imports.csv")

# df = df.drop(columns=[
#     "Total Imports (to UK)",
#     "Total Exports (from UK)",
#     "Net imports (to UK)"
# ]) # Removing columns of no interest currently

# # reshape trade balance sheet to plot trade balance over time
# df_long = df.melt(
#     id_vars=["Year"],
#     var_name="Type",
#     value_name="Value"
# )

# # Clean numeric values
# df_long['Value'] = pd.to_numeric(
#     df_long['Value'].astype(str).str.replace(',', ''),
#     errors='coerce'
# )

# df_long['Value'] = df_long['Value'].astype('Int64') # optional

# # Using regex to extract
# df_long["Variable"] = df_long["Type"].str.extract(r"^(Imports|Exports|Net imports)")
# df_long["Flow"] = df_long["Type"].str.extract(r"\((.*?)\)")

# # Clean notes
# df_long["Flow"] = df_long["Flow"].str.replace(r"\s*\[.*?\]", "", regex=True)

# # Split into From and To
# df_long[["From", "To"]] = df_long["Flow"].str.split(" to ", expand=True)

# # ---- KEY FIX ----
# # Keep non-UK country, but preserve NI/Wales correctly
# df_long["Country"] = df_long.apply(
#     lambda x: x["To"] if x["From"] == "UK" else x["From"],
#     axis=1
# )

# # Optional: group NI & Wales into UK AFTER extraction
# df_long["Country"] = df_long["Country"].replace({
#     "Northern Ireland": "UK",
#     "Wales": "UK"
# })

# # Drop rows where NaN in Variable
# df_long = df_long.dropna(subset=['Variable'])

# # Aggregate properly
# df_final = df_long.groupby(
#     ['Year', 'Country', 'Variable']
# )['Value'].sum().unstack('Variable').reset_index()

# print(df_final.head())

# df_final.to_csv("net-imports-long.csv", index=False)

# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.animation as animation # for creating animation
# import os #for saving video animation

# df = pd.read_csv("net-imports.csv")

# df = df.drop(columns=[
#     "Total Imports (to UK)",
#     "Total Exports (from UK)",
#     "Net imports (to UK)"
# ]) #Removing columns of no interest currently

# # reshape trade balance sheet
# df_long = df.melt(
#     id_vars=["Year"],
#     var_name="Type",
#     value_name="Value"
# )

# # Extract variables
# df_long["Variable"] = df_long["Type"].str.extract(r"^(Imports|Exports|Net imports)")
# df_long["Country"] = df_long["Type"].str.extract(r"\((.*?)\)")

# # ---- CLEANING ----
# df_long["Country"] = (
#     df_long["Country"]
#     .str.replace(r"\s*\[.*?\]", "", regex=True)
#     .str.replace("Northern Ireland", "UK")
#     .str.replace("Wales", "UK")
#     .str.replace(" to UK", "")
#     .str.replace("UK to ", "")
#     .str.strip()
# )

# # Drop junk rows
# df_long = df_long.dropna(subset=["Variable", "Country"])

# # Clean numeric values
# df_long["Value"] = (
#     df_long["Value"]
#     .astype(str)
#     .str.replace(",", "")
# )
# df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")

# # ---- CRUCIAL FIX ----
# # Remove rows where Value is NaN BEFORE grouping
# df_long = df_long.dropna(subset=["Value"])

# # ---- GROUP FIRST ----
# df_grouped = df_long.groupby(
#     ["Year", "Country", "Variable"],
#     as_index=False
# )["Value"].sum()

# # ---- THEN PIVOT ----
# df_final = df_grouped.pivot(
#     index=["Year", "Country"],
#     columns="Variable",
#     values="Value"
# ).reset_index()

# print(df_final.head(50))

# df_final.to_csv("net-imports-long.csv", index=False)


# # --- PRECOMPUTE GLOBAL LIMITS (DO THIS ONCE, OUTSIDE animate) ---
# df_trade = pd.read_csv("net-imports-long.csv")
# frames = df_trade["Year"].unique()

# max_import = df_trade["Imports"].max()
# max_export = df_trade["Exports"].max()
# x_limit = max(max_import, max_export)

# # Using ax to allow for animation
# fig, ax = plt.subplots(figsize=(12, 6))

# def animate(frame):
#     ax.clear()

#     df_trade_frame = df_trade[df_trade['Year'] == frame]

#     countries = df_trade_frame["Country"]
#     imports = -df_trade_frame["Imports"]
#     exports = df_trade_frame["Exports"]

#     colors = plt.cm.tab20b(np.linspace(0, 1, len(countries))) 

#     ax.barh(countries, imports, color=colors, alpha=0.7)
#     ax.barh(countries, exports, color=colors, alpha=0.7)

#     # ✅ FIX: lock axis so 0 stays centered
#     ax.set_xlim(-x_limit, x_limit)

#     # Value labels
#     for idx in range(len(countries)):
#         ax.text(imports.iloc[idx], idx, f"{abs(int(imports.iloc[idx])):,}", 
#                 va='center', ha='right', fontsize=6)
#         ax.text(exports.iloc[idx], idx, f"{int(exports.iloc[idx]):,}", 
#                 va='center', ha='left', fontsize=6)

#     ax.set_title(f"Trade Balance by Country - {frame}", fontsize=14)

#     # Bottom labels (use fixed positions, NOT min/max)
#     y_pos = -0.8
#     ax.text(-x_limit, y_pos, "Imports", ha='left', fontsize=12)
#     ax.text(x_limit, y_pos, "Exports", ha='right', fontsize=12)

#     # Zero line (now stable because axis is fixed)
#     ax.axvline(0, color="black", linewidth=1)

#     # Grid (cleaner)
#     ax.grid(axis='x', linestyle=':', linewidth=0.5, alpha=0.4)
#     ax.minorticks_on()
#     ax.grid(axis='x', which='minor', linestyle=':', linewidth=0.3, alpha=0.3)

# plt.tight_layout()
# trade_animation = animation.FuncAnimation(fig, animate, frames=frames, interval=500, repeat=True)
# plt.show()


#SMOOTH INTERPOLATION SETUP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- LOAD DATA ---
df_trade = pd.read_csv("net-imports-long.csv")

# --- CREATE TOTAL FOR ORDERING ---
df_trade["Total"] = df_trade["Imports"] + df_trade["Exports"]

# --- GLOBAL COUNTRY ORDER (stable across animation) ---
country_order = (
    df_trade.groupby("Country")["Total"]
    .mean()
    .sort_values(ascending=True)
    .index.tolist()
)

# --- ENSURE ALL COUNTRIES EXIST IN ALL YEARS ---
years = sorted(df_trade["Year"].unique())

full_index = pd.MultiIndex.from_product(
    [years, country_order],
    names=["Year", "Country"]
)

df_trade = df_trade.set_index(["Year", "Country"]).reindex(full_index).fillna(0).reset_index()

# --- INTERPOLATION SETUP ---
frames_per_year = 10  # increase for smoother animation

interp_data = []

for i in range(len(years) - 1):
    y1, y2 = years[i], years[i + 1]

    df1 = df_trade[df_trade["Year"] == y1].set_index("Country")
    df2 = df_trade[df_trade["Year"] == y2].set_index("Country")

    for t in np.linspace(0, 1, frames_per_year):
        interp = df1 + (df2 - df1) * t
        interp["Year"] = y1 + t
        interp["Country"] = interp.index
        interp_data.append(interp.reset_index(drop=True))

df_interp = pd.concat(interp_data, ignore_index=True)

# --- FIX AXIS LIMITS ---
max_import = df_trade["Imports"].max()
max_export = df_trade["Exports"].max()
x_limit = max(max_import, max_export)

# --- CONSISTENT COLORS ---
colors = plt.cm.tab20b(np.linspace(0, 1, len(country_order)))
color_map = dict(zip(country_order, colors))

# --- PLOT ---
fig, ax = plt.subplots(figsize=(12, 6))

def animate(frame):
    ax.clear()

    df_frame = df_interp.iloc[
        frame * len(country_order):(frame + 1) * len(country_order)
    ].copy()

    df_frame = df_frame.set_index("Country").loc[country_order].reset_index()

    imports = -df_frame["Imports"]
    exports = df_frame["Exports"]

    bar_colors = [color_map[c] for c in df_frame["Country"]]

    # Bars
    ax.barh(df_frame["Country"], imports, color=bar_colors, alpha=0.7)
    ax.barh(df_frame["Country"], exports, color=bar_colors, alpha=0.7)

    # Fixed axis
    ax.set_xlim(-x_limit, x_limit)

    # Value labels
    for i in range(len(df_frame)):
        ax.text(imports.iloc[i] - x_limit*0.02, i,
                f"{abs(int(imports.iloc[i])):,}",
                va='center', ha='right', fontsize=6)

        ax.text(exports.iloc[i] + x_limit*0.02, i,
                f"{int(exports.iloc[i]):,}",
                va='center', ha='left', fontsize=6)

    # Title (rounded year for display)
    year_display = int(df_frame["Year"].iloc[0])
    ax.set_title(f"Trade Balance by Country - {year_display}", fontsize=14)

    # Bottom labels
    ax.text(-x_limit, -1, "Imports", ha='left', fontsize=12)
    ax.text(x_limit, -1, "Exports", ha='right', fontsize=12)

    # Zero line
    ax.axvline(0, color="black", linewidth=1)

    # Grid
    ax.grid(axis='x', linestyle=':', linewidth=0.5, alpha=0.4)
    ax.minorticks_on()
    ax.grid(axis='x', which='minor', linestyle=':', linewidth=0.3, alpha=0.3)

# --- NUMBER OF FRAMES ---
total_frames = len(years) * frames_per_year

# --- ANIMATION ---
anim = animation.FuncAnimation(
    fig,
    animate,
    frames=total_frames,
    interval=100,
    repeat=True
)

plt.show()