# scripts/update_rates.py

import os
import requests
import yaml
from datetime import datetime, timezone

def main():
    """
    Fetches the latest currency exchange rates and writes them to a YAML file.
    """
    try:
        # Fetch the API key from the environment variables (set by GitHub Actions)
        api_key = os.environ['CURRENCY_API_KEY']
        
        # We use USD as the base because it's the most common and ensures
        # we get a full list of conversion rates from the API.
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

        print(f"Fetching rates from {url}")
        response = requests.get(url)
        # This will raise an HTTPError if the response was an error (e.g., 401, 404)
        response.raise_for_status() 
        data = response.json()

        if data.get('result') == 'error':
            raise Exception(f"API returned an error: {data.get('error-type')}")

        # Prepare the data structure for the YAML file
        output_data = {
            'last_updated_utc': datetime.now(timezone.utc).isoformat(),
            'rates': data['conversion_rates']
        }

        # Define the path to the data file
        data_file_path = '_data/rates.yml'

        # Write the data to the YAML file
        print(f"Writing updated rates to {data_file_path}")
        with open(data_file_path, 'w') as f:
            yaml.dump(output_data, f)
        
        print("Successfully updated _data/rates.yml")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Exit with a non-zero status code to fail the GitHub Actions job
        exit(1)

if __name__ == "__main__":
    main()