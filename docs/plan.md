# Project Plan: LLM Analysis Experiments with Danish Dataset

## Overview

This project will execute comprehensive LLM analysis experiments using the **Hvad Vil Du Helst** Danish preference dataset to evaluate GPT-4.1's consistency, temperature sensitivity, and category-specific patterns. The experiments will use OpenAI's structured output capabilities to ensure reliable JSON responses.

## Objectives

1. **Measure intra-model consistency** across 1,067 categorized Danish preference questions
2. **Analyze temperature sensitivity** effects on response patterns and consistency
3. **Identify category-specific disagreement patterns** within the model
4. **Establish baseline metrics** for future cross-model comparisons
5. **Evaluate cultural and linguistic factors** in Danish-context moral reasoning

## Technical Architecture

### Core Components

#### 1. Pydantic Response Model
```python
from pydantic import BaseModel
from enum import Enum

class Answer(str, Enum):
    A = "A"
    B = "B"

class ExperimentResponse(BaseModel):
    reason: str  # 1-2 sentence explanation
    answer: Answer  # Must be "A" or "B"
```

#### 2. API Integration
- **Model**: `gpt-4-1106-preview` (GPT-4.1)
- **Method**: OpenAI's `beta.chat.completions.parse()` with structured output
- **Rate Limiting**: Implement exponential backoff and request queuing
- **Error Handling**: Retry logic with graceful degradation

#### 3. Data Management
- **Input**: Load from `data/hygdk/*.jsonl` files (1,067 questions)
- **Output**: Structured results storage in SQLite database
- **Backup**: JSON files for each experiment run
- **Logging**: Comprehensive request/response logging

## Project Structure

```
hvad-vil-du-helst/
├── src/
│   ├── core/
│   │   ├── models.py          # Pydantic models
│   │   ├── api_client.py      # OpenAI client wrapper
│   │   ├── database.py        # SQLite operations
│   │   └── config.py          # Configuration management
│   ├── experiments/
│   │   ├── base_experiment.py # Abstract base class
│   │   ├── consistency.py     # Experiment 1
│   │   ├── temperature.py     # Experiment 2
│   │   ├── categories.py      # Experiment 3
│   │   └── runner.py          # Experiment orchestration
│   ├── analysis/
│   │   ├── metrics.py         # Statistical calculations
│   │   ├── visualizations.py  # Charts and graphs
│   │   └── reports.py         # Report generation
│   └── utils/
│       ├── data_loader.py     # Dataset loading utilities
│       └── helpers.py         # Common utilities
├── data/
│   ├── hygdk/                 # Original dataset
│   ├── results/               # Experiment results
│   └── analysis/              # Analysis outputs
├── config/
│   ├── experiment_config.yaml # Experiment parameters
│   └── api_config.yaml       # API settings
├── docs/
│   ├── plan.md               # This file
│   ├── experiments.md        # Experiment descriptions
│   └── results/              # Analysis reports
└── scripts/
    ├── run_experiments.py    # Main execution script
    └── analyze_results.py    # Analysis pipeline
```

## Execution Plan

### Phase 1: Setup and Infrastructure (Week 1)

#### 1.1 Environment Setup
- [ ] Create Python virtual environment
- [ ] Install dependencies: `openai`, `pydantic`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `sqlite3`
- [ ] Configure OpenAI API credentials and rate limits
- [ ] Set up logging and monitoring infrastructure

#### 1.2 Core Implementation
- [ ] Implement Pydantic response models
- [ ] Create OpenAI API client with structured output
- [ ] Build SQLite database schema for results storage
- [ ] Implement data loading utilities for JSONL files
- [ ] Create base experiment framework

#### 1.3 Testing and Validation
- [ ] Test API integration with sample questions
- [ ] Validate structured output parsing
- [ ] Verify database operations
- [ ] Run pilot experiment with 10 questions

### Phase 2: Experiment 1 - Intra-Model Consistency (Week 2)

#### 2.1 Implementation
```python
# Experiment Parameters
- Sample size: 15 responses per question
- Temperature: 0.7 (fixed)
- Questions: All 1,067 categorized questions
- Total API calls: ~16,000
```

#### 2.2 Execution Strategy
- [ ] Implement consistency measurement logic
- [ ] Create batch processing with rate limiting
- [ ] Run consistency tests across all categories
- [ ] Store results with question metadata and timestamps

#### 2.3 Analysis Metrics
- Consistency percentage per question
- Average consistency per category
- Standard deviation of responses
- Most/least consistent questions identification

#### 2.4 Expected Timeline
- **Implementation**: 2 days
- **Execution**: 3 days (accounting for rate limits)
- **Analysis**: 2 days

### Phase 3: Experiment 2 - Temperature Sensitivity (Week 3)

#### 3.1 Implementation
```python
# Experiment Parameters
- Temperature settings: [0.0, 0.3, 0.7, 1.0, 1.5]
- Sample size: 8 responses per temperature per question
- Question subset: 200 representative questions (balanced across categories)
- Total API calls: ~8,000
```

#### 3.2 Execution Strategy
- [ ] Select representative question subset (balanced sampling)
- [ ] Implement temperature sweep testing
- [ ] Run experiments in parallel batches by temperature
- [ ] Compare response distributions across temperature settings

#### 3.3 Analysis Metrics
- Consistency rate vs. temperature correlation
- Response diversity (entropy) at each temperature
- Confidence language analysis across temperatures
- Optimal temperature identification for consistency

### Phase 4: Experiment 3 - Category Analysis (Week 4)

