from flask import Flask, render_template, request, jsonify, send_file
from scraper import scrape_website  # Import your scraper logic

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    website_url = request.form['website_url']
    data = scrape_website(website_url)  # This function scrapes the data

    # Return the scraped data in JSON format
    return jsonify(data)

@app.route('/download_json', methods=['POST'])
def download_json():
    website_url = request.form['website_url']
    data = scrape_website(website_url)

    # Save the data to a JSON file
    import json
    filename = 'scraped_data.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
