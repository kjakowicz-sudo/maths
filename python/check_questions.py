#!/usr/bin/env python3
"""Check the quiz question bank in index.html.

Run it from this folder:      python3 check_questions.py

It does two jobs.

1. Structure. Every question must have four options, a valid answer index,
   one wrong-answer line per wrong option, an explanation, and a topic and
   angle the app knows about. Ids must be unique.

2. Accuracy. Any question carrying an "expect" field has its snippet
   actually run in Python 3, with the team data below already defined, and
   the real printed output is compared with what the question claims. For
   "choose the code" questions every option is run, so the marked one must
   work and the others must not. Questions with "expectError" must really
   raise that error.

Nothing is run with network access and nothing is written outside this
folder. Snippets come from index.html, which is the only source of truth
for the bank -- add questions there and run this again.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE / "index.html"

# The running example every question is built on.
TEAM = """\
names = ['Aisha', 'Ben', 'Carla', 'Dan', 'Ella', 'Finn']
depts = ['HR', 'Finance', 'HR', 'IT', 'Finance', 'IT']
years = [6, 2, 9, 1, 4, 3]          # years of service
ext   = {'Aisha': 2101, 'Ben': 2102, 'Carla': 2103,
         'Dan': 2104, 'Ella': 2105, 'Finn': 2106}
full_names = ['Aisha Khan', 'Ben Morris', 'Carla Diaz',
              'Dan Okafor', 'Ella Novak', 'Finn Walsh']
"""

ANGLES = {"concept", "predict", "bug", "choose", "error", "structure", "logic"}
AREAS = {"Foundations", "Data structures", "Conditions", "Loops", "Comprehensions"}
TIMEOUT = 10


def topics_from_index(text):
    """Read the topic ids the app defines, so the bank cannot drift from it."""
    block = re.search(r"const TOPICS = \[(.*?)\];", text, re.S)
    if not block:
        return set(), {}
    ids = re.findall(r'id:"([a-z0-9]+)"', block.group(1))
    areas = re.findall(r'area:"([^"]+)"', block.group(1))
    return set(ids), dict(zip(ids, areas))


def bank_from_index(text):
    start = text.index("const QUESTIONS = ") + len("const QUESTIONS = ")
    end = text.index("/* === QUESTION BANK END === */")
    raw = text[start:end].strip()
    if raw.endswith(";"):
        raw = raw[:-1]
    return json.loads(raw)


def run(code, stdin=""):
    """Run a snippet with the team data in front of it. Returns (out, err)."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     dir=tempfile.gettempdir(), encoding="utf-8") as fh:
        fh.write(TEAM + "\n" + code + "\n")
        path = fh.name
    try:
        p = subprocess.run([sys.executable, "-I", path], input=stdin,
                           capture_output=True, text=True, timeout=TIMEOUT)
        return p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT: the snippet did not finish (an infinite loop?)"
    finally:
        try:
            Path(path).unlink()
        except OSError:
            pass


def canonical(out):
    """How a printed result is written in an option: lines joined by ' / '."""
    lines = out.split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    if not lines:
        return "(nothing is printed)"
    return " / ".join(lines)


def error_name(err):
    hits = re.findall(r"^(\w*(?:Error|Exception|Warning))\b", err, re.M)
    return hits[-1] if hits else None


