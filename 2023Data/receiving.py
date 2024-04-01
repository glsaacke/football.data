import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.pro-football-reference.com/years/2023/receiving.htm"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

receiving = soup.find(id="receiving")

player_recData = []

for row in receiving.find_all('tr')[1:]:
    columns = row.find_all('td')
    if len(columns)>0:
        playerName = columns[0].text.strip()
        teamName = columns[1].text.strip()
        position = columns[3].text.strip()
        receptions = columns[7].text.strip()
        recYards = columns[9].text.strip()
        recTD = columns[11].text.strip()
        yardAverage = columns[10].text.strip()
        gameAverage = columns[17].text.strip()
        player_recData.append((playerName, teamName, position, receptions, recYards, recTD, yardAverage, gameAverage))

# for playerInfo in player_rechData:
#     playerName, teamName, position, receptions, recYards, rushingTD, yardAverage, gameAverage = playerInfo
#     print(f"Player: {playerInfo[0]}, Team: {playerInfo[1]}, Position: {playerInfo[2]} Rushing: {playerInfo[3]}, TDs: {playerInfo[4]}, Yard Avg: {playerInfo[5]}, Game Avg: {playerInfo[6]}")

def cleanPlayerName(playerName):
    return playerName.replace('*','').replace('+', '')


# csv output
csv_file_path = "player_receiving_data.csv"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Player', 'Team', 'Position', 'Receptions', 'Receiving Yards', 'Receiving TDs', 'Re Yard/Avg', 'Re Yard/Game']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for playerInfo in player_recData:
        playerInfo = (cleanPlayerName(playerInfo[0]),) + playerInfo[1:]
        writer.writerow({'Player': playerInfo[0], 'Team': playerInfo[1], 'Position': playerInfo[2], 'Receptions': playerInfo[3], 'Receiving Yards': playerInfo[4], 'Receiving TDs': playerInfo[5], 'Re Yard/Avg': playerInfo[6], 'Re Yard/Game': playerInfo[7]})

print("CSV file saved successfully:", csv_file_path)
