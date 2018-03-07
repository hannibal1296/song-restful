import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pdb import set_trace

DEVELOPER_KEY = 'AIzaSyBAHnqW6Pq-iPDgKxU5q8McH6qj7bKb-o8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=" ".join(["정승환", "그리고 눈"]),
        part='id, snippet',
        maxResults=1,
    ).execute()

    url = "https://www.youtube.com/watch?v="+search_response.get('items')[0]['id']['videoId']
    print(url)



# Call the search.list method to retrieve results matching the specified
    # query term.
#     search_response = youtube.search().list(
#         q=options['q'],
#         part='id, snippet',
#         maxResults=options['max_results'],
#     ).execute()
#
#     videos = []
#     channels = []
#     playlists = []
#
#     # Add each result to the appropriate list, and then display the lists of
#     # matching videos, channels, and playlists.
#     for search_result in search_response.get('items', []):
#         print("HEY HERE " + search_result['id']['videoId'])
#         if search_result['id']['kind'] == 'youtube#video':
#             videos.append('%s (%s)' % (search_result['snippet']['title'],
#                                        search_result['id']['videoId']))
#         elif search_result['id']['kind'] == 'youtube#channel':
#             channels.append('%s (%s)' % (search_result['snippet']['title'],
#                                          search_result['id']['channelId']))
#         elif search_result['id']['kind'] == 'youtube#playlist':
#             playlists.append('%s (%s)' % (search_result['snippet']['title'],
#                                           search_result['id']['playlistId']))
#
#     print('Videos:\n', '\n'.join(videos), '\n')
#     print('Channels:\n', '\n'.join(channels), '\n')
#     print('Playlists:\n', '\n'.join(playlists), '\n')
#
# option = {
#     'q': "정승환",
#     'max_results': 1,
# }
# youtube_search(option)
youtube_search()