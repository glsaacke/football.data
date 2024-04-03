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
seasonRushData = []

for row in seasons.find_all('tr')[2:]:
    season = row.find('th').text.strip()
    if(int(season) > 2009):
        seasonUrl = baseUrl + '/years/' + season
        print(seasonUrl)
        time.sleep(3.1)
        response2 = requests.get(url)

        soup2 = BeautifulSoup(response.content, 'html.parser')
        teams = soup.find(id="team_stats")
    
        for team in allTeams:
            teamUrl = baseUrl + '/teams/' + team + '/' + season + '.htm'
            print(teamUrl)
            teamIndex = allTeams.index(team)
            realTeam = realTeams[teamIndex]

            time.sleep(3.1)

            driver.get(teamUrl)
            wait = WebDriverWait(driver, 1)
            wait.until(EC.visibility_of_element_located((By.ID, "rushing_and_receiving")))
            html = driver.page_source

            soup3 = BeautifulSoup(html, 'html.parser')

            rushingStats = soup3.find('table', {'id': 'rushing_and_receiving'})

            for row in rushingStats.find_all('tr')[2:]:
                columns = row.find_all('td')
                season = season
                realTeam = realTeam
                playerName = columns[0].text.strip()
                position = columns[2].text.strip()
                gamesStarted = columns[4].text.strip()
                attempts = columns[5].text.strip()
                yards = columns[6].text.strip()
                TDs = columns[7].text.strip()
                firstDowns = columns[8].text.strip()
                success = columns[9].text.strip()
                yardsAttempt = columns[11].text.strip()
                yardsGame = columns[12].text.strip()
                if(attempts and position != ''):
                    if(int(attempts) > 0):
                        seasonRushData.append((season, realTeam, playerName, position, gamesStarted, attempts, yards, TDs, firstDowns, success, yardsAttempt, yardsGame))
                        print(season + ' ' + realTeam + ' ' + playerName + ' ' + position + ' ' + gamesStarted + ' ' + attempts + ' ' + yards + ' ' + TDs + ' ' + firstDowns + ' ' + success + ' ' + yardsAttempt + ' ' + yardsGame)

driver.quit()

# for playerInfo in seasonRushData:
#     season, realTeam, playerName, position, gamesStarted, attempts, y, rushingTD, yardAverage, gameAverage = playerInfo
#     print(f"Player: {playerInfo[0]}, Team: {playerInfo[1]}, Position: {playerInfo[2]} Rushing: {playerInfo[3]}, TDs: {playerInfo[4]}, Yard Avg: {playerInfo[5]}, Game Avg: {playerInfo[6]}")

def cleanPlayerName(playerName):
    return playerName.replace('*','').replace('+', '')


# csv output
csv_file_path = "historical_rush_data"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Season', 'Team', 'Player', 'Position', 'Games Started', 'Rushing Attempts', 'Rushing Yards', 'Rushing TDs', 'Rushing 1D', 'Success%', 'Rush Yards/Attempt', 'Rush Yards/Game']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for playerInfo in seasonRushData:
        playerInfo = (cleanPlayerName(playerInfo[0]),) + playerInfo[1:]
        writer.writerow({'Season': playerInfo[0], 'Team': playerInfo[1], 'Player': cleanPlayerName(playerInfo[2]), 'Position': playerInfo[3], 'Games Started': playerInfo[4], 'Rushing Attempts': playerInfo[5], 'Rushing Yards': playerInfo[6], 'Rushing TDs': playerInfo[7], 'Rushing 1D': playerInfo[8], 'Success%': playerInfo[9], 'Rush Yards/Attempt': playerInfo[10], 'Rush Yards/Game': playerInfo[11]})

print("CSV file saved successfully:", csv_file_path)
