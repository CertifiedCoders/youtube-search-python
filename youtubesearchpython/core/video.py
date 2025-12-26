import copy
import json
from typing import Union, List, Optional
from urllib.parse import urlencode
import httpx

from youtubesearchpython.core.constants import *
from youtubesearchpython.core.requests import RequestCore
from youtubesearchpython.core.componenthandler import getValue, getVideoId
from youtubesearchpython.core.exceptions import YouTubeRequestError, YouTubeParseError
from youtubesearchpython.core.utils import (
    get_cleaned_url,
    format_view_count,
    format_duration,
    format_published_time
)


CLIENTS = {
    "MWEB": {
        "context": {
            "client": {"clientName": "MWEB", "clientVersion": "2.20240425.01.00"}
        },
        "api_key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
    },
    "WEB": {
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20210224.06.00',
                'newVisitorCookie': True
            },
            'user': {
                'lockedSafetyMode': False
            }
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
    },
    "ANDROID": {
        "context": {"client": {"clientName": "ANDROID", "clientVersion": "19.02.39"}},
        "api_key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
    },
    "ANDROID_EMBED": {
        "context": {
            "client": {
                "clientName": "ANDROID",
                "clientVersion": "19.02.39",
                "clientScreen": "EMBED",
            }
        },
        "api_key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
    },
    "TV_EMBED": {
        "context": {
            "client": {
                "clientName": "TVHTML5_SIMPLY_EMBEDDED_PLAYER",
                "clientVersion": "2.0",
            },
            "thirdParty": {
                "embedUrl": "https://www.youtube.com/",
            },
        },
        "api_key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
    },
}


