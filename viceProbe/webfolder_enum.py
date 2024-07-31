import requests
import os

def webfolder_enum(domain):
    wordlist_path = 'wordlists/webfolder_wordlist.txt'
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file not found at {wordlist_path}")
        return

    with open(wordlist_path, 'r') as file:
        folders = [line.strip() for line in file if line.strip()]

    if not domain.startswith('https://'):
        domain = f'https://{domain}'

    results = []
    total_folders = len(folders)

    def check_url(url, depth=1):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                results.append(url)
                print(f"Found: {url}")
                if depth < 3:
                    for folder in folders:
                        check_url(f"{url}/{folder}", depth + 1)
        except requests.RequestException as e:
            print(f"Error: {url} ({e})")

    for folder in folders:
        check_url(f"{domain}/{folder}")

    output_file = 'temp/webfolder_results.txt'
    with open(output_file, 'w') as file:
        for result in results:
            file.write(f"{result}\n")

    print(f"Web folder enumeration completed. Results saved to {output_file}")
