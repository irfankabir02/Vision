---
name: vision
description: Screen-aware text budgeting and persona-adapted summarization for UI/UX workflows
---

# Vision UI Skill

Invoke this skill when working with screen summarization, persona-based text adaptation, or budget-constrained output generation.

## Core Capabilities

### 1. Linguistic Safety Auditing
- Scan summaries for perpetrator voice patterns (first/second person pronouns in threat contexts)
- Flag outputs requiring review before release
- Apply nominalization transformations to harmful action descriptions

### 2. Register Analysis
- Classify text inputs/outputs by formality level (Formal/Literary vs Colloquial/Active)
- Adjust summarization heuristics based on register risk assessment
- Apply persona vocabulary mappings accordingly

### 3. Citation Verification
- Ensure all referenced sources are physically verified or marked as AI-generated
- Validate LIMITATIONS headers in safety-critical files
- Check documentation honesty in README and schema files

### 4. Distress Signal Detection
- Integrate with OCR analyzer to classify regions (code vs sensitive text)
- Distinguish error summaries (distress signals) from threat patterns
- Route distress to support resources, never punitive actions

### 5. Drift Monitoring
- Periodically re-evaluate persona mappings against evolving colloquial registers
- Update patterns to prevent safety degradation over time
- Track provenance via content hashes and metadata tags

### 6. Ethical Alignment Assessment
- Assess persona outputs for bias
- Ensure outputs serve inclusive UX goals
- Validate that human-defined profiles and budgets take precedence

## Key Files
- `vision_ui/profiles.py` - Persona dataclass with vocabulary mappings
- `UI_UX/budget.py` - Character budget enforcement
- `vision_ui/cli.py` - Command-line interface with persona opt-in

## Usage Triggers
- Multi-profile summarization requests
- Screenshot OCR with redaction requirements
- Persona adaptation for developer/designer/manager contexts
- Budget compliance verification
