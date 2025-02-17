import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Define file path (Update with local path)
file_path = "c:/Users/asusj/Desktop/internship/API_SP.POP.TOTL_DS2_en_csv_v2_87.csv"

# Load India's population data from World Bank file
df = pd.read_csv(file_path, skiprows=4)
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]  # Remove unnamed columns

# Print column names for debugging
print("Column names in the CSV file:", df.columns.tolist())

# Ensure correct column names exist
if "Country Code" not in df.columns or "Indicator Name" not in df.columns:
    raise KeyError("Required columns not found in the dataset")

# Filter data for India
df_india = df[df["Country Code"] == "IND"]
df_india = df_india.drop(columns=["Country Name", "Country Code"], errors='ignore')

# Reshape data to have 'Year' and 'Population'
df_india = df_india.melt(id_vars=["Indicator Name", "Indicator Code"], var_name="Year", value_name="Population")
df_india["Year"] = pd.to_numeric(df_india["Year"], errors="coerce")
df_india.dropna(subset=["Year", "Population"], inplace=True)
df_india["Year"] = df_india["Year"].astype(int)
df_india["Population"] = pd.to_numeric(df_india["Population"], errors="coerce")

# Get latest available year and population
df_latest = df_india[df_india["Year"] == df_india["Year"].max()]
if df_latest.empty:
    raise ValueError("No valid population data found for the latest year")
latest_year = df_latest["Year"].values[0]
latest_population = df_latest["Population"].values[0]

# Plot India's population trend
plt.figure(figsize=(10, 5))
sns.lineplot(x=df_india["Year"], y=df_india["Population"], marker="o", color="b")
plt.xlabel("Year")
plt.ylabel("Population (in billions)")
plt.title("India's Population Growth Over Time")
plt.grid()
plt.show()

# Dummy Gender Data (World Bank API does not provide gender distribution directly)
gender_data = {"Male": 0.51, "Female": 0.49}  # Approximate distribution for India

# Create Bar Chart for Gender Distribution
plt.figure(figsize=(6, 4))
sns.barplot(x=list(gender_data.keys()), y=list(gender_data.values()), palette="viridis")
plt.xlabel("Gender")
plt.ylabel("Proportion")
plt.title(f"Estimated Gender Distribution in India ({latest_year})")
plt.ylim(0, 1)
plt.show()

# Simulated Age Distribution (Normal Distribution Approximation)
np.random.seed(42)
age_data = np.random.normal(loc=30, scale=12, size=1000)  # Simulating age distribution

# Create Histogram for Age Distribution
plt.figure(figsize=(8, 5))
sns.histplot(age_data, bins=20, kde=True, color="blue")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.title(f"Estimated Age Distribution in India ({latest_year})")
plt.show()

# Print Latest Population Data
print(f"Latest available population data for India ({latest_year}): {latest_population:.0f}")