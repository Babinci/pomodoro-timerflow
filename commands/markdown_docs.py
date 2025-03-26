"""
Usage: 
  - Without arguments: Uses default URL (example.com)
  - With arguments: python website_content_markdown.py url1 url2 url3
"""
from readability import Document
import requests
import markdownify
import sys
import argparse

default_url = "https://supabase.com/docs/reference/python"

# Browser-like headers to avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

def get_website_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        document = Document(response.text)
        markdown_content = markdownify.markdownify(document.summary())
        return markdown_content
    except Exception as e:
        return f"Error processing {url}: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description='Convert website content to markdown')
    parser.add_argument('urls', nargs='*', help='One or more URLs to process')
    
    args = parser.parse_args()
    
    # Use default URL if no arguments provided
    urls = args.urls if args.urls else [default_url]
    
    for url in urls:
        print(f"\n--- Content from {url} ---")
        content = get_website_content(url)
        print(content)
        print("----------------------------\n")


if __name__ == "__main__":
    main()