import csv
import json
import re

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://yokatlas.yok.gov.tr/"
OUTPUT_FILE = "programs.json"


def scrape_program_titles():
    program_title_dict = {}
    main_url = BASE_URL + "lisans-anasayfa.php"
    title_r = requests.get(main_url)
    title_soup = BeautifulSoup(title_r.text, "html.parser")
    select_list = title_soup.find("select", {"id": "bolum"})
    options = select_list.find_all("option")
    for item in options:
        program_value = item["value"]
        program_name = item.get_text()
        program_title_dict[program_value] = program_name
    return program_title_dict


def csv_as_dict(filename):
    """scrape_program_titles() handles program codes and names
    but if it doesn't work,
    the relevant info can be fed to the program via a CSV file as well.
    """
    program_title_dict = {}
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            program_title_dict[row[0]] = row[1]
    return program_title_dict


def add_new_program_to_dict(input_dict, program_name, program_code, list_of_links):
    new_program = {}
    new_program["name"] = program_name
    new_program["program_code"] = program_code
    new_program["university_codes"] = list_of_links
    input_dict["programs"].append(new_program)


def initiate_dict():
    programs_dict = {}
    programs_dict["programs"] = []

    return programs_dict


def scrape_links(program_code):
    url = f"{BASE_URL}lisans-bolum.php?b={program_code}"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a", {"data-parent": "#"})
    links_list = []
    for link in links:
        uni_code = re.findall(r"y=(\d+)", link["href"])[0]
        links_list.append(uni_code)
    return links_list


def build_dict(program_title_dict):
    for key, value in program_title_dict.items():
        print(key, value)
        list_of_links = scrape_links(key)
        add_new_program_to_dict(my_dict, value, key, list_of_links)


def write_json(output_filename):
    with open(output_filename, "w") as f:
        json.dump(my_dict, f, indent=4, ensure_ascii=False)


my_dict = initiate_dict()
my_title_dict = scrape_program_titles()
build_dict(my_title_dict)
write_json(OUTPUT_FILE)
