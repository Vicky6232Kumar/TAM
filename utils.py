import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pingouin as pg
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

reliability_vars = ['ADAS "Safe" rating (1-7) TAM', 'ADAS "Desirable" rating (1-7) TAM', 'ADAS "Pleasant" rating (1-7) TAM', 'ADAS "Comfortable" rating (1-7) TAM']

# Load the Excel file (Original & Perceived Data)
def load_data(file_path="data sheet.xlsx"):
    xls = pd.ExcelFile(file_path)
    df_original = xls.parse(sheet_name=xls.sheet_names[0])  
    df_perceived = xls.parse(sheet_name=xls.sheet_names[1])
    return df_original, df_perceived

# Perform Cronbach's Alpha test for reliability
def check_reliability(df, columns=reliability_vars):
    alpha, _ = pg.cronbach_alpha(df[columns])
    return alpha

# Calculate U, EOU, and Acceptance Score
def calculate_acceptance_score(df, dataset_name):
    """
    Computes User Acceptance Score using the Technology Acceptance Model (TAM).

    Returns:
    DataFrame: Updated dataset with new calculated columns.
    """
    if set(reliability_vars).issubset(df.columns):
        df["U"] = df[reliability_vars[:2]].mean(axis=1)  # Usefulness
        df["EOU"] = df[reliability_vars[2:]].mean(axis=1)  # Ease of Use
        df["Acceptance_Score"] = df[["U", "EOU"]].mean(axis=1) * (100 / 7)
        print(f"✅ Acceptance Score for {dataset_name} datasets calculated successfully!")
    else:
        print("❌ Required columns not found in dataset.")
    
    return df

# Check normality for a given column
def check_normality(data, column, dataset_name):
    if len(data) < 50:
        stat, p = stats.shapiro(data[column])  # Shapiro-Wilk for small samples
        test_used = "Shapiro-Wilk"
    else:
        mean = np.mean(data[column])
        std = np.std(data[column], ddof=1)  # Use sample standard deviation
        stat, p = stats.kstest(data[column], 'norm', args=(mean, std))  # KS Test for large samples
        test_used = "Kolmogorov-Smirnov"

    print(f"✅ {test_used} Test for Normality on {column} column in {dataset_name} data: p = {p:.3f} -> {'Normal' if p > 0.1 else 'Not Normal'}")
    return p > 0.1  # Returns True if data is normal

# check normality on the filtered data
def check_normality_on_filtered_data(data, dataset_name):
    """
    Checks if the data follows a normal distribution.
    
    Parameters:
    - data (pd.Series): Target variable values.
    - dataset_name (str): Name for reporting.

    Returns:
    - bool: True if data is normally distributed, False otherwise.
    """
    if len(data) < 3:  # Too small to test normality
        print(f"⚠️ Skipping normality test for {dataset_name} (sample too small: n={len(data)})")
        return False

    if len(data) < 50:
        stat, p = stats.shapiro(data)  # Shapiro-Wilk for small samples
        test_used = "Shapiro-Wilk"
    else:
        mean = np.mean(data)
        std = np.std(data, ddof=1)  # Sample standard deviation
        stat, p = stats.kstest(data, 'norm', args=(mean, std))  # KS Test for large samples
        test_used = "Kolmogorov-Smirnov"
    
    print(f"✅ {test_used} Test for Normality in {dataset_name}: p = {p:.3f} -> {'Normal' if p > 0.10 else 'Not Normal'}")
    return p > 0.10  # Returns True if data is normal

# Save updated data back to an Excel file
def save_updated_data(df_original, df_perceived, file_name="updated_data.xlsx"):
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        df_original.to_excel(writer, sheet_name="Original Data", index=False)
        df_perceived.to_excel(writer, sheet_name="Perceived Data", index=False)
    print(f"✅ Updated Excel file saved as '{file_name}'")

# mean, median and std for individual catergorical variable 
def compare_mean_median(df, categorical_var, target_variable, dataset_name):
    """
    Compares Mean & Median for each category in categorical_var.
    """
    print(f"\n📌 Mean & Median Comparison for {dataset_name} Data:")

    summary_stats = df.groupby(categorical_var)[target_variable].agg(["mean", "median", "std"])
    print(summary_stats)

    return summary_stats

#this function count occurrences of all combination
def count_combinations(df, cat1_var, cat2_var, dataset_name):
    """
    Counts occurrences of each category in Age Group & Gender.

    Parameters:
    - df (DataFrame): The dataset (original or perceived).
    - age_var (str): Column name for Age Group (e.g., "age group").
    - gender_var (str): Column name for Gender (e.g., "Gender").
    - dataset_name (str): Name of the dataset for printing.

    Returns:
    - dict: Dictionary of category counts.
    """
    print(f"\n📊 **Category Counts for {dataset_name} Data:**\n")

    # Count total occurrences of each gender
    cat1_counts = df[cat1_var].value_counts()
    print(f"✅ {cat1_var} counts:\n{cat1_counts}\n")

    # Count total occurrences of each age group
    cat1_counts = df[cat2_var].value_counts()
    print(f"✅ {cat2_var} counts:\n{cat1_counts}\n")

    # Count occurrences of each gender within each age group
    cat1_cat2_counts = df.groupby([cat1_var, cat2_var]).size().unstack()
    print(f"✅ {cat1_var} x {cat2_var} counts:\n{cat1_cat2_counts}\n")

    # Convert to dictionary
    result = {
        "{cat1_var} counts": cat1_counts.to_dict(),
        "{cat2_var} counts": cat1_counts.to_dict(),
        "{cat1_var} x {cat2_var} counts": cat1_cat2_counts.to_dict()
    }

    return result

