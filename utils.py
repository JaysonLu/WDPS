from langdetect import detect
from warcio.archiveiterator import ArchiveIterator

KEYNAME = "WARC-Record-ID"
PAYLOADTYPE = "WARC-Identified-Payload-Type"
PDFTYPE = "application/pdf"

def validate_html(payload):
    return payload.rec_type != 'response' or payload.rec_headers.get_header(PAYLOADTYPE) == PDFTYPE

def validate_text(text):
    if len(text) == 0:
        return False
	try:        
    	lang = detect(text)
    except:
    	lang = "error"
    return lang.startswith("en")
