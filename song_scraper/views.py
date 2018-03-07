from django.db import IntegrityError, OperationalError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from song.models import Artist, Song, Album, SongOwnership
from pdb import set_trace
from datetime import date
from bs4 import BeautifulSoup
import requests, html5lib

# YOUTUBE API ##############################################
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


############################################################


def cut_string(str):
    return str.replace('\n', '').replace('\t', '').replace('\r', '')


def reset_ename(request):
    artists = Artist.objects.all()
    for artist in artists:
        artist.ename = None
        artist.save()
    return redirect('/artist/')


def is_alphabet(char):
    try:
        if char.encode('ascii').isalpha():
            return True
        else:
            return False
    except:
        return False


def extract_ename(kname):
    if "(" in kname and ")" in kname:
        i = 0
        for i in range(len(kname)):
            if kname[i] == '(':
                if kname[i - 1] == " ":
                    # Bruno Mars (브루노 마스)
                    if is_alphabet(kname[i - 2]):
                        return kname[0:i - 1]

                    # 브루노 마스 (Bruno Mars)
                    elif is_alphabet(kname[i + 1]):
                        return kname[i + 1:len(kname) - 1]
                else:
                    # Bruno Mars(브루노 마스)
                    if is_alphabet(kname[i - 1]):
                        return kname[0:i]

                    # 브루노 마스(Bruno Mars)
                    elif is_alphabet(kname[i + 1]):
                        return kname[i + 1:len(kname) - 1]

            else:
                continue
    else:
        # WINNER
        if is_alphabet(kname[0]):
            return kname


def add_ename(request):
    artists = Artist.objects.all()
    for artist in artists:
        if not artist.ename:
            artist.ename = extract_ename(artist.kname)
            artist.save()
    return redirect('/artist/')


def get_youtube_url(artist, title):
    DEVELOPER_KEY = 'AIzaSyBAHnqW6Pq-iPDgKxU5q8McH6qj7bKb-o8'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=" ".join([artist, title]),
        part='id, snippet',
        maxResults=1,
    ).execute()

    try:
        url = "https://www.youtube.com/watch?v=" + search_response.get('items')[0]['id']['videoId']
        return url
    except:
        print(artist + ' ' + title + ' URL is missing.')
        return None


def save_album_song(album_soup):
    album_target = album_soup.find('table', class_='info')
    song_target = album_soup.find('table', class_='trackList')

    # ALBUM
    title = album_soup.find_all('div', class_='innerContainer')[1].find('h1').get_text()
    rows = album_target.find_all('tr')

    album_artists = album_type = genre = style = company = distributor = playtime = None
    release_date = ""
    for row in rows:
        if row.find('th').get_text() == "아티스트":
            album_artists = row.find_all('a')
            if album_artists:
                for i in range(len(album_artists)):
                    album_artists[i] = cut_string(album_artists[i].get_text())
            else:
                album_artists = [cut_string(row.find('td').get_text())]
        elif row.find('th').get_text() == "앨범 종류":
            album_type = row.find('td').get_text()
        elif row.find('th').get_text() == "발매일":
            _release_date = row.find('time').get_text()
            _release_date = _release_date.split('.')
            if len(_release_date) == 2:
                _release_date.append('01')
            release_date = '-'.join(_release_date)
        elif row.find('th').get_text() == "장르":
            genre = row.find('a').get_text()
        # elif row.find('th').get_text() == "스타일":
        #     style = row.find('a').get_text()
        # elif row.find('th').get_text() == "기획사":
        #     company = row.find('td').get_text()
        # elif row.find('th').get_text() == "유통사":
        #     distributor = row.find('td').get_text()
        # elif row.find('th').get_text() == "재생시간":
        #     playtime = row.find('time').get_text()
        else:
            continue

    # if 'Various Artists' in album_artists:
    #     print("Various Artists")
    #     return
    # One Artist
    if len(album_artists) == 1:
        try:
            artist = Artist.objects.get(name=album_artists[0])
            # Album exists
            if not Album.objects.filter(artist=artist, title=title, release_date=release_date).exists():
                album = Album.objects.create(artist=artist, title=title, type=album_type, release_date=release_date)
                album.save()
            # Album doesn't exist.
            else:
                pass
        except:
            print(album_artists[0] + " doesn't exist.")

    # e.g.  https://music.bugs.co.kr/album/699412?wl_ref=list_tr_11_chart
    else:  # Several artists
        for _artist in album_artists:
            artist = Artist.objects.get(name=_artist)

            # Album doesn't exist.
            if not Album.objects.filter(title=title, type=album_type, release_date=release_date).exists():
                album = Album.objects.create(artist=artist, title=title, type=album_type, release_date=release_date)
                album.save()

            # Album already exists.
            else:
                album = Album.objects.get(artist=artist, type=album_type, release_date=release_date)
                if artist not in album.artist.all():
                    album.artist.add(artist)
                    album.save()

    # SONG
    song_titles = song_target.find_all('p', class_="title")
    track_nums = song_target.find_all('p', class_="trackIndex")

    album = Album.objects.get(album_title=title, album_type=album_type, album_release=release_date)
    artists = album.artist.all()
    str_artists = ' '.join([str(each) for each in artists])
    for i in range(len(track_nums)):
        if Song.objects.filter(title=cut_string(song_titles[i].get_text()), album=album).exists():
            pass
        else:
            song_title = cut_string(song_titles[i].get_text())
            y_url = get_youtube_url(str_artists, song_title)
            if not y_url:
                y_url = None
            song = Song.objects.create(title=song_title, album=album, track_num=track_nums[i].find('em').get_text(),
                                       url=y_url)
            song.save()


