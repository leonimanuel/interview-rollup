---
name: interview-prep
description: A few interview questions for a given role and prep angle, grounded in the work done in this session when there is any. Question cards in the chat by default; --quiz builds a small drag-and-drop page. Coaches each answer. Use only when the user runs /interview-prep.
argument-hint: "<role> <angle> [--quiz]"
disable-model-invocation: true
---

# /interview-prep

Arguments: $ARGUMENTS

Read the role, the angle and the `--quiz` flag from the arguments. For example,
`"Senior Platform Engineer" "systems design"`, or `backend scaling --quiz`. If the role or
the angle is missing, ask for it with one question card and carry on.

Keep everything terse: short lines, no preamble, no closing summary.

## 1. Context

**Drop folder:** `${INTERVIEW_PREP_DIR:-~/interview-prep}`. Users drop in whatever they have:
job descriptions, notes on a company or a round, a resume, a story bank.

- List it. Read the file(s) whose name or contents fit the role, plus files that aren't tied
  to any one role (resume, CV, notes, stories). Read at most five.
- If the folder is missing or empty, carry on without it.
- Say in one line which files you used, or that you used none.

**This session:** look at what was actually done here: files changed, decisions and their
tradeoffs, numbers, what broke and how it was caught.

- If there is real work, every question treats it as one component of a bigger system the role
  would own, seen through the angle. For example, a permissions table built today becomes "the
  permissions layer of a multi-tenant service. How does it hold at 10x tenants?"
- If there isn't, say "No session work yet, so these are general." and ask questions from the
  role and the angle alone.
- Never invent a result or round one up. If you quote a number, it came from this session or
  the drop folder.

Pitch the questions at the level of the role (a senior role gets tradeoffs and failure modes, not
definitions), and make them what an interviewer for that role would actually ask.

## 2. Questions

### Default: question cards

Send one AskUserQuestion call with up to four questions.

- Each question carries its own context: the concrete scenario, the numbers, the constraint.
- `header` is a short chip, like "Q1 Scale" or "Q2 Failure".
- Give 2-4 options. One is the best answer. The others are plausible answers a decent candidate
  might give, each with a real flaw.
- **It's a quiz.** Never mark an option "(Recommended)", never put the best answer first every
  time, and never word a description so it gives the answer away.
  Each description is the reasoning a candidate would say for that answer.
- Users can type their own answer through "Other". Coach that like any other answer.

### `--quiz`: a small page

1. Write up to four questions as JSON to `${TMPDIR:-/tmp}/interview-prep/<role>-<angle>.json`,
   with each question's type chosen to fit the angle:
   - `order`: put the steps in order (debugging, incidents, rollouts, migrations). 3-8 items.
   - `match`: match components to what each is responsible for (systems design). 3-6 pairs.
   - `pick`: tick the components a service needs, out of plausible ones (whiteboard rounds).
     3-10 options, each with its own `why`.

   ```json
   {"title": "...", "role": "...", "angle": "...",
    "questions": [
      {"type": "order", "prompt": "...", "items": ["first", "second", "third"], "why": "..."},
      {"type": "match", "prompt": "...", "pairs": [{"left": "component", "right": "its job"}], "why": "..."},
      {"type": "pick",  "prompt": "...", "options": [{"label": "...", "correct": true, "why": "..."}]}
    ]}
   ```
   Write `items` in the correct order and `pairs` correctly matched; the page shuffles them.

2. Run `python3 ${CLAUDE_SKILL_DIR}/quiz/build.py <that file>`. It checks the shape, writes
   the HTML next to the JSON and opens it in the browser. If it rejects the file, fix the JSON and
   run it again.
3. If an Artifact tool is available, also publish the built HTML with it (following that
   tool's own rules) and give the link.
4. Tell the user in one line: answer on the page, press Check, then "Copy my answers" and paste
   them back here.

## 3. Coaching

When the answers come back (from the cards or pasted from the page), do this for each answer, in
2-3 lines:

- **Verdict:** Strong, Partly or Missed.
- **What landed** and **what was missing**.
- **A tighter version** in the user's own words, said the way they'd say it in the room.

For a systems-design question, add a small text diagram of the components that they could
redraw on a whiteboard.

## Rules

Write nothing except the quiz JSON and HTML in the temp folder. No edits to the project, no
commits, no tests.
