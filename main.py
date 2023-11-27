import ipaddress
import json
import re
import os
from git import Repo
from git import Actor
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

json_file_name = 'jamf_outbound_traffic.json'
jamf_ip_webpage = 'https://learn.jamf.com/bundle/technical-articles/page/Permitting_InboundOutbound_Traffic_with_Jamf_Cloud.html'

region_pattern = re.compile(r'U\.S\..*|\w*-\w*-\d*')
ip_pattern = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')
domain_pattern = re.compile(r'\b(?:[\w-]+\.){2,}[\w]+')

driver_options = Options()
driver_options.add_argument('-headless')
driver = webdriver.Firefox(driver_options)

repo = Repo(os.path.dirname(os.path.realpath(__file__)))
author = Actor('Corey Oliphant', 'coreysather@gmail.com')


def extract_data_by_region(data):
    result = {}
    current_region = None

    # Iterate through array of values. It found to be a region, start a new nested dict of its associated IPs/Domains.
    # Else, append to list of current region's IPs/Domains.
    for item in data:
        if region_pattern.match(item):
            current_region = item
            result[current_region] = []
        elif ip_pattern.match(item) or domain_pattern.match(item):
            result[current_region].append(item)

    # Sort IP addresses as per standard method, otherwise just do a generic sort for CIDR notation or domains
    for region in result.keys():
        if result.get(region):
            try:
                result[region] = list(map(str, sorted(ipaddress.ip_address(val) for val in result[region])))
            except ValueError:
                result[region] = sorted(result[region])

    return result


if __name__ == '__main__':
    ip_addresses = {}

    try:
        # Load the page
        driver.get(jamf_ip_webpage)

        # Wait for IP tables to render
        element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, "table"))
        )

        # Get all sections and check if they contain IP addresses
        sections = driver.find_elements(By.CLASS_NAME, 'section')
        for section in sections:
            try:
                title = section.find_element(By.CLASS_NAME, 'sectiontitle')
                table_contents = section.find_element(By.CLASS_NAME, 'table').text.split('\n')

                # Extract all the necessary IP/Region data found
                ip_addresses[title.text] = extract_data_by_region(table_contents)
            except NoSuchElementException:
                continue

        # Update JSON file
        with open(json_file_name, 'w') as file:
            file.write(json.dumps(ip_addresses, indent=2))

        # Stage JSON file and if there's a difference, commit the changes and push 'em up
        repo.index.add([json_file_name])

        if repo.index.diff(repo.head.commit):
            repo.index.commit('Committing Jamf outbound changes', author=author, committer=author)
            repo.remote().push().raise_if_error()
    except Exception as e:
        print(e)
    finally:
        driver.close()
