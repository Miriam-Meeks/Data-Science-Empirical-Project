
# df_long['Type'] = (
#     df_long['Type']
#     .str.replace('Northern Ireland','UK')
#     .str.replace('Wales','UK') # Replacing NI and Wales with UK so that the formatting works with the pivot
#     .str.strip() 
# )

# df_long['Value'] = pd.to_numeric(
#     df_long['Value'].str.replace(',', ''),
#     errors='coerce') # Turning all characters to numeric

# #REMOVE DECIMAL PLACES FROM VALUE COLUMN/ TRUNCATE!
# df_long['Value'] = df_long['Value'].astype('Int64') # Removing decimal places by turning to integers

# #WHAT DOES THIS LINE MEAN/ WHY IS IT SUGGESTED BY AI/ DOES IT MAKE A DIFFERENCE?
# df_final = df_long.groupby(['Year', 'Country', 'Variable'])['Value'].sum().unstack('Variable').reset_index()

# #Tried using a pivot but beause of the stacking and unstacking the import export to and from UK pivoting wasn't working, with lots of though and consulting LLMs this is what I came up with.
# # df_final = df_long.pivot_table(
# #     index=["Year", "Country"],
# #     columns="Variable",
# #     values="Value",
# #     aggfunc="sum"   # best choice for trade data acccording to AI
# # ).reset_index()



import pandas as pd

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
df_long['Country'] = (
    df_long['Country']
    .str.replace('Northern Ireland','UK')
    #.str.replace('Wales','UK') # Replacing NI and Wales with UK so that the formatting works with the pivot
    .str.strip() 
)

df_long['Country'] = (
    df_long['Country']
    #.str.replace('Northern Ireland','UK')
    .str.replace('Wales','UK') # Replacing NI and Wales with UK so that the formatting works with the pivot
    .str.strip() 
)

df_long["Country"] = (
    df_long["Country"]
    .str.replace(r"\s*\[.*?\]", "", regex=True) # remove notes in column
    .str.replace(" to UK", "", regex=False) # remove "to UK"
    .str.replace("UK to ", "", regex=False)
    .str.strip() # useful to clean whitespace and standardise
)

# Drop rows where NaN in Variable, i.e. removing transfers within UK columns
print(df_long)

df_long = df_long.dropna(subset=['Variable'])
df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")

df_final = df_long.pivot_table(
    index=["Year", "Country"],
    columns="Variable",
    values="Value",
    aggfunc="sum"
).reset_index()

print(df_final.head())
df_final.to_csv("net-imports-long.csv", index=False)

# # #Data Viualsiation
# # df_trade = pd.read_csv("net-imports-long.csv")
# # #df_trade.head()
