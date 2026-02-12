import pandas as pd
import glob

# 1. Path setup
input_path = r"data/daily_sales_data_*.csv"
output_path = "formatted_sales.csv"

# 2. Read and combine files
files = glob.glob(input_path)
if not files:
    print("Error: No CSV files found in 'data' folder!")
else:
    df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

    # 3. ROBUST FILTERING: Handles spaces and case sensitivity
    # This ensures that " pink morsel ", "PINK MORSEL", and "Pink Morsel" all match.
    df = df[df["product"].str.strip().str.lower() == "pink morsel"]

    # Check if we have data left after filtering
    if df.empty:
        print("Warning: No rows found for 'Pink Morsel'. Check the 'product' column in your source CSVs.")
    else:
        # 4. Clean price and calculate sales
        df["price"] = df["price"].replace(r'[\$,]', '', regex=True).astype(float)
        df["Sales"] = df["quantity"] * df["price"]

        # 5. Select and rename columns
        df = df[["Sales", "date", "region"]]
        df.columns = ["Sales", "Date", "Region"]

        # 6. Save final CSV
        df.to_csv(output_path, index=False)
        print(f"Success! {len(df)} rows processed into {output_path}")