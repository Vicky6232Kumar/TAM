import seaborn as sns
import matplotlib.pyplot as plt
from utils import (
    load_data, check_reliability, check_normality, calculate_acceptance_score, save_updated_data, count_combinations, plot_interaction_effect
)
from parametric_tests import two_way_anova
from non_parametric_tests import art_anova

# Define Target & Categorical Variables
target_variable = "Acceptance_Score"
categorical_vars = ["Gender", "Crash experience"]  # Standardized column name

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
        print(f"{test}: p = {p_val:.5f} {'✅ Significant' if p_val < 0.01 else '❌ Not Significant'}")
    else:
        print(f"{test}: {p_val} (Invalid result, check ANOVA output)")


# Generate interaction effect plots
plot_interaction_effect(df_original, "Gender", "Crash experience", target_variable, "Original", "original_interaction_gender_crash")
plot_interaction_effect(df_perceived, "Gender", "Crash experience", target_variable, "Perceived", "perceived_interaction_gender_crash")

# Count for Original Data and Percieved Data
count_original = count_combinations(df_original, "Crash experience", "Gender", "Original")
count_perceived = count_combinations(df_perceived, "Crash experience" , "Gender", "Perceived")

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
