#!/usr/bin/env python3
"""Build current source/auxiliary/actual-PDF proof navigation.

This is a derived navigation tool, not a theorem checker or proof certificate.
It follows the real active input closure, requires a bijection of source and
compiled proof labels, and reads every actual PDF named destination.  It does
not impose inherited label counts, page totals, or page-reference offsets.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

import pypdf
from pypdf import PdfReader

CORE_FIRST, CORE_LAST = 260, 332
NEW_CORE_FIRST, NEW_CORE_LAST = 327, 332


def core_number(path):
    match = re.fullmatch(r'core/(\d{3})_[^/]+\.tex', path)
    return int(match.group(1)) if match else None


def is_new_core(path):
    number = core_number(path)
    return number is not None and NEW_CORE_FIRST <= number <= NEW_CORE_LAST


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments(text):
    """Erase unescaped TeX comments while preserving offsets and line numbers."""
    output = []
    for line in text.splitlines(keepends=True):
        for i, char in enumerate(line):
            if char != '%':
                continue
            j, slashes = i-1, 0
            while j >= 0 and line[j] == '\\':
                slashes += 1
                j -= 1
            if slashes % 2 == 0:
                end = len(line)-int(line.endswith('\n'))
                line = line[:i]+' '*(end-i)+line[end:]
                break
        output.append(line)
    return ''.join(output)


def braced_group(text, position):
    while position < len(text) and text[position].isspace():
        position += 1
    require(position < len(text) and text[position] == '{', 'Expected auxiliary group')
    start, depth = position+1, 1
    position += 1
    while position < len(text):
        char = text[position]
        if char == '\\':
            position += 2
            continue
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return text[start:position], position+1
        position += 1
    raise RuntimeError('Unclosed auxiliary group')


def active_sources(root):
    closure, edges, seen = [], [], set()
    definitions = defaultdict(list)
    environment_aliases = {
        'sctheorem':'theorem', 'sclemma':'lemma',
        'sccorollary':'corollary', 'scproposition':'proposition',
        'scdefinition':'definition', 'scremark':'remark',
        'inputstatement':'input statement',
    }

    def visit(relative):
        require(relative not in seen, 'Repeated active input: '+relative)
        seen.add(relative)
        path = root/relative
        require(path.is_file(), 'Missing active source: '+relative)
        text = without_comments(path.read_text())
        closure.append({'path':relative, 'sha256':sha256(path), 'bytes':path.stat().st_size})
        stack = []
        for event in re.finditer(r'\\(begin|end|label)\s*\{([^{}]+)\}', text):
            command, name = event.groups()
            if command == 'begin':
                stack.append(name)
            elif command == 'end':
                if stack and stack[-1] == name:
                    stack.pop()
                elif name in stack:
                    raise RuntimeError('Unexpected environment nesting in '+relative)
            else:
                environment = environment_aliases.get(stack[-1], stack[-1]) if stack else None
                definitions[name].append({
                    'source_file':relative,
                    'source_line':text.count('\n', 0, event.start())+1,
                    'source_environment':environment,
                })
        commands = list(re.finditer(r'\\(?:input|include)\s*\{([^{}]+)\}', text))
        require(len(re.findall(r'\\(?:input|include)\b', text)) == len(commands),
                'Unparsed active input command in '+relative)
        for command in commands:
            target = command.group(1)
            if not Path(target).suffix:
                target += '.tex'
            child = (root/target).resolve()
            child_relative = str(child.relative_to(root))
            edges.append({'from':relative, 'line':text.count('\n', 0, command.start())+1, 'to':child_relative})
            visit(child_relative)

    visit('main.tex')
    multiple = {label:places for label, places in definitions.items() if len(places) != 1}
    require(not multiple, 'Multiply defined source labels: '+str(multiple))
    return closure, edges, definitions


def compiled_labels(aux_text):
    labels, metadata = defaultdict(list), []
    for line_number, line in enumerate(aux_text.splitlines(), 1):
        if not line.startswith('\\newlabel'):
            continue
        name, position = braced_group(line, len('\\newlabel'))
        payload, position = braced_group(line, position)
        if name.startswith('tocindent'):
            metadata.append({'auxiliary_label':name, 'value':payload,
                             'reason':'amsart table-of-contents indentation metadata, not a source proof label'})
            continue
        fields, position = [], 0
        while position < len(payload):
            field, position = braced_group(payload, position)
            fields.append(field)
        require(len(fields) == 5, 'Unexpected auxiliary reference format: '+name)
        labels[name].append({'number':fields[0], 'auxiliary_page_label':fields[1],
                             'title_tex':fields[2], 'pdf_anchor':fields[3], 'aux_line':line_number})
    require(all(len(entries) == 1 for entries in labels.values()), 'Multiply defined compiled labels')
    return labels, metadata


def make_navigation(index):
    evidence, validation = index['evidence'], index['validation']
    labels = index['labels']
    lines = [
        '# Current native proof navigation', '',
        'This derived navigation aid records current reference numbers and actual PDF destinations. '
        'It is not a proof certificate, independent referee endorsement, or a claim that the original '
        'raw pointwise local limit theorem is complete.', '',
        '## Exact current compiled identity', '',
        f'- Native PDF: `{evidence["pdf"]["path"]}` ({evidence["pdf"]["page_count"]} pages).',
        f'- PDF SHA256: `{evidence["pdf"]["sha256"]}`.',
        f'- Current `main.tex` SHA256: `{evidence["main_source"]["sha256"]}`.',
        f'- Final auxiliary SHA256: `{evidence["auxiliary"]["sha256"]}`.', '',
        f'The active input closure contains {validation["active_source_file_count"]} source files, '
        f'all {validation["active_core_count"]} core bodies '
        f'{validation["active_core_range"][0]}–{validation["active_core_range"][1]} exactly once, and '
        f'{validation["active_source_label_count"]} unique source labels. Every label has one '
        'compiled record and an actual PDF named destination. '
        f'The {len(index["new_modules"])} current new bodies contain '
        f'{validation["new_source_label_count"]} labels; no inherited label count was imposed. '
        'The complete label map, source hashes, source line positions, and input edges are in '
        '`PROOF_INDEX.json`.', '',
        'All pages below are one-based physical PDF pages read directly from the compiled PDF. '
        'Original auxiliary page labels and printed PDF page labels are preserved separately.', '',
        f'## {len(index["new_modules"])} new proof bodies in actual article order', '',
        '| Current native body | Actual section | Section begins on PDF page | Labels |',
        '|---|---|---:|---:|',
    ]
    for module in index['new_modules']:
        section = next(item for item in labels if item['source_file'] == module['source_file']
                       and item['kind'] in ('section', 'appendix'))
        title = section['title_tex'].replace('|', '\\|')
        lines.append(f'| `{module["source_file"]}` | {section["number"]}: {title} '
                     f'| {section["pdf_page"]} | {module["label_count"]} |')
    lines += ['', f'## Numbered statements in the {len(index["new_modules"])} current bodies', '',
              'Each row locates the numbered statement. Its proof may begin or continue on later '
              'pages; no unverified proof-page range is assigned. Numbered equations and all '
              'other source labels are included in the complete JSON index.', '']
    for module in index['new_modules']:
        section = next(item for item in labels if item['source_file'] == module['source_file']
                       and item['kind'] in ('section', 'appendix'))
        lines += [f'### Section {section["number"]}: {section["title_tex"]}', '',
                  '| Actual item | Title from the compiled reference | Label | PDF page |',
                  '|---|---|---|---:|']
        for item in labels:
            if item['source_file'] != module['source_file'] or not item['pdf_anchor'].startswith('theorem.'):
                continue
            title = item['title_tex'].replace('|', '\\|')
            lines.append(f'| {item["kind"].capitalize()} {item["number"]} | {title} '
                         f'| `{item["label"]}` | {item["pdf_page"]} |')
        lines.append('')
    lines += ['## Actual PDF pages and auxiliary references', '']
    offsets = validation['auxiliary_page_offsets']
    if offsets:
        lines += [f'{len(offsets)} current auxiliary page labels differ from the actual destination '
                  'page label. These current offsets were detected afresh; no earlier offset list '
                  'was reused. The navigation uses the actual PDF page.', '',
                  '| Label | Auxiliary page label | Actual PDF page | Printed PDF page label |',
                  '|---|---:|---:|---:|']
        for offset in offsets:
            lines.append(f'| `{offset["label"]}` | {offset["auxiliary_page_label"]} '
                         f'| {offset["actual_pdf_page"]} | {offset["printed_pdf_page_label"]} |')
        lines.append('')
    else:
        lines += ['Every current auxiliary page label agrees with its actual destination page label.', '']
    lines += ['## Reproduction and mathematical scope', '',
              'Run `python tools/build_proof_index.py` from the article directory after the final '
              'native build. The default inputs are the current native PDF and auxiliary '
              'file; `--aux` and `--pdf` select another actual build. The command fails on missing '
              'or duplicate source labels, an incomplete active core closure, or a missing PDF '
              'destination. The tool and its exact hash are recorded in the index.', '',
              'Whether a statement is unconditional on pressure, uses an inherited input, or '
              'specifies an unresolved closure is determined by its complete native statement, '
              'proof, and dependency ledger. The six new bodies prove length-sensitive physical '
              'source renewal, full selected-clearance roof height, original-normalized deep '
              'clearance payment with the unchanged comparison pool, all-label variation, '
              'actual return-tower and positive finite-band likelihood estimates, and weak '
              'endpoint-tested marked roof operator estimates. All preceding full proof bodies '
              'remain inherited. The endpoint-layer same-roof shortage, strong joint spectral '
              'and arithmetic evaluation, actual microscopic conditional denominators and '
              'the final raw pointwise inverse retain their precise remaining obligations. '
              'Finite checks, compilation and this navigation are not independent mathematical certificates.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--aux', type=Path, default=Path('build/current/native/main.aux'))
    parser.add_argument('--pdf', type=Path, default=Path('build/current/native/main.pdf'))
    parser.add_argument('--index', type=Path, default=Path('build/current/PROOF_INDEX.json'))
    parser.add_argument('--navigation', type=Path, default=Path('build/current/PROOF_NAVIGATION.md'))
    args = parser.parse_args()
    root = args.article_root.resolve()
    aux_path, pdf_path = root/args.aux, root/args.pdf
    require(aux_path.is_file() and pdf_path.is_file(), 'Actual final native PDF and auxiliary are required')
    closure, edges, source_labels = active_sources(root)
    aux_text = aux_path.read_text()
    aux_labels, metadata = compiled_labels(aux_text)
    missing = sorted(set(source_labels)-set(aux_labels))
    orphan = sorted(set(aux_labels)-set(source_labels))
    require(not missing and not orphan, 'Source/auxiliary label mismatch: '+str({'missing':missing,'orphan':orphan}))
    core_sequence = [core_number(item['path']) for item in closure
                     if core_number(item['path']) is not None]
    expected_cores = set(range(CORE_FIRST, CORE_LAST + 1))
    require(len(core_sequence) == len(expected_cores) and set(core_sequence) == expected_cores,
            f'The complete active core {CORE_FIRST}--{CORE_LAST} closure is required')
    reader = PdfReader(str(pdf_path))
    pages, destinations, page_labels = len(reader.pages), reader.named_destinations, reader.page_labels
    last_page = re.search(r'\\gdef\s*\\@abspage@last\{(\d+)\}', aux_text)
    require(last_page is not None and int(last_page.group(1)) == pages, 'Auxiliary absolute-page count differs from actual PDF')
    pdfinfo_pages = None
    if shutil.which('pdfinfo'):
        info = subprocess.check_output(['pdfinfo', str(pdf_path)], text=True)
        pdfinfo_pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
        require(pdfinfo_pages == pages, 'pdfinfo and the actual PDF reader disagree')
    source_hashes = {item['path']:item['sha256'] for item in closure}
    entries, offsets = [], []
    for label, definitions in source_labels.items():
        item = {'label':label, **definitions[0], **aux_labels[label][0]}
        anchor = item['pdf_anchor']
        require(anchor in destinations, 'Missing actual PDF destination for '+label)
        page = reader.get_destination_page_number(destinations[anchor])+1
        require(1 <= page <= pages, 'Destination outside actual PDF')
        item['pdf_page'] = page
        item['pdf_page_label'] = page_labels[page-1]
        item['pdf_page_basis'] = 'Actual named destination in the final compiled PDF'
        anchor_kind = anchor.split('.')[0]
        item['kind'] = item['source_environment'] if anchor_kind == 'theorem' else anchor_kind
        item['source_sha256'] = source_hashes[item['source_file']]
        if item['auxiliary_page_label'] != item['pdf_page_label']:
            offset = {'label':label, 'number':item['number'],
                      'auxiliary_page_label':item['auxiliary_page_label'],
                      'actual_pdf_page':page, 'printed_pdf_page_label':item['pdf_page_label']}
            if anchor_kind == 'theorem':
                heading = item['kind'].capitalize()+' '+item['number']
                require(heading in reader.pages[page-1].extract_text(),
                        'Offset theorem heading not found on its actual destination page: '+label)
                offset['actual_heading_text_verified'] = heading
            offsets.append(offset)
        entries.append(item)
    new_entries = [item for item in entries if is_new_core(item['source_file'])]
    new_modules = []
    for source in closure:
        records = [item for item in entries if item['source_file'] == source['path']]
        source['label_count'] = len(records)
        if is_new_core(source['path']):
            new_modules.append({'source_file':source['path'], 'source_sha256':source['sha256'],
                                'label_count':len(records),
                                'section_labels':[item['label'] for item in records if item['kind'] in ('section','appendix')],
                                'first_labeled_pdf_page':min(item['pdf_page'] for item in records),
                                'last_labeled_pdf_page':max(item['pdf_page'] for item in records)})
    require(len(new_modules) == NEW_CORE_LAST - NEW_CORE_FIRST + 1,
            f'All new native bodies {NEW_CORE_FIRST}--{NEW_CORE_LAST} must be active')
    generator = Path(__file__).resolve()
    index = {
        'schema':'A2-DYN-current-native-proof-navigation-v3',
        'document_title':'Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas',
        'scope':'Derived navigation only. Current source labels are joined bijectively to actual auxiliary references '
                'and PDF named destinations. This is not a mathematical proof certificate, independent referee '
                'endorsement, or completion of the raw pointwise LLT. Historical copies outside the active '
                'main.tex closure are not indexed as current claims. No old label count or page-offset list is imposed.',
        'page_convention':'pdf_page is the one-based actual PDF destination page; pdf_page_label is its printed '
                          'PDF page label; auxiliary_page_label preserves the original LaTeX auxiliary reference. '
                          'Current differences are recorded explicitly.',
        'evidence':{
            'main_source':{'path':'main.tex','sha256':sha256(root/'main.tex')},
            'auxiliary':{'path':str(aux_path.relative_to(root)),'sha256':sha256(aux_path)},
            'pdf':{'path':str(pdf_path.relative_to(root)),'sha256':sha256(pdf_path),
                   'bytes':pdf_path.stat().st_size,'page_count':pages},
            'generator':{'path':str(generator.relative_to(root)),'sha256':sha256(generator),
                         'pdf_reader':'pypdf '+pypdf.__version__},
        },
        'validation':{
            'all_source_labels_have_exactly_one_aux_record':True,
            'all_compiled_proof_labels_have_exactly_one_source_definition':True,
            'all_source_labels_have_actual_pdf_destinations':True,
            'missing_source_files':[], 'multiply_included_source_files':[],
            'missing_aux_labels':missing, 'orphan_compiled_proof_labels':orphan,
            'multiply_defined_source_labels':[], 'multiply_defined_aux_labels':[],
            'active_core_range':[CORE_FIRST,CORE_LAST], 'active_core_count':len(core_sequence),
            'active_core_sequence_in_input_order':core_sequence,
            'active_source_file_count':len(closure), 'active_source_label_count':len(entries),
            'new_core_range':[NEW_CORE_FIRST,NEW_CORE_LAST], 'new_source_label_count':len(new_entries),
            'new_core_count':len(new_modules),
            'actual_pdf_named_destinations_checked':len(entries),
            'aux_and_pdf_page_totals_agree':True, 'pdfinfo_page_count':pdfinfo_pages,
            'auxiliary_page_offset_count':len(offsets), 'auxiliary_page_offsets':offsets,
        },
        'input_closure':closure, 'input_edges':edges, 'new_modules':new_modules,
        'labels':entries, 'excluded_auxiliary_layout_metadata':metadata,
    }
    # Refuse a navigation receipt if any source changed during construction.
    for source in closure:
        require(sha256(root/source['path']) == source['sha256'], 'Source changed while indexing')
    index_path, navigation_path = root/args.index, root/args.navigation
    index_path.parent.mkdir(parents=True,exist_ok=True)
    navigation_path.parent.mkdir(parents=True,exist_ok=True)
    index_path.write_text(json.dumps(index,indent=2,ensure_ascii=False)+'\n')
    navigation_path.write_text(make_navigation(index))
    print(json.dumps({'status':'passed','active_source_files':len(closure),
                      'active_core_files':len(core_sequence),'all_labels':len(entries),
                      'new_labels':len(new_entries),'pdf_pages':pages,
                      'actual_pdf_destinations_checked':len(entries),
                      'auxiliary_page_offsets':offsets,
                      'main_sha256':index['evidence']['main_source']['sha256'],
                      'pdf_sha256':index['evidence']['pdf']['sha256'],
                      'aux_sha256':index['evidence']['auxiliary']['sha256'],
                      'generator_sha256':index['evidence']['generator']['sha256'],
                      'index_sha256':sha256(index_path),
                      'navigation_sha256':sha256(navigation_path),
                      'proof_certificate':False},sort_keys=True))


if __name__ == '__main__':
    main()
