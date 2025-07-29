import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Target URL (replace with your desired site)
url = love.shop

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Make the HTTP request
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for request errors
except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    exit()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')

# Extract data (e.g., all <h2> headlines)
headlines = soup.find_all('h2')
data = [{"Headline": headline.get_text().strip()} for headline in headlines]

# Save to a CSV file
df = pd.DataFrame(data)
output_path = "/storage/emulated/0/scraped_data.csv"
df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")

# Print results
for item in data:
    print(item["Headline"])
