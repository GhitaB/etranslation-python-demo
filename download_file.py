""" Download files from eTranslation
"""
import logging
import re
import requests
from bs4 import BeautifulSoup
from secret_config import COOKIES
from config import HEADERS, TARGET_LANGUAGE

files_data = {}

def download_translated(filename):
    """ Download a translated file from eTranslation
    """
    client_request_id = "9c491643-1e6a-4e3a-8b28-122028db7ddc" # TODO extract it
    logger = logging.getLogger(__name__)
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
    url = 'https://webgate.ec.europa.eu/etranslation/translationRequestHistory.html'
    response = requests.get(
        url,
        headers=HEADERS,
        cookies=COOKIES,
    )
    js_script = BeautifulSoup(response.content, features="html.parser").find_all("script")[-1]
    pattern = re.compile('var\s+list\s+=\s+(.*);')

    if(pattern.match(str(js_script.string))):
        import pdb; pdb.set_trace()

    import pdb; pdb.set_trace()

def main():
    """ Main
    """
    # Prepare
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Extract files data
    extract_files_data()

    # logger.info("We will try to download the translated file.")

    # The file
    # filename_translated = 'EN-RO-2022_05_05-10_47_17-93FC10021805926F_RO.html'
    # logger.info("Filename: %s", filename_translated)

    # Download
    # resp = download_translated(filename_translated)
    # logger.info("Status: %s", resp)

if __name__ == '__main__':
    main()
