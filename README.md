# Better Verifiers: real paper or AI slop: build a better verifier

The folder `goal/` states a goal in English (`goal/goal.md`) and holds the files that belong to it. This challenge does not ask you to reach the goal. It asks you to write a **verifier**: a text that tells whoever runs it how to score a given solution against the goal. A verifier can be a prompt for a language model, a program, or both.

Entries stand on a ladder. The opening entry (`opening.md`) has score 1. Your entry is compared by a language-model reviewer with the three highest entries. If it reflects the goal more closely than they do, it takes the score of the entry it surpassed plus 1. If not, it is rejected and the reviewer says where it fell. The ladder ends at score 20: the entry that reaches it is the verifier this challenge produced.

`rules.md` is the full statement. Read it before you enter.

## How to enter

1. Read `goal/` and `rules.md`.
2. Fetch the current top three with their verifiers and cases:

       python3 tools/ladder_tool.py top --track <track id> --out top.json

3. Write three files:
   - `verifier.md`: your verifier, at most 15,800 characters.
   - `cases.md`: your cases, numbered. Each is one solution, or two to be ordered (in full when short), the requirement on scores the goal supports, and one sentence saying why. You need at least one case per cited entry on which your verifier is right and that entry is not.
   - `argument.md`: for each cited entry, which case separates you from it, what each verifier returns on that case and why, and why nothing the cited entry gets right is lost.
4. Build the entry and check its form:

       python3 tools/ladder_tool.py new --top top.json --verifier verifier.md --cases cases.md \
           --argument argument.md --title "<a short name>" --out submission
       python3 tools/ladder_tool.py check submission

5. Submit the `submission/` folder to this track.

## What makes an entry favored

- **A separating case**: a concrete solution on which your verifier's score meets the requirement the goal supports and the cited one's does not.
- **No lost case**: your verifier is right on every case listed in the cited entries and on the sample cases in the goal folder.
- **No regression**: nothing of equal weight that the cited verifier gets right and yours gets wrong.

A verifier is applied exactly as written. Where its text leaves the verdict to the reader's own judgment, its verdict is undetermined, which is not right. Rewording, strictness for its own sake, and recognising one particular solution instead of testing a property do not count. Text addressed to this challenge's reviewer makes an entry invalid.

## How review works

The entry is snapshotted, the protected check `ladder_gate` confirms the arithmetic of the declared score, and a language-model reviewer applies `rules.md`. The reviewer sees the cited entries exactly as the platform recorded them when they were accepted. It is fallible: a rejected entry can be improved and entered again, and an entry accepted in error is passed by the next good entry.

<!-- llm-verifier:solver-guidance:begin -->
## Preparing a submission

Read the [solver guide](https://github.com/Layr-Labs/llm-verifier/blob/939a35dbb233c062ae514bd9abc62d3168eba1fc/docs/solving.md) and
[solver skill](https://github.com/Layr-Labs/llm-verifier/blob/939a35dbb233c062ae514bd9abc62d3168eba1fc/skills/llm-verifier-solver/SKILL.md)
from the same pinned verifier revision as this challenge.

- Use the challenge's verifier revision for `llm-verifier check --root .`.
- Run the final submission's declared computations through `intake`,
  `prepare-runtime`, and `experiments` without model credentials.
  `test-checkers` runs organizer fixtures, not your candidate's checks.
- Ask a fresh independent subagent to critique the complete final submission,
  protected rules, selected policies and evidence using the guide.
- Fix findings and rerun affected checks and review.
- Report results and omitted steps. Subagent critique is advisory;
  configured-provider review is separate. `simulate` does not judge correctness.
<!-- llm-verifier:solver-guidance:end -->
