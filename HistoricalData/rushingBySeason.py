import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Selenium webdriver (replace "chrome" with "firefox" if using Firefox)
driver = webdriver.Chrome()

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


url = "https://www.pro-football-reference.com/years/"
baseUrl = "https://www.pro-football-reference.com"
response = requests.get(url)
allTeams = ['crd', 'atl', 'bal', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'hou', 'ind', 'jax', 'kan', 'lac', 'lar', 'lvr', 'mia', 'min', 'nor', 'nwe', 'nyg', 'nyj', 'phi', 'pit', 'sea', 'sfo', 'tam', 'ten', 'was']

soup = BeautifulSoup(response.content, 'html.parser')

seasons = soup.find(id="years")
seasonRushData = []

for row in seasons.find_all('tr')[2:]:
    season = row.find('th').text.strip()
    seasonUrl = baseUrl + '/years/' + season
    print(seasonUrl)
    time.sleep(3.1)
    response2 = requests.get(url)

    soup2 = BeautifulSoup(response.content, 'html.parser')
    teams = soup.find(id="team_stats")
   
    for team in allTeams:
        teamUrl = baseUrl + '/teams/' + team + '/' + season + '.htm'
        print(teamUrl)

        time.sleep(3.1)

        driver.get(teamUrl)
        wait = WebDriverWait(driver, 3)
        wait.until(EC.visibility_of_element_located((By.ID, "rushing_and_receiving")))
        html = driver.page_source

        soup3 = BeautifulSoup(html, 'html.parser')  # Use response3 here
        # Assuming you have already fetched and parsed the webpage into soup3
        rushingStats = soup3.find('table', {'id': 'rushing_and_receiving'})
            # Now you can iterate over the rows in rushingStats table
        for row in rushingStats.find_all('tr')[2:]:
            columns = row.find_all('td')
            print(columns)
            season = season
            team = team
            playerName = columns[0].text.strip()
            position = columns[2].text.strip()
            gamesStarted = columns[4].text.strip()
            attempts = columns[5].text.strip()
            yards = columns[6].text.strip()
            TDs = columns[7].text.strip()
            yardsAttempt = columns[11].text.strip()
            yardsGame = columns[12].text.strip()
            if(int(attempts) > 0 and position != null):
                seasonRushData.append((season, team, playerName, position, gamesStarted, attempts, yards, TDs, yardsAttempt, yardsGame))
                print(season + ' ' + team + ' ' + playerName + ' ' + position + ' ' + gamesStarted + ' ' + attempts + ' ' + yards + ' ' + TDs + ' ' + yardsAttempt + ' ' + yardsGame)

        driver.quit()

                



        

       # if len(columns)>0:
    #     playerName = columns[0].text.strip()
    #     teamName = columns[1].text.strip()
    #     position = columns[3].text.strip()
    #     rushingYards = columns[7].text.strip()
    #     rushingTD = columns[8].text.strip()
    #     yardAverage = columns[12].text.strip()
    #     gameAverage = columns[13].text.strip()
    #     player_rushData.append((playerName, teamName, position, rushingYards, rushingTD, yardAverage,gameAverage))

# for playerInfo in seasonRushData:
#     playerName, teamName, position, rushingYards, rushingTD, yardAverage, gameAverage = playerInfo
#     print(f"Player: {playerInfo[0]}, Team: {playerInfo[1]}, Position: {playerInfo[2]} Rushing: {playerInfo[3]}, TDs: {playerInfo[4]}, Yard Avg: {playerInfo[5]}, Game Avg: {playerInfo[6]}")

# def cleanPlayerName(playerName):
#     return playerName.replace('*','').replace('+', '')


# # csv output
# csv_file_path = "season_rushing_data.csv"

# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#     fieldnames = ['Season', 'Team', 'Player', 'Position', 'Games Started', 'Rushing Attempts', 'Rushing Yards', 'Rushing TDs', 'Rush Yards/Attempt', 'Rush Yards/Game']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()

#     for playerInfo in seasonRushData:
#         playerInfo = (cleanPlayerName(playerInfo[0]),) + playerInfo[1:]
#         writer.writerow({'Season': playerInfo[0], 'Team': playerInfo[1], 'Player': playerInfo[2], 'Position': playerInfo[3], 'Games Started': playerInfo[4], 'Rushing Attempts': playerInfo[5], 'Rushing Yards': playerInfo[6], 'Rushing TDs': playerInfo[7], 'Rush Yards/Attempt': playerInfo[8], 'Rush Yards/Game': playerInfo[9]})

# print("CSV file saved successfully:", csv_file_path)