def main():
    text = INDEX.read_text(encoding="utf-8")
    known_topics, topic_area = topics_from_index(text)
    try:
        bank = bank_from_index(text)
    except Exception as exc:                                   # noqa: BLE001
        print("Could not read the question bank from index.html:", exc)
        return 1

    problems = []
    ran = checked_out = 0
    seen_ids = set()
    by_topic, by_angle = {}, {}

    for q in bank:
        qid = q.get("id", "<no id>")
        fail = lambda msg: problems.append(f"{qid}: {msg}")       # noqa: E731

        # ---- structure ----
        if qid in seen_ids:
            fail("duplicate id")
        seen_ids.add(qid)
        for field in ("topic", "area", "angle", "question", "options",
                      "answer", "explanation", "wrongExplanations", "difficulty"):
            if field not in q:
                fail(f"missing field '{field}'")
        if known_topics and q.get("topic") not in known_topics:
            fail(f"topic '{q.get('topic')}' is not in TOPICS")
        if q.get("area") not in AREAS:
            fail(f"area '{q.get('area')}' is not one of the five areas")
        if topic_area.get(q.get("topic")) and topic_area[q["topic"]] != q.get("area"):
            fail(f"area '{q.get('area')}' does not match the topic's area "
                 f"'{topic_area[q['topic']]}'")
        if q.get("angle") not in ANGLES:
            fail(f"angle '{q.get('angle')}' is not a known angle")
        if q.get("difficulty") not in (1, 2, 3):
            fail("difficulty must be 1, 2 or 3")
        opts = q.get("options") or []
        if len(opts) != 4:
            fail(f"needs exactly 4 options, has {len(opts)}")
        if len(set(opts)) != len(opts):
            fail("two options are identical")
        if not isinstance(q.get("answer"), int) or not 0 <= q.get("answer", -1) < len(opts):
            fail("answer is not a valid index into options")
        we = q.get("wrongExplanations") or []
        if len(we) != len(opts):
            fail(f"wrongExplanations needs {len(opts)} entries, has {len(we)}")
        else:
            ans = q.get("answer")
            for i, line in enumerate(we):
                if i == ans and line.strip():
                    fail("wrongExplanations should be empty in the answer's slot")
                if i != ans and not line.strip():
                    fail(f"no wrong-answer line for option {'ABCD'[i]}")
        if not str(q.get("explanation", "")).strip():
            fail("empty explanation")
        if q.get("code") and "\t" in q["code"]:
            fail("code uses a tab; the course says four spaces")

        by_topic[q.get("topic")] = by_topic.get(q.get("topic"), 0) + 1
        by_angle[q.get("angle")] = by_angle.get(q.get("angle"), 0) + 1

        # ---- accuracy ----
        setup = q.get("setup", "")
        stdin = q.get("stdin", "")

        if "expectError" in q:
            out, err = run((setup + "\n" if setup else "") + (q.get("code") or ""), stdin)
            ran += 1
            got = error_name(err)
            if got != q["expectError"]:
                fail(f"expected {q['expectError']}, actually got "
                     f"{got or 'no error at all'}")

        elif "expect" in q:
            if q.get("angle") == "choose":
                # every option is a candidate line of code
                results = []
                for i, opt in enumerate(opts):
                    out, err = run((setup + "\n" if setup else "") + opt, stdin)
                    ran += 1
                    results.append((out, err))
                good_out, good_err = results[q["answer"]]
                if good_err.strip():
                    fail("the marked option raises an error:\n      " +
                         good_err.strip().splitlines()[-1])
                elif good_out != q["expect"]:
                    fail("the marked option prints\n      " + repr(good_out) +
                         "\n    but the question expects\n      " + repr(q["expect"]))
                else:
                    checked_out += 1
                for i, (out, err) in enumerate(results):
                    if i == q["answer"]:
                        continue
                    if not err.strip() and out == q["expect"]:
                        fail(f"option {'ABCD'[i]} does exactly the same thing as the "
                             "answer, so it is not wrong")
            else:
                out, err = run((setup + "\n" if setup else "") + (q.get("code") or ""), stdin)
                ran += 1
                if err.strip():
                    fail("the snippet raised an error:\n      " +
                         err.strip().splitlines()[-1])
                elif out != q["expect"]:
                    fail("the snippet prints\n      " + repr(out) +
                         "\n    but the question expects\n      " + repr(q["expect"]))
                else:
                    checked_out += 1
                    # On a "predict the output" question the options ARE outputs,
                    # so the right one must read exactly like the real thing.
                    # Other angles may carry "expect" only to prove the snippet
                    # really behaves as the question claims, and there their
                    # options are explanations rather than output.
                    if q.get("angle") == "predict":
                        want = canonical(q["expect"])
                        if opts[q["answer"]] != want:
                            fail("the correct option reads\n      " + repr(opts[q["answer"]]) +
                                 "\n    but the real output written that way is\n      " + repr(want))

        elif q.get("angle") in ("predict", "choose"):
            fail(f"angle is '{q['angle']}' but there is no \"expect\" field, "
                 "so the answer has not been checked by running it")

    # ---- report ----
    print(f"Questions in the bank: {len(bank)}")
    print(f"Snippets run in Python {sys.version.split()[0]}: {ran}  "
          f"(outputs matched: {checked_out})")
    print("\nPer topic:")
    for t in sorted(by_topic):
        print(f"  {t:<16} {by_topic[t]}")
    print("\nPer angle:")
    for a in sorted(by_angle):
        print(f"  {a:<10} {by_angle[a]}")

    # the brief asks for at least four different angles per topic
    per_topic_angles = {}
    for q in bank:
        per_topic_angles.setdefault(q.get("topic"), set()).add(q.get("angle"))
    thin = {t: sorted(a) for t, a in per_topic_angles.items() if len(a) < 4}
    if thin:
        print("\nTopics tested from fewer than four angles:")
        for t, a in sorted(thin.items()):
            print(f"  {t}: only {', '.join(a)}")
            problems.append(f"{t}: tested from only {len(a)} angle(s); the brief asks for at least four")

    if problems:
        print(f"\n{len(problems)} PROBLEM(S) TO FIX:\n")
        for p in problems:
            print("  - " + p)
        return 1
    print("\nNo mismatches. Every runnable answer was checked by running it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
