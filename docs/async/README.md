# Asynchronous API Documentation

This document covers the asynchronous API for `youtube-search-python`. For installation, project overview, and general information, see the [main README](../../README.md).

## Overview

The async API provides non-blocking, high-performance access to YouTube search and data retrieval. All async methods must be called with `await` and should be used within async functions.

## Import

```python
from youtubesearchpython.aio import VideosSearch, ChannelsSearch, PlaylistsSearch, Search, CustomSearch, ChannelSearch
from youtubesearchpython.aio import Video, Playlist, Channel, Comments, Transcript, Hashtag, Suggestions
from youtubesearchpython.aio import StreamURLFetcher, playlist_from_channel_id
```

## Basic Usage

### Search for videos

```python
from youtubesearchpython.aio import VideosSearch

async def main():
    videosSearch = VideosSearch('NoCopyrightSounds', limit=2)
    result = await videosSearch.next()
    print(result)

import asyncio
asyncio.run(main())
```

### Search for channels

```python
from youtubesearchpython.aio import ChannelsSearch

async def main():
    channelsSearch = ChannelsSearch('NoCopyrightSounds', limit=10, region='US')
    result = await channelsSearch.next()
    print(result)

import asyncio
asyncio.run(main())
```

### Search for playlists

```python
from youtubesearchpython.aio import PlaylistsSearch

async def main():
    playlistsSearch = PlaylistsSearch('NoCopyrightSounds', limit=1)
    result = await playlistsSearch.next()
    print(result)

import asyncio
asyncio.run(main())
```

### Search with filters

```python
from youtubesearchpython.aio import CustomSearch, VideoSortOrder

async def main():
    customSearch = CustomSearch('NoCopyrightSounds', VideoSortOrder.uploadDate, limit=1)
    result = await customSearch.next()
    print(result)

import asyncio
asyncio.run(main())
```

### Search for everything

```python
from youtubesearchpython.aio import Search

async def main():
    search = Search('NoCopyrightSounds', limit=1)
    result = await search.next()
    print(result)

import asyncio
asyncio.run(main())
```

## Advanced Usage

### Getting next page results

```python
from youtubesearchpython.aio import VideosSearch

async def main():
    search = VideosSearch('NoCopyrightSounds')
    result = await search.next()
    print(result['result'])
    
    result = await search.next()
    print(result['result'])

import asyncio
asyncio.run(main())
```

### Getting video information

```python
from youtubesearchpython.aio import Video

async def main():
    video = await Video.get('https://www.youtube.com/watch?v=z0GKGpObgPY')
    print(video)
    
    videoInfo = await Video.getInfo('https://youtu.be/z0GKGpObgPY')
    print(videoInfo)
    
    videoFormats = await Video.getFormats('z0GKGpObgPY')
    print(videoFormats)

import asyncio
asyncio.run(main())
```

### Working with playlists

```python
from youtubesearchpython.aio import Playlist

async def main():
    playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    await playlist.init()
    
    print(f'Videos Retrieved: {len(playlist.videos)}')
    
    while playlist.hasMoreVideos:
        print('Getting more videos...')
        await playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')
    
    print('Found all the videos.')

import asyncio
asyncio.run(main())
```

### Get all videos of a channel

```python
from youtubesearchpython.aio import Playlist, playlist_from_channel_id

async def main():
    channel_id = "UC_aEa8K-EOJ3D6gOs7HcyNg"
    playlist = Playlist(playlist_from_channel_id(channel_id))
    await playlist.init()
    
    print(f'Videos Retrieved: {len(playlist.videos)}')
    
    while playlist.hasMoreVideos:
        print('Getting more videos...')
        await playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')
    
    print('Found all the videos.')

import asyncio
asyncio.run(main())
```

### Getting search suggestions

```python
from youtubesearchpython.aio import Suggestions

async def main():
    suggestions = await Suggestions.get('NoCopyrightSounds', language='en', region='US')
    print(suggestions)

import asyncio
asyncio.run(main())
```

### Getting videos by hashtag

```python
from youtubesearchpython.aio import Hashtag

async def main():
    hashtag = Hashtag('ncs', limit=1)
    result = await hashtag.next()
    print(result)

import asyncio
asyncio.run(main())
```

### Getting direct stream URLs

Requires `yt-dlp` to be installed: `pip install yt-dlp`

```python
from youtubesearchpython.aio import StreamURLFetcher, Video

async def main():
    fetcher = StreamURLFetcher()
    await fetcher.getJavaScript()
    
    video = await Video.get("https://www.youtube.com/watch?v=aqz-KE-bpKQ")
    url = await fetcher.get(video, 251)
    print(url)
    
    all_urls = await fetcher.getAll(video)
    print(all_urls)

import asyncio
asyncio.run(main())
```

### Getting comments

```python
from youtubesearchpython.aio import Comments

async def main():
    video_id = "_ZdsmLgCVdU"
    comments = Comments(video_id)
    await comments.init()
    
    print(f'Comments Retrieved: {len(comments.comments["result"])}')
    
    while comments.hasMoreComments:
        print('Getting more comments...')
        await comments.getNextComments()
        print(f'Comments Retrieved: {len(comments.comments["result"])}')
    
    print('Found all the comments.')

import asyncio
asyncio.run(main())
```

**Note:** `getNextComments()` can also be called without `init()` - it will initialize automatically on first call.

### Get first 20 comments

```python
from youtubesearchpython.aio import Comments

async def main():
    video_id = "_ZdsmLgCVdU"
    comments = await Comments.get(video_id)
    print(comments)

import asyncio
asyncio.run(main())
```

### Retrieve video transcript

```python
from youtubesearchpython.aio import Transcript

async def main():
    transcript = await Transcript.get("https://www.youtube.com/watch?v=-1xu0IP35FI")
    print(transcript)
    
    transcript_es = await Transcript.get(
        "https://www.youtube.com/watch?v=-1xu0IP35FI",
        transcript["languages"][-1]["params"]
    )
    print(transcript_es)

import asyncio
asyncio.run(main())
```

### Retrieve channel info

```python
from youtubesearchpython.aio import Channel

async def main():
    channel = await Channel.get("UC_aEa8K-EOJ3D6gOs7HcyNg")
    print(channel)

import asyncio
asyncio.run(main())
```

### Retrieve channel playlists

```python
from youtubesearchpython.aio import Channel

async def main():
    channel = Channel("UC_aEa8K-EOJ3D6gOs7HcyNg")
    await channel.init()
    print(len(channel.result["playlists"]))
    
    while channel.has_more_playlists():
        await channel.next()
        print(len(channel.result["playlists"]))

import asyncio
asyncio.run(main())
```

### Channel search

```python
from youtubesearchpython.aio import ChannelSearch

async def main():
    search = ChannelSearch('Watermelon Sugar', "UCZFWPqqPkFlNwIxcpsLOwew")
    result = await search.next()
    print(result)

import asyncio
asyncio.run(main())
```

## Timeout

The default timeout is 10 seconds. You can override it by passing a `timeout` parameter (in seconds) to class constructors:

```python
videosSearch = VideosSearch('query', limit=10, timeout=30)
```

## Key Differences from Sync API

- Use `await search.next()` instead of `search.result()` to get results
- `next()` returns the result dictionary directly (not a boolean)
- All async methods must be called with `await`
- Use `await playlist.init()` or `await channel.init()` for initialization
- Use `await comments.init()` before accessing comments (or call `getNextComments()` which initializes automatically)

## See Also

- [Main README](../../README.md) - Installation, sync API examples, and project information
- [Synchronous API Documentation](../sync/README.md) - Complete guide to the synchronous API

