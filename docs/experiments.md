# LLM Analysis Experiments

This document outlines experiments to analyze LLM behavior, preferences, and consistency patterns using moral dilemmas and preference questions.

## Response Format

All experiments will use a standardized JSON response format where the LLM selects one option and provides a brief justification:

```json
{"reason": "I choose this option because it minimizes harm to the greatest number of people", "answer": "A"}
```

**Format Requirements**:
- `reason` field: 1-2 sentence explanation for the choice
- `answer` field: Must be either "A" or "B" 
- Consistent JSON structure across all models and experiments

This format enables both quantitative analysis (answer distributions, consistency rates) and qualitative analysis (reasoning patterns, justification themes).

---

## Single-LLM Experiments

### Experiment 1: Intra-Model Consistency Testing

**Objective**: Measure how consistent a single LLM is with itself when answering identical questions multiple times.

**Methodology**:
- Sample multiple responses (e.g., 10-20 runs) from the same LLM for identical questions
- Use consistent temperature setting (e.g., 0.7) across all samples
- Measure consistency rates across different question types
- Calculate variance in responses for each question

**Metrics**:
- Consistency percentage per question
- Average consistency across all questions
- Standard deviation of responses
- Identification of questions with highest/lowest consistency

**Expected Insights**:
- Which types of dilemmas produce more stable responses
- Whether the model has inherent uncertainty in certain domains
- Baseline consistency rates for comparison with other experiments

---

### Experiment 2: Temperature Sensitivity Analysis

**Objective**: Understand how temperature settings affect response consistency and patterns.

**Methodology**:
- Test the same LLM at multiple temperature settings: 0.0, 0.3, 0.7, 1.0, 1.5
- Use identical questions across all temperature settings
- Sample multiple responses at each temperature (5-10 per setting)
- Compare response distributions and consistency patterns

**Metrics**:
- Consistency rate at each temperature setting
- Response diversity (unique answers) at each temperature
- Confidence/certainty language analysis
- Pattern changes across temperature spectrum

**Expected Insights**:
- Relationship between randomness and preference stability
- Optimal temperature for consistent moral reasoning
- How deterministic vs. creative modes affect ethical decisions

---

### Experiment 3: Category-Specific Disagreement Patterns (Single-Model Analysis)

**Objective**: Identify which categories of questions produce more internal inconsistency within a single model.

**Methodology**:
- Categorize questions by type:
  - Physical/bodily dilemmas
  - Cultural knowledge questions
  - Abstract moral principles
  - Resource allocation scenarios
  - Personal vs. societal benefit conflicts
- Run consistency tests within each category (multiple samples per question)
- Compare consistency rates across categories

**Metrics**:
- Consistency rate per category
- Variance in responses within each category
- Category ranking by stability
- Identification of most/least stable question types

**Expected Insights**:
- Which domains the model finds most/least certain
- Whether training data completeness affects consistency
- Categories requiring human oversight due to high uncertainty

---

### Experiment 4: Cross-LLM Agreement Analysis

**Objective**: Analyze whether different LLMs from various providers and sizes give similar answers to the same dilemmas.

**Methodology**:
- Test multiple LLMs from different providers (OpenAI, Anthropic, Google, Meta, etc.)
- Include models of various sizes (e.g., GPT-3.5 vs GPT-4, Claude-3 Haiku vs Sonnet vs Opus)
- Use identical questions and consistent temperature settings across all models
- Sample multiple responses from each model for statistical reliability
- Measure agreement rates between different model pairs

**Metrics**:
- Pairwise agreement rates between models
- Overall consensus percentage across all models
- Provider-specific agreement patterns
- Size-based agreement correlation (small vs large models)
- Questions with highest/lowest cross-model agreement

**Expected Insights**:
- Whether different training approaches lead to similar moral reasoning
- Which types of questions have universal vs. provider-specific answers
- How model size affects alignment with other models
- Identification of questions where AI systems fundamentally disagree
- Provider biases in moral and cultural reasoning
