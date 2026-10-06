import stanza
from stanza import DownloadMethod

# Load the Stanza English model
# stanza.download('en')

# Load the Stanza English model
nlp = stanza.Pipeline('en',
                      processors='tokenize,mwt,pos,lemma, constituency,depparse',
                      download_method=DownloadMethod.REUSE_RESOURCES)
# download_method=None)
print(nlp.config)
