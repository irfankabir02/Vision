# Vision/UI_UX — CLI usage patterns

This document extends `README.md` with recommended CLI usage patterns and examples for working with the `vision/UI_UX` one-screen budget utilities. Everything here is Python only — no JavaScript.

Note: `demo_cli.py` is currently a simple script that prints device presets and writes `report.html`. The examples below include: (1) how to use `demo_cli.py`, (2) Python one-liners to exercise the API, and (3) recommended CLI interface designs to add for future workflows (argparse / Click) and sample commands you can use immediately.

---

## 1 — Quick start (existing demo)

1. Activate your virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Run the demo CLI (prints budgets and a HTML report):

```powershell
cd vision\UI_UX
python demo_cli.py
```

The script generates `report.html` in `vision/UI_UX` with a summary of budgets for sample devices.

---

## 2 — Quick queries with Python one-liners

You can use the `compute_budget` utility directly from the Python REPL or via `python -c` to test budgets or show a one-screen summary.

Examples:

```powershell
python - << 'PY'
from vision.UI_UX.budget import compute_budget
print(compute_budget(1366, 768))
PY
```

Use `naive_summarize` to compute a one-screen summary from text:

```powershell
python - << 'PY'
from vision.UI_UX.budget import compute_budget, naive_summarize
b = compute_budget(1366, 768)
print('target_chars =', b['target_chars'])
print(naive_summarize('Put your full text here', b['target_chars']))
PY
```

This is useful if you want to create your own shell wrappers without an official CLI.

---

## 3 — Recommended CLI design (argparse / Click)

The next step is to add a small CLI wrapper (`vision-ui`) for natural commands. Below is a sample design using `argparse`.

Suggested CLI commands and flags:

- `vision-ui budget --width 1366 --height 768 --font 14 --ruler 80 --buffer 0.9`
  - Prints JSON containing `columns`, `lines`, `char_budget`, `target_chars`.

- `vision-ui summarize --width 1366 --height 768 --text-file errors.log --buffer 0.9`
  - Produces a one-screen summary of the given text file.
  - If you plan to call LLMs from your workflow, add a token-aware mode:
    - `vision-ui summarize --width 1366 --height 768 --text-file errors.log --token-aware --model gpt2`
    - This will compute a token budget based on your screen size and the model's tokenizer, so the LLM output fits the on-screen budget.

- `vision-ui profile save Laptop16x9 --width 1366 --height 768 --font 14 --ruler 80`
- `vision-ui profile load Laptop16x9 --apply --out report.html`

- `vision-ui report --profiles all --out budgets.html`
  - Builds a static HTML report for one or more profiles.

If you want a quick start for an argparse CLI, here's a suggested skeleton you can paste into `vision/UI_UX/cli.py`:

```python
import argparse
from vision.UI_UX.budget import compute_budget, naive_summarize
import json

parser = argparse.ArgumentParser(prog='vision-ui')
sub = parser.add_subparsers(dest='cmd')

bparser = sub.add_parser('budget')
bparser.add_argument('--width', type=int, required=True)
bparser.add_argument('--height', type=int, required=True)
bparser.add_argument('--font', type=int, default=14)
bparser.add_argument('--ruler', type=int, default=80)
bparser.add_argument('--buffer', type=float, default=0.9)

sparser = sub.add_parser('summarize')
sparser.add_argument('--width', type=int, required=True)
sparser.add_argument('--height', type=int, required=True)
sparser.add_argument('--text-file', type=str, required=True)

args = parser.parse_args()
if args.cmd == 'budget':
    b = compute_budget(args.width, args.height, font_size_px=args.font, editor_ruler_columns=args.ruler, buffer=args.buffer)
    print(json.dumps(b, indent=2))
elif args.cmd == 'summarize':
    with open(args.text_file, 'r', encoding='utf-8') as fh:
        text = fh.read()
    b = compute_budget(args.width, args.height)
    print(naive_summarize(text, b['target_chars']))
```

This `vision-ui` skeleton is Python-only and can be extended with `Click` for nicer CLI UX.

---

## 4 — Common usage examples

1. Budget for a laptop profile:
```powershell
vision-ui budget --width 1366 --height 768 --font 14 --ruler 80
```

2. Quick summary of error logs under a single-screen budget:
```powershell
vision-ui summarize --width 390 --height 844 --text-file errors.log
```

3. Make a static report with multiple profiles:
```powershell
vision-ui report --profiles Laptop16x9,UltraWide --out report.html
```

4. Save/load profiles as JSON (conceptual):
```powershell
vision-ui profile save MobileTall --width 390 --height 844 --font 14 --ruler 50
vision-ui profile load MobileTall --out mybudget.json
```

---

## 5 — CI / test integration

To run the unit tests you can use `pytest` in the `vision/UI_UX` folder. The tests validate the budget calculations and the naive summarizer.

```powershell
cd vision\UI_UX
pytest -q test_budget.py
```

Add the test command into your CI pipeline (GitHub Actions, Azure Pipelines, etc). Example `CI` step:

```yaml
- name: Run UI_UX tests
  run: |
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r vision\UI_UX\requirements.txt
    cd vision\UI_UX
    pytest -q

  Add a test to check token-aware budgets by using `estimate_avg_chars_per_token` and rounding to token budgets.
```

---

## 6 — Helpful tips & patterns

- Use editor `ruler`(s) in your profile to anchor `effective_columns` and keep generated replies readable (80 is a good default).
- Use `buffer` to guarantee the generated text will not overflow the editor UI (default buffer is 0.9).
- When creating a summary for long logs, consider `summarize --mode important-lines` that extracts top lines before applying the budget.
- For production summarization, use a token-mapped summarizer (token → char mapping) to keep LLM output consistent with budget; this is a great next step.

---

## 7 — Roadmap for CLI improvements

- Add an official `vision-ui` entry-point (use `pyproject.toml` / `setup.py` console-script entry point). This would provide a canonical CLI for the footprint.
- Add `profile` management so users can save and load budgets with `vision-ui profile save/load`.
- Add `format` options for `report` (CSV, HTML, JSON) and an `--open` switch to open the generated HTML in the default browser.
- Add stream-processing for summarization (read from stdin) to be friendly in Unix pipelines: `tail -n 500 /var/log/app | vision-ui summarize --width 390 --height 844`

---

If you'd like, I can implement a reference `vision-ui` CLI in Python (argparse or Click) and add tests for the CLI behavior. Say the word and I’ll add the CLI skeleton to `vision/UI_UX/cli.py` and wire a console script entry point.