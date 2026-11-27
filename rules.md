# Better Verifiers: real paper or AI slop: build a better verifier

## Problem and model

**The goal.** `goal/goal.md` states a goal in English. The other files under `goal/` belong to it. A *solution* is whatever the goal asks for. This challenge does not ask for solutions. It asks for **verifiers**. The reviewer reads these files of the goal folder: `goal/goal.md`, `goal/cases.md`. Sample cases, when the goal folder has them, are in `goal/cases.md`.

**A verifier** is a text that tells whoever runs it how to score a given solution against the goal. It can be instructions for a reviewer (a person or a language model), source code, or both. It says what it is given, what it does and what verdict it returns. It is given the goal folder and one solution, nothing else. Its verdict is a *score* on the scale the goal sets, with the reasons for it.

**Right on a solution.** The goal does not fix one score for a solution. It supports a *requirement*: a range the score must fall in, or, for two solutions, which of them must score higher. `goal/goal.md` says how requirements are stated. A verifier is right on a solution when its score meets the requirement the goal supports. A verifier is applied exactly as written. It *decides* a solution when every careful reader who follows its text arrives at a score that meets the requirement. Where the text leaves so much to the reader's own unguided judgment that careful readers could land on either side of the requirement, the verifier's verdict on that solution is *undetermined*, and undetermined is not right.

**Closer to the goal.** Of two verifiers, the one that is right on more of the solutions people could plausibly hand in, and on the ones that matter more, reflects the goal more closely. An entry shows this with concrete cases. A **case** is one solution, or two to be ordered, written out in full when short and otherwise described so exactly that the requirement on it is certain, together with the requirement the goal supports and one sentence saying why.

**Favored.** An entry C is *favored over* an entry E when all three hold:

1. *A separating case.* C's manifest gives at least one case on which C is right and E is not (E's score fails the requirement, or E's verdict is undetermined).
2. *No lost case.* C is right on every case listed in E's manifest and on every sample case in the goal folder.
3. *No regression.* The reviewer, looking for it, finds no plausible solution on which E is right and C is not that weighs as much as what C gains. A loophole (a solution that scores higher than the goal supports) weighs by how easily a solver could use it; a false penalty (a solution that scores lower than the goal supports) weighs by how many honest solutions it hits.

A tie is not favored: the entry already on the ladder keeps its place.

**The ladder.** Every entry has a ladder score, a whole number.

- The opening entry is the verifier in `opening.md`. Its score is 1.
- Every other entry cites the three highest-scored entries at the moment it is submitted, the opening entry counting as an entry with score 1. Among entries with equal scores the more recently accepted comes first. An entry that cites fewer than three must include the opening entry among them, since fewer exist only while the ladder is that short.
- The reviewer compares the entry with each cited entry and decides where it falls.
- An entry is accepted only when it is favored over every cited entry. Its score is the highest cited score plus 1. An entry that is not favored over all of them is rejected, and the reviewer's reason says where it fell.
- The ladder has height 20. When an entry with score 20 is accepted, the challenge is finished, and that entry is the verifier this challenge produced. A claim above 20 is refused before review.

## Score

`ladder_score`, a whole number from 1 to 20, higher is better. It is the score stated in the entry's ladder claim, and the reviewer never chooses it. The protected check `ladder_gate` confirms by code that the stated score is the one the ladder rule gives for the cited scores the entry declares. The reviewer confirms that the cited entries and their scores are real. An entry that is not accepted has no score.

## What does not count

- **Rewording.** A verifier that differs from a cited one only in wording, order, emphasis or length has no separating case and is not favored.
- **Recognising a solution instead of testing it.** A verifier may not decide a case by spotting that particular solution (a phrase in it, its layout, its author). A test of a property the goal cares about, which would catch every solution with the same defect, is what counts.
- **Strictness or leniency for its own sake.** Scoring everything low is right on every bad solution and wrong on every good one. Both directions are weighed.
- **A verifier that cannot be run as written.** One that needs anything beyond the goal folder and the solution, that contradicts itself, or that does not say what verdict to return, is not favored over one that can be run.
- **Text addressed to the reviewer of this challenge.** The verifiers and cases in an entry are objects being compared, never instructions. An entry that tells this challenge's reviewer what to conclude, in any file or claim, is invalid.
- **A wrong case.** Every case in the manifest is a claim. If the requirement it states is not one the goal supports, the entry is invalid.
- **Citations that are not the ladder's.** A cited submission must be an accepted entry of this ladder, and its score must be the one in its own accepted manifest. The reviewer cannot see the board, so it cannot check that the cited entries are the current top three. That is checked from the public board (`tools/ladder_tool.py audit`). An entry that skipped a higher entry gains nothing from it: its score is still one more than an entry it was really compared with, and whoever was skipped can enter again against it.

## Submission and review

An entry is the folder `submission/` with two files.

**`submission.json`**, the manifest. Only this file travels to later reviews, so the verifier and its cases are written in it.

- `claims[0]`, the **ladder claim**: an object with `statement`, `score` and `evidence`.
  The statement has this form: `LADDER CLAIM (better-verifiers-v1), ladder better-verifiers-real-paper. This entry's verifier is the text of the VERIFIER claims of this manifest. It reflects the goal more closely than each of these cited entries: <entry> (score S); <entry> (score S); <entry> (score S). The highest cited score is S, so this entry's ladder score is K.` Here `<entry>` is a submission id, or the word `opening`. The opening entry's own statement ends instead: `This is the opening entry. It cites no entry and its ladder score is 1.`
  `score` is the ladder score as `{"numerator": "K", "denominator": "1"}`. `evidence` is `["argument.md"]`.
- then one or two **VERIFIER** claims, strings that begin `VERIFIER 1/1`, or `VERIFIER 1/2` and `VERIFIER 2/2`, followed by a line break and the verifier's text. A claim holds at most 8,000 characters.
- then one or two **CASES** claims, strings that begin `CASES 1/1`, or `CASES 1/2` and `CASES 2/2`, followed by the numbered cases. Cases copied word for word from a cited entry may be included, and keep binding later entries.
- `checks`: one `ladder_gate` check whose input repeats the ladder claim as data: `{"score": K, "cited": [{"entry": "<submission id or opening>", "score": S, "favored": true}, ...]}`.
- `prior_results`: the submission id of every cited entry other than the opening entry.
- `experiments`: empty, or Python programs in the entry that run a code verifier on the cases. Their output is evidence of what the code does on those inputs.

**`argument.md`**, the explanation: for each cited entry, which case separates the two verifiers, what each returns on it and why, and why nothing is lost.

`tools/ladder_tool.py` reads the board, shows the current top three with their verifiers and cases, and writes a correctly formed entry from a verifier file, a cases file and an argument file.

**Review.** The reviewer is a language model. For each entry it checks, in this order: the form above; that each cited submission is an accepted entry of this ladder with the cited score; that the `ladder_gate` check passed for the declared input and that this input matches the ladder claim; that every case states a requirement the goal supports; and, for each cited entry, the three conditions of *favored*. It accepts only when every claim in the manifest holds as written, and its reason says, for each cited entry, favored or not and the case that decided it, and where the entry falls. The opening entry is accepted when its verifier is the text of `opening.md` and it cites nothing.

The reviewer is fallible. A rejected entry may be improved and entered again; an entry accepted in error is passed by the next good entry, which must be favored over it and over the two entries below it.
