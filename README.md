# 🔎 youtube-search-python

**Search YouTube videos, channels, and playlists — without using the YouTube Data API v3.**

[![PyPI - Version](https://img.shields.io/pypi/v/youtube-search-python?style=for-the-badge)](https://pypi.org/project/youtube-search-python)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/youtube-search-python?label=DOWNLOADS&style=for-the-badge)](https://pypi.org/project/youtube-search-python)
[![Python](https://img.shields.io/pypi/pyversions/youtube-search-python?style=for-the-badge)](https://www.python.org/downloads/)

> **⚠️ Note:** The original project by [Hitesh Kumar Saini](https://github.com/alexmercerind) has not been maintained since **June 23, 2022**.  
> This is an **actively maintained fork** by [CertifiedCoders](https://github.com/CertifiedCoders) with modern Python support (3.7–3.13) and continued updates.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Search** | Videos, channels, playlists, and custom searches with filters |
| 📹 **Video Information** | Get video details, formats, thumbnails, and metadata |
| 📝 **Comments** | Retrieve video comments with pagination support |
| 📄 **Transcripts** | Access video transcripts in multiple languages |
| 🎬 **Playlists** | Full playlist support with pagination |
| 📺 **Channels** | Channel information and playlist retrieval |
| 🔗 **Stream URLs** | Direct stream URL fetching (requires yt-dlp) |
| ⚡ **Async Support** | High-performance asynchronous API |
| 🎯 **No API Key** | Works without YouTube Data API v3 |

---

## 📦 Installation

### Quick Install

```bash
pip install git+https://github.com/CertifiedCoders/youtube-search-python.git
```

### Install from Dev Branch

```bash
pip install git+https://github.com/CertifiedCoders/youtube-search-python.git@dev
```

### Install from Source

```bash
git clone https://github.com/CertifiedCoders/youtube-search-python.git
cd youtube-search-python
pip install -e .
```

### Requirements

- **Python:** 3.7–3.13
- **httpx:** >= 0.28.1 (installed automatically)

> **💡 Tip:** Default timeout is 10 seconds. Override by passing `timeout` parameter (in seconds) to class constructors.

---

## 🚀 Quick Start

### Synchronous API

```python
from youtubesearchpython import VideosSearch

videosSearch = VideosSearch('NoCopyrightSounds', limit=2)
print(videosSearch.result())
```

### Asynchronous API

```python
from youtubesearchpython.aio import VideosSearch
import asyncio

async def main():
    videosSearch = VideosSearch('NoCopyrightSounds', limit=2)
    result = await videosSearch.next()
    print(result)

asyncio.run(main())
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[📘 Synchronous API](docs/sync/README.md)** | Complete guide to the synchronous API with examples |
| **[⚡ Asynchronous API](docs/async/README.md)** | Complete guide to the asynchronous API with examples |
| **[💻 Sync Examples](docs/examples/syncExample.py)** | Comprehensive synchronous examples |
| **[💻 Async Examples](docs/examples/asyncExample.py)** | Comprehensive asynchronous examples |

---

## 🎯 Choose Your Path

### For Beginners

Start with the **[Synchronous API](docs/sync/README.md)** — it's straightforward and blocking, perfect for simple scripts and learning.

### For Advanced Users

Use the **[Asynchronous API](docs/async/README.md)** for high-performance applications, web servers, and concurrent operations.

---

## 📖 Common Use Cases

<details>
<summary><b>🔍 Search for Videos</b></summary>

**Sync:**
```python
from youtubesearchpython import VideosSearch

videosSearch = VideosSearch('NoCopyrightSounds', limit=10)
print(videosSearch.result())
```

**Async:**
```python
from youtubesearchpython.aio import VideosSearch
import asyncio

async def main():
    videosSearch = VideosSearch('NoCopyrightSounds', limit=10)
    result = await videosSearch.next()
    print(result)

asyncio.run(main())
```
</details>

<details>
<summary><b>📹 Get Video Information</b></summary>

**Sync:**
```python
from youtubesearchpython import Video

video = Video.get('https://www.youtube.com/watch?v=z0GKGpObgPY')
print(video)
```

**Async:**
```python
from youtubesearchpython.aio import Video
import asyncio

async def main():
    video = await Video.get('https://www.youtube.com/watch?v=z0GKGpObgPY')
    print(video)

asyncio.run(main())
```
</details>

<details>
<summary><b>🎬 Work with Playlists</b></summary>

**Sync:**
```python
from youtubesearchpython import Playlist

playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
print(f'Videos Retrieved: {len(playlist.videos)}')

while playlist.hasMoreVideos:
    playlist.getNextVideos()
    print(f'Videos Retrieved: {len(playlist.videos)}')
```

**Async:**
```python
from youtubesearchpython.aio import Playlist
import asyncio

async def main():
    playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    await playlist.init()
    
    while playlist.hasMoreVideos:
        await playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')

asyncio.run(main())
```
</details>

---

## ⚠️ Important Notes

> **Legal Notice:** YouTube's Terms of Service may restrict commercial use. Please respect the law and YouTube's terms when using this library.

> **Technical Details:** This library simulates the requests made by YouTube's web client during client-side rendering. It fetches the JSON data internally used by YouTube when navigating the website, not webpage HTML.

---

## 🤝 Contributors

Thanks to everyone contributing to this library, including those not mentioned here.

### Current Maintainer

- **[CertifiedCoders](https://github.com/CertifiedCoders)** - Current fork maintainer, actively maintaining the project with modern Python support and bug fixes

### Original Project Contributors

- **[Hitesh Kumar Saini](https://github.com/alexmercerind)** - Original creator
- **[mytja](https://github.com/mytja)** - Core classes, Comments and Transcript classes, yt-dlp migration
- **[Denis (raitonoberu)](https://github.com/raitonoberu)** - Hashtag class, maintainer and reviewer
- **[Fabian Wunsch (fabi321)](https://github.com/fabi321)** - ChannelSearch & Playlist fixes
- **[Felix Stupp (Zocker1999NET)](https://github.com/Zocker1999NET)** - Video and Playlist class contributor
- **[dscrofts](https://github.com/dscrofts)** - Extensive issues, mostly about Playlist and Video class
- **[AlexandreOuellet](https://github.com/AlexandreOuellet)** - Added publishDate and uploadDate to Video class
- **[rking32](https://github.com/rking32)** - Bumped httpx version to 0.14.2
- **[Elter (Maple-Elter)](https://github.com/Maple-Elter)** - Fixes to Playlist class

Contributors are listed in no particular order. We appreciate all contributions, reports, and feedback.

##

## 📝 Recent Updates

**Version 1.7.0** includes:

- Renamed async module from `__future__` to `aio` for cleaner, clearer, and more intuitive async imports
- Robust YouTube URL cleaning and video ID extraction supporting watch, shorts, live, youtu.be, and playlist formats
- Centralized utility formatters for view counts, durations, publish time, and channel metadata with consistent outputs
- Major refactors in video data retrieval to reduce duplication and unify sync/async logic for better performance
- Improved client architecture with ANDROID as the default and stronger MWEB fallback handling
- Enhanced stream URL fetching with duplicate format prevention and improved compatibility with YouTube API changes
- Cleaner project structure and documentation with consolidated examples and updated installation/upgrade guidance

##

## 📄 License

MIT License

Copyright (c) 2021 [Hitesh Kumar Saini](https://github.com/alexmercerind)  
Copyright (c) 2022-2025 [CertifiedCoders](https://github.com/CertifiedCoders) (Fork maintainer)

##

## 🔗 Links

- **[GitHub Repository](https://github.com/CertifiedCoders/youtube-search-python)**
- **[PyPI Package](https://pypi.org/project/youtube-search-python)**
