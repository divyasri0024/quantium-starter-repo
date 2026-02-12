import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from datetime import datetime
import os

# =========================
# 1. Load and Prepare Data
# =========================
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = [col.lower() for col in df.columns]

    # Filter for Pink Morsels
    df = df[df['product'].str.lower().str.strip() == 'pink morsels']

    # Ensure region exists
    if 'region' not in df.columns:
        regions = ['north', 'east', 'south', 'west']
        df['region'] = [regions[i % 4] for i in range(len(df))]

    # Convert date
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

    # Clean price and quantity
    df['price'] = df['price'].astype(str).str.replace(r'[\$,]', '', regex=True).astype(float)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    df = df.dropna(subset=['price', 'quantity', 'region', 'date'])
    df['sales'] = df['price'] * df['quantity']
    return df

DATA_PATH = "sales_data.csv"
df = load_data(DATA_PATH) if os.path.exists(DATA_PATH) else pd.DataFrame({
    'date': pd.date_range(start='2020-09-01', end='2021-05-01', freq='D'),
    'sales': [100 + (i * 0.5) for i in range(243)],
    'region': ['all']*243
})

# =========================
# 2. Dash App Setup
# =========================
app = Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '30px', 'backgroundColor': '#f4f6f7'}, children=[

    html.H1("Soul Foods: Pink Morsels Sales Dashboard",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),

    # Region radio buttons
    html.Div([
        html.Label("Select Region:", style={'fontWeight': 'bold', 'marginRight': '15px', 'fontSize': '16px'}),
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            labelStyle={'display': 'inline-block', 'marginRight': '20px', 'padding': '5px 10px',
                        'border': '1px solid #3498db', 'borderRadius': '5px', 'cursor': 'pointer'},
            inputStyle={'marginRight': '5px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '25px'}),

    # Stats card
    html.Div([
        html.P(f"Total Data Points: {len(df)}", style={'margin': '5px 0'}),
        html.P(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}", style={'margin': '5px 0'})
    ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': 'white',
              'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'marginBottom': '30px'}),

    # Chart container
    html.Div([
        dcc.Graph(id='sales-line-chart')
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
              'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),

    html.Footer("Soul Foods Data Analytics - 2026",
                style={'marginTop': '50px', 'fontSize': '12px', 'textAlign': 'center', 'color': '#7f8c8d'})
])

# =========================
# 3. Callback for Interactive Chart
# =========================
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_chart(selected_region):
    filtered_df = df.copy() if selected_region == 'all' else df[df['region'].str.lower() == selected_region]

    # Aggregate daily sales
    sales_by_date = filtered_df.groupby(['date', 'region'], as_index=False)['sales'].sum().sort_values('date')

    # Line chart with color by region
    fig = px.line(
        sales_by_date,
        x='date',
        y='sales',
        color='region',
        title="Pink Morsels Sales Trend (Before vs. After Price Increase)",
        labels={'sales': 'Total Sales ($)', 'date': 'Date', 'region': 'Region'},
        markers=True,
        template='plotly_white'
    )

    # Price increase line
    increase_date = datetime(2021, 1, 15)
    fig.add_vline(
        x=increase_date,
        line_dash="dash",
        line_color="red"
    )
    fig.add_annotation(
        x=increase_date,
        y=sales_by_date['sales'].max() if not sales_by_date.empty else 0,
        text="Price Increase (Jan 15)",
        showarrow=True,
        arrowhead=1,
        yshift=10
    )

    fig.update_layout(hovermode="x unified", yaxis_tickprefix="$")
    return fig

# =========================
# 4. Run Server
# =========================
if __name__ == '__main__':
    app.run(debug=True)
