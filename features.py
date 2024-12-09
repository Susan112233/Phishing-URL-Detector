from bs4 import BeautifulSoup

# This section below is kept to allow testing the script independently if needed
with open('mini_dataset/9.html', 'r', encoding='utf-8') as f:
    test = f.read()

soup = BeautifulSoup(test, "html.parser")

# has_title
def has_title(soup):
    # Check if soup.title exists
    if soup.title and soup.title.text:
        return len(soup.title.text) > 0
    return 0  # Returning 0 instead of False for consistency

# has_input
def has_input(soup):
    return 1 if len(soup.find_all("input")) > 0 else 0

# has_button
def has_button(soup):
    return 1 if len(soup.find_all("button")) > 0 else 0

# has_image
def has_image(soup):
    return 1 if len(soup.find_all("img")) > 0 else 0  # Changed 'image' to 'img'

# has_submit
def has_submit(soup):
    for button in soup.find_all("input"):
        if button.get("type") == "submit":
            return 1
    return 0

# has_link
def has_link(soup):
    return 1 if len(soup.find_all("link")) > 0 else 0

# has_password
def has_password(soup):
    for input_tag in soup.find_all("input"):
        if input_tag.get("type") == "password":
            return 1
    return 0

# has_email_input
def has_email_input(soup):
    for input_tag in soup.find_all("input"):
        if input_tag.get("type") == "email":
            return 1
    return 0

# has_hidden_element
def has_hidden_element(soup):
    for input_tag in soup.find_all("input"):
        if input_tag.get("type") == "hidden":
            return 1
    return 0

# has_audio
def has_audio(soup):
    return 1 if len(soup.find_all("audio")) > 0 else 0

# has_video
def has_video(soup):
    return 1 if len(soup.find_all("video")) > 0 else 0

# number_of_inputs
def number_of_inputs(soup):
    return len(soup.find_all("input"))

# number_of_buttons
def number_of_buttons(soup):
    return len(soup.find_all("button"))

# number_of_images
def number_of_images(soup):
    return len(soup.find_all("img"))

# number_of_option
def number_of_option(soup):
    return len(soup.find_all("option"))

# number_of_list
def number_of_list(soup):
    return len(soup.find_all("li"))

# number_of_TH
def number_of_TH(soup):
    return len(soup.find_all("th"))

# number_of_TR
def number_of_TR(soup):
    return len(soup.find_all("tr"))

# number_of_href
def number_of_href(soup):
    return sum(1 for link in soup.find_all("a") if link.get("href"))

# number_of_paragraph
def number_of_paragraph(soup):
    return len(soup.find_all("p"))

# number_of_script
def number_of_script(soup):
    return len(soup.find_all("script"))

# length_of_title
def length_of_title(soup):
    return len(soup.title.text) if soup.title else 0

# has_h1
def has_h1(soup):
    return 1 if len(soup.find_all("h1")) > 0 else 0

# has_h2
def has_h2(soup):
    return 1 if len(soup.find_all("h2")) > 0 else 0

# has_h3
def has_h3(soup):
    return 1 if len(soup.find_all("h3")) > 0 else 0

# length_of_text
def length_of_text(soup):
    return len(soup.get_text())

# number_of_clickable_button
def number_of_clickable_button(soup):
    return sum(1 for button in soup.find_all("button") if button.get("type") == "button")

# number_of_a
def number_of_a(soup):
    return len(soup.find_all("a"))

# number_of_img
def number_of_img(soup):
    return len(soup.find_all("img"))

# number_of_div
def number_of_div(soup):
    return len(soup.find_all("div"))

# number_of_figure
def number_of_figure(soup):
    return len(soup.find_all("figure"))

# has_footer
def has_footer(soup):
    return 1 if len(soup.find_all("footer")) > 0 else 0

# has_form
def has_form(soup):
    return 1 if len(soup.find_all("form")) > 0 else 0

# has_text_area
def has_text_area(soup):
    return 1 if len(soup.find_all("textarea")) > 0 else 0

# has_iframe
def has_iframe(soup):
    return 1 if len(soup.find_all("iframe")) > 0 else 0

# has_text_input
def has_text_input(soup):
    return 1 if any(input_tag.get("type") == "text" for input_tag in soup.find_all("input")) else 0

# number_of_meta
def number_of_meta(soup):
    return len(soup.find_all("meta"))

# has_nav
def has_nav(soup):
    return 1 if len(soup.find_all("nav")) > 0 else 0

# has_object
def has_object(soup):
    return 1 if len(soup.find_all("object")) > 0 else 0

# has_picture
def has_picture(soup):
    return 1 if len(soup.find_all("picture")) > 0 else 0

# number_of_sources
def number_of_sources(soup):
    return len(soup.find_all("source"))

# number_of_span
def number_of_span(soup):
    return len(soup.find_all("span"))

# number_of_table
def number_of_table(soup):
    return len(soup.find_all("table"))

# Example usage to verify feature extraction
if __name__ == "__main__":
    print("has_title --> ", has_title(soup))
    print("has_input --> ", has_input(soup))
    print("has_button --> ", has_button(soup))
    print("has_image --> ", has_image(soup))
    print("has_submit --> ", has_submit(soup))
    print("has_link --> ", has_link(soup))
    print("has_password --> ", has_password(soup))
    print("has_email_input --> ", has_email_input(soup))
    print("has_hidden_element --> ", has_hidden_element(soup))
    print("has_audio --> ", has_audio(soup))
    print("has_video --> ", has_video(soup))
    print("number_of_inputs --> ", number_of_inputs(soup))
    print("number_of_buttons --> ", number_of_buttons(soup))
    print("number_of_images --> ", number_of_images(soup))
    print("number_of_option --> ", number_of_option(soup))
    print("number_of_list --> ", number_of_list(soup))
    print("number_of_TH --> ", number_of_TH(soup))
    print("number_of_TR --> ", number_of_TR(soup))
    print("number_of_href --> ", number_of_href(soup))
    print("number_of_paragraph --> ", number_of_paragraph(soup))
    print("number_of_script --> ", number_of_script(soup))
    print("length_of_title --> ", length_of_title(soup))
