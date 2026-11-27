#!/usr/bin/env python3
"""Tools for a "better verifiers" ladder: read the top of the board, build an entry, check it.

    ladder_tool.py top   --track TRACK_ID [--api URL] [--root DIR] --out top.json
    ladder_tool.py new   --top top.json --verifier verifier.md --cases cases.md
                         --argument argument.md --title "..." --out submission [--root DIR]
                         [--not-favored ENTRY ...]
    ladder_tool.py check submission [--root DIR]
    ladder_tool.py audit --track TRACK_ID [--api URL] [--root DIR]

--root is the challenge folder (the one holding checkers/ladder.json); it defaults to
the folder above this file. Reads use Yukon's public API and need no key.
"""

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_API = "https://yukon-api-dev.fly.dev"
OPENING = "opening"
PART_CAP = 7900          # a claim holds 8,000 characters; the heading takes a few
MAX_PARTS = 2
CLAIM_HEAD = "LADDER CLAIM (better-verifiers-v1), ladder "


def root_of(args):
    return Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent


def ladder_of(root):
    return json.loads((root / "checkers" / "ladder.json").read_text(encoding="utf-8"))


def gate_of(root):
    spec = importlib.util.spec_from_file_location("ladder_gate", root / "checkers" / "ladder_gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decide


def get(api, path):
    request = urllib.request.Request(api.rstrip("/") + path, headers={"accept": "application/json", "user-agent": "ladder-tool"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def opening_text(root):
    parts = (root / "opening.md").read_text(encoding="utf-8").split("\n-----\n")
    if len(parts) < 3:
        sys.exit("opening.md does not hold a verifier between two lines of dashes")
    return parts[1].strip()


def joined(claims, word):
    """The text carried by the VERIFIER or CASES claims of a manifest, parts in order."""
    found = {}
    for claim in claims:
        if isinstance(claim, str):
            match = re.match(rf"{word} (\d)/(\d)\n", claim)
            if match:
                found[int(match.group(1))] = (int(match.group(2)), claim[match.end():])
    if not found:
        return ""
    count = next(iter(found.values()))[0]
    if sorted(found) != list(range(1, count + 1)) or any(total != count for total, _ in found.values()):
        raise ValueError(f"{word} parts are not numbered 1..n")
    return "\n".join(found[i][1] for i in range(1, count + 1))


def read_entry(manifest, ladder_id):
    """Score, verifier and cases of a ladder manifest; raises ValueError if it is not one."""
    claims = manifest.get("claims") or []
    head = claims[0] if claims else None
    if not isinstance(head, dict) or not head.get("statement", "").startswith(CLAIM_HEAD + ladder_id + "."):
        raise ValueError("claims[0] is not a ladder claim of this ladder")
    score = head.get("score") or {}
    if score.get("denominator") != "1" or not re.fullmatch(r"[1-9][0-9]*", score.get("numerator", "")):
        raise ValueError("the ladder claim's score is not a whole number")
    return {"score": int(score["numerator"]), "verifier": joined(claims, "VERIFIER"), "cases": joined(claims, "CASES"),
            "cited": [c for c in next((x["inputs"]["cited"] for x in manifest.get("checks", [])
                                       if x.get("check") == "ladder_gate"), [])]}


def accepted_entries(api, track, ladder_id):
    """Accepted entries of the track, each with its manifest as the platform recorded it."""
    listing = get(api, f"/api/benchmarks/{track}/submissions")
    if listing is None:
        sys.exit("no such track on this API")
    entries = []
    for row in listing.get("submissions", []):
        if row.get("status") != "accepted":
            continue
        record = get(api, f"/api/submissions/{row['id']}/accepted-results")
        if record is None:
            continue
        text = record["bundle"]["text"]
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != record["bundle"]["sha256"]:
            sys.exit(f"record of {row['id']} does not match its digest")
        manifest = json.loads(json.loads(text)["source"]["manifest"]["text"])
        try:
            entry = read_entry(manifest, ladder_id)
        except ValueError as error:
            print(f"skipped {row['id']}: {error}", file=sys.stderr)
            continue
        if row.get("officialScore") is not None and int(row["officialScore"]) != entry["score"]:
            sys.exit(f"{row['id']}: the board's score and the manifest's score differ")
        entries.append({"entry": row["id"], "solver": row.get("solverUsername"), "title": manifest.get("title"),
                        "submitted_at": record["submitted_at"], "accepted_at": record["completed_at"],
                        "challenge_id": record.get("challenge_id"), **entry})
    return entries


def top_of(entries, cite, opening, before=None):
    """The entries a new entry must cite: the `cite` highest, most recently accepted first among equals."""
    pool = [e for e in entries if before is None or e["accepted_at"] < before]
    pool.sort(key=lambda e: e["accepted_at"], reverse=True)
    pool.sort(key=lambda e: e["score"], reverse=True)
    chosen = pool[:cite]
    if len(chosen) < cite:
        chosen.append(opening)
    return chosen


def cmd_top(args):
    root = root_of(args)
    ladder = ladder_of(root)
    opening = {"entry": OPENING, "score": 1, "verifier": opening_text(root), "cases": "", "title": "Opening entry"}
    entries = accepted_entries(args.api, args.track, ladder["ladder"])
    chosen = top_of(entries, ladder["cite"], opening)
    best = max(e["score"] for e in chosen)
    Path(args.out).write_text(json.dumps({"ladder": ladder, "track": args.track, "api": args.api, "top": chosen},
                                         indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ladder {ladder['ladder']}: height {ladder['height']}, {len(entries)} accepted entries besides the opening one")
    for place, entry in enumerate(chosen, 1):
        print(f"  {place}. score {entry['score']}  {entry['entry']}  {entry.get('title') or ''}")
    if best >= ladder["height"]:
        print("the ladder is finished: its height is reached")
    else:
        print(f"an entry favored over all of them takes score {best + 1}; written {args.out}")


def split_parts(text, word):
    text = text.strip()
    if len(text) <= PART_CAP:
        return [f"{word} 1/1\n{text}"]
    cut = text.rfind("\n", 0, PART_CAP)
    cut = cut if cut > 0 else PART_CAP
    first, rest = text[:cut], text[cut:].lstrip("\n")
    if len(rest) > PART_CAP:
        sys.exit(f"{word.lower()} text is too long: at most {MAX_PARTS} parts of {PART_CAP} characters")
    return [f"{word} 1/2\n{first}", f"{word} 2/2\n{rest}"]


def cmd_new(args):
    root = root_of(args)
    ladder = ladder_of(root)
    top = json.loads(Path(args.top).read_text(encoding="utf-8"))["top"]
    lost = set(args.not_favored or [])
    if lost - {e["entry"] for e in top}:
        sys.exit("--not-favored names an entry that is not in the top file")
    cited = [{"entry": e["entry"], "score": e["score"], "favored": e["entry"] not in lost} for e in top]
    over = [c for c in cited if c["favored"]]
    under = [c for c in cited if not c["favored"]]
    if not over:
        sys.exit("an entry must claim to be favored over at least one cited entry")
    score = max(c["score"] for c in over) + 1
    if under:
        score = min(score, min(c["score"] for c in under))
    result = gate_of(root)({"score": score, "cited": cited}, ladder)
    if not result["passed"]:
        sys.exit("this entry cannot be built: " + result["message"])

    def listed(items):
        return "; ".join(f"{c['entry']} (score {c['score']})" for c in items)

    head = CLAIM_HEAD + ladder["ladder"] + ". This entry's verifier is the text of the VERIFIER claims of this manifest. "
    if ladder["accept"] == "top":
        statement = (head + "It reflects the goal more closely than each of these cited entries: " + listed(cited)
                     + f". The highest cited score is {max(c['score'] for c in cited)}, so this entry's ladder score is {score}.")
    else:
        statement = (head + "It is favored over these cited entries: " + listed(over)
                     + ". It is not favored over these cited entries: " + (listed(under) if under else "none")
                     + f". Its ladder score is {score}.")
    claims = [{"statement": statement, "score": {"numerator": str(score), "denominator": "1"}, "evidence": ["argument.md"]}]
    claims += split_parts(Path(args.verifier).read_text(encoding="utf-8"), "VERIFIER")
    claims += split_parts(Path(args.cases).read_text(encoding="utf-8"), "CASES")
    manifest = {"version": 1, "title": args.title[:300], "claims": claims, "experiments": [],
                "checks": [{"check": "ladder_gate", "inputs": {"score": score, "cited": cited}}]}
    prior = [{"submission_id": c["entry"]} for c in cited if c["entry"] != OPENING]
    if prior:
        manifest["prior_results"] = prior
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "submission.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "argument.md").write_text(Path(args.argument).read_text(encoding="utf-8"), encoding="utf-8")
    print(f"entry written to {out}: claims score {score}, cites {listed(cited)}")


def check_entry(folder, root):
    """Problems with the form of an entry; an empty list means the form is right."""
    ladder, problems = ladder_of(root), []
    try:
        manifest = json.loads((folder / "submission.json").read_text(encoding="utf-8"))
        entry = read_entry(manifest, ladder["ladder"])
    except (OSError, ValueError) as error:
        return [f"submission.json: {error}"]
    claims = manifest["claims"]
    statement = claims[0]["statement"]
    if claims[0].get("evidence") != ["argument.md"] or not (folder / "argument.md").is_file():
        problems.append("the ladder claim's evidence must be argument.md, and the file must exist")
    kinds = ["VERIFIER" if isinstance(c, str) and c.startswith("VERIFIER ") else
             "CASES" if isinstance(c, str) and c.startswith("CASES ") else "?" for c in claims[1:]]
    if "?" in kinds or kinds != sorted(kinds, reverse=True) or not 1 <= kinds.count("VERIFIER") <= MAX_PARTS:
        problems.append("after the ladder claim come one or two VERIFIER claims, then the CASES claims, nothing else")
    if any(len(c) > 8000 for c in claims[1:] if isinstance(c, str)) or len(statement) > 8000:
        problems.append("a claim is longer than 8,000 characters")
    if not entry["verifier"].strip():
        problems.append("the verifier text is empty")
    checks = [c for c in manifest.get("checks", []) if c.get("check") == "ladder_gate"]
    if len(checks) != 1 or len(manifest.get("checks", [])) != 1:
        return problems + ["exactly one check, ladder_gate, is declared"]
    payload = checks[0]["inputs"]
    result = gate_of(root)(payload, ladder)
    if not result["passed"]:
        problems.append("ladder_gate would fail: " + result["message"])
    if payload.get("score") != entry["score"]:
        problems.append("the gate input's score differs from the ladder claim's score")
    cited = payload.get("cited", [])
    opening = "This is the opening entry." in statement
    if opening != (not cited):
        problems.append("only the opening entry cites nothing")
    for c in cited:
        if f"{c['entry']} (score {c['score']})" not in statement:
            problems.append(f"the ladder claim does not name {c['entry']} with score {c['score']}")
    prior = sorted(p["submission_id"] for p in manifest.get("prior_results", []))
    if prior != sorted(c["entry"] for c in cited if c["entry"] != OPENING):
        problems.append("prior_results must list exactly the cited submissions")
    if cited and not entry["cases"].strip():
        problems.append("an entry that cites others needs at least one case")
    return problems


def cmd_check(args):
    problems = check_entry(Path(args.folder), root_of(args))
    for problem in problems:
        print("problem: " + problem)
    if problems:
        sys.exit(1)
    print("form is right. This does not judge the verifier; run llm-verifier preflight for the package limits.")


def cmd_audit(args):
    """For every accepted entry, compare what it cited with what stood at the top when it was submitted."""
    root = root_of(args)
    ladder = ladder_of(root)
    opening = {"entry": OPENING, "score": 1}
    entries = accepted_entries(args.api, args.track, ladder["ladder"])
    by_id = {e["entry"]: e for e in entries}
    clean = True
    for entry in sorted(entries, key=lambda e: e["submitted_at"]):
        due = [e["entry"] for e in top_of(entries, ladder["cite"], opening, before=entry["submitted_at"])]
        cited = [c["entry"] for c in entry["cited"]]
        wrong_scores = [c["entry"] for c in entry["cited"]
                        if c["score"] != (1 if c["entry"] == OPENING else by_id.get(c["entry"], {}).get("score"))]
        note = []
        if set(cited) != set(due):
            note.append("skipped " + ", ".join(sorted(set(due) - set(cited))) if set(due) - set(cited) else "cited entries outside the top")
        if wrong_scores:
            note.append("cited score differs from the board for " + ", ".join(wrong_scores))
        clean = clean and not note
        print(f"{entry['submitted_at']}  score {entry['score']:>3}  {entry['entry']}  " + ("; ".join(note) or "cited the top as it stood"))
    best = max([e["score"] for e in entries] or [1])
    print(f"{len(entries)} accepted entries; highest score {best} of {ladder['height']}"
          + ("; the ladder is finished" if best >= ladder["height"] else ""))
    sys.exit(0 if clean else 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("top", "audit"):
        p = sub.add_parser(name)
        p.add_argument("--track", required=True)
        p.add_argument("--api", default=DEFAULT_API)
        p.add_argument("--root")
        if name == "top":
            p.add_argument("--out", required=True)
    p = sub.add_parser("new")
    for flag in ("--top", "--verifier", "--cases", "--argument", "--title", "--out"):
        p.add_argument(flag, required=True)
    p.add_argument("--not-favored", nargs="*")
    p.add_argument("--root")
    p = sub.add_parser("check")
    p.add_argument("folder")
    p.add_argument("--root")
    args = parser.parse_args()
    {"top": cmd_top, "new": cmd_new, "check": cmd_check, "audit": cmd_audit}[args.command](args)


if __name__ == "__main__":
    main()
