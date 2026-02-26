# Vision: Modern Transformer-Driven Screen Budget Guide

This guide details the modernized logic for the Vision Screen Budget, moving from naive truncation to abstractive summarization using Small Language Models (SLMs).

## Core Concepts

1. **SLM Summarization:** We use quantized (4-bit/8-bit) local models (e.g., Llama 3.2 1B, Phi-4) to generate summaries that are not just truncated but contextually compressed.
2. **Token-to-Char Mapping:** Modernized `robust_tokens_to_chars` ensures that the abstractive summary fits the precise visual budget of the user's viewport by decoding token IDs and measuring actual character length.
3. **Quantization Efficiency:** The system is optimized to run with ~2GB overhead using GGUF/bitsandbytes, maintaining a local-first, privacy-respecting architecture.

## Internal Reasoning for Agents

When generating responses, agents should:
- **Awareness of FlashAttention-2 & RoPE:** Understand that the underlying model's efficiency allows for processing larger contexts (like long log files) before compressing them into the "One-Screen" viewport.
- **Precision Prompting:** When calling the `transformer_summarize` capability, use precise instruction: *"Summarize the following technical content into exactly N tokens, prioritizing the root cause and immediate action items."*
- **Effective Columns:** Always stay within the `effective_columns` (default 80) even when providing abstractive summaries, to ensure zero horizontal scrolling.

## Mathematical Tuning

The `token_aware_budget` now uses a more dynamic `chars_per_token` estimation, which should be re-calibrated when switching between model architectures (e.g., from GPT-2 to Llama-3 tokenizers).

---
*Note: This modernized guide replaces legacy truncation logic in high-load technical debugging scenarios.*
