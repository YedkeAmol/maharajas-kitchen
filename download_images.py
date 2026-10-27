import sqlite3
import urllib.request
import urllib.parse
import json
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), 'food_billing.db')
IMG_DIR = os.path.join(os.path.dirname(__file__), 'static', 'img')

os.makedirs(IMG_DIR, exist_ok=True)

def get_slug(name):
    return re.sub(r'[^a-z0-9]+', '_', name.lower())

def fetch_wiki_image(query):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        resp = urllib.request.urlopen(req, timeout=10).read()
        data = json.loads(resp)
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            if 'original' in page_info:
                return page_info['original']['source']
    except Exception as e:
        print(f"Error fetching for {query}: {e}")
    return None

def download_image(url, filename):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response, open(filename, 'wb') as out_file:
            out_file.write(response.read())
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# Mapping specific hard-to-find dishes to better Wikipedia queries
QUERY_MAP = {
    'maharaja thali': 'Thali',
    'non-veg royal thali': 'Thali',
    'gujarati thali': 'Gujarati Thali',
    'punjabi thali': 'Thali',
    'bengali fish thali': 'Machher Jhol',
    'samosa (2 pcs)': 'Samosa',
    'mutton seekh kebab': 'Seekh kebab',
    'chicken 65': 'Chicken 65',
    'prawn koliwada': 'Prawn',
    'paneer butter masala': 'Paneer makhani',
    'chicken biryani': 'Biryani',
    'mutton biryani': 'Hyderabadi biryani',
    'goan fish curry': 'Fish curry',
    'kadai chicken': 'Chicken tikka masala',
    'prawn masala': 'Prawn',
    'chicken kolhapuri': 'Chicken curry',
    'idli sambar': 'Idli',
    'masala dosa': 'Dosa',
    'chicken chettinad': 'Chettinad cuisine',
    'gulab jamun (2 pcs)': 'Gulab jamun',
    'rasmalai (2 pcs)': 'Ras malai',
    'garlic naan': 'Naan',
    'butter naan': 'Naan',
    'masala chai': 'Masala chai'
}

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM items")
    items = [r[0] for r in cur.fetchall()]
    conn.close()

    for item in items:
        slug = get_slug(item)
        filepath = os.path.join(IMG_DIR, f"{slug}.jpg")
        
        # Skip if already exists
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print(f"Skipping {item} (already exists)")
            continue
            
        print(f"Processing {item}...")
        
        query = QUERY_MAP.get(item.lower(), item)
        img_url = fetch_wiki_image(query)
        
        # Fallback queries if first try fails
        if not img_url:
            fallbacks = [query.split(' ')[0], 'Indian cuisine', 'Curry']
            for fb in fallbacks:
                img_url = fetch_wiki_image(fb)
                if img_url:
                    break
                    
        if img_url:
            print(f"  Found image: {img_url}")
            download_image(img_url, filepath)
        else:
            print(f"  Could not find image for {item}")
        import time
        time.sleep(1.5)

if __name__ == '__main__':
    main()
