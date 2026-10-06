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
    root = find_dep1(['root'], 0, sentence.dependencies)
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
                xcomp = find_dep1(['xcomp'], root.id, sentence.dependencies)
                obj = find_dep1(['obj'], root.id, sentence.dependencies)
                if xcomp and xcomp.upos == 'VERB' and obj and obj.upos in ('NOUN', 'PRON'):
                    return True
                ccomp = find_dep1(['ccomp'], root.id, sentence.dependencies)
                if ccomp:
                    return True

            # do v
            aux = find_dep1(['aux'], root.id, sentence.dependencies)
            if aux and aux.lemma == 'do' and len(subjects) == 0:  # and aux.id == 1:
                return True

            return False

        # subject v
        else:
            return True

    # root with copula and subject
    elif root.upos in {"NOUN", "PRON", "ADJ", "ADV"}:
        copulas = find_dep_list(["cop"], root.id, sentence.dependencies)
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


def _cdeps(doc):
    return prettyprint.cdependency_tree(doc.sentences[0])


def is_sentence(input_text, nlp):
    doc = nlp(input_text)
    return _is_sentence(doc)


def parse_sentence(input_text, nlp, color=False):
    doc = nlp(input_text)
    flag = _is_sentence(doc)
    return flag, _deps(doc, color=color), _cdeps(doc)
