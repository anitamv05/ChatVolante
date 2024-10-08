import json
import requests
from bs4 import BeautifulSoup

# Load URLs from the JSON file
with open('volante_urls.json', 'r') as file:
    urls = json.load(file)

# Function to scrape content from each URL
def scrape_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No Title'
            body_content = soup.find('body').get_text(strip=True) if soup.find('body') else 'No Content'
            return {"title": title, "link": url, "content": body_content}
        else:
            print(f"Failed to retrieve {url}")
            return {"title": "Failed to retrieve", "link": url, "content": ""}
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {"title": "Error", "link": url, "content": ""}

# Scrape content from each URL and store in a list
scraped_data = []
for url in urls:
    print(f"Scraping {url}")
    data = scrape_content(url)
    scraped_data.append(data)

# Save scraped data to a JSON file
with open('volante_posts.json', 'w') as json_file:
    json.dump(scraped_data, json_file, indent=4)

print(f"Scraped {len(scraped_data)} posts and saved to volante_posts.json")
