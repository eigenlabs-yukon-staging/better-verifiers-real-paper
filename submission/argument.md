# Argument

This entry cites one entry, `opening` (score 1), so its ladder score is 2.

## What the opening verifier leaves open

The opening verifier asks for "how much the paper looks like a real mathematics or theoretical computer science paper and how little like AI slop, making sure the content of the paper conforms to what was submitted", with no criterion, no weight, and no arithmetic. It does not say what a false or unjustified step in the main proof costs, whether form, polish, references and style count, what a conformity failure costs or how large the gap must be, or how a SOURCE is compared. On any paper whose requirement depends on one of these, careful readers following its text can land on either side, so its verdict there is undetermined.

The new verifier fixes these by a referee's audit with written arithmetic: (1) list the central claims as announced, including every body result labelled Theorem; (2) test each step of each argument (justified, broken, lacuna; computational claims); (3) classify each central claim as (a) established as announced, (b) only a weaker result established, (c) not established; (4) check conformity inside the paper and, item by item, against the SOURCE; (5) fixed deductions D1-D6 giving H = 100 - D; (6) bands: L (some central claim (b) or (c)) at most min(30, H - 20); M (central conformity or SOURCE failure, everything established) min(50, H - 25); H (everything established and conforming) the score H.

## Separating cases against `opening`

**Case 3** (main separating case; planar graphs, same body, B overclaims). Requirement: A high, B not high, A above B by at least 20.
- New verifier: in A the central claims are the announced triangle-free statement and the body Theorem, the same result; every step is justified by (i) or by Euler's formula (ii), so status (a), conforming, band H. No deduction applies (at most D3 lacunas, 12), so A scores 88 to 100. In B the announced claim "every planar graph" is stated nowhere in the body; the body establishes only the triangle-free result, so status (b) (a reader who instead reads (c) also lands in band L). Band L: 25, capped at min(30, H - 20). B scores at most 25. A - B is at least 63.
- Opening: the text gives no cost for an abstract that overstates the body. A reader who sees a correct, complete proof with an inflated abstract can score B 60 and A 75 (gap 15) or B 30 and A 90; the gap of 20 and "B not high" are not forced. Undetermined.

**Case 4** (Paley graph with SOURCE; B adds a formal proof the SOURCE does not have). Requirement: A above B by at least 20, B not high.
- New verifier: A's central claims (P17 has no 4-clique or independent 4-set; R(4,4) >= 18) are a computational claim justified as in Step 2 (object defined, all 2380 subsets, what was checked, recorded in the SOURCE) and a deduction (i); every item agrees with the SOURCE; band H, D = 0, score 100. B is identical except that it claims a formal Lean proof: support the SOURCE does not have, on the central claim, so a central source violation; all central claims are (a), so band M: min(50, 100 - 25) = 50. Gap 50; B not high.
- Opening: one added sentence about a Lean check; the text gives no rule for comparing with the SOURCE or for what such a claim costs. Readers can deduct 5 or 40. Undetermined.

**Case 2** (polished union-closed "proof"). Requirement: low.
- New verifier: Theorem 1 is central; its only step applies Lemma 2, which is not established (its "standard averaging argument" names no fact, and the lemma is false: F = {∅, {1}, {1,2,3}} gives average 4/9). By (ii) the step is broken, status (c). Band L: no central claim (a) or (b), so 10; the abstract claims a complete proof the paper does not have, minus 5; score 5 (D1 for Lemma 2 gives H = 90, cap 30).
- Opening: the paper has correct definitions, a correct reduction, accurate references and clean prose; the text does not say that a failed central step forces a low score, so a reader weighing form can land at 35 to 55. Undetermined.

**Case 1** (clumsy real note, no abstract, no references). Requirement: high.
- New verifier: the Theorem is the only announced result and is presented as known, so it is central and needs a proof; every step is (i); status (a); no deduction (the remark on prior work is truthful). Band H, score 88 to 100. The ground rules forbid any loss for prose, layout or missing references.
- Opening: it asks how much the text "looks like" a real paper; a reader can count the missing abstract, missing reference list and chatty prose against it and land below 70. Undetermined.

## Nothing lost

`opening` lists no cases, so only the four samples need checking.

- **Sample 1 (high).** Central: the Theorem (presented as folklore, the only result, so central and needing proof). Lower bound by (i); upper bound by the pairing, each step (i); the identity 1 + floor((m - 1)/2) = ceil(m/2) is (i). Status (a), conforming. The remark's second extremal set is a routine check (iii), so no D1; the Green citation is truthful. Band H, score 88 to 100: high.
- **Sample 2 (low).** Central: Theorem 1 (labelled Main Result), and the announced "rigorous proof". The step "by construction, E is a Lyapunov functional" rests on "by construction" with an undefined E, and "standard arguments from ergodic theory" names no fact: broken, status (c). Numerical checks to 10^6 cannot prove a statement about all n. Band L: 10, minus 5 for the claimed rigorous proof, at most 30: score 5. Low.
- **Sample 3 (A above B by at least 20, B not high).** A: body Theorem and announcement agree; the proof is (i) plus AM-GM; band H, 88 to 100. B: the announced triangle-free result is not in the body, which establishes only the bipartite case: status (b) (or (c)); band L, at most 25. Gap at least 63; B not high.
- **Sample 4 (A above B by at least 20, B not high).** A: the network's sorting is a computational claim (object at a stated place, all 2^13 zero-one inputs, zero-one principle as a named result, recorded in the SOURCE); size and depth are read off the listed object; every item agrees with the SOURCE, including the previous best of 46 and the stated limits; band H, D = 0, score 100. B: the lower bound has no argument (status (c)); the depth 9 changes a number of the SOURCE, the lower bound is a result the SOURCE lacks, the formal proof is support it lacks. Band L: at most 25 - 15 = 10 (10 - 15, floored at 0, if the construction is also read as (c)). Gap at least 90; B low, so not high.