# 완성
def save_artist(artist_url, belong_to_group=False, group_name=None):
    artist_page = requests.get(artist_url)
    artist_soup = BeautifulSoup(artist_page.content, 'html.parser')
    artist_target = artist_soup.find('table', class_="info")
    artist_rows = artist_target.find_all('tr')
    name_artist = artist_soup.find_all('div', class_='innerContainer')[1].find('h1').get_text()
    ename = extract_ename(name_artist)

    if Artist.objects.filter(kname=name_artist).exists():
        print(name_artist + " already exists.")
        return

    a_type = a_debut = a_genre = a_bio = None
    a_nationality = "South Korea"
    is_group = False
    member_num = 1

    # 아티스트 저장
    for row in artist_rows:
        if row.find('th').get_text() == "유형":
            a_type = row.find('td').get_text()
        elif row.find('th').get_text() == "데뷔":
            a_debut = int(row.find('td').get_text())
        elif row.find('th').get_text() == "국적":
            a_nationality = cut_string(row.find('td').get_text())
        elif row.find('th').get_text() == "장르":
            a_genre = row.find('a').get_text()
        # elif row.find('th').get_text() == '바이오그래피':
        #     a_bio = row.find('a')['href']
        elif row.find('th').get_text() == "멤버":
            is_group = True
        else:
            continue
    # Artist doesn't exist.
    if not Artist.objects.filter(kname=name_artist).exists():
        # 저장할 아티스트가 그룹에 속해있는 경
        if belong_to_group:
            try:
                group_obj = Artist.objects.get(kname=group_name)
                Artist(kname=name_artist, ename=ename, debut_year=a_debut, type=a_type, belonged_group=group_obj,
                       nationality=a_nationality).save()
            except:
                print(group_name + " doesn't exist so failed to save " + name_artist + ".")
        else:
            Artist(kname=name_artist, ename=ename, debut_year=a_debut, type=a_type, nationality=a_nationality).save()
    # Artist already exists.
    else:
        print(name_artist + " already exists.")

    # 그룹인 경우, 마지막에 멤버들을 저장
    if is_group:
        for row in artist_rows:
            if row.find('th').get_text() == "멤버":
                member_list = []
                members = row.find_all('a')
                for each in members:
                    member_list.append((cut_string(each.get_text()), each['href']))
                for each in member_list:
                    # 각각 멤버 저장하기
                    save_artist(each[1], True, name_artist)

                member_num = len(row.find_all('a'))
            else:
                continue

    print("Artist " + name_artist + " object has been created!")


# 곡 디테일 페이지에 들어가서 정보를 긁어와 저장한다.
def save_song(song_url, track_num=1):
    song_detail_page = requests.get(song_url)
    song_detail_soup = BeautifulSoup(song_detail_page.content, 'html.parser')
    song_title = cut_string(song_detail_soup.find_all('div', class_='innerContainer')[1].find('h1').get_text())

    container = song_detail_soup.find('table', class_='info')

    info_rows = container.find_all('tr')
    for info_row in info_rows:
        if cut_string(info_row.find('th').get_text()) == "아티스트":
            artists = info_row.find_all('a')
            artist_names = []
            for i in range(len(artists)):
                artist_names.append(cut_string(artists[i].get_text()))

        elif cut_string(info_row.find('th').get_text()) == "앨범":
            album_title = cut_string(info_row.find('a').get_text())
        elif cut_string(info_row.find('th').get_text()) == "재생 시간":
            playtime = cut_string(info_row.find('time').get_text())


    lyric_container = song_detail_soup.find('div', class_='lyricsContainer')
    try:
        lyric = lyric_container.find('xmp').get_text()
    except:
        lyric = None

    youtube_url = get_youtube_url(" ".join(artist_names), song_title)

    try:
        artist_objs = []
        for each in artist_names:
            artist_objs.append(Artist.objects.get(kname=each))
        album_obj = Album.objects.get(title=album_title)
        song_obj = Song.objects.create(title=song_title, album=album_obj, track_num=track_num,
                                       playtime=playtime, lyrics=lyric, url=youtube_url)
        song_obj.save()
        for each in artist_objs:
            SongOwnership(artist=each, song=song_obj).save()
    except:
        print("Error occured at artist_obj, album_obj, or song_obj.")


