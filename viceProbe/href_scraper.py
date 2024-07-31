import requests
from bs4 import BeautifulSoup
import os

def scrape_hrefs(domain):
    """
    Scrape href links, form actions, and other relevant tags from the given domain and save the results.
    """
    url = f"https://{domain}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: Unable to access {url}, {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    hrefs = soup.find_all('a', href=True)
    forms = soup.find_all('form', action=True)
    scripts = soup.find_all('script', src=True)
    links = soup.find_all('link', href=True)
    images = soup.find_all('img', src=True)

    inside_scope = []
    miscellaneous = []

    def categorize_link(link):
        if link.startswith('/'):
            return f"https://{domain}{link}"
        elif domain in link:
            return link
        else:
            return None

    for href in hrefs:
        link = categorize_link(href['href'])
        if link:
            inside_scope.append(link)
        else:
            miscellaneous.append(href['href'])

    for form in forms:
        link = categorize_link(form['action'])
        if link:
            inside_scope.append(link)
        else:
            miscellaneous.append(form['action'])

    for script in scripts:
        link = categorize_link(script['src'])
        if link:
            inside_scope.append(link)
        else:
            miscellaneous.append(script['src'])

    for link_tag in links:
        link = categorize_link(link_tag['href'])
        if link:
            inside_scope.append(link)
        else:
            miscellaneous.append(link_tag['href'])

    for img in images:
        link = categorize_link(img['src'])
        if link:
            inside_scope.append(link)
        else:
            miscellaneous.append(img['src'])

    inside_scope = list(set(inside_scope))
    miscellaneous = list(set(miscellaneous))

    os.makedirs('temp', exist_ok=True)
    with open('temp/href_inside_scope_results.txt', 'w') as file:
        for link in inside_scope:
            file.write(f"{link}\n")

    with open('temp/href_miscellaneous_results.txt', 'w') as file:
        for link in miscellaneous:
            file.write(f"{link}\n")

    print("Href scraping completed. Results saved.")

if __name__ == "__main__":
    # Example usage
    scrape_hrefs("example.com")
