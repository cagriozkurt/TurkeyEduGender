import json

import requests
from bs4 import BeautifulSoup

with open("programs.json") as f:
    programs_dict = json.load(f)

BASE_URL = "https://yokatlas.yok.gov.tr/"


def scrape_single_stat(university_code):
    url = f"{BASE_URL}content/lisans-dynamic/2010.php?y={university_code}"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table_body = soup.find("tbody")
    try:
        females = table_body.find_all("tr")[1].find_all("td")[1].get_text()
        males = table_body.find_all("tr")[2].find_all("td")[1].get_text()
    except IndexError:
        return None
    else:
        return int(females), int(males)


def sum_up_numbers(n):
    number_of_females = 0
    number_of_males = 0
    program = programs_dict["programs"][n]
    program_name = program["name"]
    program_code = program["program_code"]
    for i in program["university_codes"]:
        stats = scrape_single_stat(i)
        try:
            number_of_females += stats[0]
            number_of_males += stats[1]
        except TypeError:
            pass
    return program_code, program_name, number_of_females, number_of_males


for x in range(len(programs_dict["programs"])):
    data = sum_up_numbers(x)
    print(data)
    with open("data.csv", "a") as f_w:
        f_w.write(
            data[0] + ";" + data[1] + ";" + str(data[2]) + ";" + str(data[3]) + "\n"
        )
