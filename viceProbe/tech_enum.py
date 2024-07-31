import os

from Wappalyzer import Wappalyzer, WebPage

def enumerate_tech(domain):
    """
    Use Wappalyzer to find technologies used by the given domain and save the results.
    """
    wappalyzer = Wappalyzer.latest()
    webpage = WebPage.new_from_url(f"https://{domain}")

    technologies = wappalyzer.analyze(webpage)

    file_path = os.path.join('temp', 'tech_enum_results.txt')
    with open(file_path, 'w') as file:
        for tech in technologies:
            file.write(f"{tech}\n")

    print(f"Technologies saved to {file_path}")
    return technologies
