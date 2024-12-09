from bs4 import BeautifulSoup
import os
import features as fe
import pandas as pd
import re

# 1 DEFINE A FUNCTION THAT EXTRACTS FEATURES DIRECTLY FROM A URL
def create_url_vector(url):
    features = {}
    features['length'] = len(url)
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['contains_https'] = int(url.startswith('https'))
    features['num_special_chars'] = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', url))
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'bank']
    features['contains_suspicious_words'] = int(any(keyword in url.lower() for keyword in suspicious_words))
    features['has_ip_address'] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)))
    features['num_subdomains'] = url.count('.') - 1
    features['contains_at_symbol'] = int('@' in url)
    features['has_redirect'] = int('//' in url[7:])
    features['contains_hyphen'] = int('-' in url)
    features['num_slashes'] = url.count('/')
    domain_match = re.search(r'://([^/]+)', url)
    features['domain_length'] = len(domain_match.group(1)) if domain_match else 0

    return list(features.values())

# 2 DEFINE A FUNCTION THAT OPENS AN HTML FILE AND RETURNS THE CONTENT
def open_file(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        return f.read()

# 3 DEFINE A FUNCTION THAT CREATES A VECTOR BY RUNNING ALL FEATURE FUNCTIONS FOR THE SOUP OBJECT
def create_vector(soup):
    return [
        fe.has_title(soup),
        fe.has_input(soup),
        fe.has_button(soup),
        fe.has_image(soup),
        fe.has_submit(soup),
        fe.has_link(soup),
        fe.has_password(soup),
        fe.has_email_input(soup),
        fe.has_hidden_element(soup),
        fe.has_audio(soup),
        fe.has_video(soup),
        fe.number_of_inputs(soup),
        fe.number_of_buttons(soup),
        fe.number_of_images(soup),
        fe.number_of_option(soup),
        fe.number_of_list(soup),
        fe.number_of_TH(soup),
        fe.number_of_TR(soup),
        fe.number_of_href(soup),
        fe.number_of_paragraph(soup),
        fe.number_of_script(soup),
        fe.length_of_title(soup),
        fe.has_h1(soup),
        fe.has_h2(soup),
        fe.has_h3(soup),
        fe.length_of_text(soup),
        fe.number_of_clickable_button(soup),
        fe.number_of_a(soup),
        fe.number_of_img(soup),
        fe.number_of_div(soup),
        fe.number_of_figure(soup),
        fe.has_footer(soup),
        fe.has_form(soup),
        fe.has_text_area(soup),
        fe.has_iframe(soup),
        fe.has_text_input(soup),
        fe.number_of_meta(soup),
        fe.has_nav(soup),
        fe.has_object(soup),
        fe.has_picture(soup),
        fe.number_of_sources(soup),
        fe.number_of_span(soup),
        fe.number_of_table(soup)
    ]

# 4 DEFINE A FUNCTION THAT CREATES A VECTOR FROM A URL OR HTML FILE
def extract_features_from_url_or_html(url_or_file):
    if os.path.isfile(url_or_file):
        # If input is a file, extract HTML features
        soup = BeautifulSoup(open_file(url_or_file), "html.parser")
        return create_vector(soup)
    else:
        # Otherwise, assume it's a URL and extract URL features
        return create_url_vector(url_or_file)

# 5 EXTRACT FEATURES FROM A FOLDER OF HTML FILES
folder = 'mini_dataset'

def create_2d_list(folder_name):
    data = []
    for file in sorted(os.listdir(folder_name)):
        if file.endswith('.html'):
            file_path = os.path.join(folder_name, file)
            soup = BeautifulSoup(open_file(file_path), "html.parser")
            data.append(create_vector(soup))
    return data

# Create a DataFrame with the extracted features
data = create_2d_list(folder)

columns = [
    'has_title',
    'has_input',
    'has_button',
    'has_image',
    'has_submit',
    'has_link',
    'has_password',
    'has_email_input',
    'has_hidden_element',
    'has_audio',
    'has_video',
    'number_of_inputs',
    'number_of_buttons',
    'number_of_images',
    'number_of_option',
    'number_of_list',
    'number_of_th',
    'number_of_tr',
    'number_of_href',
    'number_of_paragraph',
    'number_of_script',
    'length_of_title',
    'has_h1',
    'has_h2',
    'has_h3',
    'length_of_text',
    'number_of_clickable_button',
    'number_of_a',
    'number_of_img',
    'number_of_div',
    'number_of_figure',
    'has_footer',
    'has_form',
    'has_text_area',
    'has_iframe',
    'has_text_input',
    'number_of_meta',
    'has_nav',
    'has_object',
    'has_picture',
    'number_of_sources',
    'number_of_span',
    'number_of_table'
]

df = pd.DataFrame(data=data, columns=columns)

print(df)
