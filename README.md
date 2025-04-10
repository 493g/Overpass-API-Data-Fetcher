# Overpass-API-Data-Fetcher


## Overview

This project contains a Python script (`test.py`) that demonstrates how to use the Overpass API to fetch data from OpenStreetMap (OSM). The current implementation is focused on retrieving tourist attractions within a specified city and saving the results to a CSV file.

## Prerequisites

* **Python 3.x**
* **pip** (Python package installer)
* **requests:**
    ```bash
    pip install requests
    ```
* **csv:** (Built-in Python library)

## How to Run the Script

1.  **Save the Python code:** Save the provided Python script (e.g., `test.py`).

2.  **Navigate to the project directory:** Open your terminal or command prompt and navigate to the directory where you saved the file.

3.  **Run the script:** Execute the script using the Python interpreter. You will be prompted to enter the city name:
    ```bash
    python test.py
    ```

4.  **Enter the city name:** When prompted, type the name of the city you want to query (e.g., `London`) and press Enter.

5.  **Observe the output:** The script will print messages indicating the progress of fetching data from the Overpass API.

6.  **Find the CSV file:** Upon successful completion, a CSV file named after the city (e.g., `london_tourist_attractions.csv`) will be created in the same directory, containing the extracted tourist attraction data.

## Script Details

The Python script (`test.py`) performs the following actions:

1.  **Imports necessary libraries:** `requests`, `json`, and `csv`.
2.  **Defines `fetch_tourist_attractions(city_name)` function:**
    * Takes the `city_name` as input.
    * Constructs an Overpass QL (Query Language) query to find tourist attractions (nodes, ways, and relations tagged with `tourism=*`) within the specified city.
    * Sends a POST request to the Overpass API endpoint (`https://overpass-api.de/api/interpreter`).
    * Handles potential network errors (`requests.exceptions.RequestException`) and JSON decoding errors (`json.JSONDecodeError`).
    * Parses the JSON response from the Overpass API.
    * Extracts relevant information for each tourist attraction, including its type, ID, name, tourism tag, latitude, and longitude.
    * Stores the extracted data in a list of dictionaries.
    * Returns the list of tourist attractions.
3.  **Defines `save_to_csv(data, filename)` function:**
    * Takes the `data` (list of attraction dictionaries) and the `filename` for the CSV as input.
    * Defines the basic fieldnames for the CSV file (`type`, `id`, `name`, `tourism`, `latitude`, `longitude`).
    * Dynamically identifies any other unique tags present in the data and adds them as additional columns in the CSV.
    * Writes the header row and the data rows to the specified CSV file.
    * Handles potential file I/O errors (`IOError`).
4.  **Main execution block (`if __name__ == "__main__":`)**:
    * Prompts the user to enter the city name.
    * Constructs the output filename based on the entered city name.
    * Calls the `fetch_tourist_attractions()` function to retrieve the data.
    * If data is successfully fetched, it prints the number of attractions found and calls the `save_to_csv()` function to save the data.
    * If no data is found, it prints a corresponding message.

## Example Usage

1.  Run the script: `python overpass_fetcher.py`
2.  Enter a city name when prompted: `Pune`
3.  The script will fetch tourist attractions in Pune and save the data to `pune_tourist_attractions.csv`.

## Notes and Considerations

* **Overpass API Usage:** Be mindful of the usage policies of the Overpass API. Avoid making excessive requests in a short period. Consider using a local Overpass instance if you plan to perform large or frequent queries.
* **Data Accuracy:** The data retrieved depends on the information available in OpenStreetMap. The tagging and completeness of data can vary.
* **Query Customization:** The Overpass QL query in the script can be modified to fetch different types of data or apply more specific filters. Refer to the Overpass API documentation for more details on query syntax.
* **Error Handling:** The script includes basic error handling for network and JSON decoding issues. More robust error handling and logging could be added for production use.
* **Rate Limiting:** While this script makes a single request per execution, if you intend to run it repeatedly or for multiple cities in quick succession, consider implementing delays between requests to avoid being rate-limited by the Overpass API.

This script provides a starting point for fetching data from the Overpass API. You can extend and modify it to retrieve various types of geographic data based on your needs.
