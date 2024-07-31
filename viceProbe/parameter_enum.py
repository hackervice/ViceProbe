import requests
from urllib.parse import urlparse, parse_qs

def parameter_enum(domain):
    input_file = 'temp/href_inside_scope_results.txt'
    output_file = 'temp/parameter_enum_results.txt'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    with open(input_file, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    results = []

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                parsed_url = urlparse(url)
                params = parse_qs(parsed_url.query)
                if params:
                    results.append({'url': url, 'parameters': params})
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")

    with open(output_file, 'w') as file:
        for result in results:
            file.write(f"URL: {result['url']}\n")
            for param, values in result['parameters'].items():
                file.write(f"  {param}: {', '.join(values)}\n")

    print(f"Parameter enumeration completed. Results saved to {output_file}")