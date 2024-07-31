import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and Search Engine ID from environment variables
API_KEY = os.getenv('API_KEY')
SEARCH_ENGINE_ID = os.getenv('ENGINE_ID')


def google_dork_search(query, num_results=10):
    """
    Perform a Google Dork search using the Custom Search JSON API.

    Parameters:
    - query: The search query string.
    - num_results: The number of search results to retrieve (default is 10).

    Returns:
    - A list of search result items.
    """
    search_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': num_results  # Number of results to retrieve
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        results = response.json()
        return results.get('items', [])
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        print(f"URL: {response.url}")
        print(f"Response: {response.text}")
        return []


def enumerate_gd(domain):
    """
    Perform Google Dork Enumeration for the given domain.

    Parameters:
    - domain: The domain to enumerate.
    """
    print("Google Dork Enumeration")

    # Define the Google Dork query
    query = (f'site:*.{domain} '
             'ext:pdf | ext:doc | ext:docx | ext:odt | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv')

    # Print the query used for debugging
    print(f"Google Dork Query: {query}")

    # Perform the search
    results = google_dork_search(query, num_results=10)

    # Print the search results for debugging
    print("Search Results:")
    print(results)

    # Save the results to a file
    output_file = 'temp/gd_enum_results.txt'
    with open(output_file, 'w') as file:
        # Write the Google Dork query to the file
        file.write(f"Google Dork Query: {query}\n\n")

        if results:
            for result in results:
                title = result.get('title', 'No title')
                link = result.get('link', 'No link')
                snippet = result.get('snippet', 'No snippet')
                file.write(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n\n")
        else:
            file.write("No results found.")
