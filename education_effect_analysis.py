# This code is for analysis of effect of Driver education on adas (technology)

import matplotlib.pyplot as plt
import numpy as np
from utils import load_data, check_reliability, check_normality,calculate_acceptance_score, save_updated_data, compare_mean_median, check_normality_on_filtered_data
from parametric_tests import one_way_anova, ind_t_test
from non_parametric_tests import kruskal_wallis, mann_whitney_u_test
from scipy.stats import mannwhitneyu, ttest_ind

# Define target variable
target_variable = "Acceptance_Score"
categorical_variable = "Driver education"

# Step 1 - load Original & Perceived Data
df_original, df_perceived = load_data("data sheet.xlsx")

# Ensure all column names are stripped of spaces
df_original.columns = df_original.columns.str.strip()
df_perceived.columns = df_perceived.columns.str.strip()

# Step 2 - Perform Cronbach's Alpha (Reliability Test) on both datasets
alpha_original = check_reliability(df_original)
if alpha_original > 0.7:
    print(f"✅ Cronbach's Alpha for Original Data: {alpha_original:.3f} (accepted, alpha > 0.7)")
else:
    print(f"❌ Cronbach's Alpha for Original Data: {alpha_original:.3f} (rejected, alpha < 0.7)")

alpha_perceived = check_reliability(df_perceived)
if alpha_perceived > 0.7:
    print(f"✅ Cronbach's Alpha for Perceived Data: {alpha_perceived:.3f} (accepted, alpha > 0.7)")
else:
    print(f"❌ Cronbach's Alpha for Perceived Data: {alpha_perceived:.3f} (rejected, alpha < 0.7)")


# Step 3 - calculate the acceptance score 
df_original = calculate_acceptance_score(df_original, "Original")
df_perceived = calculate_acceptance_score(df_perceived, "Perceived")

# after calculation of acceptance for both datasets save e, eou and acceptance in the excel

save_updated_data(df_original, df_perceived)

# Print column names to check if "Age" exists
# print("\nOriginal Data Columns:", df_original.columns.tolist())
# print("\nPerceived Data Columns:", df_perceived.columns.tolist())

# Step 4 : Check normality
is_normal_original = check_normality(df_original, target_variable, "Original")
is_normal_perceived = check_normality(df_perceived, target_variable, "Perceived")

# step 5: performing the statiscal test 

p_values = {}

if is_normal_original:
    p_values["independent t-test (Original)"] = ind_t_test(df_original, categorical_variable,target_variable, "Original")
else:
     p_values["Mann Whitey U (Original)"]  = mann_whitney_u_test(df_original, categorical_variable, target_variable, "Original")

if is_normal_perceived:
     p_values["one-way anova (Perceived)"]  = one_way_anova(df_perceived,categorical_variable,  target_variable, "Perceived")
else:
    p_values["Krushal Wills (Perceived)"] = kruskal_wallis(df_perceived, categorical_variable,  target_variable, "Perceived")

print("\n📊 **P-Value Results Summary:**")
for test, p_val in p_values.items():
    print(f"{test}: p = {p_val:.5f} {'✅ Significant' if p_val < 0.10 else '❌ Not Significant'}")

significant_original = any(p < 0.10 for key, p in p_values.items() if "Original" in key)
significant_perceived = any(p < 0.10 for key, p in p_values.items() if "Perceived" in key)

mean_median_original = compare_mean_median(df_original, categorical_variable, target_variable, "Original")
mean_median_perceived = compare_mean_median(df_perceived, categorical_variable, target_variable, "Perceived")

