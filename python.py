import pandas as pd

# Function that reads, reshapes and renames files from wide to long formats for sheets in 5.6
def reshape (wide_files):
    df = pd.read_csv(wide_files) 
    
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")] # drop empty, unamed columns

    df["Fuel"] = df["Fuel"].astype(str).str.strip()
    df["Generation type"] = df["Generation type"].astype(str).str.strip()
    df = df[df["Generation type"].str.strip() == "All generating companies"] # interested in total generated output, removing white formatting space

    df_long = df.melt(
        id_vars=["Fuel"],    
        var_name="Year",     
        value_name="Value"
    )

    df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce") # CHECK THAT THIS USEFUL

    df_final = df_long.pivot( #Pivoting to have fuel types as columns but no aggregation
        index="Year",
        columns="Fuel",
        values="Value"
    ).reset_index()

    print(df_long.head())

    output_name = wide_files.replace(".csv", "-long.csv")
    df_long.to_csv(output_name, index=False) #saved to renamed csv

wide_files = ["electricity-generated.csv","share-electricity-generated.csv"]

for file in wide_files:
    reshape(file)