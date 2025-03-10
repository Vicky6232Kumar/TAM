
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pingouin as pg
import scipy.stats as stats


#t-test - two sample 
def ind_t_test(df, categorical_var, target_variable, dataset_name):
    """
    Performs an Independent t-test for a categorical variable with two groups.

    Parameters:
    - df (DataFrame): The dataset (original or perceived).
    - categorical_var (str): The independent variable (e.g., "Gender").
    - target_variable (str): The dependent variable (e.g., "Acceptance_Score").
    - dataset_name (str): Name of the dataset for printing results.

    Returns:
    - float: p-value of the t-test.
    """
    # Ensure categorical_var & target_variable exist
    if categorical_var not in df.columns:
        raise KeyError(f"❌ Column '{categorical_var}' not found in {dataset_name} Data!")

    if target_variable not in df.columns:
        raise KeyError(f"❌ Column '{target_variable}' not found in {dataset_name} Data!")

    # Drop NaN values
    df = df[[categorical_var, target_variable]].dropna()

    # Ensure exactly two unique groups
    unique_groups = df[categorical_var].unique()
    if len(unique_groups) != 2:
        print(f"❌ t-test Failed: '{categorical_var}' in {dataset_name} has {len(unique_groups)} unique categories. Test requires exactly 2 groups.")
        return None

    # Extract data for two groups
    group1 = df[df[categorical_var] == unique_groups[0]][target_variable]
    group2 = df[df[categorical_var] == unique_groups[1]][target_variable]

    # Check Homogeneity of Variance (Levene’s Test)
    stat, p_var = stats.levene(group1, group2)
    equal_var = p_var > 0.05  # True if variances are equal

    print(f"✅ Levene’s Test for {dataset_name} Data: p = {p_var:.5f} -> {'Equal Variance Assumed' if equal_var else 'Unequal Variance'}")

    # Perform Independent t-test
    t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=equal_var)

    print(f"✅ Independent t-test for {dataset_name} Data (Factor: {categorical_var}): p = {p_value:.5f} -> {'Significant' if p_value < 0.1 else 'Not Significant'}")

    return p_value

