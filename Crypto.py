
import requests
import pandas as pd

# Sample API for blockchain-based weather data (hypothetical)
api_url = "https://api.blockchainweatherdata.com/weather"

# Fetch weather data stored on blockchain
response = requests.get(api_url)
data = response.json()

# Convert to DataFrame for analysis
df = pd.DataFrame(data)

# Display latest weather trends from decentralized sources
print(df.head())
