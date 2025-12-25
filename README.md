# youtube-search-python

#### 🔎 Search YouTube videos, channels, and playlists — without using the YouTube Data API v3.

**Version:** 1.6.10 | **Python:** 3.7–3.13 | **Maintainer:** [CertifiedCoders](https://github.com/CertifiedCoders)

[![PyPI - Version](https://img.shields.io/pypi/v/youtube-search-python?style=for-the-badge)](https://pypi.org/project/youtube-search-python)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/youtube-search-python?label=DOWNLOADS&style=for-the-badge)](https://pypi.org/project/youtube-search-python)
[![Install via GitHub](https://img.shields.io/badge/install-gitHub-blue?style=for-the-badge&logo=github)](https://github.com/CertifiedCoders/youtube-search-python)

> ⚠️ **Note:** The original project by [Hitesh Kumar Saini](https://github.com/alexmercerind) has not been maintained since **June 23, 2022**.  
> This is an **actively maintained fork** by [CertifiedCoders](https://github.com/CertifiedCoders) with modern Python support and continued updates.

---

## ✨ Features

- 🔍 **Search** - Videos, channels, playlists, and custom searches with filters
- 📹 **Video Information** - Get video details, formats, thumbnails, and metadata
- 📝 **Comments** - Retrieve video comments with pagination support
- 📄 **Transcripts** - Access video transcripts in multiple languages
- 🎬 **Playlists** - Full playlist support with pagination
- 📺 **Channels** - Channel information and playlist retrieval
- 🔗 **Stream URLs** - Direct stream URL fetching (requires yt-dlp)
- ⚡ **Async Support** - High-performance asynchronous API
- 🎯 **No API Key Required** - Works without YouTube Data API v3

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

- Python 3.7–3.13
- httpx >= 0.28.1 (installed automatically)

**Note:** Default timeout is 10 seconds. Override by passing `timeout` parameter (in seconds) to class constructors.

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

- **[Synchronous API](docs/sync/README.md)** - Complete guide to the synchronous API
- **[Asynchronous API](docs/async/README.md)** - Complete guide to the asynchronous API
- **[Examples](syncExample.py)** - Synchronous examples
- **[Async Examples](asyncExample.py)** - Asynchronous examples

---

## Contributors

Thanks to everyone contributing to this library, including those not mentioned here.

### Current Maintainer

- **[CertifiedCoders](https://github.com/CertifiedCoders)** - Current fork maintainer, actively maintaining the project with modern Python support and bug fixes

### Original Project Contributors

- **[Hitesh Kumar Saini](https://github.com/alexmercerind)** - Original creator of this library, contributed most classes to this library
- **[mytja](https://github.com/mytja)** - Author of Core classes, Comments and Transcript classes, yt-dlp migration
- **[Denis (raitonoberu)](https://github.com/raitonoberu)** - Author of Hashtag class, maintainer and reviewer of PRs
- **[Fabian Wunsch (fabi321)](https://github.com/fabi321)** - Fixes to ChannelSearch & retrieving Playlists from Channel class
- **[Felix Stupp (Zocker1999NET)](https://github.com/Zocker1999NET)** - Video and Playlist class contributor, extensive issues
- **[dscrofts](https://github.com/dscrofts)** - Extensive issues, mostly about Playlist and Video class
- **[AlexandreOuellet](https://github.com/AlexandreOuellet)** - Added publishDate and uploadDate to Video class
- **[rking32](https://github.com/rking32)** - Bumped httpx version to 0.14.2
- **[Elter (Maple-Elter)](https://github.com/Maple-Elter)** - Fixes to Playlist class

Contributors are listed in no particular order. We appreciate all contributions, reports, and feedback that help make this library better.

---

## License

MIT License

Copyright (c) 2021 [Hitesh Kumar Saini](https://github.com/alexmercerind)  
Copyright (c) 2022-2024 [CertifiedCoders](https://github.com/CertifiedCoders) (Fork maintainer)

---

## ℹ️ About

This library simulates the requests made by YouTube's web client during client-side rendering. It fetches the JSON data internally used by YouTube when navigating the website, not webpage HTML.

**Important:** YouTube's Terms of Service may restrict commercial use. Please respect the law and YouTube's terms.

### Recent Updates

**Version 1.6.10** includes:
- Renamed async module from `__future__` to `aio` for cleaner imports
- ANDROID client as default for better compatibility
- Enhanced thumbnail handling and optimization
- Improved error handling and stream URL fetching
- Updated client versions and URL cleaning

For full changelog, see the [repository commits](https://github.com/CertifiedCoders/youtube-search-python/commits/dev).

### Credits

- **Original Author:** [Hitesh Kumar Saini](https://github.com/alexmercerind)
- **Fork Maintainer:** [CertifiedCoders](https://github.com/CertifiedCoders)
