import requests
from bs4 import BeautifulSoup
import re
import sys

# Set encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.netmeds.com/prescriptions"
names = []

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
links = soup.find_all('a', href=lambda href: href and "/prescriptions/" in href)

# Collect all names from the initial links
names = [link.text.strip() for link in links]

# Display data for each collected name
for name in names:
    # Generate new link based on the name, removing hyphens and digits in parentheses
    cleaned_name = ''.join(char for char in name if char.isalpha() or char.isspace()).strip()
    new_link = f"https://www.netmeds.com/prescriptions/{cleaned_name.lower().replace(' ', '-')}"

    # Fetch data from the new link
    new_r = requests.get(new_link)
    new_soup = BeautifulSoup(new_r.text, "html.parser")

    # Extract and display all <a> tags without the 'class' and with the 'href' attribute
    div_prescriptions_products = new_soup.find('div', class_='prescriptions_products')
    if div_prescriptions_products:
        all_tags_on_new_page = [tag for tag in div_prescriptions_products.find_all('a', class_=False, href=True) if not tag.get('class')]

        # Filter and print only names starting with 'b' or 'f'
        for a_tag in all_tags_on_new_page:
            text_content = a_tag.text.strip()
            if text_content and text_content[0].lower() in ['b', 'f']:
                print(f" {text_content}")
                print(f" {a_tag['href']}")

                # Fetch content from the link and display only span tags
                link_content_r = requests.get(a_tag['href'])
                link_content_soup = BeautifulSoup(link_content_r.text, "html.parser")

                # Extract the manufacturer information from span tags, excluding 'drug-manu ellipsis' class
                span_tags_manufacturer = link_content_soup.find_all('span', class_='drug-manu')
                span_tags_manufacturer = [span for span in span_tags_manufacturer if 'ellipsis' not in span.get('class', [])]

                for span_tag_manufacturer in span_tags_manufacturer:
                    try:
                        print(f"   Span Tag (Manufacturer): {span_tag_manufacturer.text.strip()}")
                        print(f"   ---------------")
                    except UnicodeEncodeError:
                        print("   UnicodeEncodeError: Unable to print this span tag (Manufacturer) due to encoding issue")

                # Extract the discounted price using regular expression from the first occurrence of span tag with class 'final-price'
                span_tag_discounted_price = link_content_soup.find('span', class_='final-price')
                try:
                    discounted_price_match = re.search(r'\d+(\.\d{1,2})?', span_tag_discounted_price.text)
                    if discounted_price_match:
                        discounted_price = discounted_price_match.group()
                        print(f"   Discounted Price: ₹ {discounted_price}")
                        print(f"   ---------------")
                except UnicodeEncodeError:
                    print("   UnicodeEncodeError: Unable to print this span tag (Discounted Price) due to encoding issue")

                # Extract the actual price using regular expression from span tags with class 'price'
                span_tags_actual_price = link_content_soup.find_all('span', class_='price')
                for span_tag_actual_price in span_tags_actual_price:
                    try:
                        actual_price_match = re.search(r'\d+(\.\d{1,2})?', span_tag_actual_price.text)
                        if actual_price_match:
                            actual_price = actual_price_match.group()
                            print(f"   Actual Price: ₹ {actual_price}")
                            print(f"   ---------------")
                    except UnicodeEncodeError:
                        print("   UnicodeEncodeError: Unable to print this span tag (Actual Price) due to encoding issue")

    # Special handling for links like 'Bactoclav 375mg Tablet 10'S'
    if cleaned_name.lower().startswith(('b', 'f')):
        print(f"{cleaned_name} - {new_link}")
