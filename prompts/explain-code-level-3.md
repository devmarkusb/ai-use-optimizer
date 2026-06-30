Explain the dynamic behavior of this subsystem.

Produce seven views.

## 1. Lifecycle Picture

States Transitions Who triggers each transition

## 2. Mutation Picture

Which objects may modify which other objects.

Distinguish:

- owns
- mutates
- reads
- observes
- caches

## 3. Failure Picture

List failure modes.

For each:

- trigger
- detection
- recovery
- resulting state

## 4. Ownership Picture

Describe ownership.

Include:

- lifetime
- borrowing
- shared ownership
- invalidation
- caching

## 5. Consistency Picture

Identify invariants.

Include:

- object invariants
- cross-module invariants
- persistence invariants
- concurrency assumptions

## 6. Dependency Picture

Draw the dependency graph.

Separate:

- internal modules
- external libraries
- external systems

Identify boundaries.

List side effects.

## 7. Edit Impact Picture

If each major component changes:

What is likely affected?

What is unlikely affected?

What hidden coupling exists?

## Unknown Boundaries

End with:

"Things this analysis cannot know."

Be explicit whenever behavior depends on code outside the inspected files. Never invent details.

## Next Files To Inspect

If any lifecycle, mutation, failure, ownership, consistency, dependency, or edit-impact behavior
depends on uninspected code, list the smallest useful set of files/directories to inspect next.

For each:

- path
- suspected responsibility
- uncertainty it would resolve
- which picture it affects
