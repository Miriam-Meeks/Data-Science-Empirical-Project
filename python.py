import pandas as pd


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

    df_final = df_long.pivot( #Pivoting to have fuel types as columns but no aggregation
        index="Year",
        columns="Fuel",
        values="Value"
    ).reset_index()

    print(df_long.head())

    output_name = wide_files.replace(".csv", "-long.csv")
    df_final.to_csv(output_name, index=False) #saved to renamed csv

wide_files = ["electricity-generated.csv","share-electricity-generated.csv"]

# for file in wide_files:
#     df_[file] = reshape(file) # Working reshape :)
    
gen_df = reshape("electricity-generated.csv")
share_df = reshape("share-electricity-generated.csv")

# share_df = share_df.rename(columns={
#     col: f"{col} (%)" for col in share_df.columns if col != "Year"
# })

# pd.merge(gen_df, share_df, on="Year", how="inner") 
# # Merge can be inner as you won't have missing years not in both datasets because of the nature of the datasets.