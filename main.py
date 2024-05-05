import requests
from bs4 import BeautifulSoup

BILLBOARD_LINK = "https://www.billboard.com/charts/hot-100/"
USER_DATE = input("Enter the date in the format of YYY-MM-DD : ")
link_with_date = f"{BILLBOARD_LINK}{USER_DATE}/"
response = requests.get(url=link_with_date)
print(response)
soup = BeautifulSoup(response.content,"html.parser")
song_names = soup.find('h3', class_='c-title')

print(song_names.getText())
