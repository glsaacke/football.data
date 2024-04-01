import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.pro-football-reference.com/years/2023/rushing.htm"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

rushing = soup.find(id="rushing")

player_rushData = []

for row in rushing.find_all('tr')[1:]:
    columns = row.find_all('td')
    if len(columns)>0:
        playerName = columns[0].text.strip()
        teamName = columns[1].text.strip()
        position = columns[3].text.strip()
        rushingYards = columns[7].text.strip()
        rushingTD = columns[8].text.strip()
        yardAverage = columns[12].text.strip()
        gameAverage = columns[13].text.strip()
        player_rushData.append((playerName, teamName, position, rushingYards, rushingTD, yardAverage,gameAverage))

for playerInfo in player_rushData:
    playerName, teamName, position, rushingYards, rushingTD, yardAverage, gameAverage = playerInfo
    print(f"Player: {playerInfo[0]}, Team: {playerInfo[1]}, Position: {playerInfo[2]} Rushing: {playerInfo[3]}, TDs: {playerInfo[4]}, Yard Avg: {playerInfo[5]}, Game Avg: {playerInfo[6]}")

def cleanPlayerName(playerName):
    return playerName.replace('*','').replace('+', '')


# csv output
csv_file_path = "player_rushing_data.csv"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Player', 'Team', 'Position', 'Rushing Yards', 'Rushing TDs', 'R Yard/Avg', 'R Yard/Game']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for playerInfo in player_rushData:
        playerInfo = (cleanPlayerName(playerInfo[0]),) + playerInfo[1:]
        writer.writerow({'Player': playerInfo[0], 'Team': playerInfo[1], 'Position': playerInfo[2], 'Rushing Yards': playerInfo[3], 'Rushing TDs': playerInfo[4], 'R Yard/Avg': playerInfo[5], 'R Yard/Game': playerInfo[6]})

print("CSV file saved successfully:", csv_file_path)
