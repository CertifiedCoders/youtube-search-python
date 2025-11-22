import httpx
import os

from youtubesearchpython.core.constants import userAgent

class RequestCore:
    def __init__(self):
        self.url = None
        self.data = None
        self.timeout = 2
        self.proxy = {}
        http_proxy = os.environ.get("HTTP_PROXY")
        if http_proxy:
            self.proxy["http://"] = http_proxy
        https_proxy = os.environ.get("HTTPS_PROXY")
        if https_proxy:
            self.proxy["https://"] = https_proxy

    def syncPostRequest(self) -> httpx.Response:
        # FIXED: removed `proxies=self.proxy` (no longer supported in httpx 0.28+)
        return httpx.post(
            self.url,
            headers={"User-Agent": userAgent},
            json=self.data,
            timeout=self.timeout,
        )

    async def asyncPostRequest(self) -> httpx.Response:
        # FIXED: removed `proxies=self.proxy` (no longer supported in httpx 0.28+)
        async with httpx.AsyncClient() as client:
            r = await client.post(self.url, headers={"User-Agent": userAgent}, json=self.data, timeout=self.timeout)
            return r

    def syncGetRequest(self) -> httpx.Response:
        # FIXED: removed `proxies=self.proxy` (no longer supported in httpx 0.28+)
        return httpx.get(self.url, headers={"User-Agent": userAgent}, timeout=self.timeout, cookies={'CONSENT': 'YES+1'})

    async def asyncGetRequest(self) -> httpx.Response:
        # FIXED: removed `proxies=self.proxy` (no longer supported in httpx 0.28+)
        async with httpx.AsyncClient() as client:
            r = await client.get(self.url, headers={"User-Agent": userAgent}, timeout=self.timeout, cookies={'CONSENT': 'YES+1'})
            return r