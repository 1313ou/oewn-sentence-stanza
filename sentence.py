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


def find_dep1(rels, head, dependencies):
    return next(find_dep_gen(rels, head, dependencies), None)


def find_dep_gen(rels, head, dependencies):
    return (d[2] for d in dependencies if d[1] in rels and d[2].head == head)


def find_dep_list(rels, head, dependencies):
    # return [d[2] for d in dependencies if d[1] in rels and d[2].head == head]
    return list(find_dep_gen(rels, head, dependencies))


def __is_sentence(sentence):
    # _dump(sentence)
    root = find_dep1(('root'), 0, sentence.dependencies)
    if not root:
        return False

    # root is a verb
    subjects = find_dep_list(('nsubj', 'nsubj:pass', 'nsubjpass', 'csubj'), root.id, sentence.dependencies)
    if root.upos in {"VERB"}:

        if len(subjects) == 0:

            # imperative mood feature
            if 'Mood=Imp' in root.feats:
                return True

            # let n v
            if root.lemma == 'let' and root.id == 1:
                # let's|us|him|the man V
                xcomp = find_dep1(('xcomp'), root.id, sentence.dependencies)
                obj = find_dep1(('obj'), root.id, sentence.dependencies)
                if xcomp and xcomp.upos == 'VERB' and obj and obj.upos in ('NOUN', 'PRON'):
                    return True
                ccomp = find_dep1(('ccomp'), root.id, sentence.dependencies)
                if ccomp:
                    return True

            # do v
            aux = find_dep1(('aux'), root.id, sentence.dependencies)
            if aux and aux.lemma == 'do' and len(subjects) == 0: #and aux.id == 1:
                return True

            return False

        # subject v
        else:
            return True

    # root with copula and subject
    elif root.upos in {"NOUN", "PRON", "ADJ", "ADV"}:
        copulas = find_dep_list(("cop"), root.id, sentence.dependencies)
        if len(subjects) == 0 or len(copulas) == 0:
            return False
        return True

    return False


def _is_sentence(doc):
    return len(doc.sentences) == 1 and __is_sentence(doc.sentences[0])


# P R O C E S S I N G   F U N C T I O N   F R O M   T E X T
# returns none if sentence else doc

def _deps(doc, color=False):
    # return doc.sentences[0].dependencies
    # return prettyprint.dependencies(doc.sentences[0])
    return prettyprint.dependency_tree(doc.sentences[0], color=color)


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
    examples0 = [
        "is anybody here",
        "is anybody happy",
    ]
    examples1 = [
        "go",
        "don't go",
        "do go",
        "let's go",
        "let me explain",
        "let the man go",
        "let there be more light",
    ]
    examples2 = [
        "is anybody here",
        "this is obvious",
        "This is a sentence.",
        "I like music",
        "This is a complete sentence.",
        "The quick brown fox jumps over the lazy dog.",
        "She loves programming and solving complex problems.",
        "The cat sat on the mat.",
        "He was smoking.",
        "do you smoke",
    ]
    examples3 = [
        "A full thought, it is.",
        "Incomplete",
        "running fast",
        "What about this?",
        "a quick brown fox",
        "obvious though this is ",
    ]
    examples4 = [
        "We were so far back in the theater, we could barely read the subtitles.",
        "We were so far back in the theater we could barely read the subtitles.",
        "force out the air",
        "blow on the soup to cool it down",
        "beat the living hell out of him",
        "was immensely more important to the project as a scientist than as an administrator",
        "would have scarce arrived before she would have found some excuse to leave",
        "would have scarcely arrived before she would have found some excuse to leave",
    ]
    for input_text in examples0: # + examples1 + examples2 + examples3 + examples4:
        doc = nlp(input_text)
        sentence_result = _is_sentence(doc)

        print(f"Text: {input_text}")
        print(f"Sentence: {sentence_result}")
        print(f"Deps:\n{_deps(doc, color=True)}")
        print("\n")


if __name__ == '__main__':
    main()
