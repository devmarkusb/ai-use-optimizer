# Find the Right Representation

Analyze the following problem by searching for representations that make the solution easier.

Problem:
[INSERT PROBLEM]

## 1. Surface formulation

- Restate the problem clearly.
- What is being asked?
- What would count as a valid solution?

## 2. Core structure

Identify:

- entities
- relations
- operations
- dynamics over time
- invariants
- constraints
- scarce resources
- information structure
- likely failure modes

Focus only on structure that appears relevant to solving the problem.

## 3. Representation search

Represent the problem using each of the following frameworks:

- graph
- state machine
- constraint system
- resource-flow model
- queueing model
- optimization problem
- information-flow model
- algebraic model
- probabilistic/statistical model
- game-theoretic/incentive model
- geometric/spatial model
- type-system/semantic model

For each representation provide:

### Representation: [name]

- Entities
- Relations
- Operations
- Invariants
- What becomes easier?
- What becomes harder?
- Which established toolkit does this representation import?
- One plausible solution path

Complete this sentence when possible:

> The problem becomes easier in this representation because ...

## 4. Locality analysis

For each strong candidate representation:

- What becomes local rather than global?
- What can be checked using only a small neighborhood of information?
- What dependencies disappear?
- Which bottleneck becomes visible?

## 5. Representation ranking

Rank the top three representations.

For each, explain:

- why it fits,
- what toolkit it unlocks,
- what key invariant, symmetry, bottleneck, or conservation law it exposes.

## 6. Best representation

Identify the single most useful representation.

Explain:

- why it is the most natural abstraction,
- why it shortens the solution path,
- what important structure becomes obvious,
- what competing representations hide.

## 7. Solution sketch

Using only the best representation:

- outline the solution approach,
- identify the critical insight,
- state what evidence would confirm this representation is correct,
- state what evidence would falsify it.

Prioritize representations that make the difficult part of the problem local, constrained, or governed by known theory. Do not merely rename the problem; search for transformations that expose hidden structure.