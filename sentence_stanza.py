import stanza
import sentence

# Load the Stanza English model
stanza.download('en')
nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma, constituency,depparse')

def is_sentence(input_text):
    return sentence.is_sentence(input_text, nlp)


def parse_sentence(input_text):
    return sentence.parse_sentence(input_text, nlp)
