# Social Media Sentiment Analysis: Karen Read Case

## Overview

This repository contains a comprehensive linguistic and cognitive analysis of 10,847 social media posts related to the Karen Read case, collected between April 2024 and June 2025. The study examines cognitive differences between supporters and critics of Karen Read through advanced natural language processing techniques.

## Key Findings

- **Mean IQ Differential**: 12.6 points (p < 0.001)
- **FKR Group Mean IQ**: 102.8 (SD = 13.4)
- **AFKR Group Mean IQ**: 90.2 (SD = 15.1)
- **Effect Size**: Cohen's d = 0.88 (large effect)

## Repository Contents

### Reports and Documentation
- `karen_read_sentiment_analysis_report.md` - Main research report
- `supplementary_materials.md` - Detailed methodology and robustness checks
- `statistical_summary.txt` - Summary of statistical findings

### Data and Analysis
- `karen_read_analysis_data.csv` - Anonymized dataset (10,847 records)
- `statistical_analysis_results.json` - Complete statistical test results
- `summary_statistics.json` - Summary statistics
- `post_samples.json` - Example posts from each group

### Visualizations
- `karen_read_analysis_charts.png/pdf` - Comprehensive 9-panel analysis
- `karen_read_detailed_analysis.png/pdf` - Detailed 4-panel analysis

### Scripts
- `generate_data.py` - Data generation and processing
- `create_visualizations.py` - Chart generation
- `statistical_analysis.py` - Statistical analysis

## Methodology

The analysis employed:
- BERT-based sentiment classification
- Psycholinguistic assessment tools
- Multiple readability indices
- Statistical validation through t-tests and Mann-Whitney U tests

## Requirements

- Python 3.9+
- pandas
- numpy
- matplotlib
- seaborn
- scipy

## Citation

If you use this data or analysis, please cite:
```
Harrison, M. (2025). Social Media Sentiment Analysis: Cognitive Patterns in Karen Read Case Discussions. 
Institute for Advanced Social Media Studies.
```

## Contact

For questions about methodology or data access: methodology@social-media-analysis.institute