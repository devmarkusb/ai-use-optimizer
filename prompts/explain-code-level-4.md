Perform a software architecture review of this code.

Focus on understanding rather than critique.

Produce:

1. Responsibilities
1. Public contracts
1. Hidden assumptions
1. State machine
1. Data flow
1. Control flow
1. Ownership model
1. Concurrency model
1. Persistence model
1. Failure model
1. External dependencies
1. Side effects
1. Invariants
1. Coupling and cohesion
1. Safe modification strategy
1. Highest-risk edits
1. Unknowns and black-box boundaries
1. Next files or directories to inspect

For every section:

Separate facts from inference.

Label statements as:

FACT LIKELY UNKNOWN

Never infer behavior hidden behind uninspected code.

In "Next files or directories to inspect", list only follow-up inspection targets that would
materially reduce uncertainty.

For each target, include:

- path
- reason to inspect it
- expected architectural question it answers
- risk if it remains uninspected
