import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pingouin as pg
import numpy as np


# Mann-Whitney U-Test
def mann_whitney_u_test(df, categorical_var, target_variable, dataset_name):
    """
    Performs Mann-Whitney U Test for a categorical independent variable.

    Parameters:
    df (DataFrame): The dataset (original).
    categorical_var (str): The independent variable (e.g., "Gender").
    target_variable (str): The dependent variable (e.g., "Acceptance_Score").
    dataset_name (str): Name of the dataset for printing results.

    Returns:
    float: p-value of the Mann-Whitney U test.
    """
    groups = df[categorical_var].unique()
    if len(groups) != 2:
        print(f"❌ Mann-Whitney U Test Failed: {categorical_var} has more than 2 categories.")
        return None

    group1 = df[df[categorical_var] == groups[0]][target_variable]
    group2 = df[df[categorical_var] == groups[1]][target_variable]

    stat, p_value = stats.mannwhitneyu(group1, group2)
    print(f"✅ Mann-Whitney U Test for {dataset_name} Data: p = {p_value:.5f} -> {'Significant' if p_value < 0.1 else 'Not Significant'}")
    return p_value

# Kruskal-Wallis Test (Non-Parametric Alternative)
def kruskal_wallis(df, categorical_var, target_variable, dataset_name):
    """
    Performs Kruskal-Wallis Test for a categorical independent variable.

    Parameters:
    df (DataFrame): The dataset (original or perceived).
    categorical_var (str): The independent variable (e.g., "Gender", "Age_Group").
    target_variable (str): The dependent variable (e.g., "Acceptance_Score").
    dataset_name (str): Name of the dataset for printing results.
    """
    # Ensure categorical_var exists
    if categorical_var not in df.columns:
        raise KeyError(f"❌ Column '{categorical_var}' not found in {dataset_name} Data!")

    # Ensure target_variable exists
    if target_variable not in df.columns:
        raise KeyError(f"❌ Column '{target_variable}' not found in {dataset_name} Data!")

    groups = [df[df[categorical_var] == cat][target_variable] for cat in df[categorical_var].unique()]
    kw_stat, p_value = stats.kruskal(*groups)
    print(f"✅ Kruskal-Wallis Test for {dataset_name} Data (Factor: {categorical_var}): p = {p_value:.3f} -> {'Significant' if p_value < 0.1 else 'Not Significant'}")
    return p_value

def wilcoxon_test(df_original, df_perceived, target_variable):
    """
    Performs the Wilcoxon Signed-Rank Test to compare Original vs. Perceived Acceptance Scores.

    Parameters:
    df_original (DataFrame): Original data
    df_perceived (DataFrame): Perceived data
    target_variable (str): The dependent variable (e.g., "Acceptance_Score")

    Returns:
    None (prints results)
    """
    print("\nPerforming Wilcoxon Signed-Rank Test (Non-Parametric Alternative)...")

    try:
        # Wilcoxon Signed-Rank Test (Paired Data)
        stat, p_value = stats.wilcoxon(df_original[target_variable], df_perceived[target_variable])
        
        print(f"\nWilcoxon Signed-Rank Test Results:")
        print(f"W = {stat}, p = {p_value:.3f}")

        # Interpretation
        if p_value < 0.05:
            print("✅ Significant difference between Original & Perceived Data.")
        else:
            print("❌ No significant difference between Original & Perceived Data.")

    except ValueError as ve:
        print(f"❌ Wilcoxon Test Failed: {ve}")
        print("Skipping statistical test due to invalid conditions.")

# Aligned Ranked Transformation test (two way anova alternative)
def art_anova(df, categorical_vars, target_variable, dataset_name):
    """
    Performs Aligned Rank Transformation (ART) ANOVA for non-parametric interaction effects.

    Parameters:
    - df (DataFrame): The dataset (original or perceived).
    - categorical_vars (list): Independent variables (e.g., ["Gender", "Age group"]).
    - target_variable (str): The dependent variable (e.g., "Acceptance_Score").
    - dataset_name (str): Name of the dataset for printing results.

    Returns:
    - float: p-value for the interaction effect.
    """

    # Step 1: Rank Transform the Target Variable
    df["Ranked_Score"] = stats.rankdata(df[target_variable])

    # Step 2: Fit Two-Way ANOVA Model Using Ranked Data
    formula = f'Ranked_Score ~ C(Q("{categorical_vars[0]}")) + C(Q("{categorical_vars[1]}")) + C(Q("{categorical_vars[0]}")):C(Q("{categorical_vars[1]}"))'
    model = smf.ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    # ✅ Print the full ANOVA table
    print(f"\n✅ ART ANOVA (Non-Parametric Interaction Test) Results for {dataset_name}:\n", anova_table)

    # ✅ Extract and return the interaction p-value safely
    try:
        interaction_p_value = float(anova_table.loc[f'C(Q("{categorical_vars[0]}")):C(Q("{categorical_vars[1]}"))', "PR(>F)"])
    except KeyError:
        print("\n❌ Error: Interaction term not found in ANOVA table. Returning NaN.")
        interaction_p_value = np.nan  # Return NaN if the interaction effect is missing

    return interaction_p_value
    """
    Performs Aligned Rank Transformation (ART) ANOVA for non-parametric interaction effects.

    Parameters:
    - df (DataFrame): The dataset (original or perceived).
    - categorical_vars (list): Independent variables (e.g., ["Gender", "Age group"]).
    - target_variable (str): The dependent variable (e.g., "Acceptance_Score").
    - dataset_name (str): Name of the dataset for printing results.

    Returns:
    - float: p-value for the interaction effect.
    """

    # Step 1: Rank Transform the Target Variable
    df["Ranked_Score"] = stats.rankdata(df[target_variable])

    # Step 2: Fit Two-Way ANOVA Model Using Ranked Data
    formula = f'Ranked_Score ~ C(Q("{categorical_vars[0]}")) + C(Q("{categorical_vars[1]}")) + C(Q("{categorical_vars[0]}")):C(Q("{categorical_vars[1]}"))'
    model = smf.ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    # ✅ Print the full ANOVA table in the console
    print(f"\n✅ ART ANOVA (Non-Parametric Interaction Test) Results for {dataset_name}:\n", anova_table)

    # ✅ Extract and return only the p-value for the interaction effect
    interaction_p_value = anova_table.loc[f'C(Q("{categorical_vars[0]}")):C(Q("{categorical_vars[1]}"))', "PR(>F)"]
    
    return interaction_p_value