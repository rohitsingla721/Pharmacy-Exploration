import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of store names
store_names = [
    "city-x-ray-and-scan-clinic-tilak-nagar-1",
    "suraksha-diagnostic-janakpuri-10",
    "crl-diagnostics-paschim-vihar-8",
    "mahajan-imaging-defence-colonny-13",
    "cee-dee-diagnostics-18",
    "janta-x-ray-clinic-janakpuri-d1-37",
    "mahajan-imaging-pusa-road-53",
    "saksham-imaging-and-diagnostics-center-64",
    "saksham-imaging-and-diagnostics-center-64",
    "healthians-82"
]

# Create an empty list to store lab information
lab_data = []

# Loop through each store name
for store_name in store_names:
    # Construct the URL
    url = f"https://www.labuncle.com/labDetails/{store_name}"

    # Make the request
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check if the lab name element exists
    lab_name_element = soup.find('h1', {'class': 'bann-heading'})
    lab_name = lab_name_element.text.strip() if lab_name_element else "Lab name not found"

    # Check if the lab location element exists
    lab_location_element = soup.find('span', {'class': 'ban-lab-add'})
    lab_location = lab_location_element.text.strip() if lab_location_element else "Location not found"

    # Check if the discount element exists
    discount_element = soup.find('div', {'class': 'banner-discount'})
    discount = discount_element.text.strip() if discount_element else "Discount not found"

    # Check if the description element exists
    description_element = soup.find('p', {'class': 'text-lg-center text-md-left mt-4'})
    description = description_element.text.strip() if description_element else "Description not found"

    # Extracting facilities and links
    facilities = []
    for facility_li in soup.select('.lab-faci li'):
        facility_name = facility_li.find('a').text.strip()
        facility_link = facility_li.find('a')['href']
        facilities.append({
            "Lab Name": lab_name,
            "Location": lab_location,
            "Discount": discount,
            "Description": description,
            "Facility Name": facility_name,
            "Facility Link": facility_link,
            "URL": url
        })

    # Displaying the information
    print(f"\nLab Name: {lab_name}")
    print(f"Location: {lab_location}")
    print(f"Discount: {discount}")
    print(f"Description: {description}")
    print("Facilities:")
    for facility in facilities:
        print(f" - {facility['Facility Name']}: {facility['Facility Link']}")
    print(f"URL: {url}")
    print(f"---------------------------\n")

    # Append data to lab_data list
    lab_data.extend(facilities)

# Create a DataFrame from the list
lab_data_df = pd.DataFrame(lab_data)

# Save DataFrame to CSV
lab_data_df.to_csv("lab_information.csv", index=False)

print("\nData saved to lab_information.csv")
