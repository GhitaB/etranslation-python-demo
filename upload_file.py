""" Test eTranslation document translation - Upload
"""
import datetime
import logging
import random
import requests
from secret_config import COOKIES
from config import HEADERS, UPLOAD_URL, SOURCE_LANGUAGE, TARGET_LANGUAGE, FILE_EXAMPLE

def send_document_for_translation(filename, html_file, from_lang, to_lang):
    """ Send HTML file to be translated

        filename: you can set a custom filename for the file to be uploaded
                  it is useful to save it for later usage with download

                  Example: customname.html - translated from EN to RO will be renamed to
                           customname_RO.html in listed table "My translation requests"

        html_file: the file to be translated (it will be uploaded in a post request)
        from_lang: the source language (Example: "EN")
        to_lang: the target language (Example: "RO")

    """
    upload_form_data = { # you can see these if you upload a document for translation
        # and check the parameters in Network tab for this post request
        'sourceLanguage': from_lang,
        'domain': 'GEN',
        'targetLanguages': to_lang,
        'sendEmail': 'false',
        'delete': 'false',
        'outputFormat': '',
    }
    files = {'file': (filename, open(html_file))}

    response = requests.post(
        UPLOAD_URL,
        upload_form_data,
        headers=HEADERS,
        cookies=COOKIES,
        files=files
    )
    return response

def generate_filename(from_lang, to_lang):
    """ Generate a unique filename
        Example: EN-RO-2022_05_03-13_44_54-E4E717D313A9502A
    """
    r_str = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    current_time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    filename = from_lang + "-" + to_lang + "-" + current_time + "-" + r_str
    return filename

def main():
    """ Main
    """
    # Prepare
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info("We will send a HTML file to be translated by eTranslation service.")
    logger.info("This script will upload the file to be translated from %s to %s.",
            SOURCE_LANGUAGE, TARGET_LANGUAGE)
    logger.info("You can see the original file in %s", FILE_EXAMPLE)

    # Generate the filenames
    filename = generate_filename(SOURCE_LANGUAGE, TARGET_LANGUAGE)
    custom_filename = filename + ".html"
    logger.info("We generated a custom filename: %s", custom_filename)

    filename_translated = filename + "_" + TARGET_LANGUAGE + ".html"
    logger.info("And this will be the filename as it will be listed in eTranslation \
table (the tab named 'My translation requests'): %s", filename_translated)

    # Try to upload the file to be translated
    logger.info("Good. Let's try to upload the file.")
    resp = send_document_for_translation(
        filename=custom_filename,
        html_file=FILE_EXAMPLE,
        to_lang=TARGET_LANGUAGE,
        from_lang=SOURCE_LANGUAGE
    )

    if resp.ok is not True:
        logger.error("Failed with code: %s and reason: %s. Check config and retry.",
                resp.status_code, resp.reason)
        logger.error("Response content: %s", resp.content)
    else:
        logger.info("File uploaded successfully.")

if __name__ == '__main__':
    main()