# 앨범 페이지에 존재하는 노래들을 전부 긁어서 저장한다.
def save_songs(album_url):
    album_page = requests.get(album_url)
    album_soup = BeautifulSoup(album_page.content, 'html.parser')
    album_target = album_soup.find('table', class_='info')

    temp_container = album_soup.find_all('tbody')
    song_info_container = temp_container[1]
    song_rows = song_info_container.find_all('tr')

    for song_row in song_rows:
        # 웹페이지 접속하기 전에 먼저 객체가 존재하는지 체크
        # song_title = cut_string(song_row.find('p', class_='title').find('a').get_text())
        # if Song.objects.

        song_detail_url = song_row.find('a', class_='trackInfo')['href']
        save_song(song_detail_url)


# 완성
def save_album(album_url):

    album_page = requests.get(album_url)
    album_soup = BeautifulSoup(album_page.content, 'html.parser')
    album_target = album_soup.find('table', class_='info')
    artists = album_target.find('tr').find_all('a')
    if artists == []: # Various Artists 의 경우
        artists = [album_target.find('tr').find('td')]

    artists_names = []
    for artist in artists:
        artists_names.append(cut_string(artist.get_text()))

    artist_kname = None
    if len(artists_names) > 1:
        for i in range(len(artists_names)):
            if not Artist.objects.filter(kname=artists_names[i]).exists():
                save_artist(artists[i]['href'])


        artist_kname = "Various Artists"
    else:
        artist_kname = artists_names[0]

    # 아티스트 객체가 존재
    try:
        artist_obj = Artist.objects.get(kname=artist_kname)  # 아티스트가 먼저 생성되었어야 한다.

    # 아티스트 객체 없어 -> 생성해
    except:
        for each_href in artists:
            save_artist(each_href['href'])
        artist_obj = Artist.objects.get(kname=artist_kname)  # 아티스트가 먼저 생성되었어야 한다.

    album_info_container = album_soup.find_all('tbody')[0]
    album_title_container = album_soup.find_all('div', class_='innerContainer')
    album_title = cut_string(album_title_container[1].find('h1').get_text())
    # 앨범 존재 여부 파악
    if not Album.objects.filter(artist=artist_obj, title=album_title).exists():
        # 앨범 객체 생성 및 저장
        album_info_rows = album_info_container.find_all('tr')
        album_type = release_date = None
        for row in album_info_rows:
            if cut_string(row.find('th').get_text()) == '앨범 종류':
                album_type = cut_string(row.find('td').get_text())
            elif cut_string(row.find('th').get_text()) == '발매일':
                _release_date = cut_string(row.find('time').get_text())
                _release_date = _release_date.split('.')
                if len(_release_date) == 2:
                    _release_date.append('01')
                release_date = '-'.join(_release_date)

        Album(artist=artist_obj, title=album_title, type=album_type, release_date=release_date, description=None).save()
        print("Album " + album_title + " has been saved.")

    # 노래 저장 시작
    song_rows = album_soup.find_all('a', class_='trackInfo')
    song_urls = []

    for row in song_rows:
        song_urls.append(row['href'])

    t_num = 0
    for url in song_urls:
        t_num += 1
        save_song(url, t_num)


# 아티스트 저장 -> 앨범 저장 -> 곡 저장
def save_top100(request):
    chart_url = "https://music.bugs.co.kr/chart/track/realtime/total"
    top100_page = requests.get(chart_url)
    top100_soup = BeautifulSoup(top100_page.content, 'html.parser')
    album_target = top100_soup.find(class_="byChart")

    album_urls = []
    album_list = album_target.find_all('a', class_="album")
    for each in album_list:
        album_urls.append(each['href'])
    for album_url in album_urls:
        save_album(album_url)


    return redirect('/song/')
