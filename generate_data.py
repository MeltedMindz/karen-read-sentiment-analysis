import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

np.random.seed(42)
random.seed(42)

def generate_iq_distribution(group_type, n_samples):
    if group_type == "FKR":
        mean_iq = 102.8
        std_iq = 13.4
    else:  # AFKR
        mean_iq = 90.2
        std_iq = 15.1
    
    return np.random.normal(mean_iq, std_iq, n_samples)

def generate_linguistic_scores(iq_scores):
    flesch_kincaid = 0.15 * iq_scores - 5.2 + np.random.normal(0, 1.5, len(iq_scores))
    abstract_reasoning = 0.08 * iq_scores - 2.1 + np.random.normal(0, 0.8, len(iq_scores))
    logical_coherence = 0.09 * iq_scores - 1.3 + np.random.normal(0, 0.6, len(iq_scores))
    word_count = 1.8 * iq_scores - 50 + np.random.normal(0, 20, len(iq_scores))
    grammar_errors = 450 / iq_scores + np.random.normal(0, 0.5, len(iq_scores))
    
    return {
        'flesch_kincaid': np.clip(flesch_kincaid, 3, 16),
        'abstract_reasoning': np.clip(abstract_reasoning, 1, 10),
        'logical_coherence': np.clip(logical_coherence, 1, 10),
        'word_count': np.clip(word_count, 20, 500).astype(int),
        'grammar_errors_per_100': np.clip(grammar_errors, 0.1, 10)
    }

def generate_post_samples(group_type, n_samples=20):
    if group_type == "FKR":
        templates = [
            "The timeline analysis clearly demonstrates that {evidence} contradicts the prosecution's narrative. When we examine {detail}, it becomes evident that {conclusion}.",
            "Multiple witnesses have corroborated that {observation}, which fundamentally undermines the theory that {claim}. This discrepancy requires careful consideration.",
            "The forensic evidence, particularly {finding}, raises significant questions about {aspect}. A thorough examination reveals {insight}.",
            "Considering the documented {fact} alongside {evidence}, one must question the validity of {assertion}. The logical inconsistencies are profound.",
            "The metadata from {source} clearly indicates {timing}, which is incompatible with the alleged sequence of events. This temporal impossibility cannot be ignored."
        ]
    else:  # AFKR
        templates = [
            "She definitely did it!! The evidence is obvious to anyone with common sense.",
            "I dont care what anyone says, {person} is guilty. End of story.",
            "Why are people making this so complicated?? Its clear as day what happened.",
            "Anyone defending her is just blind to the truth. Wake up people!!!",
            "The police know what there doing. They wouldn't arrest someone without proof."
        ]
    
    posts = []
    for _ in range(n_samples):
        template = random.choice(templates)
        if group_type == "FKR":
            post = template.format(
                evidence=random.choice(["phone records", "surveillance footage", "witness testimony", "medical examiner's report"]),
                detail=random.choice(["the 2:27 AM timestamp", "the glass fragment pattern", "the injury location", "the weather conditions"]),
                conclusion=random.choice(["alternative scenarios must be considered", "the timeline requires revision", "key evidence was overlooked", "reasonable doubt exists"]),
                observation=random.choice(["no defensive wounds were present", "the vehicle damage pattern", "the blood spatter analysis", "the witness locations"]),
                claim=random.choice(["premeditation", "intentional harm", "the official narrative", "the prosecution's timeline"]),
                finding=random.choice(["DNA evidence", "trajectory analysis", "toxicology results", "cellular data"]),
                aspect=random.choice(["the sequence of events", "causation", "intent", "the official theory"]),
                fact=random.choice(["communication logs", "financial records", "prior statements", "physical evidence"]),
                assertion=random.choice(["deliberate action", "the stated motive", "witness reliability", "the chain of custody"]),
                source=random.choice(["cellular towers", "security systems", "vehicle telemetry", "digital devices"]),
                timing=random.choice(["a 23-minute gap", "conflicting timestamps", "impossible sequencing", "overlapping events"]),
                insight=random.choice(["multiple interpretations exist", "further investigation is warranted", "critical questions remain", "the evidence is ambiguous"])
            )
        else:
            post = template.format(
                person=random.choice(["she", "Karen", "her", "that woman"])
            )
        posts.append(post)
    
    return posts

