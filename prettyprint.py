

def dependency_tree(sent):
    result = []
    root = next((w for w in sent.words if w.head == 0), None)
    stack = [(0, root.id, 0)]  # Start with the root word
    while stack:
        parent_id, child_id, indent_level = stack.pop()
        word = sent.words[child_id - 1]
        indent = "  " * indent_level
        rel = word.deprel
        rel = "↳" if 'root' == rel else f"└{rel.ljust(8, '—')}→"
        result.append(f"{indent}{rel} {word.text} {word.upos} {word.xpos} {word.feats}")
        for other_word in sent.words:
            if other_word.head == child_id:
                stack.append((child_id, other_word.id, indent_level + 1))
    return '\n'.join(result)


def dependencies(sent):
    result = []
    for word in sent.words:
        head_id = word.head
        d = f"{word.text} {word.upos} {word.xpos}"
        f = f"{word.feats}"
        if head_id != 0:  # Skip root word
            head_word = sent.words[head_id - 1]
            h = f"{head_word.text} ({head_word.deprel})"
            h2 = f"{head_word.upos} {head_word.xpos}"
            r = f"—{word.deprel}→"
            result.append(f"\t{d} {r} {h} {f}")
        else:
            result.append(f"↳\t{d} {f}")

    return '\n'.join(result)
