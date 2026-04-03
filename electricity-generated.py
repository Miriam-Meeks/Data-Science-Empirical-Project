import pandas as pd

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

#Altering column names for share sheet so they don't completely match electricity-generated
df = pd.read_csv("share-electricity-generated.csv")
df.columns = [
    col if col in ["Year", "Fuel", "Generation type"] else col + " (%)"
    for col in df.columns
]
print(df.head())
df.to_csv("share-electricity-generated.csv", index=False)

# gen_df = reshape("electricity-generated.csv")
# share_df = reshape("share-electricity-generated.csv") # Working reshape :)

# combined_electrcity = pd.merge(gen_df, share_df, on="Year", how="inner") 
# print(combined_electrcity.head())

# # Merge can be inner as you won't have missing years not in both datasets because of the nature of the datasets.

# cols = ["Year"] + sorted([col for col in df_final.columns if col != "Year"])
# df_final = df_final[cols] # Organising alphabetically for aesthetics, will need to edit the dataset names!!