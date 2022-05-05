""" Public (not secret) configuration for upload/download files in eTranslation
"""
UPLOAD_URL = 'https://webgate.ec.europa.eu/etranslation/translateDocument.html'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
SOURCE_LANGUAGE = "EN"
TARGET_LANGUAGE = "RO"

FILE_EXAMPLE = "./files/test-file.html"

UPLOAD_FORM_DATA = { # you can see these if you upload a document for translation
    # and check the parameters in Network tab for this post request
    'sourceLanguage': SOURCE_LANGUAGE,
    'domain': 'GEN',
    'targetLanguages': TARGET_LANGUAGE,
    'sendEmail': 'false',
    'delete': 'false',
    'outputFormat': '',
}