def plot_driver_education(df, categorical_var, target_variable, dataset_name, education_groups_display_map):
    """
    Plots Mean & Median in a bar chart with error bars for Driver Education groups.
    - Mean → Error bars using Standard Error (SE).
    - Median → Error bars using Interquartile Range (IQR).
    - Bars are properly spaced with no overlap.
    - Separate plots for Original & Perceived Data.
    - Ensures missing categories are handled correctly.
    """
    # Compute Mean, SE, Median, and IQR
    summary_stats = df.groupby(categorical_var)[target_variable].agg(
        mean="mean",
        std="std",
        count="count",
        median="median",
        q1=lambda x: np.percentile(x, 25),
        q3=lambda x: np.percentile(x, 75)
    )

    # Compute Standard Error (SE) for Mean
    summary_stats["se"] = summary_stats["std"] / np.sqrt(summary_stats["count"])

    # Compute IQR (Interquartile Range) for Median
    summary_stats["iqr"] = summary_stats["q3"] - summary_stats["q1"]

    # Rename education labels for consistency
    summary_stats = summary_stats.rename(index=education_groups_display_map)

    # Ensure consistent education order & fill missing categories
    all_education_groups = list(education_groups_display_map.values())

    # FIX: Handle missing categories safely by reindexing and filling missing values
    summary_stats = summary_stats.reindex(all_education_groups).fillna(0)

    # Extract values
    mean_values = summary_stats["mean"].tolist()
    median_values = summary_stats["median"].tolist()

    # Compute error bars
    mean_errors = summary_stats["se"].tolist()  # SE for Mean
    median_errors = summary_stats["iqr"].tolist()  # IQR for Median

    # Define bar positions
    num_groups = len(all_education_groups)
    x_indices = np.arange(num_groups * 2)  # Create positions for each bar
    width = 0.4  # Set bar width
    spacing = 0.4  # Space between groups

    mean_x = x_indices[:num_groups] * spacing  # Spread out Mean bars
    median_x = x_indices[num_groups:] * spacing + spacing  # Spread out Median bars

    # Define bar labels for clarity
    mean_labels = [f"Mean - {edu}" for edu in all_education_groups]
    median_labels = [f"Median - {edu}" for edu in all_education_groups]
    all_labels = mean_labels + median_labels

    # Define unique colors for each education group
    colors = ["#3498db", "#e74c3c", "#2ecc71"]  # Unique colors

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Mean Bars
    bars_mean = ax.bar(mean_x, mean_values, width=width, color=colors[:num_groups], edgecolor="black", yerr=mean_errors, capsize=5, error_kw=dict(elinewidth=1.5), label="Mean (SE)")

    # Plot Median Bars
    bars_median = ax.bar(median_x, median_values, width=width, color=colors[:num_groups], edgecolor="black", yerr=median_errors, capsize=5, error_kw=dict(elinewidth=1.5), alpha=0.7, label="Median (IQR)")

    # Add value labels on top of bars (Mean & Median)
    for bar, value, err in zip(bars_mean, mean_values, mean_errors):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + err + 1, f"{value:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    for bar, value, err in zip(bars_median, median_values, median_errors):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + err + 1, f"{value:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Add error range annotation below bars
    for bar, err in zip(bars_mean, mean_errors):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height - err - 2, f"±{err:.1f}", ha='center', va='top', fontsize=9, color='black')

    for bar, err in zip(bars_median, median_errors):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height - err - 2, f"±{err:.1f}", ha='center', va='top', fontsize=9, color='black')

    # Customize plot
    ax.set_xlabel("Driver Education Category")
    ax.set_ylabel(target_variable)
    ax.set_title(f"{dataset_name} Data: Mean & Median with Error Bars")
    ax.set_xticks(np.concatenate((mean_x, median_x)))  # Merge x positions
    ax.set_xticklabels(all_labels, rotation=15)

    # Create Legend for Education Groups
    education_patches = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(num_groups)]
    legend_labels = [f"{edu}" for edu in all_education_groups]

    # First Legend (Education Categories)
    legend1 = ax.legend(education_patches, legend_labels, title="Driver Education", loc="upper left", bbox_to_anchor=(1, 1))

    # Second Legend (Mean/Median)
    legend2 = ax.legend(title="Statistical Measure", loc="upper left", bbox_to_anchor=(1, 0.8))
    ax.add_artist(legend1)

    # Save plot
    plt.savefig(f"plot/{dataset_name.lower()}_driver_education_error_plot.png")
    print(f"\n✅ Plot saved as 'plot/{dataset_name.lower()}_driver_education_error_plot.png'")

    plt.show()


# Define consistent driver education labels
education_groups_original = {"> Bachelor's degree": "> Bachelor's degree", "Bachelor's degree": "Bachelor's degree"}
education_groups_perceived = {"> Bachelor's degree": "> Bachelor's degree", "Bachelor's degree": "Bachelor's degree", "< Bachelor's degree": "< Bachelor's degree"}

# Generate Driver Education Plots for Original Data and Perceived Data
plot_driver_education(df_original, categorical_variable, target_variable, "Original", education_groups_original)
plot_driver_education(df_perceived, categorical_variable, target_variable, "Perceived", education_groups_perceived)



# visualization
# fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# sns.boxplot(x=categorical_variable, y=target_variable, data=df_original, ax=axes[0])
# axes[0].set_title(f"Original Data: {target_variable} by Age")

# sns.boxplot(x=categorical_variable, y=target_variable, data=df_perceived, ax=axes[1])
# axes[1].set_title(f"Perceived Data: {target_variable} by Age")

# plt.tight_layout()

# plt.savefig("plot/education_effect_plot.png")
# print("\n✅ Plot saved as 'plot/education_effect_plot.png'")


edu_original = df_original[df_original[categorical_variable] == "Bachelor's degree"][target_variable]
edu_perceived = df_perceived[df_perceived[categorical_variable] == "Bachelor's degree"][target_variable]

is_normal_edu_original = check_normality_on_filtered_data(edu_original, "Bachelor's degree original")
is_normal_edu_perceived = check_normality_on_filtered_data(edu_perceived, "Bachelor's degree Perceived")

if is_normal_edu_original and is_normal_edu_perceived:
    t_stat, p_value = ttest_ind(edu_original, edu_perceived)
    print(f"t-test: p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(edu_original, edu_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test: p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")



edu_original = df_original[df_original[categorical_variable] == "> Bachelor's degree"][target_variable]
edu_perceived = df_perceived[df_perceived[categorical_variable] == "> Bachelor's degree"][target_variable]

is_normal_edu_original = check_normality_on_filtered_data(edu_original, "> Bachelor's degree original")
is_normal_edu_perceived = check_normality_on_filtered_data(edu_perceived, "> Bachelor's degree Perceived")

if is_normal_edu_original and is_normal_edu_perceived:
    t_stat, p_value = ttest_ind(edu_original, edu_perceived)
    print(f"t-test: p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(edu_original, edu_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test: p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")

