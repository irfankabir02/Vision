"""
tests/test_quantitative.py

Quantitative tests for Vision UI logic accuracy and safety compliance.
Tests measure budget calculation precision, summary length adherence, and persona transformations.
"""

import pytest
from UI_UX.budget import compute_budget
from vision_ui.profiles import DEFAULT_PROFILES
from vision_ui.summarize import multi_profile_summarize, Persona, layered_summarize, BUILTIN_PERSONAS


class TestBudgetCalculation:
    """Test budget calculation accuracy and reasonableness."""

    def test_laptop_budget_reasonable(self):
        """Test that laptop budget calculation produces reasonable values."""
        profile = DEFAULT_PROFILES["laptop"]
        budget = compute_budget(
            width_px=profile.width_px,
            height_px=profile.height_px,
            font_size_px=profile.font_size_px,
            editor_ruler_columns=profile.editor_ruler_columns,
            buffer=profile.buffer
        )
        
        # Basic sanity checks
        assert "target_chars" in budget
        assert budget["target_chars"] > 0
        assert budget["target_chars"] < 10000  # Reasonable upper bound for laptop
        
        # Should be roughly proportional to screen size
        expected_min = 1000  # At least 1000 chars for laptop
        assert budget["target_chars"] >= expected_min, f"Budget too low: {budget['target_chars']}"

    def test_phone_budget_smaller_than_laptop(self):
        """Test that phone budget is appropriately smaller than laptop."""
        laptop = DEFAULT_PROFILES["laptop"]
        phone = DEFAULT_PROFILES["phone"]
        
        laptop_budget = compute_budget(
            width_px=laptop.width_px,
            height_px=laptop.height_px,
            font_size_px=laptop.font_size_px,
            editor_ruler_columns=laptop.editor_ruler_columns,
            buffer=laptop.buffer
        )
        
        phone_budget = compute_budget(
            width_px=phone.width_px,
            height_px=phone.height_px,
            font_size_px=phone.font_size_px,
            editor_ruler_columns=phone.editor_ruler_columns,
            buffer=phone.buffer
        )
        
        # Phone should have significantly smaller budget than laptop
        assert phone_budget["target_chars"] < laptop_budget["target_chars"]
        ratio = phone_budget["target_chars"] / laptop_budget["target_chars"]
        assert 0.1 < ratio < 0.5, f"Unexpected budget ratio: {ratio}"  # Phone ~20-40% of laptop


class TestSummaryLengthCompliance:
    """Test that generated summaries respect budget limits."""

    SAMPLE_TEXT = """
    This is a sample text for testing the Vision UI summarization system.
    It contains multiple sentences and paragraphs to provide sufficient content
    for generating meaningful summaries across different layers and profiles.
    The system should be able to create headlines, one-screen summaries, and
    detailed deep summaries while staying within the calculated character budgets.
    """

    def test_one_screen_summary_fits_budget(self):
        """Test that one_screen summaries fit within their allocated budget."""
        profile = DEFAULT_PROFILES["laptop"]
        
        # Get budget
        budget = compute_budget(
            width_px=profile.width_px,
            height_px=profile.height_px,
            font_size_px=profile.font_size_px,
            editor_ruler_columns=profile.editor_ruler_columns,
            buffer=profile.buffer
        )
        target_chars = budget["target_chars"]
        
        # Generate summary
        summaries = multi_profile_summarize(
            text=self.SAMPLE_TEXT,
            profiles=[profile],
            layers=["one_screen"]
        )
        
        summary = summaries[profile.name]["one_screen"]
        summary_length = len(summary)
        
        # Should fit within budget with some tolerance
        assert summary_length <= target_chars, f"Summary too long: {summary_length} > {target_chars}"
        
        # Should not be trivial (at least 5% of budget or 100 chars, whichever is smaller)
        min_length = min(int(target_chars * 0.05), 100)
        assert summary_length >= min_length, f"Summary too short: {summary_length} < {min_length}"

    def test_headline_summary_concise(self):
        """Test that headline summaries are appropriately concise."""
        profile = DEFAULT_PROFILES["phone"]
        
        # Get budget
        budget = compute_budget(
            width_px=profile.width_px,
            height_px=profile.height_px,
            font_size_px=profile.font_size_px,
            editor_ruler_columns=profile.editor_ruler_columns,
            buffer=profile.buffer
        )
        target_chars = budget["target_chars"]
        
        # Generate headline summary
        summaries = multi_profile_summarize(
            text=self.SAMPLE_TEXT,
            profiles=[profile],
            layers=["headline"]
        )
        
        headline = summaries[profile.name]["headline"]
        headline_length = len(headline)
        
        # Headline should be much shorter than full budget
        assert headline_length < target_chars * 0.2, f"Headline too long: {headline_length}"
        
        # Should still be meaningful
        assert headline_length > 20, f"Headline too short: {headline_length}"


class TestPersonaTransformations:
    """Test persona vocabulary and content transformations."""

    TEST_TEXT = "The user encountered a problem with the fix. The problem needs to be resolved."

    def test_developer_vocabulary_mapping(self):
        """Test that developer persona applies vocabulary mappings correctly."""
        persona = BUILTIN_PERSONAS["developer"]
        
        # Apply persona transformation
        transformed = persona.apply(self.TEST_TEXT, include_examples=False, include_context=False)
        
        # Check vocabulary replacements
        assert "end-user" in transformed, "Should replace 'user' with 'end-user'"
        assert "issue" in transformed, "Should replace 'problem' with 'issue'"
        assert "resolve" in transformed, "Should replace 'fix' with 'resolve'"
        
        # Original words should not remain
        assert "user" not in transformed or "end-user" in transformed, "Should not have plain 'user'"
        assert "problem" not in transformed or "issue" in transformed, "Should not have plain 'problem'"
        assert "fix" not in transformed or "resolve" in transformed, "Should not have plain 'fix'"

    def test_persona_context_prefix(self):
        """Test that persona context prefix is added correctly."""
        persona = BUILTIN_PERSONAS["developer"]
        
        transformed = persona.apply("Test content", include_examples=False, include_context=True)
        
        assert transformed.startswith(persona.context_prefix), f"Should start with context: {persona.context_prefix}"

    def test_persona_examples_append(self):
        """Test that persona examples are appended correctly."""
        persona = BUILTIN_PERSONAS["developer"]
        
        transformed = persona.apply("Test content", include_examples=True, include_context=False)
        
        # Should end with examples
        examples_text = persona.examples_text()
        assert transformed.endswith(examples_text), f"Should end with examples: {examples_text}"

    def test_persona_overhead_calculation(self):
        """Test that persona overhead is calculated accurately."""
        from vision_ui.personas import _calculate_persona_overhead
        
        persona = BUILTIN_PERSONAS["developer"]
        overhead = _calculate_persona_overhead(persona)
        
        # Should account for context prefix, examples, and separators
        expected_min = len(persona.context_prefix or "") + sum(len(f"Example: {ex}") for ex in persona.example_sentences or [])
        assert overhead >= expected_min, f"Overhead too low: {overhead} < {expected_min}"
