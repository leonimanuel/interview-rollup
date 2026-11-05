#!/usr/bin/env python3
"""Build a self-contained quiz page from a quiz JSON file.

Usage: build.py quiz.json [--out quiz.html] [--no-open]
"""
import argparse
import json
import sys
import webbrowser
from pathlib import Path

TEMPLATE = Path(__file__).with_name("template.html")
QUIZ_MARK = "/*__QUIZ__*/null"


def text(value):
    return isinstance(value, str) and value.strip() != ""


def problems(quiz):
    """Every problem with the quiz, so one run reports them all."""
    errors = []

    def sized(obj, key, lo, hi, where, what):
        value = obj.get(key)
        if not isinstance(value, list) or not lo <= len(value) <= hi:
            errors.append(f"{where}: '{key}' must hold {lo} to {hi} {what}")
            return []
        return value

    def entries(items, where, fields):
        for e in items:
            if not isinstance(e, dict) or not all(text(e.get(f)) for f in fields):
                errors.append(f"{where}: each entry needs " + " and ".join(f"'{f}'" for f in fields))
                return False
        return True

    if not isinstance(quiz, dict):
        return ["the file must hold one JSON object"]
    for key in ("title", "role", "angle"):
        if not text(quiz.get(key)):
            errors.append(f"missing '{key}'")

    for n, q in enumerate(sized(quiz, "questions", 1, 4, "quiz", "questions"), 1):
        where = f"question {n}"
        if not isinstance(q, dict):
            errors.append(f"{where} must be an object")
            continue
        if not text(q.get("prompt")):
            errors.append(f"{where}: missing 'prompt'")
        kind = q.get("type")

        if kind == "order":
            items = sized(q, "items", 3, 8, where, "strings, in the correct order")
            if not all(map(text, items)):
                errors.append(f"{where}: every item must be text")
            elif len(set(items)) != len(items):
                errors.append(f"{where}: 'items' must not repeat")
        elif kind == "match":
            pairs = sized(q, "pairs", 3, 6, where, "pairs")
            if entries(pairs, where, ("left", "right")) and len({p["right"] for p in pairs}) != len(pairs):
                errors.append(f"{where}: each 'right' must be different")
        elif kind == "pick":
            options = sized(q, "options", 3, 10, where, "options")
            if entries(options, where, ("label", "why")):
                if not all(isinstance(o.get("correct"), bool) for o in options):
                    errors.append(f"{where}: each option needs 'correct' (true or false)")
                elif not any(o["correct"] for o in options):
                    errors.append(f"{where}: at least one option must be correct")
        else:
            errors.append(f"{where}: 'type' must be order, match or pick")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Build a quiz page from quiz JSON.")
    parser.add_argument("spec", type=Path, help="quiz JSON file")
    parser.add_argument("--out", type=Path, help="output HTML (default: next to the JSON)")
    parser.add_argument("--no-open", action="store_true", help="don't open it in the browser")
    args = parser.parse_args()

    try:
        quiz = json.loads(args.spec.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"build.py: no such file: {args.spec}")
    except json.JSONDecodeError as e:
        sys.exit(f"build.py: {args.spec} is not valid JSON: {e}")
    errors = problems(quiz)
    if errors:
        sys.exit("build.py: fix these and run again:\n" + "\n".join(f"  - {e}" for e in errors))

    page = TEMPLATE.read_text(encoding="utf-8")
    if QUIZ_MARK not in page:
        sys.exit("build.py: template.html is missing its quiz placeholder")
    data = json.dumps(quiz, ensure_ascii=False).replace("</", "<\\/")
    page = page.replace(QUIZ_MARK, data, 1)

    out = args.out or args.spec.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    print(out.resolve())
    if not args.no_open:
        webbrowser.open(out.resolve().as_uri())


if __name__ == "__main__":
    main()
