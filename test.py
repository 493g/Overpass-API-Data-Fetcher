import requests
import json
import csv
import pandas as pd

def fetch_tourist_attractions(city_name):
    """
    Fetches tourist attractions data from Overpass API for a given city.

    Args:
        city_name (str): The name of the city to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents a
              tourist attraction with its details (name, latitude, longitude, tags).
              Returns an empty list if no attractions are found or if an error occurs.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    area[name="{city_name}"][place~"city|town|village"]->.searchArea;
    (
      node(area.searchArea)[tourism];
      way(area.searchArea)[tourism];
      relation(area.searchArea)[tourism];
    );
    out center;
    """
    params = {"data": query}
    try:
        response = requests.post(overpass_url, data=params, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        attractions = []
        for element in data['elements']:
            if 'tags' in element and 'tourism' in element['tags']:
                attraction = {
                    'type': element['type'],
                    'id': element['id'],
                    'name': element['tags'].get('name', 'N/A'),
                    'tourism': element['tags']['tourism'],
                    'latitude': None,
                    'longitude': None,
                    'other_tags': element['tags']
                }
                if 'center' in element:
                    attraction['latitude'] = element['center']['lat']
                    attraction['longitude'] = element['center']['lon']
                elif 'lat' in element and 'lon' in element:
                    attraction['latitude'] = element['lat']
                    attraction['longitude'] = element['lon']
                if 'name' in attraction['other_tags']:
                    del attraction['other_tags']['name']
                attractions.append(attraction)
        return attractions
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Overpass API: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return []

def save_to_csv(data, filename):
    """
    Saves the fetched tourist attractions data to a CSV file.

    Args:
        data (list): A list of dictionaries representing tourist attractions.
        filename (str): The name of the CSV file to save to.
    """
    if not data:
        print("No tourist attractions data to save.")
        return

    fieldnames = ['type', 'id', 'name', 'tourism', 'latitude', 'longitude']
    # Collect all unique other tags to add as columns
    other_tags_keys = set()
    for item in data:
        if 'other_tags' in item:
            other_tags_keys.update(item['other_tags'].keys())
    fieldnames.extend(sorted(list(other_tags_keys)))

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in data:
                row = {key: item.get(key) for key in fieldnames[:6]} # Basic fields
                if 'other_tags' in item:
                    row.update(item['other_tags'])
                writer.writerow(row)
        print(f"Tourist attractions data saved to {filename}")
    except IOError as e:
        print(f"Error saving to CSV file: {e}")

if __name__ == "__main__":
    city_name = input("Enter the city name: ")
    output_filename = f"{city_name.lower().replace(' ', '_')}_tourist_attractions.csv"

    print(f"Fetching tourist attractions in {city_name}...")
    tourist_data = fetch_tourist_attractions(city_name)

    if tourist_data:
        print(f"Found {len(tourist_data)} tourist attractions.")
        save_to_csv(tourist_data, output_filename)
        print(f"Data saved to {output_filename}")
    else:
        print(f"No tourist attractions data found for {city_name}.")

    filename = f"{city_name.lower().replace(' ', '_')}_tourist_attractions.csv"
    df = pd.read_csv(filename, low_memory=False)

    print("🔹 Original data shape:", df.shape)

    # 1. Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # 2. Drop rows where 'name' or 'latitude' or 'longitude' is missing
    df.dropna(subset=['name', 'latitude', 'longitude'], inplace=True)

    # 3. Standardize name column to title case
    df['name'] = df['name'].str.title()

    # 4. Remove unnamed columns (often created by mistake)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 5. Ensure correct data types
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    # 6. Reset index after cleaning
    df.reset_index(drop=True, inplace=True)

    # 7. Optional: Rename columns for clarity
    df.rename(columns={
        'name': 'Place Name',
        'type': 'Place Type',
        'latitude': 'Latitude',
        'longitude': 'Longitude'
    }, inplace=True)

    # 8. Save cleaned CSV
    cleaned_filename = filename.replace(".csv", "_cleaned.csv")
    df.to_csv(cleaned_filename, index=False)

    print("✅ Cleaned data saved as:", cleaned_filename)
    print("🔹 Cleaned data shape:", df.shape)
