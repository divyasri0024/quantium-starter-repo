import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import glob

# 1. Load all CSV files
file_list = glob.glob("data/*.csv")

if not file_list:
    print("ERROR: No CSV files found in the 'data/' folder!")
    exit()

df_list = [pd.read_csv(file) for file in file_list]
df = pd.concat(df_list, ignore_index=True)

print(f"Files loaded: {file_list}")
print(f"Initial rows: {len(df)}")

# 2. Robust Cleaning Logic
# Clean price: Remove '$' and ',' then convert to numeric
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace(r'[$,]', '', regex=True)
)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Clean quantity: Convert to numeric, turn errors to NaN
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Convert date: Using dayfirst=True handles DD/MM/YYYY formats common in retail data
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

# --- DIAGNOSTIC CHECK ---
print("\n--- Cleaning Diagnostics ---")
print("Missing values per column before dropping:")
print(df[["date", "price", "quantity"]].isna().sum())
# -------------------------

# 3. Drop bad rows and create total_sales
df = df.dropna(subset=["date", "price", "quantity"])
df["total_sales"] = df["price"] * df["quantity"]

print(f"\nRows remaining after cleaning: {len(df)}")

if len(df) == 0:
    print("CRITICAL: All rows were dropped. Check the column formatting in your CSVs.")
    exit()

# 4. Aggregate Data for Visualization
sales_by_date = (
    df.groupby("date", as_index=False)["total_sales"]
    .sum()
    .sort_values("date")
)

print(f"Total sales sum: {df['total_sales'].sum():,.2f}")
print(f"Unique dates: {df['date'].nunique()}")

# 5. Dash App Setup
app = Dash(__name__)

# Create the Line Chart
fig = px.line(
    sales_by_date,
    x="date",
    y="total_sales",
    title="Daily Total Sales Trend",
    labels={"date": "Date", "total_sales": "Total Sales ($)"},
    markers=True,
    template="plotly_white"
)

app.layout = html.Div([
    html.H1("Quantium Sales Dashboard", style={'textAlign': 'center', 'fontFamily': 'sans-serif'}),
    
    html.Div([
        html.P(f"Total Data Points: {len(df)}"),
        html.P(f"Date Range: {sales_by_date['date'].min().date()} to {sales_by_date['date'].max().date()}")
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'marginBottom': '20px'}),

    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)