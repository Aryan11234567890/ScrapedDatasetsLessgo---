import requests
from bs4 import BeautifulSoup
import csv
from lxml import html
url = "https://en.wikipedia.org/wiki/List_of_unicorn_startup_companies"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    lxml_soup = html.fromstring(response.text)
    table = lxml_soup.xpath('//*[@id="mw-content-text"]/div[1]/table[3]')[0]
    with open('unicorn_companies.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ['Company', 'Valuation (Billion USD)', 'Date', 'Industry', 'Country', 'Founder(s)']
        csvwriter.writerow(header)
        for row in table.xpath('.//tr')[1:]:
            cells = row.xpath('.//td | .//th')
            data = [cell.text_content().strip() for cell in cells]
            csvwriter.writerow(data)