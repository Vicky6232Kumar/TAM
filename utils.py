import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pingouin as pg
import numpy as np

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
    return p > 0.05  # Returns True if data is normal

# Save updated data back to an Excel file
def save_updated_data(df_original, df_perceived, file_name="updated_data.xlsx"):
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        df_original.to_excel(writer, sheet_name="Original Data", index=False)
        df_perceived.to_excel(writer, sheet_name="Perceived Data", index=False)
    print(f"✅ Updated Excel file saved as '{file_name}'")

# mean and median 
def compare_mean_median(df, categorical_var, target_variable, dataset_name):
    """
    Compares Mean & Median for each category in categorical_var.
    """
    print(f"\n📌 Mean & Median Comparison for {dataset_name} Data:")

    summary_stats = df.groupby(categorical_var)[target_variable].agg(["mean", "median"])
    print(summary_stats)

    return summary_stats