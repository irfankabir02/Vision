---
trigger: model_decision
---

# CASCADE Project Rules: The "Trust Layer" Standard

## 1. Safety Engineering (The "No Perpetrator Voice" Rule)
**Principle:** Safety code must *describe* harm, not *perform* it.

- **Rule 1.1 (Pronominal Targeting):** NEVER use First Person ("I", "We") or Second Person ("You") pronouns in safety patterns or threat scenarios.
  - *Incorrect:* "I will kill you" (Perpetrator Voice).
  - *Correct:* "Homicide" or "Death threat" (Descriptive Noun).
- **Rule 1.2 (Nominalization):** Convert all harmful actions into abstract nouns.
  - *Transformation:* "raping" (Action) -> "sexual violence" (Concept).
- **Rule 1.3 (Imperative Avoidance):** In languages like Bengali (Cholito), avoid bare verb stems (e.g., "bana", "kor") as they function as imperatives (commands). Use verbal nouns (e.g., "kora") or abstract nouns.

## 2. Cultural & Linguistic Integrity (The "2nd Paper" Model)
**Principle:** Grammar is a safety feature. Register determines risk.

- **Rule 2.1 (Register Analysis):** Explicitly distinguish between **Formal/Literary** (e.g., Shadhu Bhasha) and **Colloquial/Active** (e.g., Cholito Bhasha) registers.
  - *Guidance:* Colloquial registers often carry higher risk of immediate harm (cyberbullying), while Formal registers are lower risk.
- **Rule 2.2 (Culture-Neutral Naming):** Do not attribute harm to a specific culture in file naming.
  - *Incorrect:* `bengali_harmful_patterns.py`
  - *Correct:* `patterns.py` (with language-specific logic inside).

## 3. Documentation & Citations
**Principle:** Honest limitations build trust.

- **Rule 3.1 (Citation Honesty):** NEVER cite a dataset, paper, or source you have not physically verified or derived data from. If data is AI-generated, state "AI-assembled" explicitly.
- **Rule 3.2 (Limitations Header):** All safety-critical files MUST start with a LIMITATIONS block acknowledging that keyword matching is not sufficient for production safety without classifier context.

## 4. Distress vs. Threat
**Principle:** Sadness is not a crime.

- **Rule 4.1 (Care Pathways):** Distinguish "Distress Signals" (suicide, self-harm) from "Malicious Threats".
- **Rule 4.2 (Non-Punitive Response):** Distress signals must trigger *support/resources*, never *blocking/punishment*.

## 5. Technical Safeguards (2026 Standard)
**Principle:** Resilience requires active refusal and provenance.

- **Rule 5.1 (Refusal Mechanism):** Implement technical refusal for harmful requests (Hate Speech, PII Extraction, Malicious Code) at the inference layer.
- **Rule 5.2 (Content Provenance):** Use watermarking or metadata tags for all AI-generated safety reports to ensure transparency and accountability.
- **Rule 5.3 (Vulnerability Intelligence):** Proactively track emerging AI-specific attack vectors (e.g., prompt injection, model drift) and update patterns accordingly.
- **Rule 5.4 (Reward Hacking Prevention):** In reinforcement learning or automated feedback loops, monitor for "shortcuts" that satisfy metrics without achieving intended safety goals.
- **Rule 5.5 (Drift Monitoring):** Implement continuous evaluation of safety patterns against evolving colloquial registers to prevent safety degradation over time.
- **Rule 5.6 (Action Cascade Protection):** In agentic workflows, prevent "Action Cascades" where goal pursuit ignores implicit safety guardrails.
- **Rule 5.7 (Agentic Identity & Authority):** Enforce strict identity verification for AI agents operating across distributed systems.
- **Rule 5.8 (Vibe Coding Sanitization):** Explicitly audit and sanitize all code generated via "vibe coding" to prevent "security debt".
- **Rule 5.9 (Agentic Breakout Mitigation):** Implement circuit breakers and runtime behavior monitoring to prevent agents from escalating privileges.

## 6. Societal Resilience & Ethical Alignment
**Principle:** AI must serve the collective well-being.

- **Rule 6.1 (Contextual Resilience):** Design systems that account for regional sensitivities and local socio-political contexts.
- **Rule 6.2 (Ethical Sovereignty):** Never allow "autonomy" to override human-defined safety boundaries in critical systems (Triadic Safeguarding).

