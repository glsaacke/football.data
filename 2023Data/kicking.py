import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.pro-football-reference.com/years/2023/kicking.htm"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

kicking = soup.find(id="kicking")

player_kickData = []

for row in kicking.find_all('tr')[1:]:
    columns = row.find_all('td')
    if len(columns)>0:
        playerName = columns[0].text.strip()
        teamName = columns[1].text.strip()
        position = columns[3].text.strip()
        fgAttempt = columns[16].text.strip()
        fgMade = columns[17].text.strip()
        xpAttempt = columns[20].text.strip()
        xpMade = columns[21].text.strip()
        longest = columns[18].text.strip()
        player_kickData.append((playerName, teamName, position, fgAttempt, fgMade, xpAttempt, xpMade, longest))

# for playerInfo in player_rechData:
#     playerName, teamName, position, receptions, recYards, rushingTD, yardAverage, gameAverage = playerInfo
#     print(f"Player: {playerInfo[0]}, Team: {playerInfo[1]}, Position: {playerInfo[2]} Rushing: {playerInfo[3]}, TDs: {playerInfo[4]}, Yard Avg: {playerInfo[5]}, Game Avg: {playerInfo[6]}")

def cleanPlayerName(playerName):
    return playerName.replace('*','').replace('+', '')


# csv output
csv_file_path = "player_kicking_data.csv"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Player', 'Team', 'Position', 'FG Attempted', 'FG Made', 'XP Attempted', 'XP Made', 'Longest FG']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for playerInfo in player_kickData:
        playerInfo = (cleanPlayerName(playerInfo[0]),) + playerInfo[1:]
        writer.writerow({'Player': playerInfo[0], 'Team': playerInfo[1], 'Position': playerInfo[2], 'FG Attempted': playerInfo[3], 'FG Made': playerInfo[4], 'XP Attempted': playerInfo[5], 'XP Made': playerInfo[6], 'Longest FG': playerInfo[7]})

print("CSV file saved successfully:", csv_file_path)
