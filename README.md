# /interview-rollup

A Claude Code skill for prepping for interviews without leaving what you're building.

Run it at the end of a session and it asks you a few interview questions for the role and the
angle you name, built from the work you just did. Today's permissions table becomes "the
permissions layer of a multi-tenant service: how does it hold at 10x tenants?" Answer them, and
it tells you what landed, what was missing, and gives a tighter version in your own words.

## Install

```bash
git clone <this repo> ~/interview-rollup-skill
ln -s ~/interview-rollup-skill/interview-rollup ~/.claude/skills/interview-rollup
```

Or copy the `interview-rollup/` folder into `~/.claude/skills/`. Start a new Claude Code session
so it picks the skill up.

## Use

```
/interview-rollup "Senior Platform Engineer" "systems design"
/interview-rollup backend debugging
/interview-rollup "Applied AI Engineer" scaling --quiz
```

- **Default:** up to four multiple-choice question cards in the chat. Pick an option or type
  your own answer.
- **`--quiz`:** a small page that opens in your browser, with drag-to-order, drag-to-match
  and pick-the-components questions. Press Check on each one, then "Copy my answers" and
  paste them back into the session to be coached.

If the session hasn't done any real work yet, the questions come from the role and the angle
alone.

## Drop folder

Put anything useful in `~/interview-rollup/` (or set `INTERVIEW_ROLLUP_DIR`): job descriptions,
notes on a company or a round, your resume, a story bank. Each run reads the files that fit the
role, plus the ones that aren't tied to any role. It works without the folder.

## Needs

Claude Code. `python3` for `--quiz` (standard library only). See [examples/sample-quiz.json](examples/sample-quiz.json)
for the quiz format; build it yourself with:

```bash
python3 interview-rollup/quiz/build.py examples/sample-quiz.json
```

## License

MIT
