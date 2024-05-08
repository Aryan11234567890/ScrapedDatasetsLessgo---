import requests
from bs4 import BeautifulSoup
import csv
url = "https://en.wikipedia.org/wiki/List_of_best-selling_books"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    with open('best_selling_books.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ['Title', 'Author(s)', 'Original language', 'First published', 'Approximate sales']
        csvwriter.writerow(header)
        for table in tables:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cells = row.find_all(['th', 'td'])
                data = [cell.get_text(strip=True) for cell in cells]
                csvwriter.writerow(data)
with open('best_selling_books_above_100mil.csv', 'w', newline='', encoding='utf-8') as csvfile_above_100mil:
    csvwriter_above_100mil = csv.writer(csvfile_above_100mil)
    csvwriter_above_100mil.writerow(header)
    with open('best_selling_books_between_50_and_100mil.csv', 'w', newline='', encoding='utf-8') as csvfile_between_50_and_100mil:
        csvwriter_between_50_and_100mil = csv.writer(csvfile_between_50_and_100mil)
        csvwriter_between_50_and_100mil.writerow(header)
        with open('best_selling_books_combined.csv', 'w', newline='', encoding='utf-8') as csvfile_combined:
            csvwriter_combined = csv.writer(csvfile_combined)
            csvwriter_combined.writerow(header)
            with open('best_selling_books.csv', 'r', newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # skip header
                for row in csvreader:
                    sales = row[-1].replace(',', '').replace('~', '')
                    if sales.isdigit():
                        sales = int(sales)
                        if sales > 100:
                            csvwriter_above_100mil.writerow(row)
                            csvwriter_combined.writerow(row)
                        elif 50 <= sales <= 100:
                            csvwriter_between_50_and_100mil.writerow(row)
                            csvwriter_combined.writerow(row)
                        else:
                            csvwriter_combined.writerow(row)
