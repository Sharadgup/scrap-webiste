import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Extract title, description, and links
    title = soup.title.string if soup.title else 'No Title'
    description = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    description = description['content'] if description else 'No Description'

    # Extract all links
    links = [a['href'] for a in soup.find_all('a', href=True)]

    # Structure the data into a JSON format
    data = {
        'title': title,
        'description': description,
        'text': soup.get_text(),
        'links': links
    }

    return data
