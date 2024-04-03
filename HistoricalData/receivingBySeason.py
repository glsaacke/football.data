import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
url = "https://www.pro-football-reference.com/years/"
baseUrl = "https://www.pro-football-reference.com"
response = requests.get(url)
realTeams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GNB', 'HOU', 'IND', 'JAX', 'KAN', 'LAC', 'LAR', 'LVR', 'MIA', 'MIN', 'NOR', 'NWE', 'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SFO', 'TAM', 'TEN', 'WAS']
allTeams = ['crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'htx', 'clt', 'jax', 'kan', 'sdg', 'ram', 'rai', 'mia', 'min', 'nor', 'nwe', 'nyg', 'nyj', 'phi', 'pit', 'sea', 'sfo', 'tam', 'oti', 'was']

soup = BeautifulSoup(response.content, 'html.parser')

seasons = soup.find(id="years")
seasonRecData = []

for row in seasons.find_all('tr')[2:]:
    season = row.find('th').text.strip()
    if(int(season) > 2009):
        seasonUrl = baseUrl + '/years/' + season
        print(seasonUrl)
        # time.sleep(3.1)
        response2 = requests.get(url)

        soup2 = BeautifulSoup(response.content, 'html.parser')
        teams = soup.find(id="team_stats")
    
        for team in allTeams:
            teamUrl = baseUrl + '/teams/' + team + '/' + season + '.htm'
            print(teamUrl)
            teamIndex = allTeams.index(team)
            realTeam = realTeams[teamIndex]

            time.sleep(3.2)

            driver.get(teamUrl)
            wait = WebDriverWait(driver, 1)
            wait.until(EC.visibility_of_element_located((By.ID, "rushing_and_receiving")))
            html = driver.page_source

            soup3 = BeautifulSoup(html, 'html.parser')  

            recStats = soup3.find('table', {'id': 'rushing_and_receiving'})

            for row in recStats.find_all('tr')[2:]:
                columns = row.find_all('td')
                season = season
                realTeam = realTeam
                playerName = columns[0].text.strip()
                position = columns[2].text.strip()
                gamesStarted = columns[4].text.strip()
                targets = columns[14].text.strip()
                receptions = columns[15].text.strip()
                yards = columns[16].text.strip()
                TDs = columns[18].text.strip()
                firstDowns = columns[19].text.strip()
                success = columns[20].text.strip()
                yardsReception = columns[17].text.strip()
                yardsGame = columns[23].text.strip()
                if(receptions and position != ''):
                    if(int(receptions) > 0):
                        seasonRecData.append((season, realTeam, playerName, position, gamesStarted, targets, receptions, yards, TDs, firstDowns, success, yardsReception, yardsGame))
                        print(season + ' ' + realTeam + ' ' + playerName + ' ' + position + ' ' + gamesStarted + ' ' + targets + ' ' + receptions + ' ' + yards + ' ' + TDs + ' ' + firstDowns + ' ' + success + ' ' + yardsReception + ' ' + yardsGame)

driver.quit()

def cleanPlayerName(playerName):
    return playerName.replace('*','').replace('+', '')


# csv output
csv_file_path = "historical_rec_data"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Season', 'Team', 'Player', 'Position', 'Games Started', 'Targets', 'Receptions', 'Receiving Yards', 'Receiving TDs', 'Receiving 1D', 'Success%', 'Rec Yards/Catch', 'Rec Yards/Game']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for playerInfo in seasonRecData:
        playerInfo = (cleanPlayerName(playerInfo[0]),) + playerInfo[1:]
        writer.writerow({'Season': playerInfo[0], 'Team': playerInfo[1], 'Player': cleanPlayerName(playerInfo[2]), 'Position': playerInfo[3], 'Games Started': playerInfo[4], 'Targets': playerInfo[5], 'Receptions': playerInfo[6], 'Receiving Yards': playerInfo[7], 'Receiving TDs': playerInfo[8], 'Receiving 1D': playerInfo[9], 'Success%': playerInfo[10], 'Rec Yards/Catch': playerInfo[11], 'Rec Yards/Game': playerInfo[12]})

print("CSV file saved successfully:", csv_file_path)
