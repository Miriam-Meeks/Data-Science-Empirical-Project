#Trade balance
import pandas as pd

df = pd.read_csv("net-imports.csv")

#reshape trade balance sheet to plot trade balance over time
df_long = df.melt(
    id_vars=["Year"],
    var_name="Type",
    value_name="Value"
)
print(df_long)


