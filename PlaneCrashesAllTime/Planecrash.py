import requests
from bs4 import BeautifulSoup
import pandas as pd
def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        data = []
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 4:
                date = cells[0].text.strip()
                location_operator = cells[1].text.strip()
                aircraft_type_reg = cells[2].text.strip()
                fatalities = cells[3].text.strip()
                data.append([date, location_operator, aircraft_type_reg, fatalities])
        return data
    else:
        return []
def combine_data(years):
    combined_data = []
    for year in years:
        url = f"https://www.planecrashinfo.com/{year}/{year}.htm"
        year_data = scrape_data(url)
        combined_data.extend(year_data)
    return combined_data
years = [str(year) for year in range(1920, 2025)]
all_data = combine_data(years)
columns = ['Date', 'Location / Operator', 'Aircraft Type / Registration', 'Fatalities']
df = pd.DataFrame(all_data, columns=columns)
df.to_csv('PlaneCrash.csv', index=False)
print('Dataset Created!!!')