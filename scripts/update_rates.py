# scripts/update_rates.py

import os
import requests
import yaml
import glob
from datetime import datetime, timezone

# --- CONFIGURATION ---
# Define the posts you want to generate. You can add more dictionaries to this list.
POST_CONFIG = [
    {
        'from_code': 'SAR',
        'to_code': 'PKR',
        'from_full': 'Saudi Riyal',
        'to_full': 'Pakistani Rupee',
        'author': 'jane', # Author for the post front matter
        'image': 'assets/images/sar-to-pkr-rate-today.jpg'
    },
    {
        'from_code': 'AED',
        'to_code': 'PKR',
        'from_full': 'UAE Dirham',
        'to_full': 'Pakistani Rupee',
        'author': 'jane',
        'image': 'assets/images/aed-to-pkr-rate-today.jpg'
    },
    {
        'from_code': 'USD',
        'to_code': 'PKR',
        'from_full': 'US Dollar',
        'to_full': 'Pakistani Rupee',
        'author': 'jane',
        'image': 'assets/images/usd-to-pkr-rate-today.jpg'
    }
    # Add more currency pairs here as needed
]

def generate_conversion_table(rate, from_code, to_code):
    """Generates a Markdown table for various conversion amounts."""
    amounts = [1, 2, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
    table = f"| {from_code} | {to_code} |\n"
    table += "| --- | --- |\n"
    for amount in amounts:
        converted = amount * rate
        table += f"| {amount:,} {from_code} | Rs. {converted:,.2f} |\n"
    return table

def generate_post_content(config, rate, date_str):
    """Generates the full Markdown content for a blog post."""
    from_code, to_code = config['from_code'], config['to_code']
    from_full, to_full = config['from_full'], config['to_full']

    # Generate the dynamic parts
    title = f"{from_full} {from_code} to {to_full} {to_code} Rate Today – {date_str}"
    h1_title = f"{from_full} to {to_full} Exchange Rate – {date_str}"
    rate_str = f"1 {from_code} = {rate:,.2f} {to_code}"
    table = generate_conversion_table(rate, from_code, to_code)
    
    # This is the Markdown template for the post
    content = f"""---
layout: post
title:  '{title}'
author: {config['author']}
categories: [ {from_code.lower()} to {to_code.lower()} ]
image: {config['image']}
tags: [{from_code.lower()},{to_code.lower()}]
---

# {h1_title}

If you’re looking for the latest exchange rate of {from_full} ({from_code}) to {to_full} ({to_code}), then you’re in the right place. As of {date_str}, the mid-market exchange rate stands at:

**{rate_str}**

This rate is updated as per reliable financial data sources and is helpful for anyone sending money, planning travel, or doing business involving {from_code} to {to_code} conversions.

{table}

## Why Keeping Track of Exchange Rates Matters

Exchange rates can fluctuate daily due to global economic conditions, making it crucial to stay informed. The rate provided here reflects mid-market values and may differ slightly based on the exchange service or bank you use.
"""
    return content

def main():
    """Main function to update rates and generate posts."""
    try:
        # --- JOB 1: UPDATE rates.yml (Existing Logic) ---
        print("Starting Job 1: Updating rates.yml")
        api_key = os.environ['CURRENCY_API_KEY']
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('result') == 'error':
            raise Exception(f"API returned an error: {data.get('error-type')}")

        master_rates = data['conversion_rates']
        output_data = {
            'last_updated_utc': datetime.now(timezone.utc).isoformat(),
            'rates': master_rates
        }
        with open('_data/rates.yml', 'w') as f:
            yaml.dump(output_data, f)
        print("Successfully updated _data/rates.yml")

        # --- JOB 2: GENERATE MARKDOWN POSTS (New Logic) ---
        print("\nStarting Job 2: Generating Markdown posts")
        today = datetime.now(timezone.utc)
        date_slug = today.strftime('%Y-%m-%d')
        date_str_formatted = today.strftime('%d %B %Y')

        for config in POST_CONFIG:
            from_code, to_code = config['from_code'], config['to_code']
            print(f"--- Processing post for {from_code} to {to_code} ---")

            # Calculate the specific exchange rate
            rate = (1 / master_rates[from_code]) * master_rates[to_code]

            # Define file paths and names
            post_dir = "_posts"
            file_slug = f"today-{from_code.lower()}-to-{to_code.lower()}-prices-updated"
            filename = f"{date_slug}-{file_slug}.md"
            filepath = os.path.join(post_dir, filename)

            # Clean up old posts for the same currency pair to avoid duplicates
            old_files = glob.glob(os.path.join(post_dir, f"*-{file_slug}.md"))
            for old_file in old_files:
                if old_file != filepath: # Don't delete the file we are about to create
                    print(f"Deleting old post: {old_file}")
                    os.remove(old_file)
            
            # Generate the full content for the new post
            post_content = generate_post_content(config, rate, date_str_formatted)
            
            # Write the new post file
            os.makedirs(post_dir, exist_ok=True) # Ensure the _posts directory exists
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(post_content)
            print(f"Successfully created new post: {filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
