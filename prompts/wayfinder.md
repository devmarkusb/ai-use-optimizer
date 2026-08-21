---
title: Wayfinder
type: task-prompt
purpose: >
  Plan a large uncertain effort as a shared map of decision tickets, then resolve one
  ticket at a time until the way to the destination is clear
targets:
  - Codex
  - Claude Code
  - Cursor
  - Generic LLM coding agents
scope:
  - long-running planning
  - decision mapping
recommended-stage: when an effort is too large or unclear for one agent session
---

# Wayfinder

## Context

A loose idea has arrived, too big for one agent session, and wrapped in fog: the way from here to
the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the
destination. This prompt charts the way as a **shared map** on the repo's issue tracker (just a repo
local dir of planning docs, where it suits best), then works its **decision tickets** (questions
whose resolution is a decision, not slices of a build to execute) one at a time until the route is
clear.

The destination varies per effort, and naming it is the first act of charting: it shapes every
ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or
a change made in place like a data-structure migration. The map is domain-agnostic: engineering
work, course content, whatever fits the shape.

## Goal

Plan a huge chunk of work as a durable map of decision tickets, then resolve those tickets one at a
time until nothing important remains undecided before execution.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the
way is clear, with nothing left to decide before someone goes and does the thing. The pull to just
do the work is usually the signal you've reached the edge of the map and it's time to hand off. An
effort can override this in its **Notes**, carrying execution into the map itself, but absent that,
produce decisions, not deliverables.

## Refer by name

Every map and ticket has a **name**: its title. In everything the human reads (narration, the map's
Decisions-so-far), refer to it by that name, never by a bare id, number, or slug. A wall of
`#42, #43, #44` or raw paths is illegible; names read at a glance. The id, URL, or path does not
vanish; a name wraps its link, but those details ride _inside_ the name, never stand in for it.

## The Map

The map is a single issue or planning document on this repo's issue tracker (just a repo local dir
of planning docs, where it suits best), labelled or tagged `wayfinder:map` when labels exist. It is
the canonical artifact. Its tickets are child issues or child planning docs of the map.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that
hold their detail; a decision lives in exactly one place, its ticket, so the map never restates it,
only gists it and links.

**Where the map, its child tickets, blocking, and frontier queries physically live is
tracker-specific.** Use the hosted tracker, project board, or repo-local planning-docs directory
this repo already provides. If none exists, create a small local Markdown tracker in the most
appropriate planning-docs directory for the repo, and keep the same map/ticket structure there.

### Local Markdown fallback

When no hosted tracker or project board is available, use plain Markdown files:

- one map file, for example `planning/wayfinder/<map-slug>/map.md`
- one ticket file per decision, for example `planning/wayfinder/<map-slug>/tickets/<ticket-slug>.md`

Use front matter or a short metadata block at the top of each ticket:

```markdown
Status: open | closed | out-of-scope
Type: research | prototype | grilling | task
Claimed by:
Blocked by:
Resolution:
```