#this function plot the point graph with error bars
def plot_interaction_effect(df, cat1_var, cat2_var, target_var, dataset_name, plot_name):
    """
    Creates an interaction plot for cat1_var and cat2_var on Acceptance Score.
    Handles missing values (NaN) to avoid KeyErrors in Seaborn's pointplot.
    """
    # print(f"\n🔍 Unique values in '{cat1_var}' ({dataset_name}): {df[cat1_var].unique()}")
    # print(f"🔍 Unique values in '{cat2_var}' ({dataset_name}): {df[cat2_var].unique()}")

    # Step 1: Remove spaces and convert to string (ensures category consistency)
    df[cat1_var] = df[cat1_var].astype(str).str.strip()
    df[cat2_var] = df[cat2_var].astype(str).str.strip()

    # Step 2: Fill missing values (NaN) with "Unknown" to avoid KeyErrors
    df[cat2_var] = df[cat2_var].fillna("Unknown")
    df[cat1_var] = df[cat1_var].fillna("Unknown")

    # Step 3: Drop rows where the target variable is NaN (ensures valid plotting)
    df = df.dropna(subset=[target_var])

    # Step 4: Plot
    plt.figure(figsize=(8, 6))
    try:
        sns.pointplot(
            x=cat1_var, y=target_var, hue=cat2_var, data=df,
            capsize=0.1, dodge=True, markers=["o", "s", "d"], linestyles=["-", "--", ":"]
        )
        plt.title(f"Interaction Effect: {cat1_var} & {cat2_var} on {target_var} ({dataset_name})")
        plt.xlabel(cat1_var)
        plt.ylabel(target_var)
        plt.legend(title=cat2_var)
        plt.grid(True)
        plt.savefig(f"plot/{plot_name}.png")
        print(f"\n✅ Plot saved as 'plot/{plot_name}.png'")

    except KeyError as e:
        print(f"\n❌ KeyError: {e}")
        print("🔹 Possible causes: Category missing or incorrectly formatted.")

#this function calculate the mean, median, std for categorial variables and their interaction(all possibility)
def compute_summary_stats_all_possibility(df, categorical_vars, target_variable):
    """
    Computes mean, median, and standard deviation for each categorical variable and their interaction.

    Parameters:
    - df (DataFrame): Dataset (original or perceived).
    - categorical_vars (list): List of categorical variables (e.g., ["Gender", "age group"]).
    - target_variable (str): The dependent variable (e.g., "Acceptance_Score").

    Returns:
    - DataFrame: Summary statistics for each categorical variable and their interaction.
    """
    summary_stats = {}

    # Compute stats for each categorical variable
    for var in categorical_vars:
        summary_stats[var] = df.groupby(var)[target_variable].agg(
            mean="mean",
            median="median",
            std="std",
            count="count"
        ).reset_index()
    
    # Compute interaction effect
    interaction_var = f"{categorical_vars[0]} x {categorical_vars[1]}"
    df[interaction_var] = df[categorical_vars[0]].astype(str) + " & " + df[categorical_vars[1]].astype(str)

    summary_stats[interaction_var] = df.groupby(interaction_var)[target_variable].agg(
        mean="mean",
        median="median",
        std="std",
        count="count"
    ).reset_index()

    return summary_stats


#this function calculate the mean, median, std for categorial variables and their interaction(singled value)
def compute_summary_stats(df, categorical_vars, target_variable):
    """
    Computes mean, median, and standard deviation for each categorical variable 
    and a single value for their interaction.

    Parameters:
    - df (DataFrame): Dataset (original or perceived).
    - categorical_vars (list): List of categorical variables (e.g., ["Gender", "age group"]).
    - target_variable (str): The dependent variable (e.g., "Acceptance_Score").

    Returns:
    - dict: Summary statistics containing mean, median, and std for each category 
            and a single value for interaction.
    """
    summary_stats = {}

    # Compute stats for each categorical variable
    for var in categorical_vars:
        summary_stats[var] = df.groupby(var)[target_variable].agg(["mean", "median", "std"])

    # Compute a single value for the interaction effect
    interaction_grouped = df.groupby(categorical_vars)[target_variable].mean()  # Grouped means
    interaction_mean = interaction_grouped.mean()   # Mean of grouped means
    interaction_median = np.median(interaction_grouped)  # Median of grouped means
    interaction_std = interaction_grouped.std()    # Standard deviation of grouped means

    summary_stats["Interaction"] = {
        "Mean": interaction_mean,
        "Median": interaction_median,
        "Std": interaction_std
    }

    return summary_stats


#this function calculate the mean, median, std for categorial variables interaction(singled value)
def compute_interaction_stats_only(df, categorical_vars, target_variable):
    """
    Computes mean, median, and standard deviation for categorial variables interaction (single values).

    Parameters:
    - df (DataFrame): Dataset (original or perceived).
    - categorical_vars (list): List of categorical variables (e.g., ["Gender", "age group"]).
    - target_variable (str): The dependent variable (e.g., "Acceptance_Score").

    Returns:
    - dict: Summary statistics containing mean, median, and std for each category 
            and a single value for interaction.
    """
    summary_stats = {}

    # Compute a single value for the interaction effect
    interaction_grouped = df.groupby(categorical_vars)[target_variable].mean()  # Grouped means
    interaction_mean = interaction_grouped.mean()   # Mean of grouped means
    interaction_median = np.median(interaction_grouped)  # Median of grouped means
    interaction_std = interaction_grouped.std()    # Standard deviation of grouped means

    summary_stats["Interaction"] = {
        "Mean": interaction_mean,
        "Median": interaction_median,
        "Std": interaction_std
    }

    return summary_stats
