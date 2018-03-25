from django.db import IntegrityError, OperationalError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from song.models import Artist, Song, Album, SongOwnership
from pdb import set_trace
from datetime import date
from bs4 import BeautifulSoup
import requests, html5lib
from .youtube_dev_key import youtube_dev_key

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
    DEVELOPER_KEY = youtube_dev_key
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


# 완성
def save_artist(artist_url, belong_to_group=False, group_name=None):
    artist_page = requests.get(artist_url)
    artist_soup = BeautifulSoup(artist_page.content, 'html.parser')
    artist_target = artist_soup.find('table', class_="info")

    name_artist = cut_string(artist_soup.find_all('div', class_='innerContainer')[1].find('h1').find(text=True))
    ename = extract_ename(name_artist)
    try:
        artist_rows = artist_target.find_all('tr')
    except:
        print("There's no information about " + name_artist)
        return

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


def save_artist_from_song(container):
    info_rows = container.find_all('tr')[0].find_all('a')
    for row in info_rows:
        save_artist(row['href'])


# 곡 디테일 페이지에 들어가서 정보를 긁어와 저장한다.
def save_song(song_url, track_num=1):
    song_detail_page = requests.get(song_url)
    song_detail_soup = BeautifulSoup(song_detail_page.content, 'html.parser')
    song_title = cut_string(song_detail_soup.find_all('div', class_='innerContainer')[1].find('h1').get_text())
    container = song_detail_soup.find('table', class_='info')

    info_rows = container.find_all('tr')
    for info_row in info_rows:
        if cut_string(info_row.find('th').find(text=True)) == "아티스트":
            artists = info_row.find_all('a')
            artist_names = []
            for i in range(len(artists)):
                artist_names.append(cut_string(artists[i].find(text=True)))

        elif cut_string(info_row.find('th').get_text()) == "앨범":
            album_title = cut_string(info_row.find('a').get_text())
        elif cut_string(info_row.find('th').get_text()) == "재생 시간":
            playtime = cut_string(info_row.find('time').get_text())

    lyric_container = song_detail_soup.find('div', class_='lyricsContainer')
    try:
        lyric = lyric_container.find('xmp').get_text()
    except:
        lyric = None

    try:
        artist_objs = []
        for each in artist_names:
            artist_objs.append(Artist.objects.get(kname=each))
    except:
        save_artist_from_song(container)
        return

    try:
        album_obj = Album.objects.get(title=album_title)
    except:
        print('Failed to get the album, ' + album_title + ' object.')
        return

    try:
        youtube_url = get_youtube_url(" ".join(artist_names), song_title)
        song_obj = Song.objects.create(title=song_title, album=album_obj, track_num=track_num,
                                       playtime=playtime, lyrics=lyric, url=youtube_url)
        song_obj.save()
    except IntegrityError:
        print('The song, ' + song_title + ' object already exists.')
        return
    except:
        print('Failed to save the song, ' + song_title + ' object.')
        return

    try:
        for each in artist_objs:
            SongOwnership(artist=each, song=song_obj).save()
    except IntegrityError:
        print('The ownership between ' + str(song_obj) + ' and ' + str(each) + ' object already exists.')
        return
    except:
        print('Failed to save ' + str(each) + " and " + str(song_obj) + " ownership.")


# 완성
def save_album(album_url):
    album_page = requests.get(album_url)
    album_soup = BeautifulSoup(album_page.content, 'html.parser')
    album_target = album_soup.find('table', class_='info')
    artists = album_target.find('tr').find_all('a')
    if artists == []:  # Various Artists 의 경우
        artists = [album_target.find('tr').find('td')]

    artists_names = []
    for artist in artists:
        artists_names.append(cut_string(artist.find(text=True)))

        # artists_names.append(cut_string(artist.get_text()))
        # set_trace()

    artist_kname = None
    artist_obj = None
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

    album_title_obj_list = Album.objects.all()
    album_title_list = []
    for each_album in album_title_obj_list:
        album_title_list.append(each_album.title)
    for each in album_list:
        # 존재하는 앨범은 생략
        if each.find(text=True) not in album_title_list:
            album_urls.append(each['href'])
    for album_url in album_urls:
        save_album(album_url)

    return redirect('/song/')