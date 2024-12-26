from flask import Flask, render_template, request, jsonify
from pyvirtualdisplay import Display
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

app = Flask(__name__)

# Start virtual display (for headless environments)
try:
    display = Display(visible=0, size=(800, 600))
    display.start()
except Exception as e:
    print(f"Virtual display could not start: {e}")

# Headers for requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to fetch webpage content
def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}"

# Function to extract links from a webpage
def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc:  # Ensure same domain
            links.add(full_url)
    return links

# Function to extract structured data from the webpage
def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")
    data = {}

    # Extract title and meta description
    data['title'] = soup.title.string if soup.title else "N/A"
    meta_desc = soup.find("meta", attrs={"name": "description"})
    data['description'] = meta_desc["content"] if meta_desc else "N/A"

    # Extract visible text
    data['text'] = " ".join(soup.stripped_strings)

    # Detect APIs or database mentions in the text
    api_patterns = re.findall(r'https?://[^\s"]+', data['text'])
    data['apis'] = api_patterns

    # Detect potential client mentions
    data['clients'] = re.findall(r'client[s]?\s?:\s?[\w, ]+', data['text'], re.IGNORECASE)

    return data

# Recursive scraper
def deep_scrape(url, max_depth=2, visited=None, results=None):
    if visited is None:
        visited = set()
    if results is None:
        results = []
    if max_depth == 0 or url in visited:
        return results

    visited.add(url)
    html = fetch_page(url)
    if not html or "Error" in html:
        results.append({url: "Error or inaccessible"})
        return results

    data = extract_data(html)
    results.append({url: data})

    links = extract_links(html, url)
    for link in links:
        deep_scrape(link, max_depth - 1, visited, results)

    return results

# Routes for Flask
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    website_url = request.form['url']
    depth = int(request.form['depth'])

    if not website_url:
        return jsonify({"error": "Please enter a website URL."})

    results = deep_scrape(website_url, max_depth=depth)
    scrape_results = []

    for result in results:
        for url, data in result.items():
            result_data = {"url": url}
            if isinstance(data, dict):
                for key, value in data.items():
                    result_data[key] = value
            else:
                result_data['error'] = data
            scrape_results.append(result_data)

    return jsonify({"results": scrape_results})

if __name__ == '__main__':
    app.run(debug=True)
