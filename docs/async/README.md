# ⚡ Asynchronous API Documentation

Complete guide to the asynchronous API for `youtube-search-python`. For installation, project overview, and general information, see the [main README](../../README.md).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Import](#import)
- [Basic Usage](#basic-usage)
- [Advanced Usage](#advanced-usage)
- [Timeout Configuration](#timeout-configuration)
- [Key Differences from Sync API](#key-differences-from-sync-api)
- [Examples](#examples)

---

## 🎯 Overview

The async API provides **non-blocking, high-performance** access to YouTube search and data retrieval. All async methods must be called with `await` and should be used within async functions.

**Best for:**
- Web servers and APIs
- High-performance applications
- Concurrent operations
- Background tasks

---

## 📥 Import

```python
from youtubesearchpython.aio import VideosSearch, ChannelsSearch, PlaylistsSearch, Search, CustomSearch, ChannelSearch
from youtubesearchpython.aio import Video, Playlist, Channel, Comments, Transcript, Hashtag, Suggestions
from youtubesearchpython.aio import StreamURLFetcher, playlist_from_channel_id
```

---

## 🚀 Basic Usage

### Search for Videos

```python
from youtubesearchpython.aio import VideosSearch
import asyncio

async def main():
    videosSearch = VideosSearch('NoCopyrightSounds', limit=2)
    result = await videosSearch.next()
    print(result)

asyncio.run(main())
```

### Search for Channels

```python
from youtubesearchpython.aio import ChannelsSearch
import asyncio

async def main():
    channelsSearch = ChannelsSearch('NoCopyrightSounds', limit=10, region='US')
    result = await channelsSearch.next()
    print(result)

asyncio.run(main())
```

### Search for Playlists

```python
from youtubesearchpython.aio import PlaylistsSearch
import asyncio

async def main():
    playlistsSearch = PlaylistsSearch('NoCopyrightSounds', limit=1)
    result = await playlistsSearch.next()
    print(result)

asyncio.run(main())
```

### Search with Filters

```python
from youtubesearchpython.aio import CustomSearch, VideoSortOrder
import asyncio

async def main():
    customSearch = CustomSearch('NoCopyrightSounds', VideoSortOrder.uploadDate, limit=1)
    result = await customSearch.next()
    print(result)

asyncio.run(main())
```

### Search for Everything

```python
from youtubesearchpython.aio import Search
import asyncio

async def main():
    search = Search('NoCopyrightSounds', limit=1)
    result = await search.next()
    print(result)

asyncio.run(main())
```

> **💡 Tip:** The `type` key in the result can be used to differentiate between videos, channels, and playlists.

---

## 🎓 Advanced Usage

### Getting Next Page Results

```python
from youtubesearchpython.aio import VideosSearch
import asyncio

async def main():
    search = VideosSearch('NoCopyrightSounds')
    
    result = await search.next()
    print(result['result'])
    
    result = await search.next()
    print(result['result'])

asyncio.run(main())
```

### Getting Video Information

```python
from youtubesearchpython.aio import Video
import asyncio

async def main():
    video = await Video.get('https://www.youtube.com/watch?v=z0GKGpObgPY')
    print(video)
    
    videoInfo = await Video.getInfo('https://youtu.be/z0GKGpObgPY')
    print(videoInfo)
    
    videoFormats = await Video.getFormats('z0GKGpObgPY')
    print(videoFormats)

asyncio.run(main())
```

> **💡 Note:** 
> - `Video.get()` returns both information and formats
> - `Video.getInfo()` returns only information
> - `Video.getFormats()` returns only formats
> - You can pass either a link or video ID
> - Use `get_upload_date=True` to enable HTML parsing for upload date (slower but more complete)

### Working with Playlists

```python
from youtubesearchpython.aio import Playlist
import asyncio

async def main():
    playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    await playlist.init()
    
    print(f'Videos Retrieved: {len(playlist.videos)}')
    
    while playlist.hasMoreVideos:
        print('Getting more videos...')
        await playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')
    
    print('Found all the videos.')

asyncio.run(main())
```

#### Alternative: Using Static Methods

```python
from youtubesearchpython.aio import Playlist
import asyncio

async def main():
    playlist = await Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlist)
    
    playlistInfo = await Playlist.getInfo('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlistInfo)
    
    playlistVideos = await Playlist.getVideos('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlistVideos)

asyncio.run(main())
```

### Get All Videos of a Channel

```python
from youtubesearchpython.aio import Playlist, playlist_from_channel_id
import asyncio

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

asyncio.run(main())
```

### Getting Search Suggestions

```python
from youtubesearchpython.aio import Suggestions
import asyncio

async def main():
    suggestions = await Suggestions.get('NoCopyrightSounds', language='en', region='US')
    print(suggestions)

asyncio.run(main())
```

### Getting Videos by Hashtag

```python
from youtubesearchpython.aio import Hashtag
import asyncio

async def main():
    hashtag = Hashtag('ncs', limit=1)
    result = await hashtag.next()
    print(result)

asyncio.run(main())
```

### Getting Direct Stream URLs

> **⚠️ Requires:** `yt-dlp` to be installed (`pip install yt-dlp`)

```python
from youtubesearchpython.aio import StreamURLFetcher, Video
import asyncio

async def main():
    fetcher = StreamURLFetcher()
    await fetcher.getJavaScript()
    
    video = await Video.get("https://www.youtube.com/watch?v=aqz-KE-bpKQ")
    url = await fetcher.get(video, 251)
    print(url)
    
    all_urls = await fetcher.getAll(video)
    print(all_urls)

asyncio.run(main())
```

> **💡 Note:** 
> - `StreamURLFetcher` can fetch direct video URLs without additional network requests
> - Avoid instantiating `StreamURLFetcher` more than once (create a global instance)
> - `get()` returns a URL for a specific format
> - `getAll()` returns all stream URLs in a dictionary

### Getting Comments

```python
from youtubesearchpython.aio import Comments
import asyncio

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

asyncio.run(main())
```

> **💡 Note:** `getNextComments()` can also be called without `init()` — it will initialize automatically on first call.

#### Get First 20 Comments (Quick Access)

```python
from youtubesearchpython.aio import Comments
import asyncio

async def main():
    video_id = "_ZdsmLgCVdU"
    comments = await Comments.get(video_id)
    print(comments)

asyncio.run(main())
```

### Retrieve Video Transcript

```python
from youtubesearchpython.aio import Transcript
import asyncio

async def main():
    transcript = await Transcript.get("https://www.youtube.com/watch?v=-1xu0IP35FI")
    print(transcript)
    
    transcript_es = await Transcript.get(
        "https://www.youtube.com/watch?v=-1xu0IP35FI",
        transcript["languages"][-1]["params"]
    )
    print(transcript_es)

asyncio.run(main())
```

### Retrieve Channel Info

```python
from youtubesearchpython.aio import Channel
import asyncio

async def main():
    channel = await Channel.get("UC_aEa8K-EOJ3D6gOs7HcyNg")
    print(channel)

asyncio.run(main())
```

### Retrieve Channel Playlists

```python
from youtubesearchpython.aio import Channel
import asyncio

async def main():
    channel = Channel("UC_aEa8K-EOJ3D6gOs7HcyNg")
    await channel.init()
    print(len(channel.result["playlists"]))
    
    while channel.has_more_playlists():
        await channel.next()
        print(len(channel.result["playlists"]))

asyncio.run(main())
```

### Channel Search

```python
from youtubesearchpython.aio import ChannelSearch
import asyncio

async def main():
    search = ChannelSearch('Watermelon Sugar', "UCZFWPqqPkFlNwIxcpsLOwew")
    result = await search.next()
    print(result)

asyncio.run(main())
```

---

## ⏱️ Timeout Configuration

The default timeout is **10 seconds**. You can override it by passing a `timeout` parameter (in seconds) to class constructors:

```python
videosSearch = VideosSearch('query', limit=10, timeout=30)
```

---

## 🔄 Key Differences from Sync API

| Feature | Sync API | Async API |
|---------|----------|-----------|
| **Getting results** | `search.result()` | `await search.next()` |
| **Return value** | Dictionary | Dictionary (direct) |
| **Initialization** | Automatic | `await playlist.init()` or `await channel.init()` |
| **Comments init** | Automatic | `await comments.init()` or auto-init on first `getNextComments()` |
| **All methods** | Synchronous | Must use `await` |

---

## 💻 Examples

For comprehensive examples covering all features, see:

- **[Async Examples](../examples/asyncExample.py)** — Complete async examples file

---

## 🔗 See Also

- **[Main README](../../README.md)** — Installation, sync API examples, and project information
- **[Synchronous API Documentation](../sync/README.md)** — Complete guide to the synchronous API
