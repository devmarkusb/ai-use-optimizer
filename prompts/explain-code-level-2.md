Analyze this source code as an architect.

Do not explain line-by-line.

Instead build a mental model.

Output:

# Purpose

One paragraph.

# Input → Processing → Output

- Inputs
- Main transformations
- Outputs

Be explicit about uncertainty. If inputs or outputs originate outside the inspected code, mark them
as external.

# Main Components

For each component:

- responsibility
- collaborators
- important public interfaces

# Data Flow

Show how information moves through the system.

# Control Flow

Who starts work? Who calls whom? Who decides?

# External Boundaries

Draw clear black-box boundaries.

List:

- external services
- operating system interactions
- databases
- files
- networking
- configuration
- environment variables
- user interaction

Mark each as:

Known Likely Unknown

# Side Effects

List every observable side effect you can identify.

# Unknowns

Explicitly list everything this analysis cannot determine without inspecting additional code. Never
speculate.

# Next Files To Inspect

If unknowns remain, list the files or directories that should be inspected next.

For each item:

- file or directory
- why it matters
- what question it would answer

Only include items that would materially improve the architecture understanding.
