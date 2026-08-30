# Round-three build failures

- Overall status: **FAIL**
- Passed: **4/11**
- Failed papers: `A2-sinai-homological-pressure, A3-full-empirical-path-ldp, B1-microcanonical-preparation, B2-collision-clusters-dynamic-ldp, B3-hamilton-boltzmann-cotangents, B4-nonlinear-kinetic-semigroups, C1-information-risk-sensitive-saddles`

## A2-sinai-homological-pressure

Return code: `12`

```text
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msa.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msb.cfg) [1{/var/lib/texm
f/fonts/map/pdftex/updmap/pdftex.map}{/usr/share/texmf/fonts/enc/dvips/lm/lm-ec
.enc}{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathsy.enc}{/usr/share/texmf/fonts
/enc/dvips/lm/lm-rm.enc}{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathit.enc}]
[2{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathex.enc}]

LaTeX Warning: Reference `lem:r3-a2-geometry' on page 3 undefined on input line
 141.


LaTeX Warning: Reference `lem:r3-a2-multiplier' on page 3 undefined on input li
ne 177.

[3] [4]
```

```text



LaTeX Warning: Reference `thm:r3-a2-high' on page 5 undefined on input line 299
.


LaTeX Warning: Reference `thm:r3-a2-spectrum' on page 5 undefined on input line
 329.


Overfull \hbox (4.6302pt too wide) detected at line 336
\OML/lmm/m/it/10.95 P[]\OT1/lmr/m/n/10.95 (\OML/lmm/m/it/10.95 ^^X \OT1/lmr/m/n
/10.95 + \OML/lmm/m/it/10.95 iu; s \OT1/lmr/m/n/10.95 + \OML/lmm/m/it/10.95 it\
OT1/lmr/m/n/10.95 ) \OMS/lmsy/m/n/10.95 ^^@ \OML/lmm/m/it/10.95 P[]\OT1/lmr/m/n
```

```text
5 u; t\OT1/lmr/m/n/10.95 )\OML/lmm/m/it/10.95 ; \OT1/lmr/m/n/10.95 ^^F[](\OML/l
mm/m/it/10.95 u; t\OT1/lmr/m/n/10.95 )\OMS/lmsy/m/n/10.95 i \OT1/lmr/m/n/10.95 
+ \OML/lmm/m/it/10.95 O\OT1/lmr/m/n/10.95 (\OMS/lmsy/m/n/10.95 j\OT1/lmr/m/n/10
.95 (\OML/lmm/m/it/10.95 u; t\OT1/lmr/m/n/10.95 )\OMS/lmsy/m/n/10.95 j[]\OT1/lm
r/m/n/10.95 )\OML/lmm/m/it/10.95 :
[5]

LaTeX Warning: Reference `lem:r3-a2-cov' on page 6 undefined on input line 338.



LaTeX Warning: Reference `thm:r3-a2-high' on page 6 undefined on input line 346
.


```

```text


./ROUND3_POSITIVE_CLOSURE.tex:361: Missing \right. inserted.
<inserted text> 
                \right .
l.361 \]
        
./ROUND3_POSITIVE_CLOSURE.tex:361:  ==> Fatal error occurred, no output PDF fil
e produced!
Transcript written on main.log.
Latexmk: Missing bbl file 'main.bbl' in following:
 No file main.bbl.
Latexmk: Missing input file 'main.toc' (or dependence on it) from following:
  No file main.toc.
Latexmk: Incomplete (and hence corrupt) bcf file 'main.bcf'
```

```text
  I'll rename the file to 'main.bcf-SAVE-ERROR'.
  I'll rename the bbl file to 'main.bbl-SAVE-ERROR',
  in case the incomplete bcf file was a result of error in
  'pdflatex' caused by an error in the bbl file.
Latexmk: ====Undefined refs and citations with line #s in .tex file:
  Reference `lem:r3-a2-geometry' on page 3 undefined on input line 141
  Reference `lem:r3-a2-multiplier' on page 3 undefined on input line 177
  Reference `lem:r3-a2-uni' on page 5 undefined on input line 264
  Reference `lem:r3-a2-uni' on page 5 undefined on input line 264
  Reference `thm:r3-a2-high' on page 5 undefined on input line 299
  Reference `thm:r3-a2-spectrum' on page 5 undefined on input line 329
  Reference `lem:r3-a2-cov' on page 6 undefined on input line 338
 And 4 more --- see log file 'main.log'
Latexmk: Sometimes, the -f option can be used to get latexmk
  to try to force complete processing.
```

## A3-full-empirical-path-ldp

Return code: `12`

```text
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msa.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msb.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/ueuf.fd)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-euf.cfg) [1{/var/lib/texm
f/fonts/map/pdftex/updmap/pdftex.map}{/usr/share/texmf/fonts/enc/dvips/lm/lm-ec
.enc}{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathit.enc}{/usr/share/texmf/fonts
/enc/dvips/lm/lm-rm.enc}{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathsy.enc}]
./ROUND3_POSITIVE_CLOSURE.tex:32: Missing } inserted.
<inserted text> 
                }
l.32 ...{\eta r+\eta\mathfrak t}\,d\widehat\mathbb
                                                   P<\infty;
./ROUND3_POSITIVE_CLOSURE.tex:32:  ==> Fatal error occurred, no output PDF file
 produced!
