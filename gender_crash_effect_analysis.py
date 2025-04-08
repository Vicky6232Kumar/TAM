# This code is for analysis for effect of interaction of gender and crash experience on technology(adas)
import scikit_posthocs as sp
from utils import (
    load_data, check_reliability, check_normality, calculate_acceptance_score, save_updated_data, plot_interaction_effect, compute_interaction_stats_only, compute_summary_stats_all_possibility, check_normality_on_filtered_data
)
from parametric_tests import two_way_anova
from non_parametric_tests import art_anova
from scipy.stats import ttest_ind, mannwhitneyu

# Define Target & Categorical Variables
target_variable = "Acceptance_Score"
categorical_vars = ["Gender", "Crash experience"]  # Standardized column name

gender_categories = ["Female", "Male"]
crash_categories = ["Crash free", "Crash experienced"]

#  Step 1: Load Data
df_original, df_perceived = load_data("data sheet.xlsx")

# Fix Column Names (Remove Spaces)
# df_original.columns = df_original.columns.str.replace(" ", "_")
# df_perceived.columns = df_perceived.columns.str.replace(" ", "_")

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

# Step 8: Perform Dunn’s Test for Pairwise Comparisons**
def perform_dunn_test(df, dataset_name):
    """
    Performs Dunn’s Test with Bonferroni correction to check pairwise differences.
    """
    # Create a combined categorical variable for pairwise testing
    df["Group"] = df["Gender"] + " - " + df["Crash experience"]

    # Perform Dunn’s Test
    dunn_results = sp.posthoc_dunn(df, val_col="Acceptance_Score", group_col="Group", p_adjust="bonferroni")

    # Print Results
    print(f"\n📊 **Dunn’s Test Results for {dataset_name} Data:**\n", dunn_results)

    # Filter Significant Comparisons (p < 0.10)
    significant_comparisons = dunn_results[dunn_results < 0.10]

    print(f"\n📊 **Significant Pairwise Differences in {dataset_name}:**\n", significant_comparisons)

    return dunn_results

# Run Dunn’s Test for Perceived Data (Since it had significant interaction)
dunn_perceived = perform_dunn_test(df_perceived, "Perceived")

# Generate interaction effect plots
plot_interaction_effect(df_original, categorical_vars[0], categorical_vars[1], target_variable, "Original", "original_interaction_gender_crash")
plot_interaction_effect(df_perceived, categorical_vars[0], categorical_vars[1], target_variable, "Perceived", "perceived_interaction_gender_crash")

# Compute summary stats for both datasets
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

print("\n📊 **Interaction Single Valued**")
print(f"Mean: {summary_interaction_original['Interaction']['Mean']:.2f}, Median: {summary_interaction_original['Interaction']['Median']:.2f}, Std: {summary_interaction_original['Interaction']['Std']:.2f}")

print("\n🔹 **Summary Statistics for Perceived Data:**")
for var, stats in summary_perceived.items():
    print(f"\n🔹 {var}:")
    if isinstance(stats, dict):  # Handling interaction effect separately
        print(f"   Mean: {stats['Mean']:.2f}, Median: {stats['Median']:.2f}, Std: {stats['Std']:.2f}")
    else:
        print(stats.to_string())

print("\n🔹 **Interaction Single Valued**")
print(f"Mean: {summary_interaction_perceived['Interaction']['Mean']:.2f}, Median: {summary_interaction_perceived['Interaction']['Median']:.2f}, Std: {summary_interaction_perceived['Interaction']['Std']:.2f}")

# fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# # Original Data Plots
# sns.boxplot(x="age_group", y=target_variable, hue="Gender", data=df_original, ax=axes[0, 0])
# axes[0, 0].set_title(f"Original: Acceptance Score by Age & Gender")

# sns.boxplot(x="Gender", y=target_variable, data=df_original, ax=axes[0, 1])
# axes[0, 1].set_title(f"Original: Acceptance Score by Gender")

