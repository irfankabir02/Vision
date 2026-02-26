"""
token_utils.py

Utilities to estimate tokens↔characters and compute token-aware budgets.
This is optional and will use Hugging Face `transformers` if available; otherwise it falls back
to a safe heuristic (chars_per_token ≈ 4).
"""
from __future__ import annotations

from typing import Optional, Sequence, List, Any
import logging

try:
    # Optional; if unavailable we'll fall back to heuristic
    from transformers import AutoTokenizer, PreTrainedTokenizer, PreTrainedTokenizerFast
    _HF_AVAILABLE = True
except ImportError:
    AutoTokenizer = None  # type: ignore
    PreTrainedTokenizer = None # type: ignore
    PreTrainedTokenizerFast = None # type: ignore
    _HF_AVAILABLE = False

logger = logging.getLogger(__name__)

def get_tokenizer(model_name: str = "gpt2"):
    """Return a tokenizer instance for `model_name` if transformers available.

    This function may download tokenizer data the first time it runs.
    If `transformers` is not installed, returns None.
    Supports modern models like Llama-3, Phi-4, etc.
    """
    if not _HF_AVAILABLE:
        return None
    try:
        # For modern Llama/Phi models, we use AutoTokenizer which handles 
        # LlamaTokenizer or FastTokenizers correctly.
        return AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    except Exception as e:
        logger.error(f"Failed to load tokenizer for {model_name}: {e}")
        return None


def estimate_avg_chars_per_token(samples: Optional[Sequence[str]] = None,
                                  tokenizer=None,
                                  model_name: str = "gpt2",
                                  fallback: float = 4.0) -> float:
    """
    Estimate the average number of characters per token.

    - If `tokenizer` is supplied it will be used.
    - If `transformers` is available and `tokenizer` is None, this will load `model_name`'s tokenizer
      and compute a sample-based average.
    - If there is no tokenizer or an error, this returns `fallback` (default 4.0).

    Returns a float > 0.
    """
    # prefer provided tokenizer
    if tokenizer is None and _HF_AVAILABLE:
        try:
            tokenizer = get_tokenizer(model_name)
        except Exception: 
            tokenizer = None

    if tokenizer is None or samples is None or len(samples) == 0:
        return float(fallback)

    total_chars = 0
    total_tokens = 0
    for s in samples:
        if not s:
            continue
        try:
            # Modern tokenizers encode/tokenize methods
            toks = tokenizer.encode(s, add_special_tokens=False)
            total_chars += len(s)
            total_tokens += len(toks)
        except Exception:
            continue

    if total_tokens == 0:
        return float(fallback)

    return float(total_chars) / float(total_tokens)


def chars_to_tokens(chars: int, chars_per_token: float) -> int:
    """Return the estimated token count for `chars` given the `chars_per_token` ratio."""
    if chars_per_token <= 0:
        raise ValueError("chars_per_token must be > 0")
    return int(max(1, round(chars / float(chars_per_token))))


def tokens_to_chars(tokens: int, chars_per_token: float) -> int:
    """Return the rough char-count that `tokens` would produce, given `chars_per_token`."""
    if tokens < 0:
        raise ValueError("tokens must be >= 0")
    return int(round(tokens * chars_per_token))


def robust_tokens_to_chars(token_ids: List[int], tokenizer: Any) -> int:
    """
    Accurately calculate the character count of a sequence of token IDs.
    This uses the actual tokenizer to decode and measure length.
    """
    if not tokenizer:
        return len(token_ids) * 4 # dumb fallback
    try:
        decoded = tokenizer.decode(token_ids, skip_special_tokens=True)
        return len(decoded)
    except Exception:
        return len(token_ids) * 4
