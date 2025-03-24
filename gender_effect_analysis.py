# This code is for analysis of effect of gender on adas (technology)

import matplotlib.pyplot as plt
import numpy as np
from utils import load_data, check_reliability, check_normality,calculate_acceptance_score, save_updated_data, compare_mean_median
from parametric_tests import ind_t_test
from non_parametric_tests import mann_whitney_u_test

# Define target variable
target_variable = "Acceptance_Score"
categorical_variable = "Gender"


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

# Printing column names to check if "Gender" exists
# print("\nOriginal Data Columns:", df_original.columns.tolist())
# print("\nPerceived Data Columns:", df_perceived.columns.tolist())


# Step 4 : Check normality
is_normal_original = check_normality(df_original, target_variable, "Original")
is_normal_perceived = check_normality(df_perceived, target_variable, "Perceived")

# step 5: performing the statiscal test 

p_values = {}

if is_normal_original:
    p_values["t-test (Original)"] = ind_t_test(df_original, categorical_variable,target_variable, "Original")
else:
    p_values["Mann-Whitney U (Original)"] = mann_whitney_u_test(df_original, categorical_variable, target_variable, "Original")

if is_normal_perceived:
    p_values["t-test (Perceived)"] = ind_t_test(df_perceived,categorical_variable,  target_variable, "Perceived")
else:
    p_values["Mann-Whitney U (Perceived)"]  = mann_whitney_u_test(df_perceived, categorical_variable,  target_variable, "Perceived")

print("\n📊 **P-Value Results Summary:**")
for test, p_val in p_values.items():
    print(f"{test}: p = {p_val:.5f} {'✅ Significant' if p_val < 0.10 else '❌ Not Significant'}")

significant_original = any(p < 0.10 for key, p in p_values.items() if "Original" in key)
significant_perceived = any(p < 0.10 for key, p in p_values.items() if "Perceived" in key)

mean_median_original = compare_mean_median(df_original, categorical_variable, target_variable, "Original")
mean_median_perceived = compare_mean_median(df_perceived, categorical_variable, target_variable, "Perceived")

# def plot_mean_median(mean_median_original, mean_median_perceived, categorical_var, dataset_name):
#     """
#     Plots Mean & Median for each category in categorical_var.
#     """
#     fig, axes = plt.subplots(1, 2, figsize=(12, 5))

#     if mean_median_original is not None:
#         mean_median_original.plot(kind="bar", ax=axes[0], colormap="coolwarm", edgecolor="black")
#         axes[0].set_title(f"Original Data: Mean & Median {target_variable} by {categorical_var}")
#         axes[0].set_ylabel(target_variable)

#     if mean_median_perceived is not None:
#         mean_median_perceived.plot(kind="bar", ax=axes[1], colormap="coolwarm", edgecolor="black")
#         axes[1].set_title(f"Perceived Data: Mean & Median {target_variable} by {categorical_var}")
#         axes[1].set_ylabel(target_variable)

#     plt.tight_layout()
#     plt.savefig("plot/gender_mean_median_plot.png")
#     print("\n✅ Mean & Median Plot saved as 'plot/gender_mean_median_plot.png'")

# # Generate Mean & Median Plots if Significant Difference is Found
# if significant_original or significant_perceived:
#     plot_mean_median(mean_median_original, mean_median_perceived, categorical_variable, "Gender")

# def plot_mean_median(mean_median, dataset_name):
#     """
#     Plots Mean & Median in a single bar plot with proper spacing.
#     """
#     fig, ax = plt.subplots(figsize=(8, 6))

#     # Extract Mean & Median values
#     mean_values = mean_median["mean"]
#     median_values = mean_median["median"]

#     # Labels for each category
#     categories = ["Mean - Male", "Mean - Female", "Median - Male", "Median - Female"]
    
#     # Flatten values in the same order
#     values = [mean_values["Male"], mean_values["Female"], median_values["Male"], median_values["Female"]]

#     # Bar positions with proper spacing between Mean and Median
#     x_pos = [0, .8, 3, 3.8]