n_fkr = 5423
n_afkr = 5424

fkr_iq = generate_iq_distribution("FKR", n_fkr)
afkr_iq = generate_iq_distribution("AFKR", n_afkr)

fkr_scores = generate_linguistic_scores(fkr_iq)
afkr_scores = generate_linguistic_scores(afkr_iq)

start_date = datetime(2024, 4, 1)
end_date = datetime(2025, 6, 30)

fkr_data = []
for i in range(n_fkr):
    days_offset = random.randint(0, (end_date - start_date).days)
    post_date = start_date + timedelta(days=days_offset)
    
    fkr_data.append({
        'user_id': f'FKR_{i:05d}',
        'group': 'FKR',
        'date': post_date,
        'estimated_iq': round(fkr_iq[i], 1),
        'flesch_kincaid_gl': round(fkr_scores['flesch_kincaid'][i], 1),
        'abstract_reasoning': round(fkr_scores['abstract_reasoning'][i], 1),
        'logical_coherence': round(fkr_scores['logical_coherence'][i], 1),
        'word_count': fkr_scores['word_count'][i],
        'grammar_errors_per_100': round(fkr_scores['grammar_errors_per_100'][i], 1),
        'platform': np.random.choice(['Facebook', 'Twitter'], p=[0.65, 0.35])
    })

afkr_data = []
for i in range(n_afkr):
    days_offset = random.randint(0, (end_date - start_date).days)
    post_date = start_date + timedelta(days=days_offset)
    
    afkr_data.append({
        'user_id': f'AFKR_{i:05d}',
        'group': 'AFKR',
        'date': post_date,
        'estimated_iq': round(afkr_iq[i], 1),
        'flesch_kincaid_gl': round(afkr_scores['flesch_kincaid'][i], 1),
        'abstract_reasoning': round(afkr_scores['abstract_reasoning'][i], 1),
        'logical_coherence': round(afkr_scores['logical_coherence'][i], 1),
        'word_count': afkr_scores['word_count'][i],
        'grammar_errors_per_100': round(afkr_scores['grammar_errors_per_100'][i], 1),
        'platform': np.random.choice(['Facebook', 'Twitter'], p=[0.65, 0.35])
    })

all_data = fkr_data + afkr_data
df = pd.DataFrame(all_data)
df = df.sample(frac=1).reset_index(drop=True)  # Shuffle the data

df.to_csv('karen_read_analysis_data.csv', index=False)

summary_stats = {
    'fkr_stats': {
        'mean_iq': round(np.mean(fkr_iq), 1),
        'std_iq': round(np.std(fkr_iq), 1),
        'median_iq': round(np.median(fkr_iq), 1),
        'min_iq': round(np.min(fkr_iq), 1),
        'max_iq': round(np.max(fkr_iq), 1),
        'n': n_fkr
    },
    'afkr_stats': {
        'mean_iq': round(np.mean(afkr_iq), 1),
        'std_iq': round(np.std(afkr_iq), 1),
        'median_iq': round(np.median(afkr_iq), 1),
        'min_iq': round(np.min(afkr_iq), 1),
        'max_iq': round(np.max(afkr_iq), 1),
        'n': n_afkr
    },
    'overall_stats': {
        'total_posts': n_fkr + n_afkr,
        'iq_difference': round(np.mean(fkr_iq) - np.mean(afkr_iq), 1),
        'cohen_d': round((np.mean(fkr_iq) - np.mean(afkr_iq)) / np.sqrt((np.std(fkr_iq)**2 + np.std(afkr_iq)**2) / 2), 2),
        'collection_period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    }
}

with open('summary_statistics.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)

post_samples = {
    'fkr_samples': generate_post_samples('FKR', 10),
    'afkr_samples': generate_post_samples('AFKR', 10)
}

with open('post_samples.json', 'w') as f:
    json.dump(post_samples, f, indent=2)

print("Data generation complete!")
print(f"Generated {len(df)} total records")
print(f"FKR Mean IQ: {summary_stats['fkr_stats']['mean_iq']}")
print(f"AFKR Mean IQ: {summary_stats['afkr_stats']['mean_iq']}")
print(f"IQ Difference: {summary_stats['overall_stats']['iq_difference']}")
print(f"Cohen's d: {summary_stats['overall_stats']['cohen_d']}")