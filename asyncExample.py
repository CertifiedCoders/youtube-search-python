from youtubesearchpython.aio import (
    VideosSearch, ChannelsSearch, PlaylistsSearch, Search, CustomSearch, ChannelSearch,
    Video, Playlist, Channel, Comments, Transcript, Hashtag, Suggestions,
    StreamURLFetcher, playlist_from_channel_id, VideoSortOrder
)
import asyncio

async def main():
    # Search examples
    search = Search('NoCopyrightSounds', limit=1, language='en', region='US')
    result = await search.next()
    print(result)

    videosSearch = VideosSearch('NoCopyrightSounds', limit=10, language='en', region='US')
    videosResult = await videosSearch.next()
    print(videosResult)

    channelsSearch = ChannelsSearch('NoCopyrightSounds', limit=1, language='en', region='US')
    channelsResult = await channelsSearch.next()
    print(channelsResult)

    playlistsSearch = PlaylistsSearch('NoCopyrightSounds', limit=1, language='en', region='US')
    playlistsResult = await playlistsSearch.next()
    print(playlistsResult)

    customSearch = CustomSearch('NoCopyrightSounds', VideoSortOrder.uploadDate, language='en', region='US')
    customResult = await customSearch.next()
    print(customResult)

    channelSearch = ChannelSearch('Watermelon Sugar', "UCZFWPqqPkFlNwIxcpsLOwew")
    result = await channelSearch.next()
    print(result)

    # Pagination example
    search = VideosSearch('NoCopyrightSounds')
    index = 0
    result = await search.next()
    for video in result['result']:
        index += 1
        print(f'{index} - {video["title"]}')
    result = await search.next()
    for video in result['result']:
        index += 1
        print(f'{index} - {video["title"]}')

    # Video examples
    video = await Video.get('https://www.youtube.com/watch?v=z0GKGpObgPY', get_upload_date=True)
    print(video)
    videoInfo = await Video.getInfo('https://youtu.be/z0GKGpObgPY')
    print(videoInfo)
    videoFormats = await Video.getFormats('z0GKGpObgPY')
    print(videoFormats)

    # Playlist examples
    playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    await playlist.init()
    while playlist.hasMoreVideos:
        print('Getting more videos...')
        await playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')
    print('Found all the videos.')

    playlist = await Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlist)
    playlistInfo = await Playlist.getInfo('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlistInfo)
    playlistVideos = await Playlist.getVideos('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlistVideos)

    # Channel examples
    channel = await Channel.get("UC_aEa8K-EOJ3D6gOs7HcyNg")
    print(channel)

    channel = Channel("UC_aEa8K-EOJ3D6gOs7HcyNg")
    await channel.init()
    print(len(channel.result["playlists"]))
    while channel.has_more_playlists():
        await channel.next()
        print(len(channel.result["playlists"]))

    # Get all videos of a channel
    channel_id = "UC_aEa8K-EOJ3D6gOs7HcyNg"
    playlist = Playlist(playlist_from_channel_id(channel_id))
    await playlist.init()
    print(f'Videos Retrieved: {len(playlist.videos)}')
    while playlist.hasMoreVideos:
        print('Getting more videos...')
        await playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')
    print('Found all the videos.')

    # Comments examples
    comments = Comments("_ZdsmLgCVdU")
    await comments.init()
    print(f'Comments Retrieved: {len(comments.comments["result"])}')
    while comments.hasMoreComments:
        print('Getting more comments...')
        await comments.getNextComments()
        print(f'Comments Retrieved: {len(comments.comments["result"])}')
    print('Found all the comments.')

    # Transcript examples
    transcript = await Transcript.get("https://www.youtube.com/watch?v=L7kF4MXXCoA")
    print(transcript)

    url = "https://www.youtube.com/watch?v=-1xu0IP35FI"
    transcript_en = await Transcript.get(url)
    transcript_es = await Transcript.get(url, transcript_en["languages"][-1]["params"])
    print(transcript_es)

    # Suggestions and hashtags
    suggestions = await Suggestions.get('NoCopyrightSounds', language='en', region='US')
    print(suggestions)

    hashtag = Hashtag('ncs', limit=1)
    result = await hashtag.next()
    print(result)

    # Stream URL fetcher (requires yt-dlp)
    fetcher = StreamURLFetcher()
    await fetcher.getJavaScript()
    videoA = await Video.get("https://www.youtube.com/watch?v=aqz-KE-bpKQ")
    videoB = await Video.get("https://www.youtube.com/watch?v=ZwNxYJfW-eU")
    singleUrlA = await fetcher.get(videoA, 22)
    allUrlsB = await fetcher.getAll(videoB)
    print(singleUrlA)
    print(allUrlsB)

if __name__ == '__main__':
    asyncio.run(main())
