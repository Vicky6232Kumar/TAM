# This code is for analysis for effect of interaction of age group and driving experience on technology(adas)

from utils import (
    load_data, check_reliability, check_normality, calculate_acceptance_score, save_updated_data, count_combinations, plot_interaction_effect, compute_summary_stats_all_possibility, compute_interaction_stats_only, check_normality_on_filtered_data
)
from parametric_tests import two_way_anova
from non_parametric_tests import art_anova
from scipy.stats import mannwhitneyu, ttest_ind

# Define Target & Categorical Variables
target_variable = "Acceptance_Score"
categorical_vars = ["age group", "Driving experience in years"]

age_o_categories = ["18 to 30", "30 to 50"]
age_p_categories = ["18 to 30 years", "30 to 50 years", "> 50 years"]
driving_exp_categories = ["< 2 years","2 to 5 years", "> 5 years", "No experience"]

#  Step 1: Load Data
df_original, df_perceived = load_data("data sheet.xlsx")

# Ensure all column names are stripped of spaces
df_original.columns = df_original.columns.str.strip()
df_perceived.columns = df_perceived.columns.str.strip()

print("\n")

# Step 2: Perform Cronbach's Alpha (Reliability Test)
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

# Step 3: Calculate Acceptance Score
df_original = calculate_acceptance_score(df_original, "Original")
df_perceived = calculate_acceptance_score(df_perceived, "Perceived")

# Step 4: Save Updated Data
save_updated_data(df_original, df_perceived)

# Step 5: Check Normality
is_normal_original = check_normality(df_original, target_variable, "Original")
is_normal_perceived = check_normality(df_perceived, target_variable, "Perceived")

# Step 6: Perform Statistical Tests & Store p-values
p_values = {}

# Original Data Statistical Tests
if is_normal_original:
    anova_results_original = two_way_anova(df_original, categorical_vars, target_variable, "Original")
    p_values["Two-Way ANOVA (Original)"] = anova_results_original["Interaction"]  # Extract only the interaction p-value
else:
    p_values["Aligned Ranked Transformation (Original)"] = art_anova(df_original, categorical_vars, target_variable, "Original")

# Perceived Data Statistical Tests
if is_normal_perceived:
    anova_results_perceived = two_way_anova(df_perceived, categorical_vars, target_variable, "Perceived")
    p_values["Two-Way ANOVA (Perceived)"] = anova_results_perceived["Interaction"]  # Extract only the interaction p-value
else:
    p_values["Aligned Ranked Transformation (Perceived)"] = art_anova(df_perceived, categorical_vars, target_variable, "Perceived")

# Step 7: Print all p-values
print("\n📊 **P-Value Results Summary:**")
for test, p_val in p_values.items():
    if isinstance(p_val, (int, float)):  # Ensures it's a number before formatting
        print(f"{test}: p = {p_val:.5f} {'✅ Significant' if p_val < 0.1 else '❌ Not Significant'}")
    else:
        print(f"{test}: {p_val} (Invalid result, check ANOVA output)")


# Generate interaction effect plots
plot_interaction_effect(df_original, categorical_vars[0], categorical_vars[1], target_variable, "Original", "original_interaction_age_driving")
plot_interaction_effect(df_perceived, categorical_vars[0], categorical_vars[1],  target_variable, "Perceived","perceived_interaction_age_driving")

# Count for Original Data and Percieved Data
summary_original = compute_summary_stats_all_possibility(df_original, categorical_vars, target_variable)
summary_perceived = compute_summary_stats_all_possibility(df_perceived, categorical_vars, target_variable)

# Compute summary stats for both datasets
summary_interaction_original = compute_interaction_stats_only(df_original, categorical_vars, target_variable)
summary_interaction_perceived = compute_interaction_stats_only(df_perceived, categorical_vars, target_variable)

# Print Summary Stats
print("\n📊 **Summary Statistics for Original Data:**")
for var, stats in summary_original.items():
    print(f"\n🔹 {var}:")
    if isinstance(stats, dict):  # Handling interaction effect separately
        print(f"   Mean: {stats['Mean']:.2f}, Median: {stats['Median']:.2f}, Std: {stats['Std']:.2f}")
    else:
        print(stats.to_string())

print("\n📊 **Summary Statistics for Perceived Data:**")
for var, stats in summary_perceived.items():
    print(f"\n🔹 {var}:")
    if isinstance(stats, dict):  # Handling interaction effect separately
        print(f"   Mean: {stats['Mean']:.2f}, Median: {stats['Median']:.2f}, Std: {stats['Std']:.2f}")
    else:
        print(stats.to_string())

#------------------------------------

filter_original = df_original[(df_original[categorical_vars[0]] == age_o_categories[0]) & (df_original[categorical_vars[1]] == driving_exp_categories[0])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == age_p_categories[0]) & (df_perceived[categorical_vars[1]] == driving_exp_categories[0])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "18 to 30 years x < 2 years Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "female x 18 to 30 years x < 2 years Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")

#-----------------

filter_original = df_original[(df_original[categorical_vars[0]] == age_o_categories[0]) & (df_original[categorical_vars[1]] == driving_exp_categories[1])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == age_p_categories[0]) & (df_perceived[categorical_vars[1]] == driving_exp_categories[1])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "18 to 30 years x 2 to 5 years Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "female x 18 to 30 years x 2 to 5 years Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")

#------------

filter_original = df_original[(df_original[categorical_vars[0]] == age_o_categories[0]) & (df_original[categorical_vars[1]] == driving_exp_categories[2])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == age_p_categories[0]) & (df_perceived[categorical_vars[1]] == driving_exp_categories[2])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "18 to 30 years x > 5 years Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "18 to 30 years x > 5 years Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")

#----------------------------------------

filter_original = df_original[(df_original[categorical_vars[0]] == age_o_categories[1]) & (df_original[categorical_vars[1]] == driving_exp_categories[0])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == age_p_categories[1]) & (df_perceived[categorical_vars[1]] == driving_exp_categories[0])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "30 to 50 years x < 2 years Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "30 to 50 years x < 2 years Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test (female x 18 to 30 years x < 2 years): p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test (female x 18 to 30 years x < 2 years): p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")


filter_original = df_original[(df_original[categorical_vars[0]] == age_o_categories[1]) & (df_original[categorical_vars[1]] == driving_exp_categories[1])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == age_p_categories[1]) & (df_perceived[categorical_vars[1]] == driving_exp_categories[1])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "30 to 50 years x 2 to 5 years Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "30 to 50 years x 2 to 5 years Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test (female x 18 to 30 years x < 2 years): p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test (female x 18 to 30 years x < 2 years): p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")


filter_original = df_original[(df_original[categorical_vars[0]] == age_o_categories[1]) & (df_original[categorical_vars[1]] == driving_exp_categories[2])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == age_p_categories[1]) & (df_perceived[categorical_vars[1]] == driving_exp_categories[2])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "30 to 50 years x > 5 years Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "30 to 50 years x > 5 years Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test (female x 18 to 30 years x < 2 years): p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test (female x 18 to 30 years x < 2 years): p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
