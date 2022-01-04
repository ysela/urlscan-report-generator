import json
import asyncio
import aiohttp
import os
from bs4 import BeautifulSoup as bs
from env import API_KEY, SCREENSHOT_PATH, REPORT_PATH
from HtmlGenerator import HtmlGenerator
from History import History


class UrlScan:
    BASE_URL = 'https://urlscan.io/api/v1'
    INITIAL_TIMEOUT_SECONDS = 10
    REPOLL_TIME = 2
    MAX_REPEATS = 10

    def __init__(self, query_url, visibility: str = 'unlisted'):
        self.query_url = query_url
        self.uuid = None
        self.results = None
        self.dom = None
        self.visibility = visibility

    async def submit_scan(self):
        async with aiohttp.ClientSession() as client:
            limit_exceeded = await self.check_limits()
            if(limit_exceeded):
                raise Exception(
                    f'The {limit_exceeded} has been exceeded for the "{self.visibility}" visibility level.\n Please try again later or change the visibility level.')
            headers = {'API-KEY': API_KEY,
                       'Content-Type': 'application/json'}
            data = {"url": self.query_url, "visibility": self.visibility}
            async with client.post(f'{self.BASE_URL}/scan', headers=headers, data=json.dumps(data)) as response:
                if response.status == 429:
                    raise Exception(
                        f'The scan request was unsuccessful; too many requests were made. Please try again later')
                res_json = await response.json()
                print(res_json)
                if response.status == 401:
                    raise Exception('Invalid API Key provided')
                if response.status >= 400:
                    raise Exception(
                        f'Oh no! Status Code: {response.status}. {res_json["message"]}. {res_json["description"] or ""}')

                self.uuid = res_json['uuid']
                History.write_site_history(
                    uuid=self.uuid, query_url=self.query_url)

    async def get_results(self):
        async with aiohttp.ClientSession() as client:
            headers = {'API-KEY': API_KEY}
            async with client.get(f'{self.BASE_URL}/result/{self.uuid}', headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.results = json.dumps(data, indent=4)
                    return True

    async def get_screenshot(self):
        async with aiohttp.ClientSession() as client:
            headers = {'API-KEY': API_KEY}
            async with client.get(f'{self.BASE_URL}/screenshots/{self.uuid}.png', headers=headers) as response:
                if response.status == 200:
                    if not(os.path.exists(SCREENSHOT_PATH) and os.path.isdir(SCREENSHOT_PATH)):
                        os.makedirs(SCREENSHOT_PATH,
                                    exist_ok=True)
                    file_path = os.path.join(
                        SCREENSHOT_PATH, f'{self.uuid}.png')
                    with open(file_path, mode="wb") as f:
                        f.write(await response.read())

    async def get_dom(self):
        async with aiohttp.ClientSession() as client:
            headers = {'API-KEY': API_KEY}
            async with client.get(f'{self.BASE_URL}/dom/{self.uuid}', headers=headers) as response:
                if(response.status == 200):
                    html_text = await response.text()
                    soup = bs(html_text, features='html.parser')
                    self.dom = soup.prettify()

    async def check_limits(self):
        async with aiohttp.ClientSession() as client:
            headers = {'API-KEY': API_KEY,
                       'Content-Type': 'application/json'}
            async with client.get(f'{self.BASE_URL}/quotas', headers=headers) as response:
                if(response.status == 200):
                    quota_results = await response.json()
                    limits = {
                        'daily limit': quota_results['limits'][self.visibility]['day']['remaining'],
                        'daily results limit': quota_results['limits']['retrieve']['day']['remaining'],
                        'hourly limit': quota_results['limits'][self.visibility]['hour']['remaining'],
                        'hourly results limit': quota_results['limits']['retrieve']['hour']['remaining'],
                        'minutely limit': quota_results['limits'][self.visibility]['minute']['remaining'],
                        'minutely results limit': quota_results['limits']['retrieve']['minute']['remaining']
                    }
                    return ({key for key, val in limits.items() if val == 0} or False)

    async def run_scan(self):
        results_loaded = False
        retries = 0
        await self.submit_scan()

        print(
            f'Waiting {self.INITIAL_TIMEOUT_SECONDS} seconds before polling...')

        await asyncio.sleep(self.INITIAL_TIMEOUT_SECONDS)
        while not results_loaded and retries < self.MAX_REPEATS:
            if retries:
                await asyncio.sleep(self.REPOLL_TIME)
                print(
                    f'The resource is not yet available. Waiting {self.REPOLL_TIME} seconds before attempting re-poll...')
            results_loaded = await self.get_results()
            retries += 1
        if retries >= self.MAX_REPEATS:
            raise Exception(
                f'Query results are currently unavailable. Please check again later manually at https://urlscan.io/result/{self.uuid}')
        await self.get_screenshot()
        await self.get_dom()
        h_gen = HtmlGenerator(uuid=self.uuid,
                              query_url=self.query_url,
                              dom_screenshot=self.dom,
                              results=self.results)
        h_gen.generate_report_template()
        print(
            f'Scan complete. The report file is available in the {REPORT_PATH} folder')
