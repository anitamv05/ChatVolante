import requests
from lxml import etree
import json

# Function to extract URLs from sitemap
def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)

    # Check if the response content is XML
    if 'xml' in response.headers.get('Content-Type'):
        try:
            # Parse the XML response with lxml
            tree = etree.fromstring(response.content)
            # Extract URLs using XPath
            urls = tree.xpath('//xmlns:loc/text()', namespaces={'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
            return urls
        except etree.XMLSyntaxError as e:
            print(f"Error parsing XML from {sitemap_url}: {e}")
            return []
    else:
        print(f"Non-XML response from {sitemap_url}")
        return []

# List of sitemap URLs
sitemaps = [
    'https://www.volantetech.com/post-sitemap.xml',
    'https://www.volantetech.com/page-sitemap.xml',
    'https://www.volantetech.com/vtl_press_releases-sitemap.xml',
    'https://www.volantetech.com/resource-sitemap.xml'
]

all_urls = []
for sitemap in sitemaps:
    urls = get_urls_from_sitemap(sitemap)
    all_urls.extend(urls)

print(f"Scraped {len(all_urls)} URLs from sitemaps.")

# Function to scrape content from each URL
def scrape_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No Title'
        content = soup.find('body').get_text(strip=True) if soup.find('body') else 'No Content'
        return {"title": title, "link": url, "content": content}
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return {"title": "Failed to fetch", "link": url, "content": ""}

# Scrape content from each URL
scraped_data = []
for url in all_urls:
    print(f"Fetching page: {url}")
    data = scrape_content(url)
    scraped_data.append(data)

# Save the scraped data to a JSON file
with open('volante_posts.json', 'w') as json_file:
    json.dump(scraped_data, json_file, indent=4)

print(f"Scraped {len(scraped_data)} posts and saved to volante_posts.json.")
