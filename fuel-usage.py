import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#Data didnt need much reshaping or cleaning/ no missing values, for years between datapoints
# Looking at fuel usage over time
fuel_consumption = pd.read_csv("uk-fuel-consumption.csv")
fuel_consumption = fuel_consumption[["Year", "All vehicles"]]
print(fuel_consumption.head())

df = fuel_consumption.copy()

# Ensure correct types/ converting all to numeric
df["Year"] = pd.to_numeric(df["Year"])
df["All vehicles"] = pd.to_numeric(df["All vehicles"]).rename("Fuel Consumption")

fig = px.line(
    df,
    x="Year",
    y="All vehicles",
    title="UK Road Transport Fuel Consumption 1970-2024",
    markers=True
)

# --- Styling improvements ---
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Fuel Consumption (millions tonnes)",
    hovermode="x unified",

    # White background
    plot_bgcolor="white",
    paper_bgcolor="white",

    # Gridlines
    xaxis=dict(
        range=[1970, 2024],
        showgrid=True,
        gridcolor="lightgrey",
        dtick=2  # gridline every 2 years (adjust if needed)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="lightgrey"
    )
)

# Optional: cleaner hover
fig.update_traces(
    hovertemplate="Year: %{x}<br>Consumption: %{y:.2f}<extra></extra>"
)

fig.write_html("Visualisations/fuel-consumption-line.html") # Saved as an interactive html
fig.show()

#Visualisation improvements
#Put a dark border around the graph.