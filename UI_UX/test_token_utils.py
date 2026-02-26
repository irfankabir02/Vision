from UI_UX.token_utils import (estimate_avg_chars_per_token, chars_to_tokens, tokens_to_chars)


def test_chars_tokens_roundtrip():
    # For fallback behavior (no tokenizer installed), we expect a default
    ratio = estimate_avg_chars_per_token(samples=["hello world", "this is a test"], tokenizer=None)
    assert ratio > 0
    tokens = chars_to_tokens(1000, ratio)
    chars = tokens_to_chars(tokens, ratio)
    assert isinstance(tokens, int)
    assert isinstance(chars, int)
    # Roundtrip should produce a chars number close to original budget (within factor 2)
    assert 500 <= chars <= 2000
