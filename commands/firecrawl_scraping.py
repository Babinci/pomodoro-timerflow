# Initialize the app
API_KEY = "fc-2e61828577aa4b4bafc43b6470e25576"


from firecrawl import FirecrawlApp
import os
import json
from pathlib import Path
import re
import time
from datetime import datetime

app = FirecrawlApp(api_key=API_KEY)
output_folder = r"C:\Users\walko\IT_projects\pomodoro-timerflow\documents\supabase_docs"

# Create the output folder if it doesn't exist
Path(output_folder).mkdir(parents=True, exist_ok=True)
print(f"[{datetime.now().strftime('%H:%M:%S')}] Output folder: {output_folder}")

# Display starting message
print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting crawl of https://supabase.com/docs/reference/python/")
print(f"[{datetime.now().strftime('%H:%M:%S')}] Maximum pages to crawl: 500")
print(f"[{datetime.now().strftime('%H:%M:%S')}] Poll interval: 30 seconds")

# Start the crawl
start_time = time.time()
print(f"[{datetime.now().strftime('%H:%M:%S')}] Submitting crawl job...")

# Use crawl_url instead of submit_crawl
crawl_result = app.crawl_url(
    'https://supabase.com/docs/reference/python/', 
    params={
        'limit': 500,
        'scrapeOptions': {'formats': ['markdown']},
        # 'includePaths': ['^/docs/reference/python/'] 
    },
    poll_interval=30
)

# Crawl completed
elapsed_time = time.time() - start_time
print(f"[{datetime.now().strftime('%H:%M:%S')}] Crawl completed in {elapsed_time:.1f} seconds")
print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(crawl_result['data'])} pages")

# Save the results
print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting to save files...")

for idx, page in enumerate(crawl_result['data']):
    # Create a safe filename from the URL
    url_path = page['metadata']['url'].split('/')
    # Get the last non-empty segment or use page_idx as fallback
    filename = next((segment for segment in reversed(url_path) if segment), f"page_{idx}")
    filename = re.sub(r'[^\w\-\.]', '_', filename)  # Remove invalid chars
    if not filename.endswith('.md'):
        filename = f"{filename}.md"
    
    # Show progress
    progress = (idx + 1) / len(crawl_result['data']) * 100
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Saving file {idx+1}/{len(crawl_result['data'])} ({progress:.1f}%): {filename}")
    
    # Save the markdown content
    file_path = os.path.join(output_folder, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(page['markdown'])

print(f"[{datetime.now().strftime('%H:%M:%S')}] Complete! Saved {len(crawl_result['data'])} pages to {output_folder}")