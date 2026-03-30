import pandas as pd

# Defining a function that reads, reshapes and renames files from wide to long formats for sheets in 5.6
def reshape (wide_files):
    df = pd.read_csv(wide_files) #Load the data
    
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")] # drop empty, unamed columns

    df_long = df.melt(
        id_vars=["Generation type", "Fuel"],  # columns to account for 2 components in the first 2 columns
        var_name="Year",                      # new column for years
        value_name="Value"                    # new column for data values
    )

    print(df_long.head())

    output_name = wide_files.replace(".csv", "-long.csv")
    df_long.to_csv(output_name, index=False) #saved to renamed csv

wide_files = ["electricity-generated.csv","share-electricity-generated.csv"]

for file in wide_files:
    reshape(file)