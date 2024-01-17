"""
Web Scraping Script for OpenCV Documentation

This script employs Selenium and BeautifulSoup to perform web scraping on the official OpenCV documentation website. Its primary purpose is to extract and store useful links from different documentation versions, focusing specifically on versions 3.4 or newer. The process includes:

1. Setting up a Selenium WebDriver to navigate the website.
2. Extracting links from the main page that correspond to different versions of the documentation, filtering out unrelated or irrelevant links.
3. For each version link, the script navigates to its page and extracts specific menu links (like main page, related pages, modules, namespaces, classes).
4. Inside each of these sections, it performs deeper scraping to extract all relevant internal links.
5. All the gathered links are then saved in a text file for easy access and use.

This tool is particularly useful for developers or researchers who need to access a comprehensive collection of OpenCV documentation links, especially when working with specific versions of OpenCV.

Note: This script is intended for educational purposes and should be used in compliance with the website's terms of service.
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import urllib.parse

# Function to set up the Selenium Webdriver
def setup_driver():
    driver = webdriver.Chrome()
    return driver

# Function to extract version-specific links from a given URL
def extract_links(driver, url):
    driver.get(url)
    # Wait until the links are present
    version_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li a"))
    )
    version_urls = []
    for link in version_links:
        href = link.get_attribute('href')
        # Exclude certain links based on their format
        if not href.endswith('.zip') and not href.endswith('.tar.xz') and 'java' not in href:
            full_url = urllib.parse.urljoin(url, href)
            # Include only links of version 3.4 or above
            if is_version_3_4_or_above(full_url):
                version_urls.append(full_url)
    return version_urls

# Function to check if the URL corresponds to version 3.4 or above
def is_version_3_4_or_above(url):
    version = url.split('/')[-1]
    if version.startswith('3.'):
        minor_version_part = version.split('.')[1]
        minor_version_num = ''.join(filter(str.isdigit, minor_version_part))
        return int(minor_version_num) >= 4
    elif version.startswith('2.'):
        return False
    return True

# Function to extract specific menu links from a version URL
def extract_menu_links(driver, version_url):
    driver.get(version_url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    menu_links = soup.select('ul#main-menu li a')

    desired_sections = ["main page", "related pages", "modules", "namespaces", "classes"]
    extracted_links = []
    for link in menu_links:
        text = link.text.strip().lower()
        if text in desired_sections:
            href = link.get('href')
            full_url = urllib.parse.urljoin(version_url + '/', href)
            extracted_links.append((text, full_url))

    return extracted_links

# Function to extract links with the last level of detail from a URL
def extract_links_with_last_level(driver, url):
    driver.get(url)
    time.sleep(0.1)

    try:
        # Check for elements indicating detail levels
        levels = driver.find_elements(By.XPATH, "//div[@class='levels']//span")
        if levels:
            last_level = levels[-1]
            last_level.click()
            time.sleep(0.1)
    except Exception as e:
        print(f"Could not open the last level of detail: {e}")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_links = soup.find_all('a')

    links = []
    for link in all_links:
        href = link.get('href')
        if href and not href.startswith('javascript') and 'globals' not in href:
            full_url = urllib.parse.urljoin(url, href)
            links.append(full_url)

    return links

# Function to save the extracted links into a text file
def save_links_in_txt(links, file_name):
    with open(file_name, "w") as file:
        for link in links:
            file.write(f"{link}\n")
    print(f"Links saved in {file_name}")

# Main function to execute the script
def main():
    driver = setup_driver()
    base_url = 'https://docs.opencv.org/'
    version_urls = extract_links(driver, base_url)

    total_links = []
    for version_url in version_urls:
        print(f"Scraping version: {version_url}")
        menu_links = extract_menu_links(driver, version_url)

        for text, link in menu_links:
            print(f"Exploring: {text} - {link}")
            internal_links = extract_links_with_last_level(driver, link)
            total_links.extend(internal_links)

    driver.quit()
    save_links_in_txt(total_links, 'opencv_links.txt')

if __name__ == "__main__":
    main()
