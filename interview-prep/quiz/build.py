#!/usr/bin/env python3
"""Build a self-contained quiz page from a quiz JSON file.

Usage: build.py quiz.json [--out quiz.html] [--no-open]
"""
import argparse
import html
import json
import sys
import webbrowser
from pathlib import Path

TEMPLATE = Path(__file__).with_name("template.html")
QUIZ_MARK = "/*__QUIZ__*/null"
TITLE_MARK = "__TITLE__"


def fail(msg):
    sys.exit(f"build.py: {msg}")


def text(value):
    return isinstance(value, str) and value.strip() != ""


def validate(quiz):
    if not isinstance(quiz, dict):
        fail("the file must hold one JSON object")
    for key in ("title", "role", "angle"):
        if not text(quiz.get(key)):
            fail(f"missing '{key}'")
    questions = quiz.get("questions")
    if not isinstance(questions, list) or not 1 <= len(questions) <= 4:
        fail("'questions' must hold 1 to 4 questions")

    for n, q in enumerate(questions, 1):
        where = f"question {n}"
        if not isinstance(q, dict):
            fail(f"{where} must be an object")
        kind = q.get("type")
        if kind not in ("order", "match", "pick"):
            fail(f"{where}: 'type' must be order, match or pick")
        if not text(q.get("prompt")):
            fail(f"{where}: missing 'prompt'")

        if kind == "order":
            items = q.get("items")
            if not isinstance(items, list) or not 3 <= len(items) <= 8 or not all(map(text, items)):
                fail(f"{where}: 'items' must be 3 to 8 strings, in the correct order")
            if len(set(items)) != len(items):
                fail(f"{where}: 'items' must not repeat")
        elif kind == "match":
            pairs = q.get("pairs")
            if not isinstance(pairs, list) or not 3 <= len(pairs) <= 6:
                fail(f"{where}: 'pairs' must hold 3 to 6 pairs")
            for p in pairs:
                if not isinstance(p, dict) or not text(p.get("left")) or not text(p.get("right")):
                    fail(f"{where}: each pair needs 'left' and 'right'")
            if len({p["right"] for p in pairs}) != len(pairs):
                fail(f"{where}: each 'right' must be different")
        else:
            options = q.get("options")
            if not isinstance(options, list) or not 3 <= len(options) <= 10:
                fail(f"{where}: 'options' must hold 3 to 10 options")
            for o in options:
                if not isinstance(o, dict) or not text(o.get("label")) or not isinstance(o.get("correct"), bool):
                    fail(f"{where}: each option needs 'label' and 'correct' (true or false)")
            if not any(o["correct"] for o in options):
                fail(f"{where}: at least one option must be correct")


def main():
    parser = argparse.ArgumentParser(description="Build a quiz page from quiz JSON.")
    parser.add_argument("spec", type=Path, help="quiz JSON file")
    parser.add_argument("--out", type=Path, help="output HTML (default: next to the JSON)")
    parser.add_argument("--no-open", action="store_true", help="don't open it in the browser")
    args = parser.parse_args()

    try:
        quiz = json.loads(args.spec.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"no such file: {args.spec}")
    except json.JSONDecodeError as e:
        fail(f"{args.spec} is not valid JSON: {e}")
    validate(quiz)

    page = TEMPLATE.read_text(encoding="utf-8")
    if QUIZ_MARK not in page or TITLE_MARK not in page:
        fail("template.html is missing its placeholders")
    data = json.dumps(quiz, ensure_ascii=False).replace("</", "<\\/")
    page = page.replace(TITLE_MARK, html.escape(quiz["title"]), 1).replace(QUIZ_MARK, data, 1)

    out = args.out or args.spec.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    print(out.resolve())
    if not args.no_open:
        webbrowser.open(out.resolve().as_uri())


if __name__ == "__main__":
    main()
