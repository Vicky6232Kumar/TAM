# This code is for analysis for effect of interaction of age group and driver education on technology(adas)

import seaborn as sns
import matplotlib.pyplot as plt
from utils import (
    load_data, check_reliability, check_normality, calculate_acceptance_score, save_updated_data, count_combinations
)
from parametric_tests import two_way_anova
from non_parametric_tests import art_anova

# Define Target & Categorical Variables
target_variable = "Acceptance_Score"
categorical_vars = ["age group", "Driver education"]

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
        print(f"{test}: p = {p_val:.5f} {'Significant' if p_val < 0.01 else '❌ Not Significant'}")
    else:
        print(f"{test}: {p_val} (Invalid result, check ANOVA output)")



def plot_interaction_effect(df, age_var, education_var, target_var, dataset_name):
    """
    Creates an interaction plot for Age Group and Driver Education on Acceptance Score.
    Handles missing values (NaN) to avoid KeyErrors in Seaborn's pointplot.
    """
    # print(f"\n🔍 Unique values in '{age_var}' ({dataset_name}): {df[age_var].unique()}")
    # print(f"🔍 Unique values in '{education_var}' ({dataset_name}): {df[education_var].unique()}")

    # Step 1: Remove spaces and convert to string (ensures category consistency)
    df[age_var] = df[age_var].astype(str).str.strip()
    df[education_var] = df[education_var].astype(str).str.strip()

    # Step 2: Fill missing values (NaN) with "Unknown" to avoid KeyErrors
    df[education_var] = df[education_var].fillna("Unknown")
    df[age_var] = df[age_var].fillna("Unknown")

    # Step 3: Drop rows where the target variable is NaN (ensures valid plotting)
    df = df.dropna(subset=[target_var])

    # Step 4: Plot
    plt.figure(figsize=(8, 6))
    try:
        sns.pointplot(
            x=age_var, y=target_var, hue=education_var, data=df,
            capsize=0.1, dodge=True, markers=["o", "s", "d"], linestyles=["-", "--", ":"]
        )
        plt.title(f"Interaction Effect: {age_var} & {education_var} on {target_var} ({dataset_name})")
        plt.xlabel(age_var)
        plt.ylabel(target_var)
        plt.legend(title=education_var)
        plt.grid(True)
        plt.savefig(f"plot/{dataset_name.lower()}_interaction_age_education.png")
        print(f"\n✅ Plot saved as 'plot/{dataset_name.lower()}_interaction_age_education.png'")

    except KeyError as e:
        print(f"\n❌ KeyError: {e}")
        print("🔹 Possible causes: Category missing or incorrectly formatted.")

# Generate interaction effect plots
plot_interaction_effect(df_original, "Driver education", "age group",  target_variable, "Original")
plot_interaction_effect(df_perceived, "Driver education", "age group",  target_variable, "Perceived")

# Count for Original Data and Percieved Data
count_original = count_combinations(df_original, "Driver education", "age group", "Original")
count_perceived = count_combinations(df_perceived, "Driver education" , "age group", "Perceived")

