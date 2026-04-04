# UI AI

> Multi-profile, screen-aware text summarization with OCR support and rich triage board interface.

## 🎯 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/irfankabir02/Vision.git
cd Vision

# Install with uv
uv sync

# Install OCR dependencies (optional, for screenshot features)
# On Ubuntu/Debian:
sudo apt-get install tesseract-ocr
# On macOS:
brew install tesseract
# On Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

### Basic Usage

**1. Multi-Profile Text Summarization**
```bash
# Summarize text for different device contexts
vision-ui summarize-multi --file document.txt --profiles phone,laptop,slides --persona developer

# Compare results in rich triage board format
vision-ui triage-compare --text document.txt --profiles phone,laptop --show-profile-info
```

**2. Screenshot OCR Summarization**
```bash
# Extract text from screenshots and summarize
vision-ui summarize-screenshot --image screenshot.png --profiles phone,laptop --format triage --verbose
```

**3. Budget Analysis**
```bash
# Calculate character budgets for different screen configurations
vision-ui budget --width 1920 --height 1080 --font-size 16
```

## 🚀 Features

### Phase 1: Multi-Profile Summarization
- **Device-Aware Budgeting**: Automatic character budget calculation based on screen dimensions
- **Persona System**: Developer, designer, and manager personas with vocabulary and context adaptation
- **Layered Summaries**: Headline, one-screen, and deep analysis layers
- **Multi-Profile Support**: Phone, laptop, slides, and custom device profiles

### Phase 2: OCR & Screenshot Analysis
- **Image Preprocessing**: Grayscale conversion, contrast enhancement, resizing, and binarization
- **Text Extraction**: pytesseract integration with confidence filtering
- **Region Classification**: Automatic categorization of code, UI elements, URLs, and text
- **Layout-Aware Analysis**: Text density estimation and budget adjustment

### Phase 3: Rich Triage Board
- **Side-by-Side Comparison**: Visual comparison across device contexts
- **Color-Coded Feedback**: Length-based styling (green/yellow/orange/red)
- **OCR Metadata Display**: Processing information and quality metrics
- **Professional Formatting**: Rich console tables with device icons

## 📋 CLI Commands

### `summarize-multi`
Generate multi-profile summaries from text input.

```bash
vision-ui summarize-multi --file INPUT.txt --profiles phone,laptop,slides \
  --layers headline,one_screen --persona developer
```

**Options:**
- `--file`: Input text file or `-` for stdin
- `--profiles`: Comma-separated profile names
- `--layers`: Summary layers to generate
- `--persona`: Optional persona for content adaptation
- `--format`: Output format (stacked, json, compact)

### `triage-compare`
Display summaries in rich triage board format.

```bash
vision-ui triage-compare --text INPUT.txt --profiles phone,laptop \
  --persona designer --show-profile-info
```

**Options:**
- `--text`: Input text file or `-` for stdin
- `--profiles`: Device profiles to compare
- `--show-profile-info`: Display detailed profile specifications

### `summarize-screenshot`
Extract text from screenshots and generate summaries.

```bash
vision-ui summarize-screenshot --image screenshot.png --profiles phone,laptop \
  --format triage --verbose --show-profile-info
```

**Options:**
- `--image`: Path to screenshot image file
- `--profiles`: Target device profiles
- `--format`: Output format (includes triage)
- `--verbose`: Show OCR processing metadata

### `budget`
Calculate character budgets for screen configurations.

```bash
vision-ui budget --width 1920 --height 1080 --font-size 16 --columns 80
```

## Release snippet

We publish releases using semantic version tags (vMAJOR.MINOR.PATCH). To create a release:

1. Bump the version in `pyproject.toml`.
2. Build and test the package locally:

```bash
uv build
uv run pytest -q
```

3. Tag and push the release:

```bash
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin v0.1.1
```

The GitHub `release.yml` workflow will create a GitHub release. Note: the `vision-ui` name on PyPI is taken by an unrelated package — use a prefixed name if publishing (e.g., `grid-vision-ui`).

## 🎨 Output Examples

### Rich Triage Board
```
🎯 MULTI-PROFILE TRIAGE BOARD

📱 Headline Layer
┌─────────┬───────────┬──────────┬─────────────────────────────┬──────────┐
│ Profile │ Device    │ Screen   │ Summary                    │ Length   │
├─────────┼───────────┼──────────┼─────────────────────────────┼──────────┤
│ PHONE   │ 📱 Mobile │ 375×667  │ Concise mobile summary      │ 140      │
│ LAPTOP  │ 💻 Laptop │ 1920×1080│ Detailed desktop summary    │ 437      │
└─────────┴───────────┴──────────┴─────────────────────────────┴──────────┘
```

