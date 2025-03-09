import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (use a real-time API or Kaggle CSV file)
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
df = pd.read_csv(url)

# Select relevant columns
df = df[['location', 'total_cases', 'total_deaths', 'total_vaccinations']]
df = df.dropna()

# Exclude 'World' and income groups from the dataset
df = df[~df['location'].str.contains("World|income", case=False, na=False)]

# Display top 5 records
print("Top 5 rows of the dataset:")
print(df.head())

# Sort by total cases and select top 10 affected countries
top_countries = df.sort_values(by='total_cases', ascending=False).head(10)

# Bar plot: Top 10 countries by total cases
plt.figure(figsize=(10, 5))
sns.barplot(x='total_cases', y='location', data=top_countries, hue='location', dodge=False, palette='Reds', legend=False)
plt.xlabel("Total Cases")
plt.ylabel("Country")
plt.title("Top 10 Countries by COVID-19 Cases")
plt.xticks(rotation=45)
for index, value in enumerate(top_countries['total_cases']):
    plt.text(value, index, f'{int(value):,}', va='center')
plt.show()

# Scatter plot: Cases vs Deaths
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df['total_cases'], y=df['total_deaths'], alpha=0.6)
plt.xlabel("Total Cases")
plt.ylabel("Total Deaths")
plt.title("COVID-19 Cases vs Deaths")
plt.xscale('log')  # Log scale for better visibility
plt.yscale('log')
plt.show()

# Heatmap: Correlation between cases, deaths, and vaccinations
plt.figure(figsize=(6, 4))
sns.heatmap(df[['total_cases', 'total_deaths', 'total_vaccinations']].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Correlation Heatmap")
plt.show()
