import subprocess
import json
import os

def active_subdomain_enum(domain):
    wordlist_path = 'wordlists/subdomains_wordlist.txt'
    output_path = 'temp/ffuf_output.json'

    try:
        # Adjusted ffuf command to match the desired syntax
        result = subprocess.run(
            ['ffuf', '-w', wordlist_path, '-u', f'https://FUZZ.{domain}', '-mc', '200', '-o',
             output_path, '-of', 'json'],
            capture_output=True, text=True, check=True)

        with open(output_path, 'r') as file:
            ffuf_results = json.load(file)

        active_results = []
        for res in ffuf_results['results']:
            active_results.append({
                'url': res['url'],
                'host': res['input']['FUZZ'],
                'status': res['status'],
                'content-type': res['content-type']
            })

        output_clean_path = 'temp/active_subdomains_clean.txt'
        with open(output_clean_path, 'w') as file:
            for result in active_results:
                file.write(f"{result['host']}.{domain}\n")

        print(f"Active subdomain enumeration completed. Results saved to {output_clean_path}")
        return active_results

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running ffuf: {e}")
        return None
