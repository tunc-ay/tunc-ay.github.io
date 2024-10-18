from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
sys.path.append(r'C:\Users\tkayaogl\AppData\Roaming\Python\Python313\site-packages')
from bs4 import BeautifulSoup
import requests
import os
import re
from urllib.parse import urlparse, urljoin
import time

# ===== Configuration ===== #
base_url = "https://tunc-ay.github.io/"  # Target website
screenshot_folder = "screenshots"  # Folder to save screenshots

# Set up the Chrome driver and options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--window-size=1920,1080")  # Default window size

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)

# Create screenshot folder if it doesn't exist
os.makedirs(screenshot_folder, exist_ok=True)

visited_links = set()  # Track visited links


def clean_filename(url):
    """Convert a URL to a valid filename."""
    parsed_url = urlparse(url)
    full_path = parsed_url.netloc + parsed_url.path
    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', full_path.strip('/'))
    return f"{clean_name[:240]}.png"


def get_all_links(url):
    """Extract all internal links from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for invalid responses
        soup = BeautifulSoup(response.content, "html.parser")
        links = set()

        for anchor in soup.find_all("a", href=True):
            # Convert relative URLs to absolute URLs
            href = urljoin(url, anchor["href"])
            # Ensure it's an internal link
            if base_url in href and is_valid_html_link(href) and href not in visited_links:
                links.add(href)

        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links from {url}: {e}")
        return set()


def is_valid_html_link(url):
    """Filter out non-HTML content."""
    excluded_extensions = (".pdf", ".jpg", ".xml", ".jpeg", ".png", ".mp4", ".gif", ".zip", ".exe")
    parsed_url = urlparse(url)
    return not parsed_url.path.lower().endswith(excluded_extensions)


def take_screenshot(url):
    """Open a page and take a screenshot."""
    try:
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load

        # Adjust the window size to capture the entire page
        total_width = driver.execute_script("return document.body.scrollWidth")
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(total_width, total_height)

        filename = clean_filename(url)
        filepath = os.path.join(screenshot_folder, filename)

        driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
    except Exception as e:
        print(f"Error taking screenshot of {url}: {e}")


def crawl_website(url):
    """Crawl the website and take screenshots."""
    try:
        links_to_visit = get_all_links(url)

        for link in links_to_visit:
            if link not in visited_links:
                visited_links.add(link)
                print(f"Visiting: {link}")
                take_screenshot(link)

                # Crawl further links recursively
                crawl_website(link)
                time.sleep(1)  # Respectful delay between requests
    except Exception as e:
        print(f"Error crawling {url}: {e}")


# ===== Start Crawling and Taking Screenshots ===== #
print(f"Starting crawl at: {base_url}")
visited_links.add(base_url)  # Mark the base URL as visited
take_screenshot(base_url)  # Take a screenshot of the homepage

crawl_website(base_url)  # Start crawling from the base URL

# Close the browser when done
driver.quit()