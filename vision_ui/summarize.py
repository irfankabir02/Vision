"""
LIMITATIONS:

This file uses keyword matching for safety, which is insufficient for production without classifier context.
"""

"""
vision_ui.summarize

Multi-profile summarization coordination and output formatting.
Integrates layered summarization with persona adaptations across device profiles.
"""

from typing import Dict, List, Optional, Callable, Any

from .profiles import Profile, load_profile, parse_profiles_from_cli
from UI_UX.budget import compute_budget, naive_summarize
from .personas import Persona, BUILTIN_PERSONAS
from .layered_summarizer import layered_summarize


def multi_profile_summarize(
    text: str,
    profiles: List[Profile],
    layers: List[str] = ['headline', 'one_screen', 'deep'],
    persona: Optional[str] = None,
    summarizer: Optional[Callable[[str, int], str]] = None
) -> Dict[str, Dict[str, str]]:
    """
    Generate multi-profile, multi-layer summaries.
    
    Args:
        text: Input text to summarize
        profiles: List of Profile objects
        layers: List of layer names to generate for each profile
        persona: Optional persona name from BUILTIN_PERSONAS
        summarizer: Optional custom summarizer function
        
    Returns:
        Nested dictionary: {profile_name: {layer_name: summary}}
    """
    if summarizer is None:
        summarizer = naive_summarize
    
    persona_obj = None
    if persona:
        if persona not in BUILTIN_PERSONAS:
            raise ValueError(f"Unknown persona: {persona}. Available: {list(BUILTIN_PERSONAS.keys())}")
        persona_obj = BUILTIN_PERSONAS[persona]
    
    results = {}
    
    for profile in profiles:
        # Compute budget for this profile
        budget = compute_budget(
            width_px=profile.width_px,
            height_px=profile.height_px,
            font_size_px=profile.font_size_px,
            editor_ruler_columns=profile.editor_ruler_columns,
            buffer=profile.buffer
        )
        
        target_chars = budget["target_chars"]
        
        # Generate layered summaries for this profile
        profile_summaries = layered_summarize(
            text=text,
            char_budget=target_chars,
            layers=layers,
            persona=persona_obj,
            summarizer=summarizer
        )
        
        results[profile.name] = profile_summaries
    
    return results


def format_multi_profile_output(
    summaries: Dict[str, Dict[str, str]],
    format_type: str = "stacked"
) -> str:
    """
    Format multi-profile summaries for display.
    
    Args:
        summaries: Output from multi_profile_summarize
        format_type: "stacked", "json", or "compact"
        
    Returns:
        Formatted string
    """
    if format_type == "json":
        import json
        return json.dumps(summaries, indent=2)
    
    elif format_type == "compact":
        lines = []
        for profile_name, profile_summaries in summaries.items():
            for layer_name, summary in profile_summaries.items():
                lines.append(f"{profile_name}.{layer_name}: {summary}")
        return "\n".join(lines)
    
    else:  # stacked (default)
        lines = []
        for profile_name, profile_summaries in summaries.items():
            lines.append(f"=== {profile_name.upper()} ===")
            for layer_name, summary in profile_summaries.items():
                lines.append(f"--- {layer_name.title().replace('_', ' ')} ---")
                lines.append(summary.strip())
                lines.append("")  # Empty line between layers
            lines.append("")  # Empty line between profiles
        return "\n".join(lines).strip()
