from youtubesearchpython import (
    VideosSearch, ChannelsSearch, PlaylistsSearch, Search, CustomSearch, ChannelSearch,
    Video, Playlist, Channel, Comments, Transcript, Hashtag, Suggestions,
    StreamURLFetcher, playlist_from_channel_id, VideoSortOrder, ResultMode
)

# Search examples
allSearch = Search('NoCopyrightSounds', limit=1, language='en', region='US')
print(allSearch.result())

videosSearch = VideosSearch('NoCopyrightSounds', limit=10, language='en', region='US')
print(videosSearch.result(mode=ResultMode.json))

channelsSearch = ChannelsSearch('NoCopyrightSounds', limit=1, language='en', region='US')
print(channelsSearch.result(mode=ResultMode.json))

playlistsSearch = PlaylistsSearch('NoCopyrightSounds', limit=1, language='en', region='US')
print(playlistsSearch.result())

customSearch = CustomSearch('NoCopyrightSounds', VideoSortOrder.uploadDate, language='en', region='US')
print(customSearch.result())

channelSearch = ChannelSearch("Watermelon Sugar", "UCZFWPqqPkFlNwIxcpsLOwew")
print(channelSearch.result(mode=ResultMode.json))

# Pagination example
search = VideosSearch('NoCopyrightSounds')
index = 0
for video in search.result()['result']:
    print(f'{index} - {video["title"]}')
    index += 1
search.next()
for video in search.result()['result']:
    print(f'{index} - {video["title"]}')
    index += 1
search.next()
for video in search.result()['result']:
    print(f'{index} - {video["title"]}')
    index += 1

# Video examples
video = Video.get('https://www.youtube.com/watch?v=z0GKGpObgPY', mode=ResultMode.json, get_upload_date=True)
print(video)
videoInfo = Video.getInfo('https://youtu.be/z0GKGpObgPY', mode=ResultMode.json)
print(videoInfo)
videoFormats = Video.getFormats('z0GKGpObgPY')
print(videoFormats)

# Playlist examples
playlist = Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK', mode=ResultMode.json)
print(playlist)
playlistInfo = Playlist.getInfo('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK', mode=ResultMode.json)
print(playlistInfo)
playlistVideos = Playlist.getVideos('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
print(playlistVideos)

playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
print(f'Videos Retrieved: {len(playlist.videos)}')
while playlist.hasMoreVideos:
    print('Getting more videos...')
    playlist.getNextVideos()
    print(f'Videos Retrieved: {len(playlist.videos)}')
print('Found all the videos.')

# Get all videos of a channel
channel_id = "UC_aEa8K-EOJ3D6gOs7HcyNg"
playlist = Playlist(playlist_from_channel_id(channel_id))
print(f'Videos Retrieved: {len(playlist.videos)}')
while playlist.hasMoreVideos:
    print('Getting more videos...')
    playlist.getNextVideos()
    print(f'Videos Retrieved: {len(playlist.videos)}')
print('Found all the videos.')

# Channel examples
channel = Channel.get("UC_aEa8K-EOJ3D6gOs7HcyNg")
print(channel)

channel = Channel("UC_aEa8K-EOJ3D6gOs7HcyNg")
print(len(channel.result["playlists"]))
while channel.has_more_playlists():
    channel.next()
    print(len(channel.result["playlists"]))

# Comments examples
comments = Comments("_ZdsmLgCVdU")
print(f'Comments Retrieved: {len(comments.comments["result"])}')
while comments.hasMoreComments:
    comments.getNextComments()
    print(f'Comments Retrieved: {len(comments.comments["result"])}')
print("Found all comments")

# Transcript examples
transcript = Transcript.get("https://www.youtube.com/watch?v=L7kF4MXXCoA")
print(transcript)

url = "https://www.youtube.com/watch?v=-1xu0IP35FI"
transcript_en = Transcript.get(url)
transcript_es = Transcript.get(url, transcript_en["languages"][-1]["params"])
print(transcript_es)

# Suggestions and hashtags
suggestions = Suggestions(language='en', region='US')
print(suggestions.get('NoCopyrightSounds', mode=ResultMode.json))

hashtag = Hashtag('ncs', limit=1)
print(hashtag.result())

# Stream URL fetcher (requires yt-dlp)
fetcher = StreamURLFetcher()
videoA = Video.get("https://www.youtube.com/watch?v=aqz-KE-bpKQ")
videoB = Video.get("https://www.youtube.com/watch?v=ZwNxYJfW-eU")
singleUrlA = fetcher.get(videoA, 22)
allUrlsB = fetcher.getAll(videoB)
print(singleUrlA)
print(allUrlsB)
