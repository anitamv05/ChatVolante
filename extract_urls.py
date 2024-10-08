import json
from lxml import etree

# List of sitemap files you've downloaded
sitemap_files = ['post-sitemap.xml']  # Add more if you have them

all_urls = []

for sitemap_file in sitemap_files:
    with open(sitemap_file, 'rb') as f:
        tree = etree.parse(f)
        urls = tree.xpath('//url/loc/text()')
        all_urls.extend(urls)

print(f"Extracted {len(all_urls)} URLs from the sitemap(s).")

# Save the URLs to volante_urls.json
with open('volante_urls.json', 'w') as f:
    json.dump(all_urls, f, indent=4)

print("Saved URLs to volante_urls.json.")