#     # Define bar colors
#     colors = ["#3498db", "#e74c3c", "#3498db", "#e74c3c"]  # Blue for Male, Red for Female

#     # ✅ Plot bars with distinct spacing
#     ax.bar(x_pos, values, color=colors, edgecolor="black", width=0.8)

#     # ✅ Customize the plot
#     ax.set_xlabel("Category")
#     ax.set_ylabel(target_variable)
#     ax.set_title(f"{dataset_name} Data: Mean & Median Comparison")
#     ax.set_xticks(x_pos)
#     ax.set_xticklabels(categories, rotation=20)

#     # ✅ Save the plot
#     plt.savefig(f"plot/{dataset_name.lower()}_gender_mean_median_plot.png")

#     plt.show()

# # ✅ Generate updated Mean & Median Plots
# plot_mean_median(mean_median_original, "Original")
# plot_mean_median(mean_median_perceived, "Perceived")


# visualization - box plot
# fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# sns.boxplot(x="Gender", y=target_variable, data=df_original, ax=axes[0])
# axes[0].set_title(f"Original Data: {target_variable} by Gender")

# sns.boxplot(x="Gender", y=target_variable, data=df_perceived, ax=axes[1])
# axes[1].set_title(f"Perceived Data: {target_variable} by Gender")

# plt.tight_layout()

# plt.savefig("plot/gender_effect_plot.png")
# print("\n✅ Plot saved as 'plot/gender_effect_plot.png'")

def plot_mean_median_with_error_bars(df, categorical_var, target_variable, dataset_name):
    """
    Plots Mean & Median in a single bar plot with error bars and annotations.
    - Mean → Error bars using Standard Error (SE).
    - Median → Error bars using Interquartile Range (IQR).
    - Annotations for important values.
    """
    # Compute Mean, SE (Standard Error), Median, and IQR
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
    summary_stats["iqr_low"] = summary_stats["q1"]
    summary_stats["iqr_high"] = summary_stats["q3"]
    summary_stats["iqr"] = summary_stats["q3"] - summary_stats["q1"]

    # Labels for each category
    categories = ["Mean - Male", "Mean - Female", "Median - Male", "Median - Female"]

    # Extract values
    values = [
        summary_stats.loc["Male", "mean"], summary_stats.loc["Female", "mean"],
        summary_stats.loc["Male", "median"], summary_stats.loc["Female", "median"]
    ]

    # Compute error bars
    error_bars = [
        summary_stats.loc["Male", "se"], summary_stats.loc["Female", "se"],  # SE for Mean
        summary_stats.loc["Male", "iqr"],  # IQR for Median
        summary_stats.loc["Female", "iqr"]  # IQR for Median
    ]

    # Bar positions
    x_pos = [0, 0.8, 2.8, 3.6]  # Ensures spacing between Mean & Median sections

    # Define bar colors
    colors = ["#3498db", "#e74c3c", "#3498db", "#e74c3c"]  # Blue for Male, Red for Female

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(x_pos, values, color=colors, edgecolor="black", width=0.8, yerr=error_bars, capsize=5, error_kw=dict(elinewidth=1.5))

    # Add value labels on top of bars
    for bar, value, err in zip(bars, values, error_bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + err + 1, f"{value:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Add error range annotation
    for bar, err in zip(bars, error_bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height - err - 2, f"±{err:.1f}", ha='center', va='top', fontsize=9, color='black')

    # Customize plot
    ax.set_xlabel("Category")
    ax.set_ylabel(target_variable)
    ax.set_title(f"{dataset_name} Data: Mean & Median with Error Bars")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories, rotation=20)

    # Save plot
    plt.savefig(f"plot/{dataset_name.lower()}_gender_mean_median_error_plot.png")
    print(f"\n✅ Plot saved as 'plot/{dataset_name.lower()}_gender_mean_median_error_plot.png'")

    plt.show()

# ✅ Generate updated Mean & Median Plots with Error Bars and Annotations
plot_mean_median_with_error_bars(df_original, categorical_variable, target_variable, "Original")
plot_mean_median_with_error_bars(df_perceived, categorical_variable, target_variable, "Perceived")