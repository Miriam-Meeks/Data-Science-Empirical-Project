import pandas as pd
import matplotlib.pyplot as plt

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

    df_long["Fuel"] = df_long["Fuel"].str.replace(r"\s*\[.*?\]", "", regex=True)

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

gen_df = reshape("electricity-generated.csv")
#Altering column names for share sheet so they don't completely match electricity-generated
share_df = reshape("share-electricity-generated.csv")
share_df.columns = [
    col if col == "Year" else col + " (%)"
    for col in share_df.columns
]
share_df.to_csv("share-electricity-generated-long.csv", index=False) #Saving (%) column addition

combined_electrcity = pd.merge(gen_df, share_df, on="Year", how="inner") 
# Merge can be inner as you won't have missing years not in both datasets because of the nature of the datasets.

# Organising alphabetically for aesthetics to have share next to generation for each fuel type
cols = ["Year"] + sorted([col for col in combined_electrcity.columns if col != "Year"])
combined_electrcity = combined_electrcity[cols] 
combined_electrcity.columns = combined_electrcity.columns.str.replace(r"\s*\[.*?\]", "", regex=True) #removing notes
print(combined_electrcity.head())


#Data visualisation
# combined_electrcity.plot(kind = 'scatter', x = 'Renewable (%)', y = 'Year')

# plt.show()