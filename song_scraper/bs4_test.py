from bs4 import BeautifulSoup
import requests
from pdb import set_trace
import html5lib


# from .models import Song, Artist, Album

# Update DB Routine: Artist -> Album -> Song
# Explicitly run with Python

def save_song():
    youtube = 'https://www.youtube.com'
    youtube_url = "https://www.youtube.com/results?search_query="
    chart_url = "https://music.bugs.co.kr/chart/track/day/total"
    page = requests.get(chart_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    target = soup.find(class_="trackList")

    artist_urls = []
    artist_list = target.find_all('p', class_="artist")
    for each in artist_list:
        if each.find('a'):
            artist_urls.append(each.find('a')['href'])
    for artist_url in artist_urls:
        artist_page = requests.get(artist_url)
        artist_soup = BeautifulSoup(artist_page.content, 'html.parser')
        artist_target = artist_soup.find('table', class_="info")

        artist_rows = artist_target.find_all('tr')
        artist = artist_soup.find_all('div', class_='innerContainer')[1].find('h1').get_text()
        song = artist_soup.find('p', class_='title').get_text().replace('\n', '')

        url = youtube_url + artist + "+" + song
        youtube_page = requests.get(url)
        youtube_soup = BeautifulSoup(youtube_page.content, 'html.parser')
        mv_url = youtube_soup.find('a', {'id': 'video-title'})['href']

        # soup.find("div", {"id": "articlebody"})

        print(artist, mv_url)

    album_urls = []
    album_list = target.find_all('a', class_="album")
    for each in album_list:
        album_urls.append(each['href'])
    for each in album_urls:
        _page = requests.get(each)
        _soup = BeautifulSoup(_page.content, 'html.parser')
        _target = _soup.find('table', class_='info')

        title = _soup.find_all('div', class_='innerContainer')[1].find('h1').get_text()
        rows = _target.find_all('tr')

        album_type = release_date = genre = style = company = distributor = playtime = None

        for row in rows:
            if row.find('th').get_text() == "아티스트":
                try:
                    artist = row.find('a').get_text()
                except AttributeError:
                    set_trace()
                    artist = row.find('td').get_text().replace('\r', '').replace('\t','').replace('\n','')
            elif row.find('th').get_text() == "앨범 종류":
                album_type = row.find('td').get_text()
            elif row.find('th').get_text() == "발매일":
                release_date = row.find('time').get_text()
            elif row.find('th').get_text() == "장르":
                genre = row.find('a').get_text()
            elif row.find('th').get_text() == "스타일":
                style = row.find('a').get_text()
            elif row.find('th').get_text() == "기획사":
                company = row.find('td').get_text()
            elif row.find('th').get_text() == "유통사":
                distributor = row.find('td').get_text()
            elif row.find('th').get_text() == "재생시간":
                playtime = row.find('time').get_text()
            else:
                continue
        try:
            print(artist, album_type, release_date, genre, style, company, distributor, playtime)
        except ValueError:
            pass


def test():
    youtube = 'https://www.youtube.com'
    youtube_url = "https://www.youtube.com/results?search_query=정승환+눈사람"
    youtube_page = requests.get(youtube_url)
    youtube_soup = BeautifulSoup(youtube_page.content, 'html5lib')
    # set_trace()
    mv_url = youtube_soup.find('a', class_="yt-uix-tile-link").get('href')
    print(youtube+mv_url)


# save_song()
test()

# titles[1].input['title']
