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

import pandas as pd

df = pd.read_csv("net-imports.csv")

df = df.drop(columns=[
    "Total Imports (to UK)",
    "Total Exports (from UK)",
    "Net imports (to UK)"
]) #Removing columns of no interest currently

# reshape trade balance sheet
df_long = df.melt(
    id_vars=["Year"],
    var_name="Type",
    value_name="Value"
)

# Extract variables
df_long["Variable"] = df_long["Type"].str.extract(r"^(Imports|Exports|Net imports)")
df_long["Country"] = df_long["Type"].str.extract(r"\((.*?)\)")

# ---- CLEANING ----
df_long["Country"] = (
    df_long["Country"]
    .str.replace(r"\s*\[.*?\]", "", regex=True)
    .str.replace("Northern Ireland", "UK")
    .str.replace("Wales", "UK")
    .str.replace(" to UK", "")
    .str.replace("UK to ", "")
    .str.strip()
)

# Drop junk rows
df_long = df_long.dropna(subset=["Variable", "Country"])

# Clean numeric values
df_long["Value"] = (
    df_long["Value"]
    .astype(str)
    .str.replace(",", "")
)
df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")

# ---- CRUCIAL FIX ----
# Remove rows where Value is NaN BEFORE grouping
df_long = df_long.dropna(subset=["Value"])

# ---- GROUP FIRST ----
df_grouped = df_long.groupby(
    ["Year", "Country", "Variable"],
    as_index=False
)["Value"].sum()

# ---- THEN PIVOT ----
df_final = df_grouped.pivot(
    index=["Year", "Country"],
    columns="Variable",
    values="Value"
).reset_index()

print(df_final.head(50))

df_final.to_csv("net-imports-long.csv", index=False)