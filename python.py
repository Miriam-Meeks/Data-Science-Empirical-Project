import pandas as pd

# Function that reads, reshapes and renames files from wide to long formats for sheets in 5.6
def reshape (wide_files):
    df = pd.read_csv(wide_files) 
    
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")] # drop empty, unamed columns

    df = df[df["Generation type"].str.strip() == "All generating companies"] # interested in total generated output

    df_long = df.melt(
        id_vars=["Fuel"],    
        var_name="Year",     
        value_name="Value"
    )

    df_final = df_long.pivot_table( #Pivoting to have fuel types as columns
        index="Year",
        columns="Fuel",
        values="Value",
        aggfunc="first"
    ).reset_index()

    print(df_long.head())

    output_name = wide_files.replace(".csv", "-long.csv")
    df_long.to_csv(output_name, index=False) #saved to renamed csv

wide_files = ["electricity-generated.csv","share-electricity-generated.csv"]

for file in wide_files:
    reshape(file)