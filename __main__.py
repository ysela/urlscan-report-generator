from UrlScan import UrlScan
import asyncio
from env import API_KEY


def main():
    if not API_KEY:
        raise Exception(
            'No API_KEY specified. Please add a valid UrlScan API Key to the env.py file')
    else:
        visibility_list = {'public', 'private', 'unlisted'}
        query_url = None
        while not query_url:
            query_url = input('Please enter the URL you wish to scan:\n')

        visibility = input(
            'Please select a visibility level ("public", "private", or "unlisted"), or press enter for the default visibility settings:\n')

        if not any(visibility in str for str in visibility_list):
            print('Invalid entry. Reverting to default visibility.')
            visibility = 'unlisted'

        url_scan = UrlScan(query_url=query_url, visibility=visibility)
        asyncio.run(url_scan.run_scan())


if __name__ == '__main__':
    main()