class VideoCore(RequestCore):
    def __init__(self, videoLink: str, componentMode: str, resultMode: int, timeout: Optional[int], enableHTML: bool, overridedClient: str = "ANDROID"):
        super().__init__(timeout=timeout)
        self.timeout = timeout
        self.resultMode = resultMode
        self.componentMode = componentMode
        self.videoLink = get_cleaned_url(videoLink)
        self.enableHTML = enableHTML
        self.overridedClient = overridedClient
    
    # We call this when we use only HTML
    def post_request_only_html_processing(self):
        self.__getVideoComponent(self.componentMode)
        self.result = self.__videoComponent

    def post_request_processing(self):
        self.__parseSource()
        self.__getVideoComponent(self.componentMode)
        self.result = self.__videoComponent

    async def async_post_request_processing(self):
        self.__parseSource()
        await self.__getVideoComponentAsync(self.componentMode)
        self.result = self.__videoComponent

    def prepare_innertube_request(self):
        self.url = 'https://www.youtube.com/youtubei/v1/player' + "?" + urlencode({
            'key': searchKey,
            'contentCheckOk': True,
            'racyCheckOk': True,
            "videoId": getVideoId(self.videoLink)
        })
        self.data = copy.deepcopy(CLIENTS[self.overridedClient])

    async def async_create(self):
        self.prepare_innertube_request()
        response = await self.asyncPostRequest()
        if response is None:
            video_link = getattr(self, "videoLink", None)
            request_params = getattr(self, "innertube_request", None)
            raise YouTubeRequestError(
                f"The request returned an empty response. "
                f"Video link: {video_link}, Request parameters: {request_params}"
            )

        self.response = response.text
        if response.status_code == 200:
            await self.async_post_request_processing()
        else:
            raise YouTubeRequestError(f"Invalid status code {response.status_code} for video {self.videoLink}")

    def sync_create(self):
        self.prepare_innertube_request()
        response = self.syncPostRequest()
        self.response = response.text
        if response.status_code == 200:
            self.post_request_processing()
        else:
            try:
                # Get full error response for debugging
                error_msg = response.text if hasattr(response, 'text') and response.text else 'No response text available'
                # Try to parse JSON error for better message
                try:
                    import json
                    error_json = json.loads(error_msg)
                    if 'error' in error_json:
                        error_details = error_json['error']
                        error_msg = f"Code: {error_details.get('code', 'N/A')}, Message: {error_details.get('message', 'N/A')}"
                        if 'errors' in error_details and len(error_details['errors']) > 0:
                            first_error = error_details['errors'][0]
                            error_msg += f", Reason: {first_error.get('reason', 'N/A')}"
                except (json.JSONDecodeError, KeyError, AttributeError):
                    pass
                # Limit to 500 chars for readability
                if len(error_msg) > 500:
                    error_msg = error_msg[:500] + "..."
            except (AttributeError, KeyError):
                error_msg = 'Could not read response text'
            raise YouTubeRequestError(f'Invalid status code {response.status_code} for video {self.videoLink}. Response: {error_msg}')

    def prepare_html_request(self):
        self.url = 'https://www.youtube.com/youtubei/v1/player' + "?" + urlencode({
            'key': searchKey,
            'contentCheckOk': True,
            'racyCheckOk': True,
            "videoId": getVideoId(self.videoLink)
        })
        self.data = CLIENTS["MWEB"]

    def sync_html_create(self):
        self.prepare_html_request()
        response = self.syncPostRequest()
        self.HTMLresponseSource = response.json()

    async def async_html_create(self):
        self.prepare_html_request()
        response = await self.asyncPostRequest()
        self.HTMLresponseSource = response.json()

    def __parseSource(self) -> None:
        try:
            self.responseSource = json.loads(self.response)
        except json.JSONDecodeError as e:
            raise YouTubeParseError(f'Failed to parse JSON response for video {self.videoLink}: {str(e)}')
        except Exception as e:
            raise YouTubeParseError(f'Failed to parse YouTube response: {str(e)}')

    def __result(self, mode: int) -> Union[dict, str]:
        if mode == ResultMode.dict:
            return self.__videoComponent
        elif mode == ResultMode.json:
            return json.dumps(self.__videoComponent, indent=4)

    def __checkThumbnailExists(self, url: str) -> bool:
        try:
            response = httpx.head(url, headers={"User-Agent": userAgent}, timeout=2, follow_redirects=True)
            return response.status_code == 200
        except (httpx.RequestError, httpx.HTTPStatusError, Exception):
            return False

    async def __checkThumbnailExistsAsync(self, url: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(url, headers={"User-Agent": userAgent}, timeout=2, follow_redirects=True)
                return response.status_code == 200
        except (httpx.RequestError, httpx.HTTPStatusError, Exception):
            return False

    def __getBestHq720FromThumbnails(self, thumbnails: List[dict]) -> Union[dict, None]:
        best_thumb = None
        best_resolution = 0
        for thumb in thumbnails:
            url_value = thumb.get('url', '')
            if 'hq720.jpg' in url_value:
                width = thumb.get('width', 0)
                height = thumb.get('height', 0)
                resolution = width * height
                if resolution > best_resolution:
                    best_resolution = resolution
                    full_url = url_value if url_value.startswith('http') else 'https:' + url_value
                    best_thumb = {
                        "url": full_url,
                        "width": width,
                        "height": height
                    }
        return best_thumb

    def __getOptimizedHq720Url(self, video_id: str) -> Union[dict, None]:
        try:
            request_body = copy.deepcopy(requestPayload)
            request_body['query'] = f"https://www.youtube.com/watch?v={video_id}"
            request_body['client'] = {
                'hl': 'en',
                'gl': 'US',
            }
            
            url = 'https://www.youtube.com/youtubei/v1/search' + '?' + urlencode({'key': searchKey})
            response = httpx.post(
                url,
                headers={"User-Agent": userAgent, "Content-Type": "application/json"},
                json=request_body,
                timeout=self.timeout if self.timeout else 5
            )
            
            if response.status_code == 200:
                data = response.json()
                contents = getValue(data, contentPath)
                fallback_contents = getValue(data, fallbackContentPath)
                
                search_contents = contents if contents else fallback_contents
                if search_contents:
                    for item in search_contents:
                        video_data = None
                        if itemSectionKey in item:
                            section_contents = getValue(item, [itemSectionKey, 'contents'])
                            if section_contents:
                                for section_item in section_contents:
                                    if videoElementKey in section_item:
                                        video_data = section_item[videoElementKey]
                                        break
                        elif videoElementKey in item:
                            video_data = item[videoElementKey]
                        
                        if video_data:
                            found_video_id = getValue(video_data, ['videoId'])
                            if found_video_id == video_id:
                                thumbnails = getValue(video_data, ['thumbnail', 'thumbnails'])
                                if thumbnails:
                                    best_thumb = self.__getBestHq720FromThumbnails(thumbnails)
                                    if best_thumb:
                                        return best_thumb
        except Exception:
            pass
        return None

    async def __getOptimizedHq720UrlAsync(self, video_id: str) -> Union[dict, None]:
        try:
            request_body = copy.deepcopy(requestPayload)
            request_body['query'] = f"https://www.youtube.com/watch?v={video_id}"
            request_body['client'] = {
                'hl': 'en',
                'gl': 'US',
            }
            
            url = 'https://www.youtube.com/youtubei/v1/search' + '?' + urlencode({'key': searchKey})
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"User-Agent": userAgent, "Content-Type": "application/json"},
                    json=request_body,
                    timeout=self.timeout if self.timeout else 5
                )
            
            if response.status_code == 200:
                data = response.json()
                contents = getValue(data, contentPath)
                fallback_contents = getValue(data, fallbackContentPath)
                
                search_contents = contents if contents else fallback_contents
                if search_contents:
                    for item in search_contents:
                        video_data = None
                        if itemSectionKey in item:
                            section_contents = getValue(item, [itemSectionKey, 'contents'])
                            if section_contents:
                                for section_item in section_contents:
                                    if videoElementKey in section_item:
                                        video_data = section_item[videoElementKey]
                                        break
                        elif videoElementKey in item:
                            video_data = item[videoElementKey]
                        
                        if video_data:
                            found_video_id = getValue(video_data, ['videoId'])
                            if found_video_id == video_id:
                                thumbnails = getValue(video_data, ['thumbnail', 'thumbnails'])
                                if thumbnails:
                                    best_thumb = self.__getBestHq720FromThumbnails(thumbnails)
                                    if best_thumb:
                                        return best_thumb
        except Exception:
            pass
        return None

    def __enhanceThumbnails(self, thumbnails: List[dict], video_id: str) -> List[dict]:
        if not thumbnails or not video_id:
            return thumbnails
        
        enhanced = list(thumbnails)
        existing_urls = {thumb.get("url", "") for thumb in enhanced if isinstance(thumb, dict)}
        existing_base_urls = {url.split('?')[0] if '?' in url else url for url in existing_urls}
        
        standard_thumbnails = [
            {"url": f"https://i.ytimg.com/vi/{video_id}/default.jpg", "width": 120, "height": 90},
            {"url": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg", "width": 320, "height": 180},
            {"url": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg", "width": 480, "height": 360},
            {"url": f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg", "width": 640, "height": 480},
            {"url": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg", "width": 1920, "height": 1080},
            {"url": f"https://i.ytimg.com/vi/{video_id}/hq720.jpg", "width": 1280, "height": 720},
        ]
        
        for thumb in standard_thumbnails:
            base_url = thumb["url"]
            if base_url not in existing_base_urls:
                if self.__checkThumbnailExists(base_url):
                    enhanced.append(thumb)
        
        optimized_hq720 = self.__getOptimizedHq720Url(video_id)
        if optimized_hq720:
            optimized_url = optimized_hq720["url"]
            if optimized_url not in existing_urls and optimized_url.split('?')[0] not in existing_base_urls:
                enhanced.append(optimized_hq720)
        
        return enhanced

    async def __enhanceThumbnailsAsync(self, thumbnails: List[dict], video_id: str) -> List[dict]:
        if not thumbnails or not video_id:
            return thumbnails
        
        enhanced = list(thumbnails)
        existing_urls = {thumb.get("url", "") for thumb in enhanced if isinstance(thumb, dict)}
        existing_base_urls = {url.split('?')[0] if '?' in url else url for url in existing_urls}
        
        standard_thumbnails = [
            {"url": f"https://i.ytimg.com/vi/{video_id}/default.jpg", "width": 120, "height": 90},
            {"url": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg", "width": 320, "height": 180},
            {"url": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg", "width": 480, "height": 360},
            {"url": f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg", "width": 640, "height": 480},
            {"url": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg", "width": 1920, "height": 1080},
            {"url": f"https://i.ytimg.com/vi/{video_id}/hq720.jpg", "width": 1280, "height": 720},
        ]
        
        for thumb in standard_thumbnails:
            base_url = thumb["url"]
            if base_url not in existing_base_urls:
                if await self.__checkThumbnailExistsAsync(base_url):
                    enhanced.append(thumb)
        
        optimized_hq720 = await self.__getOptimizedHq720UrlAsync(video_id)
        if optimized_hq720:
            optimized_url = optimized_hq720["url"]
            if optimized_url not in existing_urls and optimized_url.split('?')[0] not in existing_base_urls:
                enhanced.append(optimized_hq720)
        
        return enhanced

    def __getVideoComponent(self, mode: str) -> None:
        videoComponent = {}
        if mode in ["getInfo", None]:
            responseSource = getattr(self, "responseSource", None)
            if self.enableHTML:
                responseSource = self.HTMLresponseSource
            raw_view_count = getValue(responseSource, ["videoDetails", "viewCount"])
            raw_duration = getValue(responseSource, ["videoDetails", "lengthSeconds"])
            publish_date = getValue(
                responseSource,
                ["microformat", "playerMicroformatRenderer", "publishDate"],
            )
            
            component = {
                "id": getValue(responseSource, ["videoDetails", "videoId"]),
                "title": getValue(responseSource, ["videoDetails", "title"]),
                "duration": format_duration(raw_duration),
                "viewCount": format_view_count(raw_view_count),
                "thumbnails": getValue(
                    responseSource, ["videoDetails", "thumbnail", "thumbnails"]
                ),
                "description": getValue(
                    responseSource, ["videoDetails", "shortDescription"]
                ),
                "channel": {
                    "name": getValue(responseSource, ["videoDetails", "author"]),
                    "id": getValue(responseSource, ["videoDetails", "channelId"]),
                },
                "allowRatings": getValue(
                    responseSource, ["videoDetails", "allowRatings"]
                ),
                "averageRating": getValue(
                    responseSource, ["videoDetails", "averageRating"]
                ),
                "keywords": getValue(responseSource, ["videoDetails", "keywords"]),
                "isLiveContent": getValue(
                    responseSource, ["videoDetails", "isLiveContent"]
                ),
                "publishDate": publish_date,
                "uploadDate": getValue(
                    responseSource,
                    ["microformat", "playerMicroformatRenderer", "uploadDate"],
                ),
                "isFamilySafe": getValue(
                    responseSource,
                    ["microformat", "playerMicroformatRenderer", "isFamilySafe"],
                ),
                "category": getValue(
                    responseSource,
                    ["microformat", "playerMicroformatRenderer", "category"],
                ),
            }
            
            component["publishedTime"] = format_published_time(publish_date)
            if not component["publishedTime"] and component.get("publishDate"):
                component["publishedTime"] = format_published_time(component["publishDate"])
            
            component["isLiveNow"] = (
                component["isLiveContent"]
                and component["duration"].get("seconds") == 0
            )
            
            if component["id"]:
                component["link"] = "https://www.youtube.com/watch?v=" + component["id"]
            else:
                component["link"] = None
            if component["channel"]["id"]:
                component["channel"]["link"] = (
                    "https://www.youtube.com/channel/" + component["channel"]["id"]
                )
            else:
                component["channel"]["link"] = None
            
            if component.get("thumbnails") and component.get("id"):
                component["thumbnails"] = self.__enhanceThumbnails(component["thumbnails"], component["id"])
            
            videoComponent.update(component)
        if mode in ["getFormats", None]:
            videoComponent.update(
                {"streamingData": getValue(self.responseSource, ["streamingData"])}
            )
        if self.enableHTML:
            videoComponent["publishDate"] = getValue(
                self.HTMLresponseSource,
                ["microformat", "playerMicroformatRenderer", "publishDate"],
            )
            videoComponent["uploadDate"] = getValue(
                self.HTMLresponseSource,
                ["microformat", "playerMicroformatRenderer", "uploadDate"],
            )
        self.__videoComponent = videoComponent

    async def __getVideoComponentAsync(self, mode: str) -> None:
        videoComponent = {}
        if mode in ["getInfo", None]:
            responseSource = getattr(self, "responseSource", None)
            if self.enableHTML:
                responseSource = self.HTMLresponseSource
            raw_view_count = getValue(responseSource, ["videoDetails", "viewCount"])
            raw_duration = getValue(responseSource, ["videoDetails", "lengthSeconds"])
            publish_date = getValue(
                responseSource,
                ["microformat", "playerMicroformatRenderer", "publishDate"],
            )
            
            component = {
                "id": getValue(responseSource, ["videoDetails", "videoId"]),
                "title": getValue(responseSource, ["videoDetails", "title"]),
                "duration": format_duration(raw_duration),
                "viewCount": format_view_count(raw_view_count),
                "thumbnails": getValue(
                    responseSource, ["videoDetails", "thumbnail", "thumbnails"]
                ),
                "description": getValue(
                    responseSource, ["videoDetails", "shortDescription"]
                ),
                "channel": {
                    "name": getValue(responseSource, ["videoDetails", "author"]),
                    "id": getValue(responseSource, ["videoDetails", "channelId"]),
                },
                "allowRatings": getValue(
                    responseSource, ["videoDetails", "allowRatings"]
                ),
                "averageRating": getValue(
                    responseSource, ["videoDetails", "averageRating"]
                ),
                "keywords": getValue(responseSource, ["videoDetails", "keywords"]),
                "isLiveContent": getValue(
                    responseSource, ["videoDetails", "isLiveContent"]
                ),
                "publishDate": publish_date,
                "uploadDate": getValue(
                    responseSource,
                    ["microformat", "playerMicroformatRenderer", "uploadDate"],
                ),
                "isFamilySafe": getValue(
                    responseSource,
                    ["microformat", "playerMicroformatRenderer", "isFamilySafe"],
                ),
                "category": getValue(
                    responseSource,
                    ["microformat", "playerMicroformatRenderer", "category"],
                ),
            }
            
            component["publishedTime"] = format_published_time(publish_date)
            if not component["publishedTime"] and component.get("publishDate"):
                component["publishedTime"] = format_published_time(component["publishDate"])
            
            component["isLiveNow"] = (
                component["isLiveContent"]
                and component["duration"].get("seconds") == 0
            )
            
            if component["id"]:
                component["link"] = "https://www.youtube.com/watch?v=" + component["id"]
            else:
                component["link"] = None
            if component["channel"]["id"]:
                component["channel"]["link"] = (
                    "https://www.youtube.com/channel/" + component["channel"]["id"]
                )
            else:
                component["channel"]["link"] = None
            
            if component.get("thumbnails") and component.get("id"):
                component["thumbnails"] = await self.__enhanceThumbnailsAsync(component["thumbnails"], component["id"])
            
            videoComponent.update(component)
        if mode in ["getFormats", None]:
            videoComponent.update(
                {"streamingData": getValue(self.responseSource, ["streamingData"])}
            )
        if self.enableHTML:
            videoComponent["publishDate"] = getValue(
                self.HTMLresponseSource,
                ["microformat", "playerMicroformatRenderer", "publishDate"],
            )
            videoComponent["uploadDate"] = getValue(
                self.HTMLresponseSource,
                ["microformat", "playerMicroformatRenderer", "uploadDate"],
            )
        self.__videoComponent = videoComponent
