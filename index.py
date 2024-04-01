import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.pro-football-reference.com/years/2023/passing.htm"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

passing = soup.find(id="passing")

player_passData = []

for row in passing.find_all('tr')[1:]:
    columns = row.find_all('td')
    if len(columns)>0:
        player_name = columns[0].text.strip()
        team_name = columns[1].text.strip()
        position = columns[3].text.strip()
        passing_yards = columns[10].text.strip()
        player_passData.append((player_name, team_name, position, passing_yards))

for player_info in player_passData:
    player_name, team_name, position, passing_yards = player_info
    print(f"Player: {player_info[0]}, Team: {player_info[1]}, Position: {player_info[2]} Passing: {player_info[3]}")

def cleanPlayerName(player_name):
    return player_name.replace('*','').replace('+', '')


# csv output
csv_file_path = "player_passing_data.csv"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Player', 'Team', 'Position', 'Passing Yards']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for player_info in player_passData:
        player_info = (cleanPlayerName(player_info[0]),) + player_info[1:]
        writer.writerow({'Player': player_info[0], 'Team': player_info[1], 'Position': player_info[2], 'Passing Yards': player_info[3]})

print("CSV file saved successfully:", csv_file_path)
