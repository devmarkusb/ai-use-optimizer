You are analyzing a source code subtree.

Goal: Produce the shortest possible explanation that gives a correct intuition for what this code
exists to do.

Avoid implementation details.

Output:

1. One sentence "This code is responsible for ..."

1. Input → Processing → Output Keep this to 3-6 bullets.

1. Metaphor Explain it using an everyday analogy that even a young child could roughly understand.
   The analogy must preserve the important relationships.

1. Main moving pieces List only the major components/modules/classes.

1. Black boxes Explicitly state what is NOT understood from the inspected code. Mention unknown
   external inputs, hidden dependencies, and assumptions.

1. Next files to inspect If black boxes remain, list the smallest set of files/directories that
   should be inspected next. For each, say what uncertainty it would likely resolve.

Keep the answer under 250 words.
