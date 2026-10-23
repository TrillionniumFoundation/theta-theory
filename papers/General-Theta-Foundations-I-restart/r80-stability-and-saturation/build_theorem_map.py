#!/usr/bin/env python3
"""Rebuild the R80 author dependency maps from the actual native index.

Every one of the 252 predecessor proof records is preserved except current
locators and their display identity. New author-declared premises are
separate from mechanically extracted statement/immediate-proof references.
This is a source/dependency consistency tool, not a mathematical proof checker.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
sys.dont_write_bytecode = True
from verify import active_tex, without_comments

ROOT = Path(__file__).resolve().parent
OLD_LEDGER = "inputs/r79/THEOREM_DEPENDENCIES.json"
OLD_LEDGER_SHA256 = '9848e49e07e0d8ae3c988ecf88c108d11e93fa4476f542a8d7f4746aa91a9585'
BASE_SOURCE = '90cae2f5aca243b39d3a2194a4d6e0696671a101'
BASE_PUBLICATION = 'a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2'
REVIEW_COMMIT = "358481b21ceeeedb1205ebd30f86982e32a2cb04"
EXPECTED_INHERITED, EXPECTED_NEW, EXPECTED_CURRENT = 252, 15, 267
DECLARATIONS_PATH = "provenance/R80_DECLARED_STATEMENTS.json"
NEW_SOURCES = ['sections/57-sharp-stability.tex', 'sections/58-arithmetic-saturation.tex', 'sections/59-finite-search-saturation.tex']

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def native_statements(files: list[str]) -> tuple[dict, dict]:
    origins, statements = {}, {}
    pattern = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|example)\}"
                         r"(?:\[([^\]]*)\])?(.*?)\\end\{\1\}", re.S)
    for relative in files:
        text = without_comments((ROOT / relative).read_text(encoding="utf-8"))
        for label in re.findall(r"\\label\{([^}]+)\}", text):
            require(label not in origins or origins[label] == relative,
                    "Duplicated active label: " + label)
            origins[label] = relative
        for match in pattern.finditer(text):
            labels = re.findall(r"\\label\{((?:thm|lem|prop|cor|ex):[^}]+)\}", match.group(3))
            if not labels:
                continue
            require(len(labels) == 1, "Ambiguous statement labels in " + relative)
            label = labels[0]
            block = match.group(0)
            following = text[match.end():]
            proof = re.match(r"\s*\\begin\{proof\}(?:\[[^\]]*\])?.*?\\end\{proof\}", following, re.S)
            if proof:
                block += proof.group(0)
            references = set()
            for items in re.findall(r"\\(?:eqref|ref|cref|Cref|autoref|nameref)\{([^}]+)\}", block):
                references.update(item.strip() for item in items.split(","))
            statements[label] = {"kind": match.group(1), "title": (match.group(2) or "").strip(),
                                 "source": relative, "references": sorted(references)}
    return origins, statements


def linked_labels(labels: list[str]) -> str:
    return ", ".join("`" + label + "`" for label in labels) or "None listed in this category."


def build() -> dict[str, bytes]:
    old_bytes = (ROOT / OLD_LEDGER).read_bytes()
    require(sha(old_bytes) == OLD_LEDGER_SHA256, "The exact R79 proof authority differs")
    old = json.loads(old_bytes)
    old_rows = {row["label"]: row for row in old["statements"]}
    require(len(old_rows) == len(old["statements"]) == EXPECTED_INHERITED,
            "Expected all 252 unique R79 proof records")
    index_bytes = (ROOT / "THEOREM_INDEX.json").read_bytes()
    index = json.loads(index_bytes)
    require(index["schema"] == "theta.r80.compiled-theorem-index.v1",
            "An actual R80 native theorem index is required")
    rows = {row["label"]: row for row in index["statements"]}
    require(len(rows) == len(index["statements"]) == EXPECTED_CURRENT,
            "Expected exactly 267 current compiled statement labels")
    require(index["indexed_statement_count"] == EXPECTED_CURRENT
            and index["inherited_statement_count"] == EXPECTED_INHERITED
            and index["new_statement_count"] == EXPECTED_NEW,
            "Wrong inherited/current index counts")
    declaration_bytes = (ROOT / DECLARATIONS_PATH).read_bytes()
    declaration_list = json.loads(declaration_bytes)
    declarations = {row["label"]: copy.deepcopy(row) for row in declaration_list}
    require(len(declarations) == len(declaration_list) == EXPECTED_NEW,
            "Expected exactly the declared unique author additions")
    require({row["source"] for row in declarations.values()} == set(NEW_SOURCES),
            "Unexpected new mathematical source inventory")
    require(set(rows) == set(old_rows) | set(declarations)
            and not set(old_rows) & set(declarations),
            "Current label set differs from the fixed inherited-plus-new author inventory")
    files = list(dict.fromkeys(active_tex("main") + active_tex("supplement")))
    origins, native = native_statements(files)
    require(set(rows) <= set(native), "A compiled statement has no native body")
    bibkeys = set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}",
                             (ROOT / "references.tex").read_text()))
    catalog, new_rows, inherited_hashes = [], [], {}
    locator_fields = {"source", "document", "number", "page", "identity"}
    for locator in index["statements"]:
        label = locator["label"]
        require(origins[label] == locator["source"], "Wrong current source locator: " + label)
        require(locator["document"] in {"main", "supplement"}
                and type(locator["page"]) is int and locator["page"] > 0
                and isinstance(locator["number"], str) and bool(locator["number"]),
                "Invalid compiled document/number/page: " + label)
        if label in old_rows:
            record = copy.deepcopy(old_rows[label])
            inherited_hashes[label] = sha(canonical(old_rows[label]))
            for key in ("source", "document", "number", "page"):
                record[key] = locator[key]
            record["identity"] = ("Current R80 native locator; the exact R79 proof-authority "
                                  "record remains at inputs/r79/THEOREM_DEPENDENCIES.json.")
            # Preserve earlier retained_proof_authority and r74 fields exactly.
            # The immediate R79 layer has its own new keys rather than overwriting them.
            require(not {"inherited_from_r79", "retained_r79_record_sha256",
                         "r79_proof_authority"} & set(old_rows[label]),
                    "Unexpected preexisting R79 wrapper keys: " + label)
            record["inherited_from_r79"] = True
            record["retained_r79_record_sha256"] = inherited_hashes[label]
            record["r79_proof_authority"] = {"path": OLD_LEDGER, "label": label,
                                             "commit": BASE_SOURCE}
            for key, value in old_rows[label].items():
                if key not in locator_fields:
                    require(record[key] == value,
                            "Inherited nondisplay proof field changed: " + label + ":" + key)
        else:
            record = declarations[label]
            require(record["source"] == locator["source"],
                    "Declared/current source mismatch: " + label)
            for key in ("kind", "title", "source"):
                require(record[key] == native[label][key],
                        "Declared/native " + key + " differs: " + label)
            record.update({key: locator[key] for key in ("document", "number", "page")})
            record["inherited_from_r79"] = False
            record["identity"] = ("R80 numbered author addition; the inventory includes "
                                  "lemmas and corollaries and is not a novelty or editorial verdict.")
            record["explicit_statement_or_immediate_proof_references"] = [
                ref for ref in native[label]["references"] if ref in rows]
            record["other_explicit_references"] = [
                ref for ref in native[label]["references"] if ref not in rows]
            record["reference_extraction_scope"] = (
                "Statement and immediately following proof only; syntactic references "
                "are not automatically logical premises.")
            require(set(record["priority_keys"]) <= bibkeys,
                    "Undefined bibliography priority key: " + label)
            new_rows.append(record)
        for field in ("direct_dependencies", "inherited_mechanisms",
                      "supporting_definition_labels",
                      "explicit_statement_or_immediate_proof_references",
                      "other_explicit_references"):
            for dependency in record.get(field, []):
                require(dependency in origins,
                        "Undefined active " + field + ": " + label + " -> " + dependency)
        catalog.append(record)

    done, visiting = set(), set()
    def visit(label: str) -> None:
        require(label not in visiting, "New logical dependency cycle: " + label)
        if label in done or label not in declarations:
            return
        visiting.add(label)
        for dependency in declarations[label]["direct_dependencies"]:
            visit(dependency)
        visiting.remove(label)
        done.add(label)
    for label in declarations:
        visit(label)
    source_hashes = {name: sha((ROOT / name).read_bytes()) for name in NEW_SOURCES}
    dependency_labels = {dependency for row in new_rows
                         for field in ("direct_dependencies", "inherited_mechanisms")
                         for dependency in row[field] if dependency not in declarations}
    authority_hashes = {origins[label]: sha((ROOT / origins[label]).read_bytes())
                       for label in sorted(dependency_labels)}
    documents = {document: sum(row["document"] == document for row in new_rows)
                 for document in ("main", "supplement")}
    checks = {
        "current_compiled_statement_count": EXPECTED_CURRENT,
        "all_inherited_records_retained": EXPECTED_INHERITED,
        "new_declared_statement_count": EXPECTED_NEW,
        "all_inherited_nondisplay_proof_fields_unchanged": True,
        "earlier_retained_proof_authority_fields_unchanged": True,
        "all_current_label_references_resolve": True,
        "new_logical_dependency_graph_acyclic": True,
        "new_native_titles_kinds_sources_match": True,
        "all_declared_priority_keys_in_bibliography": True,
        "active_tex_file_count": len(files), "active_label_count": len(origins),
        "scope": "Author catalog, identity and dependency consistency; not a proof checker, native build, priority clearance or independent assessment."
    }
    semantics = (
        "direct_dependencies are author-declared logical premises. inherited_mechanisms "
        "record reused constructions or contextual authorities, including arguments "
        "proved again in full. Definition labels and internal facts are separate. "
        "Extracted LaTeX references are syntax, not an automatic logical graph.")
    addendum = {
        "schema": "theta.r80.author-dependency-addendum.v1",
        "paper": "General Theta Foundations I",
        "scope": "Fifteen numbered additions include a sharp fixed-memory singularity and two supporting lemmas; the finite-n search saddle, projected support rigidity, exact saturation criterion, explicit prior and memory bounds, effective rational cap and elementary fallback; and the full two-location refinement. Classical restatements, supporting lemmas and corollaries are identified separately. This is not a count of fifteen new discoveries.",
        "inherited_source_commit": BASE_SOURCE,
        "inherited_publication_commit": BASE_PUBLICATION,
        "controlling_referee_commit": REVIEW_COMMIT,
        "current_source_identity": "Source hashes and the actual compiled index bind this map; the final Git source identity is supplied by the later source/publication handshake.",
        "numbered_statement_count": EXPECTED_NEW,
        "main_statement_count": documents["main"],
        "supplement_statement_count": documents["supplement"],
        "retained_dependency_authority": OLD_LEDGER,
        "retained_dependency_authority_sha256": OLD_LEDGER_SHA256,
        "author_declarations": DECLARATIONS_PATH,
        "author_declarations_sha256": sha(declaration_bytes),
        "compiled_index_sha256": sha(index_bytes),
        "source_sha256": source_hashes,
        "inherited_dependency_source_sha256": authority_hashes,
        "reference_semantics": semantics,
        "statements": new_rows, "source_verification": checks,
        "verification_limits": [
            "Written author proofs are not proof-assistant certificates.",
            "Finite diagnostics do not prove continuum theorems, optimality or novelty.",
            "The R65 report evaluated R65, not the R66–R80 revisions.",
            "No independently verified human endorsement or editorial decision is asserted.",
            "A1/A2 and the wider Theta pipeline retain their own proof obligations."]
    }
    full = {
        "schema": "theta.r80.author-dependencies.v1",
        "paper": "General Theta Foundations I",
        "controlling_predecessor_source_commit": BASE_SOURCE,
        "base_publication_commit": BASE_PUBLICATION,
        "inherited_statement_count": EXPECTED_INHERITED,
        "added_statement_count": EXPECTED_NEW,
        "expected_current_statement_count": EXPECTED_CURRENT,
        "compiled_locator": "Actual native main/supplement index; the strict source-bound build must reproduce every document, number, page and source.",
        "compiled_index_sha256": sha(index_bytes),
        "declared_current_proof_addendum": "provenance/R80_PROOF_DEPENDENCIES.json",
        "retained_dependency_authority": OLD_LEDGER,
        "retained_dependency_authority_sha256": OLD_LEDGER_SHA256,
        "reference_semantics": semantics,
        "statements": catalog,
        "inherited_proof_record_sha256": inherited_hashes,
        "historical_dependency_ledgers": copy.deepcopy(old["historical_dependency_ledgers"]),
        "superseded_duplicate_drafts": copy.deepcopy(old["superseded_duplicate_drafts"]),
        "inherited_instrument_authorities": copy.deepcopy(old["inherited_instrument_authorities"]),
        "historical_label_boundary": "Earlier embedded ledgers retain historical renamed labels and old edition-relative wording. They are not new graph edges or claims of R80 novelty. Every current reference resolves, and all 252 old nondisplay proof fields retain their exact values.",
        "source_verification": checks, "research_status": "RESEARCH_STATUS.md",
        "limitations": "Author map, not formal proof checking, priority clearance, independent human assessment or editorial approval."
    }
    count_sentence = (f"The actual paired native index has **{EXPECTED_CURRENT} statement labels**: "
                      f"all **{EXPECTED_INHERITED} inherited R79 labels** and **{EXPECTED_NEW} additions** "
                      f"({documents['main']} main, {documents['supplement']} supplement). "
                      "Supporting lemmas and corollaries are included; this is not a novelty count. "
                      "The independent R58 companion keeps its separate source and numbering.")
    lines = ["# Theorem and dependency map — General Theta Foundations I, R80", "",
             count_sentence, "", "## Main proof chains and scope", "",
             "| Chain | Conclusion and mathematical boundary |", "|---|---|",
             "| General finite-dimensional instruments → inherited reachable-support potentials | Common controller, model-dependent supports; exact robust quantifier order and compact semialgebraic synthesis without all-label properness. |",
             "| All-initial-state cost → random return to the counted initial label | Initial cost b/(1-epsilon*b/c_*) and full-space cost c^*/epsilon+U, with exactly the same M labels and no physical reset. |",
             "| Bounded full-space witnesses → centered primitive transfer → same-size optimizer | A local square-root upper modulus for the entire cost frontier, uniform in all M and valid across support changes. |",
             "| Uniform per-command success floor → full-space contraction → exact scalar lower | Lipschitz dependence zeta/kappa+c^* eta/kappa^2 for all M, with locally sharp coefficients; geometric history-horizon approximation. This is a stronger hypothesis and a classical resolvent refinement. |",
             "| Counted finite prefixes → one-row completion | The inherited general finite-memory values decrease to the history infimum. Exact saturation requires an additional structural argument. |",
             "| Two fixed hidden models → sharp two-label lower bound → explicit realization | Exact frontier 2, golden ratio, 3/2 thereafter; pure initializer charged and model-specific dark-label support required. |",
             "| Positive-polynomial baseline inequality → unique effective boundary optimum → coercivity | Exact baseline value and opposite-orientation gap over all stochastic two-label controllers. Local row and escape scales are proved, not assumed. |",
             "| Activated dark label → compactness of all optimizers → matching asymptotic | V2(epsilon)=B0+c0*sqrt(epsilon)+o(sqrt(epsilon)); the general exponent 1/2 is optimal already at M=2. The leading constant is specific to this family. |",
             "| Classical finite-n saddle → projected commensurability classes → finite support-set rigidity | For every finite number of imperfect search locations and arbitrary positive costs, finite stochastic saturation is equivalent to rationality of every failure-log ratio, including partial commensurability. |",
             "| Classical common-power cycles → counted initial mixture → finite synthesis cap | Positive rational prime-exponent collinearity decides saturation; an explicit primitive-data cap gives algebraic synthesis for arbitrary rational positive costs. No polynomial or minimal-label claim. |",
             "| Command deletion → uniform least-favourable prior bound → geometric greedy tails | An explicit delta from primitive data controls all optimal priors and removes an unknown saddle parameter from the resource bound. |",
             "| At most n consistent priorities → n counted prefixes → one-label fallback | For all M>=n the cost gap is at most B*A*kappa^floor(M/n); every nonsaturating finite gap is strict. The supplement retains sharper normalized two-location constants; no matching lower rate is asserted. |",
             "| All-state reset primitives → same-row Bellman reduction | Deterministic report-only routing dominates every stochastic update using the existing rows. Mixed commands remain allowed; no strict exposure assumption. |",
             "| Same-row reduction → explicit compact cap → supersolution certificate | Exact attained cost at every live-memory budget, including PSD effects and ties; finite algebraic synthesis, without a polynomial claim. |",
             "| Proper controller perturbation → compact lower limits | Continuity of the complete finite-memory values; strict gaps persist within valid instruments. |",
             "| Physical action-cover family → continuing-row purification → capped simplex | Complete all-memory formula for any finite action-cover incidence system; a uniform-subset initializer attains it. |",
             "| Singleton cover → exact staircase → compatible noncommuting perturbation | Arbitrarily many strict resource improvements in dimension 2n, a factor-two comparison with the old residual certificate, and stable strict inequalities. The exact formula is for the unperturbed family. |",
             "| Inherited shared preparation / Fourier / approximation chains | All R79 shared-device, initialization and unrestricted-decoder results remain active at their exact hypotheses. |",
             "| Inherited general causal / measurement / rank / dual / geometry results | All 252 previous statement labels and full proof bodies remain current; the R58 companion retains its independent scope. |", "",
             "[THEOREM_DEPENDENCIES_R80.md](THEOREM_DEPENDENCIES_R80.md) lists each new statement's exact hypotheses, logical premises, proof mechanism, priority boundary and limits. Its structured counterpart is `provenance/R80_PROOF_DEPENDENCIES.json`. The complete current catalog retains the exact predecessor at `inputs/r79/THEOREM_DEPENDENCIES.json`; all older R74–R79 addenda remain unchanged.", "",
             "Logical premises, reused/contextual mechanisms, definition labels, internal proof facts and mechanically extracted references are distinct fields. All current referenced labels resolve. Earlier proof-authority fields are preserved byte-for-value; a new `r79_proof_authority` layer does not overwrite them.", "",
             "## Actual compiled locators", "",
             "These locators come from the actual paired auxiliary files via `THEOREM_INDEX.json`. M means main and S means current supplement; moving a full proof body changes its locator, not its historical authority.", "",
             "| Document | Number | Page | Label | Source | Role |",
             "|---|---|---:|---|---|---|"]
    for row in catalog:
        role = "Inherited R79 authority" if row["inherited_from_r79"] else "R80 numbered addition"
        lines.append(f"| {'M' if row['document']=='main' else 'S'} | {row['number']} | {row['page']} | `{row['label']}` | `{row['source']}` | {role} |")
    lines += ["", "## Identity and evidence limits", "",
              f"The compiled-index SHA-256 is `{sha(index_bytes)}`. The predecessor-ledger SHA-256 is `{OLD_LEDGER_SHA256}`. The generator checks 252 unchanged nondisplay proof records, fifteen native title/kind/source matches, every current referenced label and acyclicity of the new declared dependency graph. It does not prove the mathematics or certify priority.", "",
              "Run `python build_theorem_map.py` to regenerate or `python build_theorem_map.py --check` to require exact byte identity. Regeneration requires the actual 267-entry paired native index. A changed index or proof source requires regenerated maps and a new source seal.", ""]
    detail = ["# R80 theorem dependencies, hypotheses and claim boundaries", "",
              "This is the author dependency addendum for General Theta Foundations I. " + count_sentence, "",
              "## Reading the map", "",
              "Direct logical prerequisites are actual premises of the proof. Inherited mechanisms identify related retained arguments or a construction reproduced in full. Definition labels and internal facts are separate. Automatically extracted references in the structured record are syntactic evidence and do not replace this author analysis.", "",
              "The actual compiled index and every new proof source are hashed in `provenance/R80_PROOF_DEPENDENCIES.json`. The final Git identity is supplied by the source/publication handshake. Current native kind is authoritative: a label beginning `thm:` may name a compiled corollary and is not counted again as an independent theorem.", ""]
    for i, row in enumerate(new_rows, 1):
        detail += [f"## {i}. {row['title']}", "",
                   f"**Native locator:** {row['document']}, {row['kind']} {row['number']}, page {row['page']}; `{row['label']}` in `{row['source']}`.", "",
                   "**Hypotheses.** " + " ".join(row["hypotheses"]), "",
                   "**Conclusion.** " + row["conclusion"], "",
                   "**Direct logical prerequisites.** " + linked_labels(row["direct_dependencies"]), "",
                   "**Inherited mechanisms and contextual authorities.** " + linked_labels(row["inherited_mechanisms"]), "",
                   "**Proof mechanism.** " + row["proof"], "",
                   "**Classical ingredients and priority boundary.** " + "; ".join(row["classical_ingredients"]) + ". " + row["claim_class"], "",
                   "**Limits.** " + row["limits"], ""]
    detail += ["## Retained authority and unresolved questions", "",
               "All 252 predecessor proof records retain every nondisplay field unchanged. Current document, number, page, source and locator-description fields are refreshed. The original ledger remains byte-identical, as do the R74–R79 addenda and all protected proof bodies. Edition-relative words such as 'new' within an unchanged old record refer to that original edition, not to R80.", "",
               "The original general-M squared-sign risk frontier, optional-stopping tied control and universal finite-memory saturation, unrestricted high-contrast classification for every finite group, the matching unrestricted-decoder approximation rate, intermediate timing, coefficient-bit/precision/program/workspace costs, unknown-model recovery and independent Theta objectives remain distinct. In particular matrix parameter-feasibility equivalence does not classify every off-boundary positive factorization, and a sharp excursion probability is not a sharp universal approximation cost. The inherited R76 matching leading logarithm applies only to the stated fixed physical density dictionaries with Born terminal decoders, at fixed positive target budget and a fixed badly approximable phase.", "",
               "## Evidence categories", "",
               "The written proofs are ordinary author arguments. Author-team AI challenges, finite exact/floating diagnostics, native compilation, source hashing, independent human assessment and editorial decisions remain separate evidence types. General real quantifier elimination is an existence/computability ingredient; these maps do not claim it was executed. The R65 deposited report is not reclassified as a review of R80.", "",
               "Regenerate with `python build_theorem_map.py` and check with `python build_theorem_map.py --check`. Missing labels, a different inherited authority, altered nondisplay old proof fields or an incomplete current statement inventory are rejected.", ""]
    return {"THEOREM_DEPENDENCIES.json": canonical(full),
            "provenance/R80_PROOF_DEPENDENCIES.json": canonical(addendum),
            "THEOREM_MAP.md": "\n".join(lines).encode(),
            "THEOREM_DEPENDENCIES_R80.md": "\n".join(detail).encode()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Require byte-identical maps without writing")
    args = parser.parse_args()
    generated = build()
    for name, data in generated.items():
        path = ROOT / name
        if args.check:
            require(path.is_file() and path.read_bytes() == data,
                    "Generated map differs: " + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print(json.dumps({"status": "PASS", "mode": "check" if args.check else "write",
                      "scope": "Author dependency-map consistency, not mathematical proof verification",
                      "inherited": EXPECTED_INHERITED, "added": EXPECTED_NEW,
                      "current": EXPECTED_CURRENT,
                      "outputs": {name: sha(data) for name, data in generated.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()


