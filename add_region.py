import pandas as pd
import numpy as np

# Load your existing CSV
df = pd.read_csv("sales_data.csv")

# Add a new 'region' column (randomly assign regions)
regions = ['north', 'east', 'south', 'west']
df['region'] = np.random.choice(regions, size=len(df))

# Save back to the same CSV
df.to_csv("sales_data.csv", index=False)

print("Region column added successfully!")
print(df.head())  # Shows first 5 rows
