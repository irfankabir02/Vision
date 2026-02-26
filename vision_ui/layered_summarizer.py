"""
LIMITATIONS:

This file uses keyword matching for safety, which is insufficient for production without classifier context.
"""

"""
vision_ui.layered_summarizer

Layered summarization logic for multi-layer summaries across different character budgets.
Handles headline, one_screen, and deep layer generation with persona support.
"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass

from .personas import Persona, _calculate_persona_overhead
from UI_UX.budget import naive_summarize


@dataclass
class LayerConfig:
    """Configuration for a summary layer."""
    name: str
    budget_multiplier: float  # Fraction of target_chars to use
    max_sentences: Optional[int] = None
    include_hash: bool = False  # For deep layer - include content hash


# Default layer configurations
DEFAULT_LAYERS: Dict[str, LayerConfig] = {
    "headline": LayerConfig(
        name="headline",
        budget_multiplier=0.1,  # 10% of budget
        max_sentences=2
    ),
    "one_screen": LayerConfig(
        name="one_screen", 
        budget_multiplier=0.8,  # 80% of budget
        max_sentences=None
    ),
    "deep": LayerConfig(
        name="deep",
        budget_multiplier=1.0,  # Full budget
        include_hash=True
    )
}


def layered_summarize(
    text: str,
    char_budget: int,
    layers: List[str],
    persona: Optional[Persona] = None,
    summarizer: Optional[Callable[[str, int], str]] = None
) -> Dict[str, str]:
    """
    Generate layered summaries for a single character budget.
    
    Args:
        text: Input text to summarize
        char_budget: Available character budget
        layers: List of layer names to generate
        persona: Optional persona adapter
        summarizer: Optional custom summarizer function
        
    Returns:
        Dictionary mapping layer names to summaries
    """
    if summarizer is None:
        summarizer = naive_summarize
    
    results = {}
    
    for layer_name in layers:
        if layer_name not in DEFAULT_LAYERS:
            raise ValueError(f"Unknown layer: {layer_name}")
        
        layer_config = DEFAULT_LAYERS[layer_name]
        layer_budget = int(char_budget * layer_config.budget_multiplier)
        
        # Calculate persona overhead if persona is specified
        persona_overhead = 0
        if persona:
            persona_overhead = _calculate_persona_overhead(persona)
        
        # Calculate hash overhead for deep layer
        hash_overhead = 15 if layer_config.include_hash else 0  # "[hash:xxxxxxxx] "
        
        # Adjust budget for overheads
        effective_budget = layer_budget
        if persona and layer_name == "headline":
            # Headline layer always uses vocabulary-only persona for conciseness
            if persona.vocabulary_mappings:
                transformed_text = text
                for old_word, new_word in persona.vocabulary_mappings.items():
                    transformed_text = transformed_text.replace(old_word, new_word)
                summary = summarizer(transformed_text, effective_budget - hash_overhead)
            else:
                summary = summarizer(text, effective_budget - hash_overhead)
        elif persona and persona.examples_location == "append":
            # Append persona examples after generating the summary; do not make examples consume
            # the text budget so headlines remain concise and one_screen/detailed layers can include
            # persona material as an addendum.
            effective_budget = layer_budget - hash_overhead
            summary = summarizer(text, effective_budget)
            # Append examples/context as a postfix if present
            examples = persona.examples_text()
            context = persona.context_text()
            postfix_items = []
            if context:
                postfix_items.append(context)
            if examples:
                postfix_items.append(examples)
            if postfix_items:
                summary = summary.strip() + "\n\n" + "\n\n".join(postfix_items)
        elif persona and layer_budget > persona_overhead + hash_overhead + 20:  # Keep at least 20 chars for content
            # Other layers use full persona if budget permits
            effective_budget = layer_budget - persona_overhead - hash_overhead
            # Apply persona transformation for summarization (includes examples/context)
            persona_text = persona.apply(text)
            summary = summarizer(persona_text, effective_budget)
        else:
            # No persona or insufficient budget - summarize original text
            summary = summarizer(text, effective_budget - hash_overhead)
        
        # Add hash for deep layer if requested
        if layer_config.include_hash:
            import hashlib
            content_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            summary = f"[hash:{content_hash}] {summary}"
        
        results[layer_name] = summary
    
    return results
