import pandas as pd

# Load dataset
df = pd.read_csv("data/expenses.csv")

print("Original Data Shape:", df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove missing values
df = df.dropna()

# Standardize category names
df['Category'] = df['Category'].str.capitalize()

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='mixed')

# Save cleaned dataset
df.to_csv("data/expenses_clean.csv", index=False)

print("Cleaned Data Shape:", df.shape)

print("Data cleaned and saved successfully!")