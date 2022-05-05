""" Download files from eTranslation
"""
import logging
import json
import requests
from bs4 import BeautifulSoup
from secret_config import COOKIES
from config import HEADERS, TARGET_LANGUAGE

files_data = {}

def download_translated(filename):
    """ Download a translated file from eTranslation
    """
    logger = logging.getLogger(__name__)
    client_request_id = files_data.get(filename, None)
    if client_request_id is None:
        logger.error("Missing info for this filename. Cannot download.")
        return "pending"

    url = 'https://webgate.ec.europa.eu/etranslation/download.html'
    form_data = {
        'clientRequestId': client_request_id,
        'targetLanguage': TARGET_LANGUAGE,
        'targetFileName': filename,
        'targetFormat': 'html',
        'deleteFile': 'false'
    }
    response = requests.post(
        url,
        form_data,
        headers=HEADERS,
        cookies=COOKIES,
    )

    if response.status_code == 200:
        if len(response.content) == 0:
            logger.warning("0 bytes response. Check clientRequestId.")
            return 'pending'
        file = open('./files/' + filename, "wb")
        file.write(response.content)
        file.close()
        logger.info("Downloading... " + filename)
        return 'downloaded'
    return 'pending'

def extract_files_data():
    """ Get files data from eTranslation table in 'My translation requests'
    """
    logger = logging.getLogger(__name__)
    url = 'https://webgate.ec.europa.eu/etranslation/translationRequestHistory.html'
    response = requests.get(
        url,
        headers=HEADERS,
        cookies=COOKIES,
    )

    # We can get the list of files from a js var named list which contains all we need.
    js_scripts = BeautifulSoup(
        response.content, features="html.parser").find_all("script")

    if len(js_scripts) == 0:
        logger.error("Cannot extract the files from table")
        return None

    js_script = js_scripts[-1]
    js_variable_value = js_script.string.split("var list =")[1].split("}];")[0] + "}]"
    list_of_files = json.loads(js_variable_value)

    for item in list_of_files:
        files_data[item['translatedOriginalFileName']] = item['clientRequestId']
    logger.info("Extracted the details of files in 'My translation requests' table.")
    return files_data

def main():
    """ Main
    """
    # Prepare
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Extract files data
    files = extract_files_data()

    logger.info("We will try to download the translated file.")

    # The file
    filename_translated = 'EN-RO-2022_05_05-10_47_17-93FC10021805926F_RO.html'
    logger.info("Filename: %s", filename_translated)

    # Download
    resp = download_translated(filename_translated)
    logger.info("Status: %s", resp)

if __name__ == '__main__':
    main()
