import os
import sys

# Ensure the repo root is on sys.path so imports work when running tests
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from UI_UX.budget import compute_budget, naive_summarize

def test_compute_budget_basic():
    b = compute_budget(1366, 768, font_size_px=14)
    assert b["columns"] > 0
    assert b["lines"] > 0
    assert b["char_budget"] >= b["target_chars"]


def test_naive_summarize_respects_limit():
    text = "One sentence. Two sentence is longer. Three short."
    s = naive_summarize(text, 10)
    # If the first sentence is longer than the char limit, we should fall back to
    # a truncated string that ends with '...'; otherwise the returned summary is
    # within the requested char limit.
    assert len(s) <= 10 or s.endswith('...')


def test_naive_summarize_truncates_very_small():
    text = "One sentence. Two sentence is longer. Three short."
    s = naive_summarize(text, 3)
    # For very small char limits we must fall back to truncation with an ellipsis
    assert s.endswith('...')