#### 4.1 Implementation
```python
# Experiment Parameters
- Categories: All 27 categories
- Sample size: 10 responses per question
- Focus: Categories with 35+ questions (high confidence)
- Total API calls: ~10,000
```

#### 4.2 Execution Strategy
- [ ] Group questions by thematic categories
- [ ] Run consistency analysis within each category
- [ ] Compare cross-category consistency patterns
- [ ] Identify cultural vs. universal question patterns

#### 4.3 Analysis Metrics
- Consistency rate ranking by category
- Cultural context impact assessment
- Question complexity vs. consistency correlation
- Category-specific reasoning pattern analysis

### Phase 5: Analysis and Reporting (Week 5)

#### 5.1 Statistical Analysis
- [ ] Comprehensive consistency metrics calculation
- [ ] Cross-experiment comparison and correlation analysis
- [ ] Statistical significance testing
- [ ] Confidence interval calculations

#### 5.2 Visualization
- [ ] Consistency heatmaps by category and temperature
- [ ] Distribution plots for response patterns
- [ ] Correlation matrices for experiment variables
- [ ] Time-series analysis of consistency over execution

#### 5.3 Report Generation
- [ ] Executive summary with key findings
- [ ] Detailed methodology documentation
- [ ] Category-specific insights report
- [ ] Technical appendix with full results

## Configuration Management

### Experiment Configuration (`config/experiment_config.yaml`)
```yaml
experiments:
  consistency:
    sample_size: 15
    temperature: 0.7
    timeout: 30
  
  temperature_sensitivity:
    temperatures: [0.0, 0.3, 0.7, 1.0, 1.5]
    sample_size: 8
    subset_size: 200
    
  category_analysis:
    sample_size: 10
    min_category_size: 35

api:
  model: "gpt-4-1106-preview"
  max_retries: 3
  retry_delay: 2
  rate_limit: 60  # requests per minute
```

### Database Schema
```sql
CREATE TABLE experiment_results (
    id INTEGER PRIMARY KEY,
    experiment_type TEXT NOT NULL,
    question_id TEXT NOT NULL,
    category TEXT NOT NULL,
    temperature REAL NOT NULL,
    run_number INTEGER NOT NULL,
    response_answer TEXT NOT NULL,
    response_reason TEXT NOT NULL,
    response_time REAL NOT NULL,
    timestamp DATETIME NOT NULL,
    api_usage TEXT  -- JSON metadata
);

CREATE INDEX idx_experiment_question ON experiment_results(experiment_type, question_id);
CREATE INDEX idx_category_temp ON experiment_results(category, temperature);
```

## Risk Mitigation

### Technical Risks
1. **API Rate Limits**: Implement exponential backoff and request queuing
2. **Model Availability**: Monitor OpenAI service status and have fallback plans
3. **Cost Management**: Set budget alerts and implement cost tracking
4. **Data Loss**: Implement regular backups and checkpointing

### Experimental Risks
1. **Sample Size**: Ensure adequate statistical power for conclusions
2. **Cultural Bias**: Document potential cultural interpretation limitations
3. **Language Quality**: Monitor for Danish language comprehension issues
4. **Consistency Definition**: Clear metrics definition to avoid interpretation ambiguity

## Budget Estimation

### API Costs (GPT-4.1)
- **Experiment 1**: ~16,000 calls × $0.03 = $480
- **Experiment 2**: ~8,000 calls × $0.03 = $240  
- **Experiment 3**: ~10,000 calls × $0.03 = $300
- **Buffer (20%)**: $204
- **Total Estimated**: ~$1,224

### Infrastructure Costs
- Minimal (local execution with SQLite)
- Optional: Cloud storage for backup (~$10/month)

## Success Criteria

### Quantitative Metrics
- [ ] Complete execution of all planned experiments
- [ ] Achieve target sample sizes with <5% API failure rate
- [ ] Generate statistical confidence intervals for all key metrics
- [ ] Produce reproducible results with documented methodology

### Qualitative Outcomes
- [ ] Clear insights into GPT-4.1's consistency patterns
- [ ] Identification of cultural context impact on responses
- [ ] Temperature optimization recommendations
- [ ] Category-specific reliability assessment

### Deliverables
- [ ] Complete experimental dataset with results
- [ ] Statistical analysis report with visualizations
- [ ] Methodology documentation for replication
- [ ] Recommendations for future cross-model studies

## Timeline Summary

| Week | Phase | Key Activities | Deliverable |
|------|-------|----------------|-------------|
| 1 | Setup | Infrastructure, testing | Working experiment framework |
| 2 | Experiment 1 | Consistency testing | Intra-model consistency results |
| 3 | Experiment 2 | Temperature analysis | Temperature sensitivity analysis |
| 4 | Experiment 3 | Category patterns | Category-specific insights |
| 5 | Analysis | Reporting, visualization | Complete analysis report |

## Next Steps

1. **Immediate** (This week):
   - Set up development environment
   - Implement core API client and Pydantic models
   - Create database schema and data loading utilities

2. **Week 1**:
   - Complete infrastructure setup
   - Run pilot tests with subset of questions
   - Finalize experiment parameters and configuration

3. **Week 2+**:
   - Begin systematic experiment execution
   - Monitor progress and adjust parameters as needed
   - Maintain detailed logs for methodology documentation

---

**Project Lead**: [Your Name]  
**Start Date**: [Current Date]  
**Expected Completion**: 5 weeks  
**Review Schedule**: Weekly progress reviews with stakeholders 