from bs4 import BeautifulSoup
import requests
import pandas as pd
from csv import writer
import json

sample_url = "https://www.redfin.com/city/30818/TX/Austin"


def scrape_redfin_sales(url, num_page = 30, headers=None):
    # change header and url to the user's configuration and interested city redfin website

    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    if headers is None:
        headers = headers

    address = []
    beds = []
    baths = []
    prices = []
    sqft = []
    sqft_lot = []
    description = []
    valid_latitudes = []
    valid_longitudes = []
    webpage = []
    type_home = []
    picture = []

    for i in range(1, num_page):
        website = requests.get(url + '/page-' + str(i), headers=headers)
        soup = BeautifulSoup(website.text, 'lxml')
        result = soup.find_all('div', class_="bp-Homecard")

        for res in result:
            address.append([lis.find('div', class_="bp-Homecard__Address").get_text() for lis in res if
                            lis.find('div', class_="bp-Homecard__Address") is not None])
            prices.append([lis.find('span', class_="bp-Homecard__Price--value").get_text() for lis in res if
                           lis.find('span', class_="bp-Homecard__Price--value") is not None])
            beds.append([lis.find('span', class_="bp-Homecard__Stats--beds").get_text() for lis in res if
                         lis.find('span', class_="bp-Homecard__Stats--beds") is not None])
            baths.append([lis.find('span', class_="bp-Homecard__Stats--baths").get_text() for lis in res if
                          lis.find('span', class_="bp-Homecard__Stats--baths") is not None])
            sqft.append([lis.find('span', class_="bp-Homecard__Stats--sqft").get_text() for lis in res if
                         lis.find('span', class_="bp-Homecard__Stats--sqft") is not None])
            sqft_lot.append([lis.find('span', class_="bp-Homecard__Stats--lotsize").get_text() for lis in res if
                             lis.find('span', class_="bp-Homecard__Stats--lotsize") is not None])
            description.append(
                [lis.find('div', class_="ListingRemarks ListingRemarks__withTitle").get_text()[39:] for lis in res if
                 lis.find('div', class_="ListingRemarks ListingRemarks__withTitle") is not None])

        script_tag = soup.find_all('script', type='application/ld+json')

        for i in range(len(script_tag)):
            try:
                # Extract the JSON data from the script tag
                json_data = json.loads(script_tag[i].string)
                geo_data = json_data[0]['geo']
                home_type_data = json_data[0]["@type"]
                url_data = json_data[0]["url"]
                latitude = geo_data['latitude']
                longitude = geo_data['longitude']
                valid_latitudes.append(latitude)
                valid_longitudes.append(longitude)
                type_home.append(home_type_data)
                webpage.append(url_data)

            except KeyError:
                # Skip the item if 'geo' property does not exist
                continue

        img_tags = soup.find_all('img', class_='bp-Homecard__Photo--image')
        if img_tags:
            for img_tag in img_tags:
                picture.append(img_tag['src'])
        else:
            print("picture not working at page: ", i)
            picture.append('NaN')

    concat_list = [address, prices, beds, baths, sqft, sqft_lot, description, valid_latitudes, valid_longitudes, webpage,
                   type_home, picture]

    real_estate_sales_df = _create_dataframe(concat_list)

    return real_estate_sales_df


def _create_dataframe(concat_list):
    flattened_list = [
        [item[0] if isinstance(item, list) and len(item) > 0 else item for item in sublist]
        for sublist in concat_list]
    real_estate_sale_df = pd.concat([pd.Series(x) for x in flattened_list], axis=1)
    real_estate_sale_df.columns = ['Address', 'Price', 'Bed', 'Bath', 'SQFT', 'Lot Sqft', 'Description', 'latitude',
                                   'longitude', 'Listing URL', 'Type of Home', 'Picture']
    real_estate_sale_df = real_estate_sale_df[real_estate_sale_df.astype(str)['Address'] != '[]']
    real_estate_sale_df = _df_preprocessing(real_estate_sale_df)

    return real_estate_sale_df


def _df_preprocessing(df):
    df['Bed'] = df['Bed'].str.replace(r'\D', '', regex=True)
    df['Bath'] = df['Bath'].str.replace(r'\D', '', regex=True)
    df['SQFT'] = df['SQFT'].str.replace(r'\D', '', regex=True)
    df['Lot Sqft'] = df['Lot Sqft'].str.replace(r'\D', '', regex=True)
    df['Street'] = df['Address'].apply(lambda x: x.split(',')[0])
    df['City'] = df['Address'].apply(lambda x: x.split(',')[1])
    df['State'] = df['Address'].apply(lambda x: x.split(',')[2].split(' ')[1])
    df['Zip Code'] = df['Address'].apply(lambda x: x.split(',')[2].split(' ')[2])
    return df


def _save_csv(df):
    df.to_csv("redfin_sales_data.csv")




