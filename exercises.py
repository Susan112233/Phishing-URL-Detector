import requests
from bs4 import BeautifulSoup
import os

# Step 1: Define the folder for saving HTML files
folder = "mini_dataset"

if not os.path.exists(folder):
    os.mkdir(folder)

# Step 2: Define a function that scrapes content from a URL and returns it
def scrape_content(URL):
    try:
        # Adding a User-Agent to mimic a browser visit and avoid being blocked by certain websites
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(URL, headers=headers, timeout=10)  # Added headers and timeout for better handling
        if response.status_code == 200:
            print("HTTP connection is successful! for the URL:", URL)
            return response.text
        else:
            print("HTTP connection is NOT successful! for the URL:", URL, "| Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred for URL:", URL, "| Error:", e)
        return None

# Step 3: Define a function to save HTML content to a file
def save_html(to_where, text, name):
    file_name = name + ".html"
    with open(os.path.join(to_where, file_name), "w", encoding="utf-8") as f:
        f.write(text)

# Step 4: Define a list of URLs to be scraped
URL_list = [
    "https://www.kaggle.com",
    "https://stackoverflow.com",
    "https://www.researchgate.net",
    "https://www.python.org",
    "https://www.w3schools.com",
    "https://wwwen.uni.lu",
    "https://github.com",
    "https://scholar.google.com",
    "https://www.mendeley.com",
    "https://www.overleaf.com"
]

# Step 5: Define a function that takes the URL list and scrapes each URL, saving the content
def create_mini_dataset(to_where, URL_list):
    for i, url in enumerate(URL_list):
        content = scrape_content(url)
        if content is not None:
            save_html(to_where, content, str(i))
        else:
            print(f"Skipping URL {url} due to connection issues.")
    print("Mini dataset is created")

# Run the function to create the dataset
create_mini_dataset(folder, URL_list)
