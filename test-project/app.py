from flask import Flask, render_template
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def scrape_website(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    subscription_plans = []
    plans = soup.find_all('div', class_='subscription-plan')
    for plan in plans:
        name = plan.find('h3', class_='plan-name').text.strip()
        price = plan.find('span', class_='price').text.strip()
        description = plan.find('p', class_='description').text.strip()
        subscription_plans.append({
            'name': name,
            'price': price,
            'description': description
        })
    
    user_stats = {
        'total_users': soup.find('span', class_='total-users').text.strip(),
        'total_likes': soup.find('span', class_='total-likes').text.strip(),
        'total_shares': soup.find('span', class_='total-shares').text.strip(),
        'total_views': soup.find('span', class_='total-views').text.strip(),
        'total_posts': soup.find('span', class_='total-posts').text.strip()
    }
    
    links = [a['href'] for a in soup.find_all('a', href=True)]
    driver.quit()

    return subscription_plans, user_stats, links

@app.route('/')
def home():
    url = 'YOUR_TARGET_URL_HERE'
    subscription_plans, user_stats, links = scrape_website(url)
    return render_template('index.html', subscription_plans=subscription_plans, user_stats=user_stats, links=links)

if __name__ == '__main__':
    app.run(debug=True)
