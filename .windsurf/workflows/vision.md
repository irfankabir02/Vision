---
description: Screen-aware summarization workflow with persona adapters and budget compliance
auto_execution_mode: 2
---

# Vision UI Workflow

## Phase 1: Multi-Profile Summarization (Current)

1. **Parse Input Profiles**
   - Load persona definitions from `vision_ui/profiles.py`
   - Validate vocabulary mappings and example sentences
   - Check budget constraints (headline/one_screen/deep layers)

2. **Apply Persona Adapters**
   - Transform vocabulary based on persona (developer/designer/manager)
   - Set `examples_location` based on register risk assessment
   - Ensure outputs use descriptive nouns, not perpetrator voice

3. **Enforce Budget Compliance**
   - Calculate character counts for each summarization layer
   - Apply buffer overrides via immutable copies (no mutation)
   - Generate content hashes for deep layer provenance tracking

4. **Safety Validation**
   - Scan for perpetrator voice patterns (Rule 1.1)
   - Verify citation honesty (Rule 3.1)
   - Check LIMITATIONS headers in generated files

## Phase 2: Screenshot OCR & Triage (Planned)

1. **OCR Processing**
   - Extract text regions from screenshots
   - Classify regions: code, UI text, sensitive content
   - Redact PII before summarization

2. **Triage Board Integration**
   - Flag high-confidence OCR regions for manual review
   - Distinguish distress signals (stack traces) from threat patterns
   - Route accordingly (support vs blocking)

## Phase 3: Advanced Personas (Planned)

1. **Drift Monitoring**
   - Re-evaluate persona mappings quarterly
   - Update colloquial register patterns
   - Track provenance via metadata tags

2. **Attention Research**
   - Analyze user attention patterns
   - Optimize screen-ratio configurations
   - Validate ethical alignment

## CI/CD Integration

- Automated tests include safety checks (no perpetrator voice, budget fidelity)
- Human reviews required for quality validation
- Content provenance tags on all AI-generated outputs
