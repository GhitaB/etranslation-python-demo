""" Download files from eTranslation
"""
import logging
import requests
from secret_config import COOKIES
from config import HEADERS, TARGET_LANGUAGE

def download_translated(filename):
    """ Download a translated file from eTranslation
    """
    client_request_id = "111" # TODO extract it
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
        response.raise_for_status() # ensure we notice bad responses
        file = open('./translated_files/' + filename, "wb")
        file.write(response.content)
        file.close()
        import pdb; pdb.set_trace()
        logger.info("Downloading... " + filename)
        return 'downloaded'
    return 'pending'

def main():
    """ Main
    """
    # Prepare
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info("We will try to download the translated file.")

    # The file
    filename_translated = 'EN-RO-2022_05_05-10_19_36-80E596E28826107A_RO.html'
    logger.info("Filename: %s", filename_translated)

    # Download
    resp = download_translated(filename_translated)
    logger.info("Status: %s", resp)

if __name__ == '__main__':
    main()
