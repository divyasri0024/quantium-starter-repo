import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# =========================
# 1. Load and Prepare Data
# =========================
def load_data(file_path):
    df = pd.read_csv(file_path)

    # Normalize column names
    df.columns = [col.lower() for col in df.columns]

    # Filter for Pink Morsels
    df = df[df['product'].str.lower().str.strip() == 'pink morsels']

    # Convert date
    df['date'] = pd.to_datetime(df['date'])

    # Clean and convert price
    df['price'] = (
        df['price']
        .astype(str)
        .str.replace(r'[\$,]', '', regex=True)
        .astype(float)
    )

    # Convert quantity
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    # Drop bad rows
    df = df.dropna(subset=['price', 'quantity'])

    # Calculate total sales
    df['sales'] = df['price'] * df['quantity']

    # Aggregate daily sales
    df = (
        df.groupby('date', as_index=False)['sales']
        .sum()
        .sort_values('date')
    )

    return df


# =========================
# 2. Load Dataset
# =========================
DATA_PATH = "sales_data.csv"

try:
    processed_df = load_data(DATA_PATH)
except FileNotFoundError:
    print(f"File {DATA_PATH} not found. Using placeholder data.")
    processed_df = pd.DataFrame({
        'date': pd.date_range(start='2020-09-01', end='2021-05-01', freq='D'),
        'sales': [100 + (i * 0.5) for i in range(243)]
    })


# =========================
# 3. Create Visualization
# =========================
fig = px.line(
    processed_df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Trend (Before vs. After Price Increase)",
    labels={'sales': 'Total Sales ($)', 'date': 'Date'}
)

# Vertical line (STRING to avoid Pandas bug)
fig.add_vline(
    x="2021-01-15",
    line_dash="dash",
    line_color="red"
)

# Annotation (robust workaround)
fig.add_annotation(
    x="2021-01-15",
    y=processed_df['sales'].max(),
    text="Price Increase (Jan 15)",
    showarrow=True,
    arrowhead=1,
    yshift=10
)

fig.update_layout(
    yaxis_tickprefix="$",
    hovermode="x unified",
    template="plotly_white"
)


# =========================
# 4. Build Dash App
# =========================
app = Dash(__name__)

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'},
    children=[

        html.H1(
            "Soul Foods: Pink Morsels Visualizer",
            style={'textAlign': 'center', 'color': '#2c3e50'}
        ),

        html.Div([
            html.P(f"Total Data Points: {len(processed_df)}"),
            html.P(
                f"Date Range: "
                f"{processed_df['date'].min().date()} "
                f"to {processed_df['date'].max().date()}"
            )
        ], style={'marginBottom': '20px', 'color': '#7f8c8d'}),

        dcc.Graph(
            id='sales-line-chart',
            figure=fig
        ),

        html.Footer(
            "Soul Foods Data Analytics - 2026",
            style={'marginTop': '50px', 'fontSize': '12px'}
        )
    ]
)

# =========================
# 5. Run Server
# =========================
if __name__ == '__main__':
    app.run(debug=True)
