import stanza
from stanza import DownloadMethod
import prettyprint


def _dump(sentence):
    pos = [w.pos for w in sentence.words]
    xpos = [w.xpos for w in sentence.words]
    deps = [w.deps for w in sentence.words]
    deprels = [w.deprel for w in sentence.words]
    sdeps = sentence.dependencies
    sconstituency = sentence.dependencies
    print(pos)
    print(xpos)
    print(deps)
    print(deprels)
    print(sdeps)
    print(sconstituency)


def _is_sentence2(sentence):
    # _dump(sentence)
    roots = [d[2] for d in sentence.dependencies if d[1] in ('root')]
    if len(roots) != 1:
        return False
    root = roots[0]

    # root is a verb or aux
    if root.upos in {"VERB"}:
        # Check for nominal or clausal subject linked to the root
        subjects = [d[2] for d in sentence.dependencies if
                    d[1] in ("nsubj", "nsubj:pass", "nsubjpass", "csubj") and d[2].head == root.id]
        if len(subjects) == 0:
            return False
        subject = subjects[0]
        return True

    elif root.upos in {"NOUN", "PRON", "ADJ"}:
        copulas = [d[2] for d in sentence.dependencies if
                   d[1] in ("cop") and d[2].head == root.id]
        if len(copulas) == 0:
            return False
        return True

    return False


def _is_sentence(doc):
    return len(doc.sentences) == 1 and _is_sentence2(doc.sentences[0])


# P R O C E S S I N G   F U N C T I O N   F R O M   T E X T
# returns none if sentence else doc

def _deps(doc):
    # return doc.sentences[0].dependencies
    #return prettyprint.dependencies(doc.sentences[0])
    return prettyprint.dependency_tree(doc.sentences[0])


def is_sentence(input_text, nlp):
    doc = nlp(input_text)
    return _is_sentence(doc)


def parse_sentence(input_text, nlp):
    doc = nlp(input_text)
    flag = _is_sentence(doc)
    return flag, _deps(doc)


# T E S T

def main():
    # Load the Stanza English model
    # stanza.download('en')
    nlp = stanza.Pipeline('en',
                          processors='tokenize,mwt,pos,lemma, constituency,depparse',
                          download_method=DownloadMethod.REUSE_RESOURCES)
    # download_method=None)
    print(nlp.config)
    examples1 = [
        "go",
        "don't go",
        "let's go",
    ]
    examples2 = [
        "is anybody here",
        "A full thought, it is.",

        "this is obvious",
        "Incomplete",
        "running fast",
        "This is a sentence.",
        "I like music",
        "This is a complete sentence.",
        "What about this?",
        "The quick brown fox jumps over the lazy dog.",
        "a quick brown fox",
        "She loves programming and solving complex problems.",
        "The cat sat on the mat.",
        "He was smoking.",
        "obvious though this is ",
        "do you smoke",
    ]
    for input_text in examples1 + examples2:
        doc = nlp(input_text)
        sentence_result = _is_sentence(doc)

        print(f"Text: {input_text}")
        print(f"Sentence: {sentence_result}")
        print(f"Deps:\n{_deps(doc)}")
        print("\n")


if __name__ == '__main__':
    main()
