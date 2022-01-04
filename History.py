import os
import json
from env import HISTORY_FILE_PATH, REPORT_PATH, SCREENSHOT_PATH


class History:
    @classmethod
    def write_site_history(cls, uuid, query_url):
        if not os.path.exists(HISTORY_FILE_PATH):
            cls.__create_file()
        with open(HISTORY_FILE_PATH) as json_file:
            json_decoded = json.load(json_file)
        existing_uuid = json_decoded.get(query_url)
        json_decoded[query_url] = uuid
        with open(HISTORY_FILE_PATH, 'w') as json_file:
            json.dump(json_decoded, json_file)
        if existing_uuid:
            cls.__remove_old_data(existing_uuid=existing_uuid)

    @classmethod
    def __create_file(cls):
        if not(os.path.exists(HISTORY_FILE_PATH) and os.path.isdir(HISTORY_FILE_PATH)):
            os.makedirs(os.path.dirname(HISTORY_FILE_PATH), exist_ok=True)
        with open(HISTORY_FILE_PATH, 'w') as f:
            f.write('{}')

    @classmethod
    def __remove_old_data(cls, existing_uuid):
        screenshot_link = os.path.join(SCREENSHOT_PATH, f'{existing_uuid}.png')
        report_link = os.path.join(REPORT_PATH, f'{existing_uuid}.html')
        if os.path.exists(report_link):
            os.remove(report_link)
        if os.path.exists(screenshot_link):
            os.remove(screenshot_link)
