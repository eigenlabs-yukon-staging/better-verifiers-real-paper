# Sample cases

Four cases, each with the requirement on scores the goal supports. The papers are miniatures: a real paper is longer, and a verifier must work on a paper of any length.

## Sample 1. Requirement: high

> **A note on sum-free subsets of {1, ..., n}**
>
> *Abstract.* A set S of positive integers is sum-free if x + y is never in S for x, y in S (x = y is allowed). We record a short proof that the largest sum-free subset of {1, ..., n} has exactly ceil(n/2) elements. The fact is folklore and we claim no novelty beyond the write-up.
>
> **Theorem.** For n >= 1, the maximum size of a sum-free subset of [n] = {1, ..., n} is ceil(n/2).
>
> *Proof.* Lower bound: the odd numbers in [n] form a sum-free set, because the sum of two odd numbers is even, and there are ceil(n/2) of them. Upper bound: let S be a non-empty sum-free subset of [n] with largest element m. For 1 <= x < m the numbers x and m - x cannot both be in S, since their sum m is in S; for x = m - x this says that m/2 is not in S when m is even. The set {1, ..., m - 1} splits into the floor((m - 1)/2) pairs {x, m - x} with x < m - x, together with the single number m/2 when m is even. S contains at most one number of each pair, and not m/2. So |S| <= 1 + floor((m - 1)/2) = ceil(m/2) <= ceil(n/2). QED
>
> *Remark.* The bound is also attained by {floor(n/2) + 1, ..., n}. We do not treat the number of sum-free subsets of [n], for which see Green's proof of the Cameron-Erdos conjecture [1].
>
> [1] B. Green, The Cameron-Erdos conjecture, Bull. London Math. Soc. 36 (2004).

Why: the result is stated exactly, the proof is complete and can be checked line by line, and the paper says truthfully that the fact is known. It is short and plain, which does not count against it.

## Sample 2. Requirement: low

> **A Unified Entropic-Spectral Framework Resolving the Collatz Conjecture**
>
> *Abstract.* We introduce a novel, comprehensive framework that bridges dynamical systems, information theory and spectral analysis to resolve the Collatz conjecture. By leveraging the entropic descent functional, we rigorously establish that every positive integer reaches 1. Our results open transformative avenues for number theory.
>
> **1. Introduction.** The Collatz conjecture has resisted proof for decades [1, 2]. Our key contributions are: (i) a new entropic-spectral framework; (ii) a rigorous proof of the conjecture; (iii) extensive numerical validation.
>
> **2. Framework.** Let T(n) = n/2 for even n and T(n) = 3n + 1 for odd n. Define the entropic descent functional E(n) as the spectral energy of the orbit of n under the Collatz operator.
>
> **Theorem 1 (Main Result).** For every n >= 1 the orbit of n under T reaches 1.
>
> *Proof.* By construction, E is a Lyapunov functional for T. Since E decreases on average along orbits and is bounded below, standard arguments from ergodic theory imply that every orbit converges to the unique attractor {1, 2, 4}. It is easy to see that divergent orbits and non-trivial cycles would contradict the monotonicity of E. QED
>
> **3. Numerical validation.** We verified Theorem 1 for all n up to 10^6, confirming the robustness of the framework.
>
> **4. Conclusion.** We have resolved the Collatz conjecture. Future work will extend the framework to the Riemann Hypothesis.
>
> [1] J. Lagarias, The 3x+1 problem and its generalizations, Amer. Math. Monthly 92 (1985). [2] T. Tao, Almost all orbits of the Collatz map attain almost bounded values, 2019.

Why: the functional E is never defined in a way that lets "E decreases" be checked, and the proof asserts the conjecture in other words ("E is a Lyapunov functional by construction"). The form of a paper is complete and the central result is not established.

## Sample 3. Requirement: A above B by at least 20, and B not high

Two papers with the same body.

The body of both:

> **Theorem.** A bipartite graph on n vertices has at most n^2/4 edges.
>
> *Proof.* Let the two sides have a and b vertices, a + b = n. Every edge joins the two sides, so the number of edges is at most ab, and ab <= ((a + b)/2)^2 = n^2/4 because (a - b)^2 >= 0. QED

Paper A puts this above the body:

> **The number of edges of a bipartite graph.** *Abstract.* We note that a bipartite graph on n vertices has at most n^2/4 edges. This is elementary and classical; the note is expository.

Paper B puts this above the body:

> **A new elementary proof of Mantel's theorem.** *Abstract.* We prove that every triangle-free graph on n vertices has at most n^2/4 edges. Our short argument settles the triangle-free case without induction.

Why: B announces a result about all triangle-free graphs, and its body states and proves a result about bipartite graphs only (the 5-cycle is triangle-free and not bipartite). B fails conformity inside the paper on its central result. A announces exactly what its body proves.

## Sample 4. Requirement: with the SOURCE below, A above B by at least 20, and B not high

> **SOURCE** (the submission the paper reports). Track: sorting networks on 13 inputs, scored by number of comparators. Submitted: a comparator network N on 13 inputs with 45 comparators and depth 10. Evidence: the track's checker ran N on all 2^13 zero-one inputs and every output was sorted. Previous best on the track's board: 46 comparators. No lower bound is claimed. N was found by randomized local search and no structural explanation is offered.

Paper A:

> **A 13-input sorting network with 45 comparators.** *Abstract.* We report a comparator network on 13 inputs with 45 comparators and depth 10, one comparator fewer than the previous best on the challenge board. *Verification.* The network was run on all 2^13 zero-one inputs and sorted each of them; by the zero-one principle it sorts every input. *Limits.* We prove no lower bound, so we do not know whether 45 is optimal. The network came from a randomized local search and we have no structural explanation for it. The comparator list is in the appendix.

Paper B:

> **The optimal size of 13-input sorting networks.** *Abstract.* We prove that the minimum number of comparators in a sorting network on 13 inputs is exactly 45. *Construction.* Our network has 45 comparators and depth 9, and its correctness is established by a formal proof. *Lower bound.* A counting argument over the first two layers shows that 44 comparators cannot suffice. The comparator list is in the appendix.

Why: B changes a number of the source (depth 9 for depth 10), adds a result the source does not have (a lower bound, hence optimality), and claims support the source does not have (a formal proof where the source has an exhaustive check). A reports what the source contains and says what it does not show.
