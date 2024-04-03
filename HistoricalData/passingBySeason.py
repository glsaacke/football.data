import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Selenium webdriver (replace "chrome" with "firefox" if using Firefox)

# # Navigate to the webpage
#driver.get("https://www.example.com")
# wait = WebDriverWait(driver, 10)
# wait.until(EC.visibility_of_element_located((By.ID, "rushing_and_receiving")))
# html = driver.page_source

# # Parse the HTML using BeautifulSoup
# soup = BeautifulSoup(html, "html.parser")

# # Now you can extract data using BeautifulSoup as usual
# # For example:
# # rushingStats = soup.find("table", {"id": "rushing_and_receiving"})
# # for row in rushingStats.find_all("tr"):
# #     # Process the rows

# # Don't forget to close the browser when done
# driver.quit()

driver = webdriver.Chrome()
url = "https://www.pro-football-reference.com/years/"
baseUrl = "https://www.pro-football-reference.com"
response = requests.get(url)
realTeams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GNB', 'HOU', 'IND', 'JAX', 'KAN', 'LAC', 'LAR', 'LVR', 'MIA', 'MIN', 'NOR', 'NWE', 'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SFO', 'TAM', 'TEN', 'WAS']
allTeams = ['crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'htx', 'clt', 'jax', 'kan', 'sdg', 'ram', 'rai', 'mia', 'min', 'nor', 'nwe', 'nyg', 'nyj', 'phi', 'pit', 'sea', 'sfo', 'tam', 'oti', 'was']

soup = BeautifulSoup(response.content, 'html.parser')

seasons = soup.find(id="years")
passingData = []

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
            wait.until(EC.visibility_of_element_located((By.ID, "passing")))
            html = driver.page_source

            soup3 = BeautifulSoup(html, 'html.parser')  # Use response3 here
            # Assuming you have already fetched and parsed the webpage into soup3

            passStats = soup3.find('table', {'id': 'passing'})
                # Now you can iterate over the rows in rushingStats table
            for row in passStats.find_all('tr')[1:]:
                columns = row.find_all('td')
                season = season
                realTeam = realTeam
                playerName = columns[0].text.strip()
                position = columns[2].text.strip()
                gamesStarted = columns[4].text.strip()
                completions = columns[6].text.strip()
                passAttempts = columns[15].text.strip()
                yards = columns[9].text.strip()
                TDs = columns[10].text.strip()
                interceptions = columns[12].text.strip()
                firstDowns = columns[14].text.strip()
                success = columns[15].text.strip()
                yardsCompletion = columns[19].text.strip()
                yardsGame = columns[20].text.strip()
                qbr = columns[21].text.strip()
                if(completions and position != ''):
                    if(int(completions) > 0):
                        passingData.append((season, realTeam, playerName, position, gamesStarted, completions, passAttempts, yards, TDs, interceptions, firstDowns, success, yardsCompletion, yardsGame, qbr))
                        print(season + ' ' + realTeam + ' ' + playerName + ' ' + position + ' ' + gamesStarted + ' ' + completions + ' ' + passAttempts + ' ' + yards + ' ' + TDs + ' ' + interceptions + ' ' + firstDowns + ' ' + success + ' ' + yardsCompletion + ' ' + yardsGame + ' ' + qbr)

driver.quit()

# for playerInfo in seasonRushData:
#     season, realTeam, playerName, position, gamesStarted, attempts, y, rushingTD, yardAverage, gameAverage = playerInfo
#     print(f"Player: {playerInfo[0]}, Team: {playerInfo[1]}, Position: {playerInfo[2]} Rushing: {playerInfo[3]}, TDs: {playerInfo[4]}, Yard Avg: {playerInfo[5]}, Game Avg: {playerInfo[6]}")

def cleanPlayerName(playerName):
    return playerName.replace('*','').replace('+', '')


# csv output
csv_file_path = "historical_pass_data"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Season', 'Team', 'Player', 'Position', 'Games Started', 'Completions', 'Pass Attempts', 'Passing Yards', 'Passing TDs', 'Interceptions', 'Passing 1D', 'Success%', 'Pass Yards/Comp', 'Pass Yards/Game', 'QBR']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for playerInfo in passingData:
        playerInfo = (cleanPlayerName(playerInfo[0]),) + playerInfo[1:]
        writer.writerow({'Season': playerInfo[0], 'Team': playerInfo[1], 'Player': cleanPlayerName(playerInfo[2]), 'Position': playerInfo[3], 'Games Started': playerInfo[4], 'Completions': playerInfo[5], 'Pass Attempts': playerInfo[6], 'Passing Yards': playerInfo[7], 'Passing TDs': playerInfo[8], 'Interceptions': playerInfo[9], 'Passing 1D': playerInfo[10], 'Success%': playerInfo[11], 'Pass Yards/Comp': playerInfo[12], 'Pass Yards/Game': playerInfo[13], 'QBR': playerInfo[14]})

print("CSV file saved successfully:", csv_file_path)
