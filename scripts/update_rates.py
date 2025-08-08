import os
import requests
import yaml
import glob
from datetime import datetime, timezone
import random

# --- CONFIGURATION ---
# Load the post generation config from a YAML file
with open('_data/post_generator_config.yml', 'r') as f:
    POST_CONFIG = yaml.safe_load(f)['post_configs']

def generate_conversion_table(rate, from_code, to_code):
    """Generates a Markdown table for various conversion amounts."""
    amounts = [1, 5, 10, 25, 50, 100, 500, 1000, 5000, 10000]
    table = f"| {from_code} | {to_code} |\n"
    table += "| --- | --- |\n"
    for amount in amounts:
        converted = amount * rate
        table += f"| {amount:,} {from_code} | {to_code} {converted:,.2f} |\n"
    return table

def generate_faqs(faqs, rate):
    """Generates a Markdown formatted FAQ section."""
    faq_content = "## Frequently Asked Questions (FAQs)\n\n"
    for faq in faqs:
        # Replace placeholder for dynamic value if it exists
        answer = faq['answer'].replace('[calculated_value]', f"{1000 * rate:,.2f}")
        faq_content += f"### {faq['question']}\n\n{answer}\n\n"
    return faq_content

def generate_post_content(config, rate, date_str):
    """Generates the full Markdown content for a blog post."""
    from_code, to_code = config['from_code'], config['to_code']
    from_full, to_full = config['from_full'], config['to_full']

    # Title variations for better SEO
    title_templates = [
        f"{from_full} ({from_code}) to {to_full} ({to_code}) Rate Today – {date_str}",
        f"Today's {from_code} to {to_code} Exchange Rate: {date_str}",
        f"Live {from_full} to {to_full} Rate on {date_str}",
    ]
    title = random.choice(title_templates)
    
    h1_title = f"{from_full} to {to_full} Exchange Rate – {date_str}"
    rate_str = f"**1 {from_code} = {rate:,.2f} {to_code}**"
    table = generate_conversion_table(rate, from_code, to_code)
    faqs = generate_faqs(config.get('faqs', []), rate)
    
    content = f"""---
layout: post
title:  '{title}'
author: {config['author']}
categories: [ {from_code.lower()}-to-{to_code.lower()} ]
image: {config['image']}
tags: {config.get('keywords', [from_code.lower(), to_code.lower()])}
---

# {h1_title}

For anyone looking to convert {from_full} ({from_code}) to {to_full} ({to_code}), staying updated with the latest exchange rate is essential. As of {date_str}, the current mid-market rate is:

{rate_str}

This rate is a benchmark for currency conversion and is sourced from reliable global financial data providers.

{table}

## Understanding Exchange Rate Fluctuations

Exchange rates are dynamic and can change due to a variety of economic and geopolitical factors. The rate provided here is the mid-market rate, which means it's the midpoint between the buy and sell rates on the global currency markets. When you exchange money through a bank or a remittance service, they will typically offer a rate that includes a small margin.

{faqs}

*Disclaimer: The exchange rates provided are for informational purposes only and are subject to change. For the most accurate rates, please consult with your financial institution or a currency exchange service.*
"""
    return content

def main():
    """Main function to update rates and generate posts."""
    try:
        print("Starting Job 1: Updating rates.yml")
        api_key = os.environ.get('CURRENCY_API_KEY')
        if not api_key:
            raise Exception("CURRENCY_API_KEY environment variable not set.")
            
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

        print("\nStarting Job 2: Generating Markdown posts")
        today = datetime.now(timezone.utc)
        date_slug = today.strftime('%Y-%m-%d')
        date_str_formatted = today.strftime('%d %B %Y')
        day, month_name, year = date_str_formatted.split()

        for config in POST_CONFIG:
            from_code, to_code = config['from_code'], config['to_code']
            from_full, to_full = config['from_full'], config['to_full']
            print(f"--- Processing post for {from_code} to {to_code} ---")

            if from_code not in master_rates or to_code not in master_rates:
                print(f"Warning: Currency code not found in API rates. Skipping {from_code} to {to_code}.")
                continue

            rate = master_rates[to_code] / master_rates[from_code]
            
            post_dir = "_posts"
            file_slug = f"today-{from_full.lower().replace(' ','-')}-to-{to_code.lower()}-exchange-rate-{month_name.lower()}-{year}-prices-updated-{from_code.lower()}-to-{to_code.lower()}"
            filename = f"{date_slug}-{file_slug}.md"
            filepath = os.path.join(post_dir, filename)

            # Clean up old posts for the same currency pair
            for old_file in glob.glob(os.path.join(post_dir, f"*-{file_slug}.md")):
                if old_file != filepath:
                    print(f"Deleting old post: {old_file}")
                    os.remove(old_file)
            
            post_content = generate_post_content(config, rate, date_str_formatted)
            
            os.makedirs(post_dir, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(post_content)
            print(f"Successfully created or updated post: {filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()


