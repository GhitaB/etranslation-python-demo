import datetime
import logging
from config import cookies, headers, UPLOAD_URL, UPLOAD_FORM_DATA

def download_translated(filename):
    logger = logging.getLogger(__name__)
    url = 'https://webgate.ec.europa.eu/etranslation/download.html'
    form_data = {
        'clientRequestId': client_request_id,
        'targetLanguage': 'RO', # TODO extract language
        'targetFileName': filename,
        'targetFormat': 'html',
        'deleteFile': 'false'
    }
    response = requests.post(
        url,
        form_data,
        headers=headers,
        cookies=cookies,
    )

    if response.status_code == 200:
        if len(response.content) == 0:
            logger.warning("0 bytes response. Check clientRequestId.")
            return 'pending'
        response.raise_for_status() # ensure we notice bad responses
        file = open('./archive/' + filename, "wb")
        file.write(response.content)
        file.close()
        import pdb; pdb.set_trace()
        logger.info("Downloading... " + filename)
        return 'downloaded'
    return 'pending'
