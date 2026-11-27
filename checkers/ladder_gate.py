"""Ladder gate: the arithmetic of the ladder, decided by code.

It reads one declared payload, never a submitted file:

    {"score": K, "cited": [{"entry": ID, "score": S, "favored": true|false}, ...]}

and the protected ladder.json beside it (height, how many entries are cited, which
placements are accepted). It passes only when K is the score the ladder rule gives for
exactly that payload. Whether the cited entries are real, whether their scores are
right and whether the entry really is favored over them is the reviewer's part.
"""

import json
import os
import re
import sys

OPENING = "opening"
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


def decide(payload, ladder):
    height, top_k, accept = ladder["height"], ladder["cite"], ladder["accept"]
    score, cited = payload["score"], payload["cited"]

    def out(passed, message, beaten=0):
        return {"passed": passed, "ladder_score": score if passed else 0, "beaten_score": beaten,
                "cited_count": len(cited), "height": height, "message": message}

    if not cited:
        if score == 1:
            return out(True, "opening entry: cites nothing, score 1")
        return out(False, "an entry that cites nothing can only be the opening entry, score 1")
    if len(cited) > top_k:
        return out(False, "too many cited entries")
    names = [c["entry"] for c in cited]
    if len(set(names)) != len(names):
        return out(False, "an entry is cited twice")
    for c in cited:
        if c["entry"] == OPENING:
            if c["score"] != 1:
                return out(False, "the opening entry has score 1")
        elif not UUID.match(c["entry"]):
            return out(False, "a cited entry is the word opening or a lower-case submission id")
        elif c["score"] < 2:
            return out(False, "a submitted entry has score 2 or more")
    if len(cited) < top_k and OPENING not in names:
        return out(False, "fewer cited entries than the ladder asks for must include the opening entry")
    over = [c["score"] for c in cited if c["favored"]]
    under = [c["score"] for c in cited if not c["favored"]]
    if not over:
        return out(False, "the entry claims to be favored over none of the cited entries")
    if accept == "top" and under:
        return out(False, "this ladder accepts an entry only when it is favored over every cited entry")
    beaten = max(over)
    earned = beaten + 1
    if under:
        earned = min(earned, min(under))
    if earned > height:
        return out(False, "the ladder is finished: its height is reached", beaten)
    if score != earned:
        return out(False, "declared score is not the score the ladder rule gives", beaten)
    return out(True, "score follows the ladder rule", beaten)


def main():
    # In the verifier's sandbox the protected bundle is mounted at this fixed path;
    # beside the source file is where a local run finds it.
    path = "/snapshot/files/checkers/ladder.json"
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ladder.json")
    with open(path, encoding="utf-8") as handle:
        ladder = json.load(handle)
    payload = json.load(sys.stdin)
    json.dump(decide(payload, ladder), sys.stdout, sort_keys=True)


if __name__ == "__main__":
    main()
