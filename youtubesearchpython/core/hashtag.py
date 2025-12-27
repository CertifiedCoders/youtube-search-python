import copy
import json
from typing import Union, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import httpx

from youtubesearchpython.core.constants import *
from youtubesearchpython.core.componenthandler import ComponentHandler
from youtubesearchpython.core.exceptions import YouTubeRequestError, YouTubeParseError


class HashtagCore(ComponentHandler):
    response = None
    resultComponents = []

    def __init__(self, hashtag: str, limit: int, language: str, region: str, timeout: Optional[int]):
        self.hashtag = hashtag
        self.limit = limit
        self.language = language
        self.region = region
        self.timeout = timeout if timeout is not None else 10
        self.continuationKey = None
        self.params = None

    def sync_create(self):
        self._getParams()
        self._makeRequest()
        self._getComponents()

    def result(self, mode: int = ResultMode.dict) -> Union[str, dict]:
        '''Returns the hashtag videos.
        Args:
            mode (int, optional): Sets the type of result. Defaults to ResultMode.dict.
        Returns:
            Union[str, dict]: Returns JSON or dictionary.
        '''
        if mode == ResultMode.json:
            return json.dumps({'result': self.resultComponents}, indent = 4)
        elif mode == ResultMode.dict:
            return {'result': self.resultComponents}

    def next(self) -> bool:
        '''Gets the videos from the next page. Call result
        Returns:
            bool: Returns True if getting more results was successful.
        '''
        self.response = None
        self.resultComponents = []
        if self.continuationKey:
            self._makeRequest()
            self._getComponents()
        if self.resultComponents:
            return True
        return False

    def _getParams(self) -> None:
        requestBody = copy.deepcopy(requestPayload)
        requestBody['query'] = "#" + self.hashtag
        requestBody['client'] = {
            'hl': self.language,
            'gl': self.region,
        }
        requestBodyBytes = json.dumps(requestBody).encode('utf_8')
        request = Request(
            'https://www.youtube.com/youtubei/v1/search' + '?' + urlencode({
                'key': searchKey,
            }),
            data = requestBodyBytes,
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Content-Length': len(requestBodyBytes),
                'User-Agent': userAgent,
            }
        )
        try:
            response = urlopen(request, timeout=self.timeout).read().decode('utf_8')
        except (URLError, HTTPError, TimeoutError) as e:
            raise YouTubeRequestError(f'Failed to make request: {str(e)}')
        except Exception as e:
            raise YouTubeRequestError(f'Unexpected error making request: {str(e)}')
        content = self._getValue(json.loads(response), contentPath)
        for item in self._getValue(content, [0, 'itemSectionRenderer', 'contents']):
            if hashtagElementKey in item.keys():
                self.params = self._getValue(item[hashtagElementKey], ['onTapCommand', 'browseEndpoint', 'params'])
                return

    async def _asyncGetParams(self) -> None:
        requestBody = copy.deepcopy(requestPayload)
        requestBody['query'] = "#" + self.hashtag
        requestBody['client'] = {
            'hl': self.language,
            'gl': self.region,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'https://www.youtube.com/youtubei/v1/search',
                    params = {
                        'key': searchKey,
                    },
                    headers = {
                        'User-Agent': userAgent,
                    },
                    json = requestBody,
                    timeout = self.timeout
                )
                response = response.json()
        except httpx.RequestError as e:
            raise YouTubeRequestError(f'Failed to make request: {str(e)}')
        except httpx.HTTPStatusError as e:
            raise YouTubeRequestError(f'HTTP error {e.response.status_code}: {str(e)}')
        except Exception as e:
            raise YouTubeRequestError(f'Unexpected error making request: {str(e)}')
        content = self._getValue(response, contentPath)
        for item in self._getValue(content, [0, 'itemSectionRenderer', 'contents']):
            if hashtagElementKey in item.keys():
                self.params = self._getValue(item[hashtagElementKey], ['onTapCommand', 'browseEndpoint', 'params'])
                return

    def _makeRequest(self) -> None:
        if self.params == None:
            return
        requestBody = copy.deepcopy(requestPayload)
        requestBody['browseId'] = hashtagBrowseKey
        requestBody['params'] = self.params
        requestBody['client'] = {
            'hl': self.language,
            'gl': self.region,
        }
        if self.continuationKey:
            requestBody['continuation'] = self.continuationKey
        requestBodyBytes = json.dumps(requestBody).encode('utf_8')
        request = Request(
            'https://www.youtube.com/youtubei/v1/browse' + '?' + urlencode({
                'key': searchKey,
            }),
            data = requestBodyBytes,
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Content-Length': len(requestBodyBytes),
                'User-Agent': userAgent,
            }
        )
        try:
            self.response = urlopen(request, timeout=self.timeout).read().decode('utf_8')
        except (URLError, HTTPError, TimeoutError) as e:
            raise YouTubeRequestError(f'Failed to make request: {str(e)}')
        except Exception as e:
            raise YouTubeRequestError(f'Unexpected error making request: {str(e)}')

    async def _asyncMakeRequest(self) -> None:
        if self.params == None:
            return
        requestBody = copy.deepcopy(requestPayload)
        requestBody['browseId'] = hashtagBrowseKey
        requestBody['params'] = self.params
        requestBody['client'] = {
            'hl': self.language,
            'gl': self.region,
        }
        if self.continuationKey:
            requestBody['continuation'] = self.continuationKey
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'https://www.youtube.com/youtubei/v1/browse',
                    params = {
                        'key': searchKey,
                    },
                    headers = {
                        'User-Agent': userAgent,
                    },
                    json = requestBody,
                    timeout = self.timeout
                )
                self.response = response.content
        except httpx.RequestError as e:
            raise YouTubeRequestError(f'Failed to make request: {str(e)}')
        except httpx.HTTPStatusError as e:
            raise YouTubeRequestError(f'HTTP error {e.response.status_code}: {str(e)}')
        except Exception as e:
            raise YouTubeRequestError(f'Unexpected error making request: {str(e)}')

    def _getComponents(self) -> None:
        if self.response == None:
            return
        self.resultComponents = []
        try:
            if not self.continuationKey:
                responseSource = self._getValue(json.loads(self.response), hashtagVideosPath)
            else:
                responseSource = self._getValue(json.loads(self.response), hashtagContinuationVideosPath)
            if responseSource:
                for element in responseSource:
                    if richItemKey in element.keys():
                        richItemElement = self._getValue(element, [richItemKey, 'content'])
                        if videoElementKey in richItemElement.keys():
                            videoComponent = self._getVideoComponent(richItemElement)
                            self.resultComponents.append(videoComponent)
                    if len(self.resultComponents) >= self.limit:
                        break
                self.continuationKey = self._getValue(responseSource[-1], continuationKeyPath)
        except json.JSONDecodeError as e:
            raise YouTubeParseError(f'Failed to parse JSON response: {str(e)}')
        except KeyError as e:
            raise YouTubeParseError(f'Missing expected key in response: {str(e)}')
        except Exception as e:
            raise YouTubeParseError(f'Failed to parse YouTube response: {str(e)}')