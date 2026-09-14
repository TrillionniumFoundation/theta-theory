#!/usr/bin/env python3
"""Materialize the complete v48 entry, preserving the exact reviewed v47 inputs.

Only the main entry and one section heading of the inherited manuscript are
changed.  New mathematical modules are ordinary readable TeX files; their
contact-centered observation convention is made explicit before compilation.
This script is idempotent and rejects unexpected edit anchors.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
from source_provenance import require, write_json

P = Path(__file__).resolve().parents[1]
ARCHIVE = P / 'history/v47-review-baseline'
CHANGES = ('main.tex', 'article/01_introduction_v41.tex')
SOURCE_V47 = '219b39e94b14187561dc3b7e5bdbae49dbd92cc2'
REVIEW_V47 = '757f2ee4e3bf766d2eb56d972e6d2f621b3fd2a6'
NEW_INPUTS = ('article/00_structural_introduction_v48.tex',
              'article/23m_differential_rigidity_v48.tex')
ABSTRACT = r'''\begin{abstract}
We recover the two labelled contact jets of a smooth dispersing billiard
channel from its gap and one signed conditional endpoint law of each type
at a fixed positive offset.  The laws are obtained as nonlinear relative
limits of long alternating bridges on collars independent of the flight
number.  A four-density identity eliminates the unknown flux amplitudes;
a finite-remainder action inverse recovers all signed contact jets through
explicit invertible two-by-two blocks.  For $N$ labelled analytic obstacle
orbits with trivial proper symmetries, $N+1$ selected clear channels
determine the entire periodic table and its unknown marked Euclidean
lattice up to a common proper Euclidean motion.  The same observation map
is infinitesimally rigid on common-strip analytic-support families.  On
every immersed finite-dimensional model, finitely many gap and interior
law expectations give local coordinates.  Under quantified analytic and
asymmetry bounds we obtain full-table stability from finite transverse
histograms.  A same-flight physical pilot yields a charged finite
acquisition prescription with separate finite-flight, timing and
cell-crossing errors.  We also determine the distinct local experiments
associated with retaining residual times, waiting counts or full planar
positions, and prove global reconstruction with all preparation failures
charged.
\end{abstract}'''


def replace_once(text: str, before: str, after: str) -> str:
    require(text.count(before) == 1, 'Unexpected edit anchor: ' + before)
    return text.replace(before, after, 1)


def revised(name: str, text: str) -> str:
    if name == CHANGES[1]:
        return replace_once(text, r'\section{Introduction}',
                            r'\section{Local mechanisms and observation-specific consequences}')
    require(name == 'main.tex', 'Unknown edited file')
    text = text.replace('A2 revision 47', 'A2 revision 48')
    text = replace_once(text,
        '\\title[Boundary laws and intrinsic periodic rigidity]{Boundary laws, intrinsic periodic rigidity, and global physical reconstruction\\\\\nin dispersing billiards}',
        r'\title[Boundary laws and periodic rigidity]{Boundary laws and rigidity of periodic dispersing billiards}')
    text = replace_once(text,
        'pdftitle={Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards}',
        'pdftitle={Boundary laws and rigidity of periodic dispersing billiards}')
    text = replace_once(text, 'generic finite-channel rigidity, quantized-law stability,',
        'generic finite-channel rigidity, infinitesimal rigidity, finite observable coordinates, quantized-law stability,')
    a, b = text.index(r'\begin{abstract}'), text.index(r'\end{abstract}') + len(r'\end{abstract}')
    text = text[:a] + ABSTRACT + text[b:]
    part = r'\part{Relative laws, signed inversion, and intrinsic rigidity}'
    text = replace_once(text, '\\tableofcontents\n',
        '\\tableofcontents\n\\input{article/00_structural_introduction_v48}\n\n' + part + '\n')
    require(text.count(part) == 2, 'Unexpected Part I markers')
    second = text.index(part, text.index(part) + len(part))
    text = text[:second] + text[second+len(part):]
    return replace_once(text, r'\input{article/23j_generic_finite_channel_rigidity_v45}',
        '\\input{article/23j_generic_finite_channel_rigidity_v45}\n\\input{article/23m_differential_rigidity_v48}')


def clarify_contact_squares() -> None:
    edits = (
        (NEW_INPUTS[0],
         'vanishes on a positive interior square, then the table variation is the',
         'vanishes on a contact-centered positive interior square, then the table variation is the'),
        (NEW_INPUTS[1],
         'The two positive-density squares $Q_{e,b}$ and their nonzero\nanchors can be fixed on a parameter neighborhood.',
         'Fix contact-centered squares $Q_{e,b}=(-r_{e,b},r_{e,b})^2$ whose\nclosures lie in the respective positive-density regions, and nonzero scalar\nanchors $a_{e,b}\\in(-r_{e,b},r_{e,b})$.  These choices persist on a\nparameter neighborhood.'),
    )
    for name, before, after in edits:
        path = P/name
        text = path.read_text()
        if before in text:
            text = replace_once(text, before, after)
            path.write_text(text)
        else:
            require(text.count(after) == 1, 'Unexpected contact-coordinate convention: ' + name)


def materialize() -> dict:
    for name in NEW_INPUTS:
        require((P/name).is_file(), 'Missing readable new TeX input: ' + name)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    manifest_path = ARCHIVE/'active-source-manifest.json'
    if not manifest_path.exists():
        repo = P.parents[1]
        original = repo/'deliveries/a2-v47'/SOURCE_V47/'active-source-manifest.json'
        require(original.is_file(), 'Missing source-matched v47 native manifest')
        manifest_path.write_bytes(original.read_bytes())
    manifest = json.loads(manifest_path.read_text())
    old = {name: info for entry in manifest.values() for name, info in entry.items()}
    require(len(old) == 103, 'Unexpected reviewed v47 active input count')
    for name, info in old.items():
        archived = ARCHIVE/name
        target = archived if name in CHANGES and archived.exists() else P/name
        data = target.read_bytes()
        require(hashlib.sha256(data).hexdigest() == info['sha256'], 'Unexpected v47 baseline: ' + name)
        if name in CHANGES:
            if not archived.exists():
                archived.parent.mkdir(parents=True, exist_ok=True)
                archived.write_bytes(data)
            expected = revised(name, data.decode())
            current = (P/name).read_text()
            require(current in (data.decode(), expected), 'Unexpected existing edit: ' + name)
            (P/name).write_text(expected)
    clarify_contact_squares()
    return {'baseline_source': SOURCE_V47, 'review_head': REVIEW_V47,
            'archived_exact_originals': list(CHANGES), 'baseline_active_inputs': len(old),
            'new_inputs': list(NEW_INPUTS), 'contact_centered_observation_squares': True,
            'mathematical_certification': False}


if __name__ == '__main__':
    print(json.dumps(materialize(), indent=2, sort_keys=True))
