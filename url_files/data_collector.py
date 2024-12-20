import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from bs4 import BeautifulSoup
import pandas as pd
import feature_extraction as fe
import os
import concurrent.futures
import time

# Disable insecure request warnings
disable_warnings(InsecureRequestWarning)

# Define absolute path to CSV file
URL_file_name = 'verified_online.csv'

# Check if file exists
if not os.path.isfile(URL_file_name):
    raise FileNotFoundError(f"The file {URL_file_name} does not exist.")

# Read CSV into DataFrame
data_frame = pd.read_csv(URL_file_name)

# Retrieve only the "url" column and convert it to a list
URL_list = data_frame['url'].tolist()

# Restrict the number of URLs for collection
begin = 0
end = 100
collection_list = URL_list[begin:end]

# Ensure URLs start with 'http://' or 'https://'
collection_list = [
    url if url.startswith("http://") or url.startswith("https://") else "http://" + url
    for url in collection_list
]

# Function to scrape the content of the URL and convert to structured form
def scrape_url(i, url):
    attempt = 0
    max_attempts = 2
    while attempt < max_attempts:
        try:
            response = requests.get(url, verify=False, timeout=2)
            if response.status_code == 200:
                print(f"{i}. HTTP connection was successful for the URL: {url}")
                soup = BeautifulSoup(response.content, "html.parser")
                vector = fe.create_vector(soup)
                vector.append(url)
                return vector
            elif response.status_code == 403:
                print(f"{i}. HTTP connection was forbidden for the URL: {url} (Status Code: 403), skipping.")
                break
            else:
                print(f"{i}. HTTP connection was not successful for the URL: {url} (Status Code: {response.status_code})")
                break
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"{i} (Attempt {attempt}/{max_attempts}) --> {e}")
            if attempt < max_attempts:
                time.sleep(1)  # Wait before retrying
            else:
                print(f"{i}. Failed to retrieve URL after {max_attempts} attempts: {url}")
    return None

# Collect structured data from URLs using multithreading
def create_structured_data_multithreaded(url_list):
    data_list = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scrape_url, i, url): i for i, url in enumerate(url_list)}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                data_list.append(result)

    return data_list

# Collect structured data
data = create_structured_data_multithreaded(collection_list)

# Define columns for DataFrame
columns = [
    'has_title', 'has_input', 'has_button', 'has_image', 'has_submit', 
    'has_link', 'has_password', 'has_email_input', 'has_hidden_element', 
    'has_audio', 'has_video', 'number_of_inputs', 'number_of_buttons', 
    'number_of_images', 'number_of_option', 'number_of_list', 'number_of_th', 
    'number_of_tr', 'number_of_href', 'number_of_paragraph', 'number_of_script', 
    'length_of_title', 'has_h1', 'has_h2', 'has_h3', 'length_of_text', 
    'number_of_clickable_button', 'number_of_a', 'number_of_img', 'number_of_div', 
    'number_of_figure', 'has_footer', 'has_form', 'has_text_area', 'has_iframe', 
    'has_text_input', 'number_of_meta', 'has_nav', 'has_object', 'has_picture', 
    'number_of_sources', 'number_of_span', 'number_of_table', 'URL'
]

# Create DataFrame
df = pd.DataFrame(data=data, columns=columns)

# Add label column (assuming this is for phishing detection, label=1 for phishing)
df['label'] = 0

# Save DataFrame to CSV (append mode without header after the first run)
output_file = 'structured_data_phishing_2.csv'

if not os.path.isfile(output_file):
    df.to_csv(output_file, mode='w', index=False, header=True)  # Write header if file does not exist
else:
    df.to_csv(output_file, mode='a', index=False, header=False)  # Append data without writing header

print("Data saved successfully.")
