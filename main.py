import requests
from bs4 import BeautifulSoup
import json
import os
import re
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
links_festival = []
festival_data_list = []
for i in range(0, 165, 24):  # 145
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=March"
    # print(url)

    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data['html']
    with open(f"data/page_{i}.html", "w", encoding="utf-8") as file:
        file.write(html_response)
    with open(f"data/page_{i}.html", "r", encoding="utf-8") as file:
        html_responce = file.read()

    soup = BeautifulSoup(html_responce, 'lxml')
    all_fest = soup.find_all('a', class_='card-details-link')
    for item in all_fest:
        links_festival.append(
            f"https://www.skiddle.com{item['href'].strip()}")

        # print(item['href'])

with open("list_links_v1.txt", 'a', encoding='utf-8') as file:
    for link in links_festival:
        file.write(f"{link.strip()}\n")
# print(links_festival)
count = 1
with open("list_links_v1.txt", "r", encoding="utf-8") as file:
    for link in [link.strip() for link in file.readlines()]:
        req = requests.get(link, headers=headers)
        # src = req.text

        soup = BeautifulSoup(req.text, 'lxml')
        # print(soup)
        # location_tag = soup.find('svg',
        #                          {"data-testid": "LocationOnIcon"}).find_next('span')
        # print('sss', location_tag, 'sss')
        try:
            start_date = soup.find('svg',
                                   {"data-testid": "CalendarTodayIcon"}).find_next('span')
            end_date = start_date.find_next('span')
            festival_dates = f"{start_date.text} {end_date.text}"
        except Exception:
            festival_dates = 'No festival date info'
        try:
            location_tag = soup.find('svg',
                                     {"data-testid": "LocationOnIcon"}).find_next('span')
            # print(location_tag)
            festival_location = location_tag.text
        except Exception:
            pass
            festival_location = 'no info about location'
        # print(festival_location)
        title_tag = soup.find(
            'h1', class_="MuiTypography-root")
        # print(title_tag)
        try:
            festival_title = title_tag.text
        except Exception:
            festival_title = 'no title'
        print(f"записано: {count} - {festival_title}")
        count += 1
        try:
            bill_tag = soup.find('svg',
                                 {"data-testid": "LocalActivityOutlinedIcon"}).find_next('span')
            # per_tag = bill_tag.find_next('span')
            festival_tickets = f"{bill_tag.text.strip()}"
            # print(festival_tickets)
        except Exception:
            pass
            festival_tickets = 'No info about tickets'

        try:
            search_about = soup.find(
                'div', id='about').find(class_='MuiBox-root')
            festival_about_tag = search_about.find_all(
                'p')
            festival_about = ' '.join(
                [item.text for item in festival_about_tag])
            # print(festival_about)
        except Exception:
            festival_about = "no info"

        # print(festival_about)
        festival_data_list.append({
            "festival_title": festival_title,
            "festival_link": link,
            "festival_dates": festival_dates,
            "festival_location": festival_location,
            "festival_tickets": festival_tickets,
            "festival_about": festival_about,
        })

        # dd = soup.find(
        #     class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 css-2re0kq").find_all('span')
        # print(dd)

        # if not os.path.isdir(f"data/page_{i}"):
        #     os.mkdir(f"data/page_{i}")
        # with open(f"data/page_{i}/page.html", "w", encoding="utf-8") as file:
        #     file.write(req.text)

        # print(link)
with open("data/summary_json.json", "w", encoding="utf-8") as file:
    json.dump(festival_data_list, file, indent=4, ensure_ascii=False)
# print(festival_data_list)

# print(json_data)
# print(html_response)
