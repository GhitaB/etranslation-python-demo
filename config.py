""" Public (not secret) configuration for upload/download files in eTranslation
"""
UPLOAD_URL = 'https://webgate.ec.europa.eu/etranslation/translateDocument.html'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
SOURCE_LANGUAGE = "EN"
TARGET_LANGUAGE = "RO"

FILE_EXAMPLE = "./files/test-file.html"
