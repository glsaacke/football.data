import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.pro-football-reference.com/years/2023/passing.htm"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

rushing = soup.find(id="passing")

player_passData = []

for row in rushing.find_all('tr')[1:]:
    columns = row.find_all('td')
    if len(columns)>0:
        playerName = columns[0].text.strip()
        teamName = columns[1].text.strip()
        position = columns[3].text.strip()
        passingYards = columns[10].text.strip()
        passingTD = columns[11].text.strip()
        interceptions = columns[13].text.strip()
        yardAvgCompletion = columns[20].text.strip()
        gameAverage = columns[21].text.strip()
        player_passData.append((playerName, teamName, position, passingYards, passingTD, interceptions, yardAvgCompletion,gameAverage))

for playerInfo in player_passData:
    playerName, teamName, position, passingYards, passingTD, interceptions, yardAvgCompletion, gameAverage = playerInfo
    print(f"Player: {playerInfo[0]}, Team: {playerInfo[1]}, Position: {playerInfo[2]} Rushing: {playerInfo[3]}, TDs: {playerInfo[4]}, Int: {playerInfo[5]}, Yard Avg: {playerInfo[6]}, Game Avg: {playerInfo[7]}")

def cleanPlayerName(playerName):
    return playerName.replace('*','').replace('+', '')


# csv output
csv_file_path = "player_passing_data.csv"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Player', 'Team', 'Position', 'Passing Yards', 'Passing TDs', 'Interceptions', 'Yards/Completion', 'P Yard/Game']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for playerInfo in player_passData:
        playerInfo = (cleanPlayerName(playerInfo[0]),) + playerInfo[1:]
        writer.writerow({'Player': playerInfo[0], 'Team': playerInfo[1], 'Position': playerInfo[2], 'Passing Yards': playerInfo[3], 'Passing TDs': playerInfo[4], 'Interceptions': playerInfo[5], 'Yards/Completion': playerInfo[6], 'P Yard/Game': playerInfo[7]})

print("CSV file saved successfully:", csv_file_path)
