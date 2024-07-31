import subprocess
import os

def assetfinder_subdomains(domain):
    result = subprocess.run(['assetfinder', '--subs-only', domain],
                            capture_output=True, text=True, check=True)
    subdomains = result.stdout.strip().split('\n')
    cleaned_subdomains = {sub.lstrip('*.') for sub in subdomains if sub}

    file_path = os.path.join('temp', 'assetfinder_results.txt')
    with open(file_path, 'w') as file:
        for subdomain in sorted(cleaned_subdomains):
            file.write(f"{subdomain}\n")

    print(f"Subdomains saved to {file_path}")
    return cleaned_subdomains