### OCR Metadata
```
=== OCR METADATA ===
Text density: 75.00%
Regions found: 5
Preprocessing applied: grayscale, enhance, sharpen
Image size: 1200 × 900
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/test_profiles.py          # Profile system
uv run pytest tests/test_summarize.py         # Multi-profile summarization
uv run pytest tests/test_ocr.py               # OCR functionality
uv run pytest tests/test_triage.py            # Triage board formatting
uv run pytest tests/test_screenshot_integration.py  # End-to-end integration

# Run with coverage
uv run pytest --cov=vision_ui --cov-report=html
```

## 🏗️ Architecture

Vision UI is a modular screen-aware summarization system with safety-first design. The architecture separates concerns into specialized components for maintainability and extensibility.

### Core Components
- **Profiles**: Device-specific configurations (phone, laptop, slides, tweet)
- **Budget Calculation**: Pixel-to-character limit computation with font metrics
- **Personas**: User-role transformations avoiding perpetrator voice patterns
- **Layered Summarization**: Headline/one-screen/deep layers with budget constraints
- **OCR Integration**: Image preprocessing and text extraction for screenshots
- **CLI Interface**: Command-line orchestration with rich formatting

### Safety Foundations
- **LIMITATIONS Blocks**: All files acknowledge keyword matching insufficiency
- **Perpetrator Voice Prevention**: Nominalization and persona transformations
- **Budget Enforcement**: Hard character limits prevent information overload

### Pipeline Flow
1. Input parsing (text/OCR) → 2. Profile selection → 3. Budget calculation → 4. Persona application → 5. Layered summarization → 6. Output formatting

### Baselines
- **105 tests pass** with comprehensive coverage
- **Budget accuracy** within 5% of expected calculations
- **Safety compliance** with 100% persona transformation fidelity

For detailed architecture documentation including example use cases and implementation details, see [`ARCHITECTURE.md`](ARCHITECTURE.md).

```
vision/
├── vision_ui/                 # Main package
│   ├── cli.py                 # Command-line interface
│   ├── profiles.py            # Device profile management
│   ├── personas.py            # Persona transformations
│   ├── layered_summarizer.py  # Multi-layer summarization
│   ├── summarize.py           # Multi-profile coordination
│   ├── screenshot_handlers.py # OCR integration
│   ├── ocr.py                 # Image processing
│   └── triage.py              # Rich display system
├── UI_UX/                     # Core utilities
│   └── budget.py              # Screen budget calculations
├── tests/                     # Test suite (105 tests)
├── ARCHITECTURE.md            # Detailed documentation
└── pyproject.toml             # Package configuration
```

## 📊 Device Profiles

| Profile  | Resolution | Font Size | Columns | Budget    |
|----------|------------|-----------|---------|-----------|
| Phone    | 375×667    | 14px      | 40      | ~1,600    |
| Laptop   | 1920×1080  | 16px      | 80      | ~8,000    |
| Slides   | 1024×768   | 18px      | 60      | ~4,500    |
| Tweet    | 400×400    | 14px      | 30      | ~800      |

## 🔧 Configuration

### Custom Profiles
Create custom device profiles by modifying `vision_ui/profiles.py`:

```python
Profile(
    name="tablet",
    width_px=768,
    height_px=1024,
    font_size_px=15,
    editor_ruler_columns=50,
    buffer=0.85
)
```

### Persona Customization
Extend personas with vocabulary mappings and context prefixes in the persona system.

## 🤝 Contributing

Contributions are welcome! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
uv sync --group dev
uv run pytest
uv run pip-audit
```

## 📄 License

This project is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for details.

## 📖 Documentation

- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** — Detailed project explanation, implemented use cases, unexplored opportunities, and growth strategy
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System architecture, component descriptions, and baselines
- **[roadmap.md](roadmap.md)** — Phase-by-phase development roadmap and acceptance criteria
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Contribution guidelines and development workflow

## 🔗 Related Projects

- **UI_UX**: Core screen budget and text processing utilities
- **Vision**: Future computer vision and neural network components

---

Built by [irfankabir02](https://github.com/irfankabir02).
