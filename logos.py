import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.sportslogos.net/teams/list_by_league/7/National_Football_League/NFL/logos/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

logos = soup.find(class_="logoWall")

logoData = []

for li in logos.find_all('li'):
    image_tag = li.find('a')
    if image_tag:
        image_href = image_tag.get('href')
        image_title = image_tag.get('title')
        logoData.append((image_href, image_title))

for image_info in logoData:
    image_href, image_title = image_info
    print(f"Image Href: {image_href}, Image Title: {image_title}")



# csv output
csv_file_path = "logos.csv"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['logo', 'team']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for imageInfo in logoData:
        writer.writerow({'logo': imageInfo[0], 'team': imageInfo[1]})

print("CSV file saved successfully:", csv_file_path)