# # Perceived Data Plots
# sns.boxplot(x="age_group", y=target_variable, hue="Gender", data=df_perceived, ax=axes[1, 0])
# axes[1, 0].set_title(f"Perceived: Acceptance Score by Age & Gender")

# sns.boxplot(x="Gender", y=target_variable, data=df_perceived, ax=axes[1, 1])
# axes[1, 1].set_title(f"Perceived: Acceptance Score by Gender")

# plt.tight_layout()
# plt.savefig("plot/age_gender_effect_plot.png")
# print("\n✅ Plot saved as 'plot/age_gender_effect_plot.png'")


# # Load the Excel file
# file_path = "female_crash_free.xlsx"  # Replace with your actual file path
# df_testing = pd.read_excel(file_path)

# p_val_testing = {}
# p_val_testing["Aligned Ranked Transformation (Perceived)"] = art_anova(df_testing, categorical_vars, target_variable, "Perceived")

# print("\n📊 **P-Value for female - crash freeResults Summary:**")
# for test, p_val in p_val_testing.items():
#     if isinstance(p_val, (int, float)):  # Ensures it's a number before formatting
#         print(f"{test}: p = {p_val:.5f} {'✅ Significant' if p_val < 0.1 else '❌ Not Significant'}")
#     else:
#         print(f"{test}: {p_val} (Invalid result, check ANOVA output)")

# Filter for females with "crash free" experience
# filtered_df = df[(df["Gender"] == "Female") & (df["Crash experience"] == "Crash free")][["Gender", "Crash experience", "Acceptance_Score"]]

# # Save the filtered data to a new Excel file
# filtered_file_path = "female_crash_free.xlsx"
# filtered_df.to_excel(filtered_file_path, index=False)

# print(f"Filtered data saved to {filtered_file_path}")


# comparision of fot and percieved data

# -------------------------------------

filter_original = df_original[(df_original[categorical_vars[0]] == gender_categories[0]) & (df_original[categorical_vars[1]] == crash_categories[0])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == gender_categories[0]) & (df_perceived[categorical_vars[1]] == crash_categories[0])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "Female x Crash free Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "Female x Crash free Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")

#-----------------

filter_original = df_original[(df_original[categorical_vars[0]] == gender_categories[0]) & (df_original[categorical_vars[1]] == crash_categories[1])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == gender_categories[0]) & (df_perceived[categorical_vars[1]] == crash_categories[1])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "Female x Crash experienced Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "Female x Crash experienced Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")

# ---------------------------------------------

filter_original = df_original[(df_original[categorical_vars[0]] == gender_categories[1]) & (df_original[categorical_vars[1]] == crash_categories[0])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == gender_categories[1]) & (df_perceived[categorical_vars[1]] == crash_categories[0])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "Male x Crash free Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "Male x Crash free Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")

#-----------------

filter_original = df_original[(df_original[categorical_vars[0]] == gender_categories[1]) & (df_original[categorical_vars[1]] == crash_categories[1])][target_variable]
filter_perceived = df_perceived[(df_perceived[categorical_vars[0]] == gender_categories[1]) & (df_perceived[categorical_vars[1]] == crash_categories[1])][target_variable]

is_normal_interaction_original = check_normality_on_filtered_data(filter_original, "Male x Crash experienced Original")
is_normal_interaction_perceived = check_normality_on_filtered_data(filter_perceived, "Male x Crash experienced Perceived")

if is_normal_interaction_original and is_normal_interaction_perceived:
    t_stat, p_value = ttest_ind(filter_original, filter_perceived)
    print(f"t-test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")
else:
    u_stat, p_value = mannwhitneyu(filter_original, filter_perceived, alternative='two-sided')
    print(f"Mann-Whitney U Test : p = {p_value:.5f} {'✅ Significant' if p_value < 0.10 else '❌ Not Significant'}")