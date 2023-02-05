import requests
from bs4 import BeautifulSoup
import pandas as pd

def append_dict(dct, name_div, area_div, post_div):
    if name_div is not None and area_div is not None:
        dct["name"].append(name_div.text)
        dct["area"].append(area_div.text)
        if post_div.find("a") is not None:
            dct["email"].append(post_div.find("a").text)
        else:
            dct["email"].append("")
        dct["post"].append(post_div.next_element.next_element.text)

def extend_dict(dct, names, areas, posts, emails):
    dct["name"].extend(names)
    dct["post"].extend(posts)
    dct["email"].extend(emails)
    dct["area"].extend(areas)

url = 'https://mediakit.iportal.ru/our-team'
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

workers_blocks = soup.findAll("div", {"class": "t396"})

workers_info = {"name": [], "area": [], "post": [], "email": []}

for block in workers_blocks:

    left_area_div = block.find("div", attrs={"class": "tn-elem", "data-field-top-value": "1",
                                             "data-field-left-value": "20", "data-elem-type": "text"})
    left_name_div = block.findAll("div", attrs={"class": "tn-elem", "data-field-top-value": ["200", "209", "210"],
                                             "data-field-left-value": "280", "data-elem-type": "text"})
    left_post_div = block.findAll("div", attrs={"class": "tn-elem", "data-field-top-value": ["237", "240", "245"],
                                             "data-field-left-value": "280", "data-elem-type": "text"})

    right_area_div = block.find("div", attrs={"class": "tn-elem", "data-field-top-value": ["0", "1"],
                                             "data-field-left-value": ["620", "619"]})
    right_name_div = block.find("div", attrs={"class": "tn-elem", "data-field-top-value": ["194", "200", "209", "208"],
                                              "data-field-left-value": ["880", "882", "891"]})
    right_post_div = block.find("div", attrs={"class": "tn-elem", "data-field-top-value": ["237", "240", "245", "228", "231"],
                                                       "data-field-left-value": ["880", "882", "891"]})
    append_dict(workers_info, right_name_div, right_area_div, right_post_div)

    if left_name_div is None or len(left_name_div) == 0:
        continue
    else:
        left_name_div = left_name_div[-1]
        left_post_div = left_post_div[-1]
    append_dict(workers_info, left_name_div, left_area_div, left_post_div)



dev_workers_names = list(map(lambda x: x.text, soup.findAll("div", class_="t527__persname")))
dev_workers_descriptions = list(map(lambda x: x.text, soup.findAll("div", class_="t527__persdescr")))
extend_dict(workers_info, dev_workers_names, len(dev_workers_names)*[None], dev_workers_descriptions, len(dev_workers_names)*[None])

lead_workers_names = list(map(lambda x: x.text, soup.findAll("div", class_="t544__title")))
lead_workers_descriptions = list(map(lambda x: x.text, soup.findAll("div", class_="t544__descr")))
lead_workers_email = list(map(lambda x: x.find("a").text, soup.findAll("div", class_="t544__text")))
extend_dict(workers_info, lead_workers_names, len(dev_workers_names)*[None], lead_workers_descriptions, lead_workers_email)

df = pd.DataFrame(data=workers_info)
df.to_csv("workers.csv")




