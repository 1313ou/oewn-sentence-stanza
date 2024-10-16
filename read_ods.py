import argparse
import sys
import os
from pathlib import Path

import ezodf
import ods_columns as col
import sentence_stanza

synsetid_col = col.synsetid_col
nid_col = col.nid_col
clazz_col = col.class_col
text_col = col.text_col
text0_col = col.text0_col
result_clazz_col = col.stanza_col
result_deps_col = col.stanza_deps_col
result_cdeps_col = col.stanza_cdeps_col


def ensure_row(sheet, row_index):
    current_rows = sheet.nrows()
    if current_rows <= row_index:
        sheet.append_rows(row_index - current_rows + 1)


def ensure_col(sheet, col_index):
    current_cols = sheet.ncols()
    if current_cols <= col_index:
        sheet.append_columns(col_index - current_cols + 1)


def default_process(row):
    return row


def process(row):
    id = row[nid_col].value
    if not id:
        return
    clazz = row[clazz_col].value
    tagged_sentence = clazz is not None and clazz in ('S', 'I')
    tagged_phrase = clazz is not None and clazz in ('P', 'N', 'V', 'A', 'D')
    if not tagged_sentence and not tagged_phrase:
        raise ValueError(id)
    if not (tagged_sentence or tagged_phrase):
        raise ValueError(id)
    input_text = row[text_col].value
    is_sentence, deps, cdeps = sentence_stanza.parse_sentence(input_text)
    diff = (tagged_sentence and not is_sentence) or (tagged_phrase and is_sentence)
    if diff:
        row[result_clazz_col].set_value('S!' if is_sentence else 'P!')
    else:
        row[result_clazz_col].set_value('s' if is_sentence else 'p')
    row[result_deps_col].set_value(deps)
    row[result_cdeps_col].set_value(cdeps)
    return row if diff else None


def process_sentence(row):
    clazz = row[clazz_col].value
    if clazz is not None and clazz in ('S', 'I'):
        input_text = row[text_col].value
        is_sentence, deps = sentence_stanza.parse_sentence(input_text)
        if not is_sentence:
            deps = str(deps)  # .replace('\n','')
            row[result_clazz_col].set_value(deps)
            return row


def process_not_sentence(row):
    clazz = row[clazz_col].value
    if clazz is not None and clazz in ('P', 'N', 'V', 'A', 'D'):
        input_text = row[text_col].value
        is_sentence, deps = sentence_stanza.parse_sentence(input_text)
        if is_sentence:
            deps = str(deps)  # .replace('\n','')
            row[result_clazz_col].set_value(deps)
            return row


def read_row(sheet):
    for row in range(sheet.nrows()):
        yield [sheet[row, col] for col in range(sheet.ncols())]


def get_processing(name):
    return globals()[name] if name else process


def run(filepath, processf):
    file_abspath = os.path.abspath(filepath)
    doc = ezodf.opendoc(file_abspath)
    sheet = doc.sheets[0]
    ensure_col(sheet, col.last_col)  # for result

    count = 0
    for row in read_row(sheet):
        new_row = processf(row)
        if new_row:
            # print(f"{'\t'.join([str(col.value) for col in new_row])}")
            synsetid = row[synsetid_col].value
            id = row[nid_col].value
            clazz = row[clazz_col].value
            print(f"{synsetid}\t{id}\t{clazz}\t{row[text_col].value}\t{new_row[result_clazz_col].value.replace('\n', '')}")
            count += 1
    p = Path(file_abspath)
    saved = f"{p.parent}/{p.stem}_{processf.__name__}{p.suffix}"
    doc.saveas(saved)
    return count


def main():
    parser = argparse.ArgumentParser(description="scans the ods analyzing for sentence status")
    parser.add_argument('file', type=str, help='file')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processf = get_processing(args.processing)
    if processf:
        print(processf, file=sys.stderr)
    run(args.file, processf)


if __name__ == '__main__':
    main()
