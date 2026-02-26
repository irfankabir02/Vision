"""
LIMITATIONS:

This file uses keyword matching for safety, which is insufficient for production without classifier context.
"""

"""
vision_ui.personas

Persona management for text transformation and adaptation in summarization.
Provides vocabulary mappings, example sentences, and context prefixes for different user roles.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Persona:
    """Persona adapter for text transformation before summarization."""
    name: str
    vocabulary_mappings: Optional[Dict[str, str]] = None
    example_sentences: Optional[List[str]] = None
    context_prefix: Optional[str] = None
    
    examples_location: str = "append"  # one of: 'prepend', 'append', 'none'

    def examples_text(self) -> str:
        """Return the persona example lines as a single text block."""
        if not self.example_sentences:
            return ""
        return "\n".join(f"Example: {example}" for example in self.example_sentences)

    def context_text(self) -> str:
        return self.context_prefix or ""

    def apply(self, text: str, include_examples: bool = True, include_context: bool = True) -> str:
        """Apply persona transformations to text."""
        transformed = text
        
        # Apply vocabulary mappings first (before adding other content)
        if self.vocabulary_mappings:
            for old_word, new_word in self.vocabulary_mappings.items():
                transformed = transformed.replace(old_word, new_word)
        
        # Add context prefix if specified
        if include_context and self.context_prefix:
            transformed = f"{self.context_prefix}\n\n{transformed}"

        # Add example sentences if specified
        if include_examples and self.example_sentences and self.examples_location == "prepend":
            examples = self.examples_text()
            transformed = f"{examples}\n\n{transformed}"

        if include_examples and self.example_sentences and self.examples_location == "append":
            examples = self.examples_text()
            transformed = f"{transformed}\n\n{examples}"
        
        return transformed


# Built-in personas
BUILTIN_PERSONAS: Dict[str, Persona] = {
    "developer": Persona(
        name="developer",
        vocabulary_mappings={"user": "end-user", "problem": "issue", "fix": "resolve"},
        example_sentences=["Focus on technical implementation details.", "Consider API design patterns."],
        context_prefix="As a software developer reviewing this content:"
    ),
    "designer": Persona(
        name="designer", 
        vocabulary_mappings={"functionality": "user experience", "code": "interface"},
        example_sentences=["Consider visual hierarchy and layout.", "Focus on user interaction patterns."],
        context_prefix="From a UX/UI design perspective:"
    ),
    "manager": Persona(
        name="manager",
        vocabulary_mappings={"technical": "strategic", "implementation": "execution"},
        example_sentences=["Consider business impact and timeline.", "Focus on resource allocation."],
        context_prefix="From a project management viewpoint:"
    )
}


def _calculate_persona_overhead(persona: Persona) -> int:
    """Calculate the character overhead added by persona transformation."""
    overhead = 0
    
    # Context prefix overhead
    if persona.context_prefix:
        overhead += len(persona.context_prefix) + 2  # +2 for newlines
    
    # Example sentences overhead
    if persona.example_sentences:
        for example in persona.example_sentences:
            overhead += len(f"Example: {example}") + 1  # +1 for newline
    
    # Add separators if both exist
    if persona.context_prefix and persona.example_sentences:
        overhead += 2  # Extra newlines between sections
    
    return overhead
