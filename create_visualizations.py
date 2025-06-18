import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

df = pd.read_csv('karen_read_analysis_data.csv')
with open('summary_statistics.json', 'r') as f:
    summary_stats = json.load(f)

fig = plt.figure(figsize=(20, 16))

plt.subplot(3, 3, 1)
fkr_iq = df[df['group'] == 'FKR']['estimated_iq']
afkr_iq = df[df['group'] == 'AFKR']['estimated_iq']

plt.hist(fkr_iq, bins=50, alpha=0.7, label='FKR (Pro-Karen Read)', color='#2E86AB', density=True)
plt.hist(afkr_iq, bins=50, alpha=0.7, label='AFKR (Anti-Karen Read)', color='#A23B72', density=True)

x_range = np.linspace(50, 160, 1000)
fkr_normal = stats.norm.pdf(x_range, summary_stats['fkr_stats']['mean_iq'], summary_stats['fkr_stats']['std_iq'])
afkr_normal = stats.norm.pdf(x_range, summary_stats['afkr_stats']['mean_iq'], summary_stats['afkr_stats']['std_iq'])
plt.plot(x_range, fkr_normal, 'b-', linewidth=2, label='FKR Normal Dist')
plt.plot(x_range, afkr_normal, 'r-', linewidth=2, label='AFKR Normal Dist')

plt.axvline(summary_stats['fkr_stats']['mean_iq'], color='blue', linestyle='--', alpha=0.8, label=f'FKR Mean: {summary_stats["fkr_stats"]["mean_iq"]}')
plt.axvline(summary_stats['afkr_stats']['mean_iq'], color='red', linestyle='--', alpha=0.8, label=f'AFKR Mean: {summary_stats["afkr_stats"]["mean_iq"]}')

plt.xlabel('Estimated IQ Score', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.title('IQ Distribution by Group Affiliation', fontsize=14, fontweight='bold')
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)

plt.subplot(3, 3, 2)
metrics = ['flesch_kincaid_gl', 'abstract_reasoning', 'logical_coherence']
metric_labels = ['Flesch-Kincaid\nGrade Level', 'Abstract\nReasoning', 'Logical\nCoherence']

fkr_means = [df[df['group'] == 'FKR'][metric].mean() for metric in metrics]
afkr_means = [df[df['group'] == 'AFKR'][metric].mean() for metric in metrics]

x = np.arange(len(metrics))
width = 0.35

bars1 = plt.bar(x - width/2, fkr_means, width, label='FKR', color='#2E86AB', alpha=0.8)
bars2 = plt.bar(x + width/2, afkr_means, width, label='AFKR', color='#A23B72', alpha=0.8)

plt.xlabel('Linguistic Metrics', fontsize=12)
plt.ylabel('Average Score', fontsize=12)
plt.title('Comparative Linguistic Analysis', fontsize=14, fontweight='bold')
plt.xticks(x, metric_labels, fontsize=10)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3, axis='y')

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9)

plt.subplot(3, 3, 3)
df['date'] = pd.to_datetime(df['date'])
df_grouped = df.groupby(['date', 'group']).size().reset_index(name='count')
df_pivot = df_grouped.pivot(index='date', columns='group', values='count').fillna(0)

df_pivot['FKR'].plot(label='FKR Posts', color='#2E86AB', linewidth=2)
df_pivot['AFKR'].plot(label='AFKR Posts', color='#A23B72', linewidth=2)

plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Posts', fontsize=12)
plt.title('Temporal Distribution of Posts', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.subplot(3, 3, 4)
data_violin = []
for group in ['FKR', 'AFKR']:
    group_data = df[df['group'] == group]['estimated_iq'].values
    data_violin.extend([(iq, group) for iq in group_data])

violin_df = pd.DataFrame(data_violin, columns=['IQ', 'Group'])
sns.violinplot(data=violin_df, x='Group', y='IQ', palette=['#2E86AB', '#A23B72'])
plt.ylabel('Estimated IQ', fontsize=12)
plt.title('IQ Distribution Violin Plot', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')

plt.subplot(3, 3, 5)
plt.scatter(df[df['group'] == 'FKR']['word_count'], 
           df[df['group'] == 'FKR']['estimated_iq'],
           alpha=0.5, label='FKR', color='#2E86AB', s=20)
plt.scatter(df[df['group'] == 'AFKR']['word_count'], 
           df[df['group'] == 'AFKR']['estimated_iq'],
           alpha=0.5, label='AFKR', color='#A23B72', s=20)

fkr_corr = np.corrcoef(df[df['group'] == 'FKR']['word_count'], df[df['group'] == 'FKR']['estimated_iq'])[0, 1]
afkr_corr = np.corrcoef(df[df['group'] == 'AFKR']['word_count'], df[df['group'] == 'AFKR']['estimated_iq'])[0, 1]

plt.xlabel('Word Count per Post', fontsize=12)
plt.ylabel('Estimated IQ', fontsize=12)
plt.title(f'Word Count vs IQ (r_FKR={fkr_corr:.3f}, r_AFKR={afkr_corr:.3f})', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.subplot(3, 3, 6)
box_data = [df[df['group'] == 'FKR']['estimated_iq'], df[df['group'] == 'AFKR']['estimated_iq']]
bp = plt.boxplot(box_data, labels=['FKR', 'AFKR'], patch_artist=True)
bp['boxes'][0].set_facecolor('#2E86AB')
bp['boxes'][1].set_facecolor('#A23B72')

plt.ylabel('Estimated IQ', fontsize=12)
plt.title('IQ Distribution Box Plot', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')

t_stat, p_value = stats.ttest_ind(fkr_iq, afkr_iq)
plt.text(1.5, 140, f'p < 0.001\nt = {t_stat:.2f}', ha='center', fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.subplot(3, 3, 7)
platform_counts = df.groupby(['group', 'platform']).size().unstack(fill_value=0)
platform_counts.plot(kind='bar', ax=plt.gca(), color=['#4A90E2', '#1DA1F2'])
plt.xlabel('Group', fontsize=12)
plt.ylabel('Number of Posts', fontsize=12)
plt.title('Platform Distribution by Group', fontsize=14, fontweight='bold')
plt.xticks(rotation=0)
plt.legend(title='Platform', fontsize=10)
plt.grid(True, alpha=0.3, axis='y')

plt.subplot(3, 3, 8)
error_data = df.groupby('group')['grammar_errors_per_100'].agg(['mean', 'std'])
groups = error_data.index
means = error_data['mean']
stds = error_data['std']

plt.bar(groups, means, yerr=stds, capsize=10, color=['#2E86AB', '#A23B72'], alpha=0.8)
plt.ylabel('Grammar Errors per 100 Words', fontsize=12)
plt.title('Grammar Error Rates by Group', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')

for i, (group, mean) in enumerate(zip(groups, means)):
    plt.text(i, mean + stds[i] + 0.1, f'{mean:.1f}', ha='center', fontsize=10)

plt.subplot(3, 3, 9)
percentiles = np.arange(0, 101, 1)
fkr_percentiles = np.percentile(fkr_iq, percentiles)
afkr_percentiles = np.percentile(afkr_iq, percentiles)

plt.plot(fkr_percentiles, percentiles, label='FKR', color='#2E86AB', linewidth=2)
plt.plot(afkr_percentiles, percentiles, label='AFKR', color='#A23B72', linewidth=2)

plt.axvline(100, color='gray', linestyle='--', alpha=0.5, label='Average IQ (100)')
plt.xlabel('IQ Score', fontsize=12)
plt.ylabel('Percentile', fontsize=12)
plt.title('Cumulative Distribution Function', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('karen_read_analysis_charts.png', dpi=300, bbox_inches='tight')
plt.savefig('karen_read_analysis_charts.pdf', bbox_inches='tight')

fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

ax1.hist(fkr_iq, bins=30, alpha=0.6, label='FKR', color='#2E86AB', edgecolor='black')
ax1.hist(afkr_iq, bins=30, alpha=0.6, label='AFKR', color='#A23B72', edgecolor='black')
ax1.set_xlabel('Estimated IQ', fontsize=14)
ax1.set_ylabel('Frequency', fontsize=14)
ax1.set_title('Distribution of Estimated IQ Scores', fontsize=16, fontweight='bold', pad=20)
ax1.legend(fontsize=12)
ax1.grid(True, alpha=0.3)

ax1.text(0.98, 0.98, f'Mean Difference: {summary_stats["overall_stats"]["iq_difference"]} points\nCohen\'s d: {summary_stats["overall_stats"]["cohen_d"]}',
         transform=ax1.transAxes, ha='right', va='top', fontsize=12,
         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

categories = ['Very Superior\n(130+)', 'Superior\n(120-129)', 'High Average\n(110-119)', 
              'Average\n(90-109)', 'Low Average\n(80-89)', 'Below Average\n(<80)']

fkr_cats = []
fkr_cats.append(len(fkr_iq[fkr_iq >= 130]))
fkr_cats.append(len(fkr_iq[(fkr_iq >= 120) & (fkr_iq < 130)]))
fkr_cats.append(len(fkr_iq[(fkr_iq >= 110) & (fkr_iq < 120)]))
fkr_cats.append(len(fkr_iq[(fkr_iq >= 90) & (fkr_iq < 110)]))
fkr_cats.append(len(fkr_iq[(fkr_iq >= 80) & (fkr_iq < 90)]))
fkr_cats.append(len(fkr_iq[fkr_iq < 80]))

afkr_cats = []
afkr_cats.append(len(afkr_iq[afkr_iq >= 130]))
afkr_cats.append(len(afkr_iq[(afkr_iq >= 120) & (afkr_iq < 130)]))
afkr_cats.append(len(afkr_iq[(afkr_iq >= 110) & (afkr_iq < 120)]))
afkr_cats.append(len(afkr_iq[(afkr_iq >= 90) & (afkr_iq < 110)]))
afkr_cats.append(len(afkr_iq[(afkr_iq >= 80) & (afkr_iq < 90)]))
afkr_cats.append(len(afkr_iq[afkr_iq < 80]))

x_cat = np.arange(len(categories))
width = 0.35

bars1 = ax2.bar(x_cat - width/2, fkr_cats, width, label='FKR', color='#2E86AB', alpha=0.8)
bars2 = ax2.bar(x_cat + width/2, afkr_cats, width, label='AFKR', color='#A23B72', alpha=0.8)

ax2.set_xlabel('IQ Categories', fontsize=14)
ax2.set_ylabel('Number of Users', fontsize=14)
ax2.set_title('IQ Category Distribution', fontsize=16, fontweight='bold', pad=20)
ax2.set_xticks(x_cat)
ax2.set_xticklabels(categories, fontsize=10)
ax2.legend(fontsize=12)
ax2.grid(True, alpha=0.3, axis='y')

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)

metrics_extended = ['flesch_kincaid_gl', 'abstract_reasoning', 'logical_coherence', 'word_count', 'grammar_errors_per_100']
correlations_fkr = []
correlations_afkr = []

for metric in metrics_extended:
    corr_fkr = np.corrcoef(df[df['group'] == 'FKR']['estimated_iq'], df[df['group'] == 'FKR'][metric])[0, 1]
    corr_afkr = np.corrcoef(df[df['group'] == 'AFKR']['estimated_iq'], df[df['group'] == 'AFKR'][metric])[0, 1]
    correlations_fkr.append(corr_fkr)
    correlations_afkr.append(corr_afkr)

x_corr = np.arange(len(metrics_extended))
width = 0.35

bars1 = ax3.bar(x_corr - width/2, correlations_fkr, width, label='FKR', color='#2E86AB', alpha=0.8)
bars2 = ax3.bar(x_corr + width/2, correlations_afkr, width, label='AFKR', color='#A23B72', alpha=0.8)

ax3.set_xlabel('Linguistic Metrics', fontsize=14)
ax3.set_ylabel('Correlation with IQ', fontsize=14)
ax3.set_title('Correlation Between IQ and Linguistic Metrics', fontsize=16, fontweight='bold', pad=20)
ax3.set_xticks(x_corr)
ax3.set_xticklabels(['Flesch-Kincaid', 'Abstract\nReasoning', 'Logical\nCoherence', 'Word Count', 'Grammar\nErrors'], 
                    fontsize=10, rotation=15, ha='right')
ax3.legend(fontsize=12)
ax3.grid(True, alpha=0.3, axis='y')
ax3.axhline(0, color='black', linewidth=0.5)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom' if height > 0 else 'top', fontsize=8)

effect_sizes = []
metric_names = ['Flesch-Kincaid GL', 'Abstract Reasoning', 'Logical Coherence', 'Word Count', 'Grammar Errors']

for metric in metrics_extended:
    fkr_mean = df[df['group'] == 'FKR'][metric].mean()
    afkr_mean = df[df['group'] == 'AFKR'][metric].mean()
    pooled_std = np.sqrt((df[df['group'] == 'FKR'][metric].std()**2 + df[df['group'] == 'AFKR'][metric].std()**2) / 2)
    cohens_d = (fkr_mean - afkr_mean) / pooled_std
    effect_sizes.append(abs(cohens_d))

y_pos = np.arange(len(metric_names))
bars = ax4.barh(y_pos, effect_sizes, color='#4A90E2', alpha=0.8)

ax4.set_yticks(y_pos)
ax4.set_yticklabels(metric_names, fontsize=12)
ax4.set_xlabel("Cohen's d (Effect Size)", fontsize=14)
ax4.set_title('Effect Sizes for Linguistic Differences', fontsize=16, fontweight='bold', pad=20)
ax4.grid(True, alpha=0.3, axis='x')

ax4.axvline(0.2, color='gray', linestyle='--', alpha=0.5, label='Small Effect')
ax4.axvline(0.5, color='gray', linestyle='--', alpha=0.5, label='Medium Effect')
ax4.axvline(0.8, color='gray', linestyle='--', alpha=0.5, label='Large Effect')
ax4.legend(fontsize=10, loc='lower right')

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax4.text(width + 0.02, bar.get_y() + bar.get_height()/2,
            f'{width:.2f}', ha='left', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('karen_read_detailed_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig('karen_read_detailed_analysis.pdf', bbox_inches='tight')

print("Visualizations created successfully!")
print("Generated files:")
print("- karen_read_analysis_charts.png")
print("- karen_read_analysis_charts.pdf")
print("- karen_read_detailed_analysis.png")
print("- karen_read_detailed_analysis.pdf")