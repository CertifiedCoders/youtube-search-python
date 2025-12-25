# Synchronous API Documentation

This document covers the synchronous API for `youtube-search-python`. For installation, project overview, and general information, see the [main README](../../README.md).

## Overview

The synchronous API provides blocking, straightforward access to YouTube search and data retrieval. All methods execute synchronously and return results immediately.

## Import

```python
from youtubesearchpython import VideosSearch, ChannelsSearch, PlaylistsSearch, Search, CustomSearch, ChannelSearch
from youtubesearchpython import Video, Playlist, Channel, Comments, Transcript, Hashtag, Suggestions
from youtubesearchpython import StreamURLFetcher, playlist_from_channel_id, ResultMode
```

## Basic Usage

### Search for videos

```python
from youtubesearchpython import VideosSearch

videosSearch = VideosSearch('NoCopyrightSounds', limit=2)
print(videosSearch.result())
```

### Search for channels

```python
from youtubesearchpython import ChannelsSearch

channelsSearch = ChannelsSearch('NoCopyrightSounds', limit=10, region='US')
print(channelsSearch.result(mode=ResultMode.json))
```

### Search for playlists

```python
from youtubesearchpython import PlaylistsSearch

playlistsSearch = PlaylistsSearch('NoCopyrightSounds', limit=1)
print(playlistsSearch.result())
```

### Search with filters

```python
from youtubesearchpython import CustomSearch, VideoSortOrder

customSearch = CustomSearch('NoCopyrightSounds', VideoSortOrder.uploadDate, language='en', region='US')
print(customSearch.result())
```

Available filters include:
- `SearchMode.videos`
- `VideoUploadDateFilter.lastHour`
- `VideoDurationFilter.long`
- `VideoSortOrder.viewCount`
- `VideoSortOrder.uploadDate`

You can also pass custom filter strings by extracting them from YouTube query URLs (e.g., `"EgQIBRAB"` from `https://www.youtube.com/results?search_query=NoCopyrightSounds&sp=EgQIBRAB`).

### Search for everything

```python
from youtubesearchpython import Search

allSearch = Search('NoCopyrightSounds', limit=1, language='en', region='US')
print(allSearch.result())
```

The `type` key in the result can be used to differentiate between videos, channels, and playlists.

## Advanced Usage

### Getting next page results

```python
from youtubesearchpython import VideosSearch

search = VideosSearch('NoCopyrightSounds')
print(search.result()['result'])

search.next()
print(search.result()['result'])

search.next()
print(search.result()['result'])
```

### Getting video information

```python
from youtubesearchpython import Video, ResultMode

video = Video.get('https://www.youtube.com/watch?v=z0GKGpObgPY', mode=ResultMode.json, get_upload_date=True)
print(video)

videoInfo = Video.getInfo('https://youtu.be/z0GKGpObgPY', mode=ResultMode.json)
print(videoInfo)

videoFormats = Video.getFormats('z0GKGpObgPY')
print(videoFormats)
```

**Note:** 
- `Video.get()` returns both information and formats
- `Video.getInfo()` returns only information
- `Video.getFormats()` returns only formats
- You can pass either a link or video ID
- `get_upload_date=True` enables HTML parsing to get upload date (slower but more complete)

### Working with playlists

```python
from youtubesearchpython import Playlist, ResultMode

playlist = Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK', mode=ResultMode.json)
print(playlist)

playlistInfo = Playlist.getInfo('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK', mode=ResultMode.json)
print(playlistInfo)

playlistVideos = Playlist.getVideos('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
print(playlistVideos)
```

### Getting all videos from a playlist

```python
from youtubesearchpython import Playlist

playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
print(f'Videos Retrieved: {len(playlist.videos)}')

while playlist.hasMoreVideos:
    print('Getting more videos...')
    playlist.getNextVideos()
    print(f'Videos Retrieved: {len(playlist.videos)}')

print('Found all the videos.')
```

