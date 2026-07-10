import re
from urllib.parse import urlparse

import httpx
from decouple import config


class GitParser:
    def __init__(self):
        self._HEADERS = {
            "Authorization": f"Bearer {config('GITHUB_KEY')}",
            "Accept": "application/vnd.github.diff",
        }

    @staticmethod
    def _html_pr_url_to_api(html_url: str) -> str:
        """
        https://github.com/Crais2905/gt3_project/pull/1 -> https://api.github.com/repos/Crais2905/gt3_project/pulls/1
        """
        parsed = urlparse(html_url)

        if parsed.netloc != "github.com":
            raise ValueError(f"Expecting github.com, get: {parsed.netloc}")

        match = re.match(r"^/([^/]+)/([^/]+)/pull/(\d+)", parsed.path)
        if not match:
            raise ValueError(f"Can't parse PR URL: {html_url}")

        owner, repo, number = match.groups()
        return f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}"

    async def get_pr_diff(self, pr_url: str):
        url = self._html_pr_url_to_api(pr_url)

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self._HEADERS)

        if response.status_code != 200:
            raise Exception("Oops, can't get your pull request. Pls try later")

        return response.text
