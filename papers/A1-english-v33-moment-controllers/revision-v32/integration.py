"""Pure, fail-closed transformations of the pinned v30 entry points."""
from __future__ import annotations
from pathlib import Path
import re


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"Expected one integration anchor, found {count}: {old!r}")
    return text.replace(old, new, 1)


def make_main(original: str) -> str:
    result = replace_once(original, r'\input{v30/introduction}', r'\input{v32/introduction}')
    result = replace_once(result, r'\input{text/collision_consequences}',
                          r'\input{text/collision_consequences}'+'\n'+r'\input{v32/new_results}')
    result = replace_once(result, r'\input{references-v29}',
                          r'\input{v32/model_ledger}'+'\n'+r'\input{references-v32}')
    pattern = re.compile(r'\\begin\{abstract\}.*?\\end\{abstract\}', re.S)
    if len(pattern.findall(result)) != 1:
        raise ValueError('The pinned main file must have exactly one abstract.')
    result = pattern.sub(lambda _: '\\begin{abstract}\n\\input{v32/abstract}\n\\end{abstract}', result)
    # Every inherited input except the two deliberately replaced entry points stays active.
    before = re.findall(r'\\input\{([^}]+)\}', original)
    after = re.findall(r'\\input\{([^}]+)\}', result)
    for item in before:
        if item not in {'v30/introduction', 'references-v29'} and after.count(item) != before.count(item):
            raise ValueError(f'Inherited input lost or duplicated: {item}')
    return result


def make_introduction(original: str, module_dir: Path) -> str:
    first = original.find(r'\subsection{')
    if first < 0 or original.count(r'\section{Introduction}') != 1:
        raise ValueError('Unexpected introduction structure.')
    # The old introduction remains byte-identical in v30/. Only the new active copy changes.
    result = (module_dir/'introduction_opening.tex').read_text() + original[first:]
    anchor = r'\subsection{Adaptive graphs and reusable acquisition}'
    result = replace_once(result, anchor,
                          (module_dir/'introduction_compatibility.tex').read_text()+anchor)
    result += '\n\n'+r'\input{v32/positioning}'+'\n'+r'\input{v32/introduction_organization}'+'\n'
    if result.count(r'\input{text/main_classification}') != 1:
        raise ValueError('The inherited leading theorem input must occur exactly once.')
    if result.count(r'\section{Introduction}') != 1:
        raise ValueError('Exactly one active introduction is required.')
    return result


def bibliography_wrapper() -> str:
    # v29 already wraps v27's bibliography. Compose, rather than replace, that wrapper.
    return r'''% All inherited bibliography entries remain active.
\begingroup
\let\vThirtyTwoEndBibliography\endthebibliography
\def\endthebibliography{%
\input{v32/bibliography_entries}%
\vThirtyTwoEndBibliography}
\input{references-v29}
\endgroup
'''


def exported_labels(auxiliary: str) -> str:
    """Export only reference labels; do not import bibliography state across volumes."""
    labels = []
    for line in auxiliary.splitlines():
        match = re.match(r'\\newlabel\{([^}]+)\}', line)
        if match and not re.fullmatch(r'tocindent-?\d+', match.group(1)):
            labels.append(line)
    # AMS tocindent labels contain bare dimensions, not reference tuples.
    # Importing them through xr-hyper corrupts the receiving volume's layout state.
    return '\\relax\n'+'\n'.join(labels)+'\n'
