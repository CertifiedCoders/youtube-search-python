import json
from typing import Union
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import httpx

from youtubesearchpython.core.constants import ResultMode, userAgent
from youtubesearchpython.core.requests import RequestCore


class SuggestionsCore(RequestCore):
    '''Gets search suggestions for the given query.

    Args:
        language (str, optional): Sets the suggestion language. Defaults to 'en'.
        region (str, optional): Sets the suggestion region. Defaults to 'US'.

    Examples:
        Calling `result` method gives the search result.

        >>> suggestions = Suggestions(language = 'en', region = 'US').get('Harry Styles', mode = ResultMode.json)
        >>> print(suggestions)
        {
            'result': [
                'harry styles',
                'harry styles treat people with kindness',
                'harry styles golden music video',
                'harry styles interview',
                'harry styles adore you',
                'harry styles watermelon sugar',
                'harry styles snl',
                'harry styles falling',
                'harry styles tpwk',
                'harry styles sign of the times',
                'harry styles jingle ball 2020',
                'harry styles christmas',
                'harry styles live',
                'harry styles juice'
            ]
        }
    '''

    def __init__(self, language: str = 'en', region: str = 'US', timeout: int = None):
        super().__init__()
        self.language = language
        self.region = region
        self.timeout = timeout

    def _post_request_processing(self, mode):
        searchSuggestions = []

        self.__parseSource()
        for element in self.responseSource:
            if type(element) is list:
                for searchSuggestionElement in element:
                    searchSuggestions.append(searchSuggestionElement[0])
                break
        if mode == ResultMode.dict:
            return {'result': searchSuggestions}
        elif mode == ResultMode.json:
            return json.dumps({'result': searchSuggestions}, indent=4)

    def _get(self, query: str, mode: int = ResultMode.dict) -> Union[dict, str]:
        self.url = 'https://clients1.google.com/complete/search' + '?' + urlencode({
            'hl': self.language,
            'gl': self.region,
            'q': query,
            'client': 'youtube',
            'gs_ri': 'youtube',
            'ds': 'yt',
        })

        self.__makeRequest()
        return self._post_request_processing(mode)

    async def _getAsync(self, query: str, mode: int = ResultMode.dict) -> Union[dict, str]:
        self.url = 'https://clients1.google.com/complete/search' + '?' + urlencode({
            'hl': self.language,
            'gl': self.region,
            'q': query,
            'client': 'youtube',
            'gs_ri': 'youtube',
            'ds': 'yt',
        })

        await self.__makeAsyncRequest()
        return self._post_request_processing(mode)

    def __parseSource(self) -> None:
        try:
            # Try to find JSON between parentheses
            start_idx = self.response.find('(')
            end_idx = self.response.rfind(')')
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = self.response[start_idx + 1:end_idx]
                self.responseSource = json.loads(json_str)
            else:
                # Try parsing the entire response as JSON
                try:
                    self.responseSource = json.loads(self.response)
                except:
                    # Try to extract JSON array directly
                    # Look for array pattern like [["query1", ...], ["query2", ...]]
                    import re
                    # Find JSON array pattern
                    match = re.search(r'\[\[.*?\]\]', self.response, re.DOTALL)
                    if match:
                        self.responseSource = json.loads(match.group())
                    else:
                        raise Exception('Could not find JSON in response')
        except Exception as e:
            raise Exception(f'ERROR: Could not parse YouTube response. {str(e)}')

    def __makeRequest(self) -> None:
        request = self.syncGetRequest()
        self.response = request.text

    async def __makeAsyncRequest(self) -> None:
        request = await self.asyncGetRequest()
        self.response = request.text