### Get all videos of a channel

```python
from youtubesearchpython import Playlist, playlist_from_channel_id

channel_id = "UC_aEa8K-EOJ3D6gOs7HcyNg"
playlist = Playlist(playlist_from_channel_id(channel_id))

print(f'Videos Retrieved: {len(playlist.videos)}')

while playlist.hasMoreVideos:
    print('Getting more videos...')
    playlist.getNextVideos()
    print(f'Videos Retrieved: {len(playlist.videos)}')

print('Found all the videos.')
```

### Getting search suggestions

```python
from youtubesearchpython import Suggestions, ResultMode

suggestions = Suggestions(language='en', region='US')
print(suggestions.get('NoCopyrightSounds', mode=ResultMode.json))
```

### Getting videos by hashtag

```python
from youtubesearchpython import Hashtag

hashtag = Hashtag('ncs', limit=1)
print(hashtag.result())
```

### Channel search

```python
from youtubesearchpython import ChannelSearch, ResultMode

channel = ChannelSearch("Watermelon Sugar", "UCZFWPqqPkFlNwIxcpsLOwew")
print(channel.result(mode=ResultMode.json))
```

### Getting direct stream URLs

Requires `yt-dlp` to be installed: `pip install yt-dlp`

```python
from youtubesearchpython import StreamURLFetcher, Video

fetcher = StreamURLFetcher()

videoA = Video.get("https://www.youtube.com/watch?v=aqz-KE-bpKQ")
videoB = Video.get("https://www.youtube.com/watch?v=ZwNxYJfW-eU")

singleUrlA = fetcher.get(videoA, 22)
allUrlsB = fetcher.getAll(videoB)
print(singleUrlA)
print(allUrlsB)
```

**Note:** 
- `StreamURLFetcher` can fetch direct video URLs without additional network requests
- Avoid instantiating `StreamURLFetcher` more than once (create a global instance)
- `get()` returns a URL for a specific format
- `getAll()` returns all stream URLs in a dictionary

### Getting comments

```python
from youtubesearchpython import Comments

comments = Comments("_ZdsmLgCVdU")
print(len(comments.comments["result"]))

while comments.hasMoreComments:
    comments.getNextComments()
    print(len(comments.comments["result"]))

print("Found all comments")
```

**Note:** Comments are automatically initialized when creating a `Comments` instance. Use `hasMoreComments` to check if more comments are available.

### Retrieve video transcript

```python
from youtubesearchpython import Transcript

transcript = Transcript.get("https://www.youtube.com/watch?v=-1xu0IP35FI")
print(transcript)

url = "https://www.youtube.com/watch?v=-1xu0IP35FI"
transcript_en = Transcript.get(url)
transcript_es = Transcript.get(url, transcript_en["languages"][-1]["params"])
print(transcript_es)
```

### Retrieve channel info

```python
from youtubesearchpython import Channel

channel = Channel.get("UC_aEa8K-EOJ3D6gOs7HcyNg")
print(channel)
```

### Retrieve channel playlists

```python
from youtubesearchpython import Channel

channel = Channel("UC_aEa8K-EOJ3D6gOs7HcyNg")
print(len(channel.result["playlists"]))

while channel.has_more_playlists():
    channel.next()
    print(len(channel.result["playlists"]))
```

## Result Modes

You can specify the result format using `ResultMode`:

```python
from youtubesearchpython import ResultMode

result = videosSearch.result(mode=ResultMode.json)  # Returns JSON string
result = videosSearch.result(mode=ResultMode.dict)  # Returns dictionary (default)
```

## Timeout

The default timeout is 10 seconds. You can override it by passing a `timeout` parameter (in seconds) to class constructors:

```python
videosSearch = VideosSearch('query', limit=10, timeout=30)
```

## See Also

- [Main README](../../README.md) - Installation, async API examples, and project information
- [Asynchronous API Documentation](../async/README.md) - Complete guide to the asynchronous API

