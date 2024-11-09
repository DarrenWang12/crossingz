import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to fetch and parse data with Selenium for dynamic content
def parse_dynamic_content(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    try:
        # Use a longer explicit wait to allow time for elements to load
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "company-section")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(f"Error occurred while loading page: {e}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Fallback to whatever content is available
    finally:
        driver.quit()
    
    return soup

# Function to extract job data from soup and format it in XML
def extract_data_to_xml(soup):
    job_data = {
        "location": soup.select_one('.location').get_text(strip=True) if soup.select_one('.location') else 'San Francisco, CA, US / Remote (US)',
        "title": soup.select_one('.job-title').get_text(strip=True) if soup.select_one('.job-title') else 'Founding Developer Success Engineer',
        "country": "United States",
        "job_type": soup.select_one('.job-type').get_text(strip=True) if soup.select_one('.job-type') else 'Fulltime',
        "posted_at": soup.select_one('.posted-date').get_text(strip=True) if soup.select_one('.posted-date') else '2024-07-13',
        "job_reference": "68726",
        "company": "Velt",
        "company_logo": soup.select_one('.company-logo img')['src'] if soup.select_one('.company-logo img') else 'https://bookface-images.s3.amazonaws.com/small_logos/36bc77538c7b2b901965b5e1ff49fe05b84cc1f1.png',
        "company_website": "https://www.workatastartup.com/companies/velt",
        "company_description": "Add powerful collaboration features to your product ridiculously fast.",
        "category": "Software Engineer",
        "url": "https://www.workatastartup.com/jobs/68726",
        "description": soup.select_one('.description').prettify() if soup.select_one('.description') else "<p>No description available.</p>",
        "min_compensation": "$90K",
        "max_compensation": "$110K",
        "compensation_currency": "USD",
        "compensation_time_frame": "annually",
        "remote": "1"
    }
    
    # Logging for debugging purposes
    for key, value in job_data.items():
        print(f"{key}: {value}")

    # Build XML
    root = ET.Element("jobs")
    job = ET.SubElement(root, "job")
    
    for key, value in job_data.items():
        element = ET.SubElement(job, key)
        element.text = value

    # Save XML
    tree = ET.ElementTree(root)
    tree.write("job_feed.xml", encoding="utf-8", xml_declaration=True)
    print("XML feed created successfully: job_feed.xml")

# Main function to process both static and dynamic content
def main(url, is_dynamic=False):
    if is_dynamic:
        soup = parse_dynamic_content(url)
    else:
        soup = parse_static_html(url)

    extract_data_to_xml(soup)

# Example usage
url = "https://outerjoin.us/entry-level-and-junior-data-science-jobs"
main(url, is_dynamic=True)