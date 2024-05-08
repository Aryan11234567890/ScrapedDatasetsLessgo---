import requests
from bs4 import BeautifulSoup
import csv
from lxml import html
url = "https://en.wikipedia.org/wiki/List_of_best-selling_game_consoles"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    lxml_soup = html.fromstring(response.text)
    table = lxml_soup.xpath('//table')[0]
    with open('best_selling_consoles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ['Platform', 'Type', 'Company', 'Released', 'Sales', 'Ref']
        csvwriter.writerow(header)
        for row in table.xpath('.//tr')[1:]:
            cells = row.xpath('.//td | .//th')
            data = [cell.text_content().strip() for cell in cells]
            csvwriter.writerow(data)
