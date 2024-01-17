"""
OpenCV Documentation Scraping Script

This script uses Selenium and BeautifulSoup to scrape and save content from specific OpenCV documentation links. The script reads a list of URLs from a text file, navigates to each link, and extracts the textual content of the page. It organizes and saves the content based on different versions of OpenCV documentation. The script also handles errors and saves the links that could not be scraped successfully to a separate file.

Key Steps:
1. Set up a Selenium WebDriver for web navigation.
2. Read URLs from a text file and scrape content from each URL.
3. Organize content by OpenCV documentation version and save to separate text files.
4. Handle errors and record failed URLs for review.
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.parse

# Function to set up the Selenium WebDriver
def setup_driver():
    driver = webdriver.Chrome()
    return driver

# Function to scrape content from a given URL
def scrape_content(driver, url):
    try:
        driver.get(url)
        time.sleep(0.1)  # Ensure the page has fully loaded
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None  # Return None in case of error

# Function to save the scraped content to a file
def save_content(version, content):
    with open(f'opencv_{version}.txt', 'w', encoding='utf-8') as file:  # Specify encoding as UTF-8
        file.write(content)

# Main function to execute the script
def main():
    driver = setup_driver()

    with open('opencv_links.txt', 'r') as file:
        links = file.readlines()

    current_content = ""
    error_links = []
    current_version = None

    for link in links:
        link = link.strip()
        if link:
            version = link.split('/')[3]  # Extract the version from the link

            if current_version != version:
                if current_version is not None:
                    save_content(current_version, current_content)
                current_version = version
                current_content = ""
            
            print(f"Scraping {link}")
            content = scrape_content(driver, link)
            if content is not None:
                current_content += content + "\n\n"
            else:
                error_links.append(link)

    # Save the content of the last processed version
    if current_version is not None:
        save_content(current_version, current_content)

    driver.quit()

    # Save the links with errors for further review
    with open('error_links.txt', 'w') as file:
        for link in error_links:
            file.write(link + '\n')

if __name__ == "__main__":
    main()
