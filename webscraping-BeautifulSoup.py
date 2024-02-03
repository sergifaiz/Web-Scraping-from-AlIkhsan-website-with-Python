from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import numpy as np

# Headers for requests - Create Request
# HTTP headers let the client and the server pass additional information with an HTTP request or response
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# link for Football boot for Nike Section 
base_url = 'https://al-ikhsan.com/football/footwear/nike.html'

# List to store all product links in searched page (Football - Nike)
all_links = []

# Loop through each page of loaded page, there are a button 'load more'
# Without this loop, it will read only 24 products
for page_number in range(1, 4):  
    # Construct URL for the current page
    each_url = f'{base_url}?p={page_number}'

    # Make an HTTP request to the webpage
    webpage = requests.get(each_url, headers=HEADERS)

    # Create a Soup object
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Find all links of every product in the current page
    links = soup.find_all("a", attrs={'class': 'product-item-link'})

    # Extract and store the all the links of every product in the list
    all_links.extend(link['href'] for link in links)

# Initialize an empty list products_list to store the details of each product
products_list = []

# Iterate through each product link
for link in all_links:
    # Store product details in an empty list
    product_details = {}

    # Make HTTP Request for indiv product link
    product_page = requests.get(link, headers=HEADERS)
    product_soup = BeautifulSoup(product_page.content, "html.parser")

    # Extract Product Details
    product_details['Product Name'] = product_soup.find("h1", attrs={"class": 'product-name'}).text.strip()
    product_details['Product Price'] = product_soup.find("span", attrs={"class": 'price'}).text.strip()
    product_details['SKU Code'] = product_soup.find("div", attrs={"itemprop": 'sku'}).text.strip()
    product_details['Image Link'] = product_soup.find("img", attrs={"class": "img-fluid"})['src']

    # Append the product details to the empty list
    products_list.append(product_details)

# Save the product details to a CSV file
csv_columns = ['Product Name', 'Product Price', 'SKU Code', 'Image Link']
csv_file = "product_details.csv"

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        
        # DictWriter - maps dictionaries (product_details) to CSV rows
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for product in products_list:
            writer.writerow(product)
    print(f"Product details saved to {csv_file}") #showing it is saved in the folder

    # Create DataFrame from the CSV file
    df = pd.read_csv(csv_file)

    # Replace empty values with NaN
    df.replace('', np.nan, inplace=True)

except IOError:
    print("I/O error")