For local docs, the **frontier** is the set of ticket files with `Status: open`, no `Claimed by`,
and no open tickets listed under `Blocked by`.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed: they are
open child tickets, found by query or by scanning the tracker directory.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; repo-specific guidance or workflows every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a **child issue** or **child planning doc** of the map; the tracker's issue id or the
document path is its identity. Its body is the question, sized to one large agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label or tag, one of `research`, `prototype`, `grilling`,
`task` (see [Ticket Types](#ticket-types)).

A session **claims** a ticket before any work so concurrent sessions skip it. In a hosted tracker,
assign it to the dev driving the map. In local planning docs, add a clear claim line such as
`Claimed by: <agent/session>` near the top. That assignment or claim _is_ the claim: an open,
unclaimed ticket is available.

Blocking uses the tracker's **native** dependency relationship when it has one. Only a tracker that
lacks native blocking falls back to a body convention such as `Blocked by: <ticket links>`. A ticket
is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked,
unclaimed children, the edge of the known.

The answer is not part of the initial body; it is recorded on resolution (see
[Work through the map](#work-through-the-map)). Assets created while resolving a ticket are linked
from the ticket, not pasted in.

A **context pointer** is the smallest durable reference that lets a later session inspect the
details: a ticket link, file path, branch name, commit, artifact URL, or short note path.

## Ticket Types

Every ticket is either **HITL** (human in the loop, worked _with_ a human who speaks for themselves)
or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the
agent never stands in for the human's side of it (a grilling agent that answers its own questions
has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge
  bases to surface a fact a decision waits on. Use a research subagent or research workflow when the
  environment provides one; otherwise do the research directly and record a concise sourced note.
  Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete
  artifact to react to (an outline, a rough take, a stub, or UI/logic code). Use a prototype
  workflow or tool when available; otherwise make the smallest artifact the current environment can
  support. Link the prototype as an asset. Use when "how should it look" or "how should it behave"
  is the key question.
- **Grilling** (HITL): Conversation. The default case. Run a focused clarification and
  domain-modeling exchange with the human. If named grilling or domain-modeling workflows exist, use
  them; otherwise ask direct questions until the decision vocabulary and tradeoffs are clear.
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made: nothing to
  decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a
  service so its API can be judged, provisioning access, moving data so its shape can be seen. This
  is the one type that _does_ rather than decides, and it earns its place by unblocking a decision,
  not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it
  hands the human a precise checklist (HITL). Resolved when the work is done; the answer records
  what was done and any resulting facts (credentials location, new URLs, row counts) later tickets
  depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets
lies the **fog of war**: the dim view of decisions and investigations you can tell are coming but
can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog
ahead of it, graduating whatever's now specifiable into fresh tickets, one at a time, until the way
to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected
question, the area to revisit later. It's the undiscovered frontier _toward_ the destination:
everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the
view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now, _not_ whether you
can answer it now.

- **Ticket when** the question is already sharp, even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into
  ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets,
  or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live
ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it
is **out of scope**: it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own
**Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not
sharpness, lands it here.

Out-of-scope work never graduates (the frontier stops at the destination), so it returns only if the
destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already
exists turns out to sit past the destination (mis-scoped in while charting, or exposed by a
resolution), **close it** (a closed ticket is unambiguously off the frontier) and leave one line in
the **Out of scope** section: the gist plus why it's out of scope, linking the closed ticket. It
stays out of **Decisions so far**, which records the route actually walked; a scope boundary isn't a
step on it.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session**, with the exception of
research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run a focused clarification and domain-modeling pass to pin down what
   this map is finding its way to: the spec, decision, or change. Use named workflows when the
   environment provides them. The destination fixes the scope, so it's settled first.
1. **Map the frontier.** Ask breadth-first this time: fan out across the whole space rather than
   deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this
   surfaces no fog** (the way to the destination is already clear, the whole journey small enough
   for one session), you don't need a map. Stop and ask the user how they'd like to proceed.
1. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far
   empty, the fog sketched into **Not yet specified**.
1. **Create the tickets you can specify now** as child issues or child planning docs of the map,
   then wire blocking edges in a **second pass** (tickets need ids or paths before they can
   reference each other). Wiring sorts them into the frontier and the blocked; everything you can't
   yet specify stays in the fog: the **Not yet specified** section.
1. **Fire the research subagents when available.** For each `research` ticket you just created, spin
   up a research subagent or focused research pass to resolve it in parallel where possible. If
   parallel agents or branches are unavailable, leave the research tickets open on the frontier.
   Capture findings with a context pointer from the ticket.
1. Stop: charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with a map (URL, number, or path). A ticket is **optional**: without one, you pick the
next decision, not the user.

1. Load the **map**: the low-res view, not every ticket body.
1. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in
   order. **Claim it** before any work.
1. Resolve it. **Zoom as needed**: fetch the full body of any related or closed ticket on demand;
   use whichever skills, workflows, or tools the `## Notes` block names. If in doubt, run a focused
   clarification and domain-modeling pass.
1. Record the resolution: post the answer as a **resolution comment** or resolution section,
   **close** the ticket, and **append a context pointer** to the map's Decisions-so-far.
1. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable,
   clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If
   the answer reveals that a ticket (this one or another) sits beyond the destination, **rule it out
   of scope** rather than resolving it on the route. If the decision invalidates other parts of the
   map, update or delete those tickets.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker
concurrently.

## Output Format

Return a short summary with:

- mode used: charted a map or worked one ticket
- map location
- tickets created, claimed, resolved, blocked, or ruled out of scope
- decision recorded, when a ticket was resolved
- next frontier ticket or stop condition
