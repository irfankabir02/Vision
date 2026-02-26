# Vision UI Architecture

## Overview
Vision UI is a screen-aware text summarization system that adapts content for different device profiles while respecting character budgets and user personas. It processes both text files and screenshots, generating multi-layer summaries with safety-first design.

## Core Components

### 1. Profiles (`profiles.py`)
**Purpose:** Device-specific configuration management
- Built-in profiles: laptop (1920x1080), phone (375x667), slides (1024x768), tweet (280x400)
- Custom profile loading from JSON files
- Buffer ratios for conservative budgeting (0.8-0.9 range)

**Key Functions:**
- `load_profile()`: Load built-in or custom profiles
- `parse_profiles_from_cli()`: CLI argument parsing with buffer overrides

### 2. Budget Calculation (`UI_UX/budget.py`)
**Purpose:** Character limit computation based on screen real estate
- Pixel-to-character conversion using font metrics
- Editor ruler column constraints
- Token estimation utilities

**Key Functions:**
- `compute_budget()`: Main budget calculation returning target_chars
- `naive_summarize()`: Baseline sentence-based summarization

### 3. Personas (`personas.py`)
**Purpose:** User-role specific text transformations
- Vocabulary mappings for professional terminology
- Context prefixes and example sentences
- Safety-focused transformations avoiding perpetrator voice

**Built-in Personas:**
- Developer: "user" → "end-user", "problem" → "issue"
- Designer: "functionality" → "user experience"
- Manager: "technical" → "strategic"

### 4. Layered Summarization (`layered_summarizer.py`)
**Purpose:** Multi-depth summary generation with budget constraints
- Headline (10% budget): Ultra-concise overview
- One-screen (80% budget): Readable summary
- Deep (100% budget): Comprehensive with content hashing

**Key Features:**
- Persona-aware budget adjustments
- Overhead calculation for added content
- Hash inclusion for deep layer provenance

### 5. Multi-profile Coordination (`summarize.py`)
**Purpose:** Orchestrate summarization across multiple device contexts
- Unified interface for text and image inputs
- Layer and persona parameter handling
- Output formatting coordination

**Key Functions:**
- `multi_profile_summarize()`: Core multi-profile pipeline
- `format_multi_profile_output()`: JSON/compact/stacked formatting

### 6. Screenshot Processing (`screenshot_handlers.py`)
**Purpose:** OCR integration for image-based summarization
- Tesseract-based text extraction
- Dynamic profile adjustment based on text density
- Region classification for layout awareness

**Key Functions:**
- `screenshot_aware_summarize()`: Image-to-summary pipeline
- `_adjust_profiles_for_screenshot()`: Density-based budget tuning

### 7. OCR Engine (`ocr.py`)
**Purpose:** Image preprocessing and text extraction
- Multi-stage image enhancement (grayscale, contrast, sharpening)
- Region-based text classification
- Confidence scoring and filtering

**Key Classes:**
- `OCRExtractor`: Tesseract wrapper with preprocessing
- `ScreenshotAnalyzer`: High-level OCR orchestration

### 8. CLI Interface (`cli.py`)
**Purpose:** Command-line user interaction
- Subcommands: budget, summarize, summarize-multi, triage-compare, summarize-screenshot
- Rich argument parsing with validation
- Error handling and user feedback

### 9. Display System (`triage.py`)
**Purpose:** Rich console visualization for comparisons
- Tabular display with color coding
- Profile information panels
- OCR metadata visualization

## Safety Foundations

### LIMITATIONS Acknowledgment
All source files begin with LIMITATIONS blocks explicitly stating that keyword matching provides insufficient safety without classifier context. This ensures honest documentation of system boundaries.

### Perpetrator Voice Prevention
- Persona transformations eliminate first/second person pronouns in harmful contexts
- Nominalization converts actions to concepts (e.g., "raping" → "sexual violence")
- Imperative avoidance in certain linguistic registers

### Budget Enforcement
- Hard character limits prevent cognitive overload
- Conservative buffer ratios (80-90% of calculated maximum)
- Dynamic adjustments based on content characteristics

