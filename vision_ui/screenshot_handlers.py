"""
LIMITATIONS:

This file uses keyword matching for safety, which is insufficient for production without classifier context.
"""

"""
vision_ui.screenshot_handlers

Screenshot-aware summarization handlers for OCR-based text extraction and profile adjustment.
Provides functions to process screenshots and generate multi-profile summaries.
"""

from typing import Dict, List, Optional, Callable, Any
from pathlib import Path

from .profiles import Profile
from UI_UX.budget import compute_budget
from .ocr import OCRExtractor, ScreenshotAnalyzer, OCRResult


def screenshot_aware_summarize(
    image_path: str,
    profiles: List[Profile],
    layers: List[str] = ['headline', 'one_screen'],
    persona: Optional[str] = None,
    summarizer: Optional[Callable[[str, int], str]] = None,
    ocr_analyzer: Optional[ScreenshotAnalyzer] = None
) -> Dict[str, Dict[str, str]]:
    """
    Generate multi-profile summaries from a screenshot using OCR.
    
    Args:
        image_path: Path to the screenshot image file
        profiles: List of Profile objects for target devices
        layers: List of layer names to generate
        persona: Optional persona name from BUILTIN_PERSONAS
        summarizer: Optional custom summarizer function
        ocr_analyzer: Optional ScreenshotAnalyzer instance
        
    Returns:
        Nested dictionary: {profile_name: {layer_name: summary}}
    """
    # Initialize OCR analyzer
    if ocr_analyzer is None:
        ocr_analyzer = ScreenshotAnalyzer()
    
    # Extract text from screenshot
    try:
        ocr_result = ocr_analyzer.analyze_screenshot(image_path)
    except Exception as e:
        raise RuntimeError(f"Failed to analyze screenshot: {e}")
    
    if not ocr_result.full_text.strip():
        raise ValueError("No text found in screenshot")
    
    # Extract structured regions for layout-aware processing
    regions_by_type = ocr_analyzer.extract_ui_regions(ocr_result)
    
    # Estimate text density for budget adjustment
    text_density = ocr_analyzer.estimate_text_density(ocr_result)
    
    # Adjust profiles based on screenshot content
    adjusted_profiles = _adjust_profiles_for_screenshot(profiles, ocr_result, text_density)
    
    # Import here to avoid circular import
    from .summarize import multi_profile_summarize
    
    # Generate summaries using extracted text
    summaries = multi_profile_summarize(
        text=ocr_result.full_text,
        profiles=adjusted_profiles,
        layers=layers,
        persona=persona,
        summarizer=summarizer
    )
    
    # Add OCR metadata to summaries
    summaries['_ocr_metadata'] = {
        'text_density': text_density,
        'regions_found': len(ocr_result.regions),
        'preprocessing_applied': ocr_result.preprocessing_applied,
        'image_size': ocr_result.image_info['size']
    }
    
    return summaries


def _adjust_profiles_for_screenshot(
    profiles: List[Profile], 
    ocr_result: OCRResult, 
    text_density: float
) -> List[Profile]:
    """
    Adjust profile budgets based on screenshot content characteristics.
    
    Args:
        profiles: Original list of Profile objects
        ocr_result: OCR extraction result
        text_density: Estimated text density (0.0 to 1.0)
        
    Returns:
        List of adjusted Profile objects
    """
    adjusted_profiles = []
    
    for profile in profiles:
        # Create a copy of the profile
        adjusted_profile = Profile(
            name=profile.name,
            width_px=profile.width_px,
            height_px=profile.height_px,
            font_size_px=profile.font_size_px,
            editor_ruler_columns=profile.editor_ruler_columns,
            buffer=profile.buffer,
            image_regions=profile.image_regions
        )
        
        # Adjust buffer based on text density
        # Higher text density = more conservative budget
        if text_density > 0.7:
            adjusted_profile.buffer = max(0.7, profile.buffer - 0.1)  # Reduce buffer for dense content
        elif text_density < 0.3:
            adjusted_profile.buffer = min(0.95, profile.buffer + 0.05)  # Increase buffer for sparse content
        
        adjusted_profiles.append(adjusted_profile)
    
    return adjusted_profiles


def extract_text_from_screenshot(image_path: str, preprocess: bool = True) -> str:
    """
    Convenience function to extract text from a screenshot.
    
    Args:
        image_path: Path to the screenshot image file
        preprocess: Whether to apply preprocessing
        
    Returns:
        Extracted text as string
    """
    extractor = OCRExtractor()
    result = extractor.extract_text(image_path, preprocess=preprocess)
    return result.full_text


def summarize_screenshot(
    image_path: str,
    profile_name: str = "laptop",
    layer: str = "one_screen",
    persona: Optional[str] = None
) -> str:
    """
    Convenience function to summarize a screenshot for a single profile and layer.
    
    Args:
        image_path: Path to the screenshot image file
        profile_name: Name of the target profile
        layer: Name of the summary layer
        persona: Optional persona name
        
    Returns:
        Generated summary as string
    """
    from .profiles import load_profile
    profile = load_profile(profile_name)
    summaries = screenshot_aware_summarize(
        image_path=image_path,
        profiles=[profile],
        layers=[layer],
        persona=persona
    )
    
    return summaries[profile.name][layer]