Transcript written on main.log.
```

## B1-microcanonical-preparation

Return code: `12`

```text
(./ROUND3_POSITIVE_CLOSURE.tex
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msa.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msb.cfg) [1{/var/lib/texm
f/fonts/map/pdftex/updmap/pdftex.map}{/usr/share/texmf/fonts/enc/dvips/lm/lm-ec
.enc}{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathit.enc}{/usr/share/texmf/fonts
/enc/dvips/lm/lm-rm.enc}{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathex.enc}{/us
r/share/texmf/fonts/enc/dvips/lm/lm-mathsy.enc}]
./ROUND3_POSITIVE_CLOSURE.tex:55: Missing $ inserted.
<inserted text> 
                $
l.55  \left(^^L
               rac1{\mu_\varepsilon}\sum_iC(z_i(0))\right).
./ROUND3_POSITIVE_CLOSURE.tex:55:  ==> Fatal error occurred, no output PDF file
 produced!
Transcript written on main.log.
```

## B2-collision-clusters-dynamic-ldp

Return code: `12`

```text
Underfull \hbox (badness 1005) in paragraph at lines 126--130
[]\T1/lmr/bx/n/10.95 (+20) Lemma 1.3 \T1/lmr/m/n/10.95 (+20) (Al-l--con-tact ex
-po-nen-tial gen-er-at-ing bound)\T1/lmr/bx/n/10.95 (+20) . []\T1/lmr/m/it/10.9
5 (+20) There are
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/ueuf.fd)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-euf.cfg)

LaTeX Warning: Reference `lem:r3-b2-first-cycle' on page 3 undefined on input l
ine 162.

[3]

LaTeX Warning: Reference `lem:r3-b2-generating' on page 4 undefined on input li
ne 204.

```

```text
LaTeX Warning: Reference `prop:r3-b2-balance' on page 5 undefined on input line
 264.


LaTeX Warning: Reference `thm:r3-b2-gc-cluster' on page 5 undefined on input li
ne 280.

./ROUND3_POSITIVE_CLOSURE.tex:282: Missing { inserted.
<to be read again> 
                   \begingroup 
l.282 exponential moment for \(\Gamma^

                                       arepsilon(1)\), including recollisions.
./ROUND3_POSITIVE_CLOSURE.tex:282:  ==> Fatal error occurred, no output PDF fil
e produced!
```

```text
Latexmk: Incomplete (and hence corrupt) bcf file 'main.bcf'
Latexmk: ========== Incomplete bcf_file 'main.bcf'.
  I'll rename the file to 'main.bcf-SAVE-ERROR'.
  I'll rename the bbl file to 'main.bbl-SAVE-ERROR',
  in case the incomplete bcf file was a result of error in
  'pdflatex' caused by an error in the bbl file.
Latexmk: ====Undefined refs and citations with line #s in .tex file:
  Reference `lem:r3-b2-first-cycle' on page 3 undefined on input line 162
  Reference `lem:r3-b2-generating' on page 4 undefined on input line 204
  Reference `prop:r3-b2-balance' on page 5 undefined on input line 264
  Reference `thm:r3-b2-gc-cluster' on page 5 undefined on input line 280
Latexmk: Sometimes, the -f option can be used to get latexmk
  to try to force complete processing.
  But normally, you will need to correct the file(s) that caused the
  error, and then rerun latexmk.
```

## B3-hamilton-boltzmann-cotangents

Return code: `12`

```text
No file main.toc.
(./ROUND3_POSITIVE_CLOSURE.tex
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msa.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msb.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/ueuf.fd)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-euf.cfg)

./ROUND3_POSITIVE_CLOSURE.tex:20: LaTeX Error: Unicode character ^^H (U+0008)
               not set up for use with LaTeX.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...                                              
                                                  
l.20  ^^H
```

## B4-nonlinear-kinetic-semigroups

Return code: `12`

```text
/lmtt/m/n/10.95 ROUND3-POSITIVE-CLOSURE\T1/lmr/m/n/10.95 (-20) . 
No file main.toc.
(./ROUND3_POSITIVE_CLOSURE.tex
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msa.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msb.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/ueuf.fd)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-euf.cfg)
./ROUND3_POSITIVE_CLOSURE.tex:17: Missing $ inserted.
<inserted text> 
                $
l.17  \|G\|_\alpha=\sum_{k\ge0}^^L
                                  rac{e^{\alpha k}}{k!}
./ROUND3_POSITIVE_CLOSURE.tex:17:  ==> Fatal error occurred, no output PDF file
 produced!
Transcript written on main.log.
```

## C1-information-risk-sensitive-saddles

Return code: `12`

```text
(./ROUND3_POSITIVE_CLOSURE.tex
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msa.cfg)
(/usr/share/texlive/texmf-dist/tex/latex/microtype/mt-msb.cfg) [1{/var/lib/texm
f/fonts/map/pdftex/updmap/pdftex.map}{/usr/share/texmf/fonts/enc/dvips/lm/lm-ec
.enc}{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathit.enc}{/usr/share/texmf/fonts
/enc/dvips/lm/lm-mathsy.enc}{/usr/share/texmf/fonts/enc/dvips/lm/lm-rm.enc}]
[2{/usr/share/texmf/fonts/enc/dvips/lm/lm-mathex.enc}]
./ROUND3_POSITIVE_CLOSURE.tex:140: Missing $ inserted.
<inserted text> 
                $
l.140  \int\ell\left(^^L
                        rac{d\Gamma}{q^{u,v}dA_f}\right)
./ROUND3_POSITIVE_CLOSURE.tex:140:  ==> Fatal error occurred, no output PDF fil
e produced!
Transcript written on main.log.
```