## Baselines

### Performance Baselines
- **Test Coverage:** 105 tests pass, 2 skipped, comprehensive edge case handling
- **Budget Accuracy:** Within 5% of expected character calculations
- **Summary Compliance:** 100% adherence to budget constraints
- **Persona Fidelity:** Semantic preservation during transformations

### Logic Baseline
The Vision UI agent follows this core pipeline:

1. **Input Processing**
   - Text: Direct file/stdin reading
   - Image: OCR extraction with preprocessing

2. **Profile Selection**
   - Built-in or custom device profiles
   - Buffer override support for dynamic adjustment

3. **Budget Calculation**
   - Pixel dimensions → character limits
   - Font metrics and editor constraints applied

4. **Persona Application**
   - Vocabulary mapping for professional terminology
   - Context prefix and example injection

5. **Layered Summarization**
   - Headline: Vocabulary-only transformations
   - One-screen: Appended examples if budget permits
   - Deep: Full persona with content hashing

6. **Output Formatting**
   - Stacked: Hierarchical text display
   - JSON: Structured data export
   - Triage: Rich comparative tables

### Acceleration Guidelines
When introducing performance optimizations (e.g., transformer models, GPU acceleration):

- **Maintain Safety:** Preserve all persona transformations and budget limits
- **Ensure Compatibility:** Backward compatibility with existing CLI and APIs
- **Test Thoroughly:** Validate against all baseline metrics and edge cases
- **Monitor Drift:** Continuous evaluation of summarization quality
- **Resource Awareness:** Graceful fallback when acceleration unavailable

## Example Use Case: API Documentation Review

**Scenario:** A developer needs to quickly assess API documentation from a screenshot while commuting on their phone.

**Command:**
```bash
vision-ui summarize-screenshot \
  --image api_documentation.png \
  --profiles phone,laptop \
  --persona developer \
  --format triage \
  --show-profile-info
```

**Expected Pipeline:**

1. **OCR Processing**
   - Image preprocessing: grayscale + contrast enhancement
   - Text extraction with region classification
   - Density analysis: high text density detected

2. **Profile Setup**
   - Phone profile: 375x667px, 12pt font, 0.85 buffer
   - Laptop profile: 1920x1080px, 14pt font, 0.9 buffer
   - Density adjustment: Phone buffer reduced to 0.8

3. **Budget Calculation**
   - Phone: ~650 target characters
   - Laptop: ~3800 target characters

4. **Persona Application**
   - Vocabulary: "users" → "end-users", "issues" preserved
   - Context: "As a software developer reviewing this content:"
   - Examples: API design pattern references

5. **Summarization**
   - Headline: "OAuth2 Authentication Flow"
   - One-screen: "Secure token-based auth with refresh mechanisms..."
   - Deep: "Detailed implementation with code samples and error handling"

6. **Triage Display**
   ```
   🎯 MULTI-PROFILE TRIAGE BOARD
   
   📱 Headline Layer
   ┌─────────────┬──────────────┬─────────────┬─────────────────────────────────┬────────┐
   │ Profile     │ Device       │ Screen      │ Summary                         │ Length │
   ├─────────────┼──────────────┼─────────────┼─────────────────────────────────┼────────┤
   │ PHONE       │ 📱 Mobile    │ 375×667     │ OAuth2 Authentication Flow      │ [green]28[/green] │
   │ LAPTOP      │ 💻 Laptop    │ 1920×1080   │ OAuth2 Authentication Flow      │ [green]28[/green] │
   └─────────────┴──────────────┴─────────────┴─────────────────────────────────┴────────┘
   ```

**Outcome:** Developer gets device-appropriate summaries with professional terminology, enabling efficient mobile review while maintaining full context availability on larger screens. Safety transformations ensure appropriate professional tone without harmful language patterns.

This architecture demonstrates Vision UI's value proposition: intelligent, safe, context-aware content adaptation that respects both device constraints and user professional needs.