# One-Way ANOVA
def one_way_anova(df, categorical_var, target_variable, dataset_name):
    """
    Performs One-Way ANOVA for a categorical independent variable.

    Parameters:
    - df (DataFrame): The dataset (original or perceived).
    - categorical_var (str): The independent variable (e.g., "Gender", "Age_Group").
    - target_variable (str): The dependent variable (e.g., "Acceptance_Score").
    - dataset_name (str): Name of the dataset for printing results.

    Returns:
    - float: p-value of the ANOVA test.
    """
    model = smf.ols(f"{target_variable} ~ C(Q('{categorical_var}'))", data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    p_value = anova_table["PR(>F)"].iloc[0] # p-value for the main factor
    # print(f"✅ One-Way ANOVA Results for {dataset_name} Data (Factor: {categorical_var}):\n", anova_table)
    print(f"✅ One-Way ANOVA for {dataset_name} Data (Factor: {categorical_var}): p = {p_value:.3f} -> {'Significant' if p_value < 0.1 else 'Not Significant'}")

    # Extract p-value

    # Compute Effect Size (Eta Squared)
    # eta_squared = anova_table["sum_sq"][0] / anova_table["sum_sq"].sum()
    # print(f"Effect Size (η²) for {dataset_name} ({categorical_var}): {eta_squared:.3f} "
    #       f"(Small: 0.01, Medium: 0.06, Large: 0.14)")

    return p_value

# Two-Way ANOVA (Corrected)
def two_way_anova(df, categorical_vars, target_variable, dataset_name):
    """
    Performs Two-Way ANOVA for multiple categorical independent variables.

    Parameters:
    - df (DataFrame): The dataset (original).
    - categorical_vars (list): Independent variables (e.g., ["Gender", "age group"]).
    - target_variable (str): The dependent variable (e.g., "Acceptance_Score").
    - dataset_name (str): Name of the dataset for printing results.

    Returns:
    - dict: Dictionary of p-values for main effects & interaction effect.
    """

    formula = f"{target_variable} ~ C({categorical_vars[0]}) + C({categorical_vars[1]}) + C({categorical_vars[0]}):C({categorical_vars[1]})"
    model = smf.ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    print(f"✅ Two-Way ANOVA Results for {dataset_name} Data:\n", anova_table)

    # Extract p-values for main effects and interaction
    p_values = {
        categorical_vars[0]: anova_table["PR(>F)"].iloc[0],  # p-value for Factor 1 (e.g., Gender)
        categorical_vars[1]: anova_table["PR(>F)"].iloc[1],  # p-value for Factor 2 (e.g., Age Group)
        "Interaction": anova_table["PR(>F)"].iloc[2]  # p-value for Interaction Effect
    }

    # Compute Effect Sizes (Partial Eta Squared)
    # sum_sq_total = anova_table["sum_sq"].sum()
    # eta_squared_values = {
    #     categorical_vars[0]: anova_table["sum_sq"][0] / sum_sq_total,
    #     categorical_vars[1]: anova_table["sum_sq"][1] / sum_sq_total,
    #     "Interaction": anova_table["sum_sq"][2] / sum_sq_total
    # }

    # print(f"\n🔹 Effect Size (η²) for {categorical_vars[0]}: {eta_squared_values[categorical_vars[0]]:.3f} "
    #       f"(Small: 0.01, Medium: 0.06, Large: 0.14)")
    # print(f"🔹 Effect Size (η²) for {categorical_vars[1]}: {eta_squared_values[categorical_vars[1]]:.3f} "
    #       f"(Small: 0.01, Medium: 0.06, Large: 0.14)")
    # print(f"🔹 Effect Size (η²) for Interaction: {eta_squared_values['Interaction']:.3f} "
    #       f"(Small: 0.01, Medium: 0.06, Large: 0.14)")

    return p_values

# two way mixed anova
def two_way_mixed_anova(df_original, df_perceived, categorical_var, target_variable="Acceptance_Score"):
    print(f"\nPerforming Two-Way Mixed ANOVA (Comparing Original vs. Perceived Data with {categorical_var})...")

    # Identify participant column names in both datasets
    participant_col_original = "Driver No."
    participant_col_perceived = "Sr No."

    # Ensure the participant ID columns exist
    if participant_col_original not in df_original.columns:
        raise KeyError(f"❌ Column '{participant_col_original}' not found in Original Data!")
    if participant_col_perceived not in df_perceived.columns:
        raise KeyError(f"❌ Column '{participant_col_perceived}' not found in Perceived Data!")

    # Rename participant ID columns for consistency
    df_original = df_original.rename(columns={participant_col_original: "Participant_ID"})
    df_perceived = df_perceived.rename(columns={participant_col_perceived: "Participant_ID"})

    # Reshape Original Data
    df_mixed = df_original[['Participant_ID', categorical_var, target_variable]].copy()
    df_mixed = df_mixed.rename(columns={target_variable: 'Original_Score'})

    df_perceived = df_perceived[['Participant_ID', target_variable]].copy()
    df_perceived = df_perceived.rename(columns={target_variable: 'Perceived_Score'})

    df_mixed = df_mixed.merge(df_perceived, on='Participant_ID', how='left')

    # Ensure no column is named "Score" before melting
    df_mixed = df_mixed.rename(columns={"Original_Score": "Original", "Perceived_Score": "Perceived"})

    # Reshape Data for Pingouin ANOVA
    df_mixed = df_mixed.melt(id_vars=['Participant_ID', categorical_var], 
                              var_name='Data_Type', 
                              value_name='Score')

    # Perform Two-Way Mixed ANOVA
    anova_mixed = pg.mixed_anova(dv='Score', between=categorical_var, within='Data_Type', subject='Participant_ID', data=df_mixed)
    print(f"✅ Two-Way Mixed ANOVA Results (Factor: {categorical_var}):\n", anova_mixed)


