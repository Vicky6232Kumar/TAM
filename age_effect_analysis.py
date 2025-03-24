# This code is for analysis of effect of age on original and perceived data

import numpy as np
import matplotlib.pyplot as plt
from utils import load_data, check_reliability, check_normality,calculate_acceptance_score, save_updated_data, compare_mean_median
from parametric_tests import one_way_anova, ind_t_test
from non_parametric_tests import kruskal_wallis, mann_whitney_u_test

# Define target variable
target_variable = "Acceptance_Score"
categorical_variable = "age group"

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
    p_values["t-test (Original)"] = ind_t_test(df_original, categorical_variable,target_variable, "Original")
else:
    p_values["Mann-Whitney U (Original)"]  = mann_whitney_u_test(df_original, categorical_variable, target_variable, "Original")

if is_normal_perceived:
    p_values["one-way anova (Perceived)"] = one_way_anova(df_perceived,categorical_variable,  target_variable, "Perceived")
else:
    p_values["Kruskal Wallis (Perceived)"]  = kruskal_wallis(df_perceived, categorical_variable,  target_variable, "Perceived")

print("\n📊 **P-Value Results Summary:**")
for test, p_val in p_values.items():
    print(f"{test}: p = {p_val:.5f} {'✅ Significant' if p_val < 0.10 else '❌ Not Significant'}")

significant_original = any(p < 0.10 for key, p in p_values.items() if "Original" in key)
significant_perceived = any(p < 0.10 for key, p in p_values.items() if "Perceived" in key)

mean_median_original = compare_mean_median(df_original, categorical_variable, target_variable, "Original")
mean_median_perceived = compare_mean_median(df_perceived, categorical_variable, target_variable, "Perceived")

# visualization
# fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# sns.boxplot(x=categorical_variable, y=target_variable, data=df_original, ax=axes[0])
# axes[0].set_title(f"Original Data: {target_variable} by Age")

# sns.boxplot(x=categorical_variable, y=target_variable, data=df_perceived, ax=axes[1])
# axes[1].set_title(f"Perceived Data: {target_variable} by Age")

# plt.tight_layout()

# plt.savefig("plot/age_effect_plot.png")
# print("\n✅ Plot saved as 'plot/age_effect_plot.png'")

# def plot_comparison_bar_chart(df_original, df_perceived, categorical_var, target_variable):
#     """
#     Plots Mean & Median Comparison Bar Chart Between Original and Perceived Data for each Age Group.
#     """
#     # Compute Mean & Median for each dataset
#     stats_original = df_original.groupby(categorical_var)[target_variable].agg(["mean", "median"])
#     stats_perceived = df_perceived.groupby(categorical_var)[target_variable].agg(["mean", "median"])

#     # Find common age groups across both datasets
#     all_age_groups = sorted(set(stats_original.index).union(set(stats_perceived.index)))

#     # Ensure valid age groups exist
#     if len(all_age_groups) == 0:
#         print("❌ No valid age groups found. Skipping bar chart.")
#         return

#     # Align data by reindexing (fill missing groups with NaN)
#     stats_original = stats_original.reindex(all_age_groups)
#     stats_perceived = stats_perceived.reindex(all_age_groups)

#     # Extract values (handling missing values)
#     mean_original = stats_original["mean"].fillna(0).tolist()
#     median_original = stats_original["median"].fillna(0).tolist()
#     mean_perceived = stats_perceived["mean"].fillna(0).tolist()
#     median_perceived = stats_perceived["median"].fillna(0).tolist()

#     # Bar positions
#     x_pos = np.arange(len(all_age_groups))  # Positions for age groups
#     width = 0.3  # Bar width

#     fig, axes = plt.subplots(1, 2, figsize=(14, 6))

#     # Plot for Original Data
#     axes[0].bar(x_pos - width / 2, mean_original, width=width, color="#3498db", label="Mean")
#     axes[0].bar(x_pos + width / 2, median_original, width=width, color="#e74c3c", label="Median")
#     axes[0].set_title("Original Data: Mean & Median by Age Group")
#     axes[0].set_xticks(x_pos)
#     axes[0].set_xticklabels(all_age_groups, rotation=15)
#     axes[0].set_ylabel(target_variable)
#     axes[0].legend()

#     # Plot for Perceived Data
#     axes[1].bar(x_pos - width / 2, mean_perceived, width=width, color="#3498db", label="Mean")
#     axes[1].bar(x_pos + width / 2, median_perceived, width=width, color="#e74c3c", label="Median")
#     axes[1].set_title("Perceived Data: Mean & Median by Age Group")
#     axes[1].set_xticks(x_pos)
#     axes[1].set_xticklabels(all_age_groups, rotation=15)
#     axes[1].set_ylabel(target_variable)
#     axes[1].legend()

#     # Save and show plot
#     plt.tight_layout()
#     plt.savefig("plot/age_group_mean_median_comparison.png")
#     print("\n✅ Comparison Bar Chart saved as 'plot/age_group_mean_median_comparison.png'")
#     plt.show()

# Call function to generate the comparison bar chart
# plot_comparison_bar_chart(df_original, df_perceived, categorical_variable, target_variable)

# def plot_separate_mean_bar_charts(df_original, df_perceived, categorical_var, target_variable):
#     """
#     Plots two separate Mean Bar Charts:
#     - Left: Mean for each age group in Original Data.
#     - Right: Mean for each age group in Perceived Data.
#     - Each age group is assigned a unique color.
#     """
#     # Compute Mean for each dataset
#     stats_original = df_original.groupby(categorical_var)[target_variable].mean()
#     stats_perceived = df_perceived.groupby(categorical_var)[target_variable].mean()

#     # Find all unique age groups
#     all_age_groups = sorted(set(stats_original.index).union(set(stats_perceived.index)))

#     # Ensure valid age groups exist
#     if len(all_age_groups) == 0:
#         print("❌ No valid age groups found. Skipping bar chart.")
#         return

#     # Align data (fill missing values with NaN, then replace with 0)
#     stats_original = stats_original.reindex(all_age_groups).fillna(0)
#     stats_perceived = stats_perceived.reindex(all_age_groups).fillna(0)

#     # Extract values
#     mean_original = stats_original.tolist()
#     mean_perceived = stats_perceived.tolist()

#     # Define bar positions (ensuring bars are fully adjacent)
#     x_pos = np.arange(len(all_age_groups))  # X positions for bars
#     bar_width = 1  # Ensures bars touch each other with no space

#     # Define unique colors for each age group
#     colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]  # Unique colors
#     color_map = {age_group: colors[i % len(colors)] for i, age_group in enumerate(all_age_groups)}

#     fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)  # Shared Y-axis for comparison

#     # Plot for Original Data
#     for i, age_group in enumerate(all_age_groups):
#         axes[0].bar(x_pos[i], mean_original[i], width=bar_width, color=color_map[age_group])
#     axes[0].set_title("Original Data: Mean by Age Group")
#     axes[0].set_xticks(x_pos)
#     axes[0].set_xticklabels(all_age_groups, rotation=15)
#     axes[0].set_ylabel(target_variable)

#     # Plot for Perceived Data
#     for i, age_group in enumerate(all_age_groups):
#         axes[1].bar(x_pos[i], mean_perceived[i], width=bar_width, color=color_map[age_group])
#     axes[1].set_title("Perceived Data: Mean by Age Group")
#     axes[1].set_xticks(x_pos)
#     axes[1].set_xticklabels(all_age_groups, rotation=15)

#     # Add a legend to indicate which color corresponds to which age group
#     handles = [plt.Rectangle((0,0),1,1, color=color_map[age_group]) for age_group in all_age_groups]
#     labels = all_age_groups
#     fig.legend(handles, labels, title="Age Groups", loc="upper center", ncol=len(all_age_groups))

#     # Save and show plot
#     plt.tight_layout()
#     plt.savefig("plot/age_group_separate_mean_plots.png")
#     print("\n✅ Separate Mean Bar Charts saved as 'plot/age_group_separate_mean_plots.png'")
#     plt.show()

# # Call function to generate the separate mean bar charts
# plot_separate_mean_bar_charts(df_original, df_perceived, categorical_variable, target_variable)

def plot_mean_median_with_error_bars(df, categorical_var, target_variable, dataset_name, age_groups_display_map):
    """
    Plots Mean & Median in a single bar plot with error bars and annotations for Age Groups.
    - Mean → Error bars using Standard Error (SE).
    - Median → Error bars using Interquartile Range (IQR).
    - Annotations for important values.
    - Legend & labels to clearly distinguish Mean & Median bars.
    """
    # Compute Mean, Standard Error (SE), Median, and IQR
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

    # Rename age group labels for consistency
    summary_stats = summary_stats.rename(index=age_groups_display_map)

    # Ensure consistent age group order
    all_age_groups = list(age_groups_display_map.values())

    # Align data (fill missing values with NaN, then replace with 0)
    summary_stats = summary_stats.reindex(all_age_groups).fillna(0)

    # Extract values
    mean_values = summary_stats["mean"].tolist()
    median_values = summary_stats["median"].tolist()

    # Compute error bars
    mean_errors = summary_stats["se"].tolist()  # Standard Error (SE) for Mean
    median_errors = summary_stats["iqr"].tolist()  # Interquartile Range (IQR) for Median

    # Bar positions
    x_pos = np.arange(len(all_age_groups))  # Base positions for bars
    width = 0.4  # Width of each bar
    gap = 1.2  # Space between Mean and Median sections

    # Define unique colors for each age group
    colors = ["#3498db", "#e74c3c", "#2ecc71"]  # Unique colors for age groups

    fig, ax = plt.subplots(figsize=(10, 6))

    # Adjusted positions for separate Mean & Median grouping
    mean_x = x_pos - gap / 2
    median_x = x_pos + gap / 2

    # Plot Mean Bars
    bars_mean = ax.bar(mean_x, mean_values, width=width, color=colors[:len(all_age_groups)], edgecolor="black", yerr=mean_errors, capsize=5, error_kw=dict(elinewidth=1.5), label="Mean (SE)")

    # Plot Median Bars
    bars_median = ax.bar(median_x, median_values, width=width, color=colors[:len(all_age_groups)], edgecolor="black", yerr=median_errors, capsize=5, error_kw=dict(elinewidth=1.5), alpha=0.7, label="Median (IQR)")

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
    ax.set_xlabel("Age Group")
    ax.set_ylabel(target_variable)
    ax.set_title(f"{dataset_name} Data: Mean & Median with Error Bars")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(all_age_groups, rotation=15)

    # Create Legend for Age Groups & Statistics
    age_group_patches = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(all_age_groups))]
    legend_labels = [f"{age}" for age in all_age_groups]

    # First Legend (Age Groups)
    legend1 = ax.legend(age_group_patches, legend_labels, title="Age Groups", loc="upper left", bbox_to_anchor=(1, 1))

    # Second Legend (Mean/Median)
    legend2 = ax.legend(title="Statistical Measure", loc="upper left", bbox_to_anchor=(1, 0.8))
    ax.add_artist(legend1)

    # Save plot
    plt.savefig(f"plot/{dataset_name.lower()}_age_group_mean_median_error_plot.png")
    print(f"\n✅ Plot saved as 'plot/{dataset_name.lower()}_age_group_mean_median_error_plot.png'")

    plt.show()



# def plot_mean_median_grouped(df, categorical_var, target_variable, dataset_name, age_groups_display_map):
#     """
#     Plots separate bar charts for Mean & Median in a single plot.
#     - First group: Mean values (with Standard Error - SE).
#     - Second group: Median values (with Interquartile Range - IQR).
#     - Separate plots for Original & Perceived Data.
#     """
#     # Compute Mean, SE, Median, and IQR
#     summary_stats = df.groupby(categorical_var)[target_variable].agg(
#         mean="mean",
#         std="std",
#         count="count",
#         median="median",
#         q1=lambda x: np.percentile(x, 25),
#         q3=lambda x: np.percentile(x, 75)
#     )

#     # Compute Standard Error (SE) for Mean
#     summary_stats["se"] = summary_stats["std"] / np.sqrt(summary_stats["count"])

#     # Compute IQR (Interquartile Range) for Median
#     summary_stats["iqr"] = summary_stats["q3"] - summary_stats["q1"]

#     # Rename age group labels for consistency
#     summary_stats = summary_stats.rename(index=age_groups_display_map)

#     # Ensure consistent age group order
#     all_age_groups = list(age_groups_display_map.values())

#     # Align data (fill missing values with NaN, then replace with 0)
#     summary_stats = summary_stats.reindex(all_age_groups).fillna(0)

#     # Extract values
#     mean_values = summary_stats["mean"].tolist()
#     median_values = summary_stats["median"].tolist()

#     # Compute error bars
#     mean_errors = summary_stats["se"].tolist()  # SE for Mean
#     median_errors = summary_stats["iqr"].tolist()  # IQR for Median

#     # Bar positions
#     x_pos = np.arange(len(all_age_groups))  # Base positions for bars
#     width = 0.4  # Width of each bar
#     gap = 1.2  # Space between Mean and Median sections

#     # Define unique colors for each age group
#     colors = ["#3498db", "#e74c3c", "#2ecc71"]  # Unique colors

#     fig, ax = plt.subplots(figsize=(8, 6))

#     # Adjusted positions for separate Mean & Median grouping
#     mean_x = x_pos - gap / 2
#     median_x = x_pos + gap / 2

#     # Plot Mean Bars
#     bars_mean = ax.bar(mean_x, mean_values, width=width, color=colors[:len(all_age_groups)], edgecolor="black", yerr=mean_errors, capsize=5, error_kw=dict(elinewidth=1.5), label="Mean (SE)")

#     # Plot Median Bars
#     bars_median = ax.bar(median_x, median_values, width=width, color=colors[:len(all_age_groups)], edgecolor="black", yerr=median_errors, capsize=5, error_kw=dict(elinewidth=1.5), alpha=0.7, label="Median (IQR)")

#     # Add value labels on top of bars (Mean & Median)
#     for bar, value, err in zip(bars_mean, mean_values, mean_errors):
#         height = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width()/2, height + err + 1, f"{value:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

#     for bar, value, err in zip(bars_median, median_values, median_errors):
#         height = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width()/2, height + err + 1, f"{value:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

#     # Add error range annotation below bars
#     for bar, err in zip(bars_mean, mean_errors):
#         height = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width()/2, height - err - 2, f"±{err:.1f}", ha='center', va='top', fontsize=9, color='black')

#     for bar, err in zip(bars_median, median_errors):
#         height = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width()/2, height - err - 2, f"±{err:.1f}", ha='center', va='top', fontsize=9, color='black')

#     # Customize plot
#     ax.set_xlabel("Age Group")
#     ax.set_ylabel(target_variable)
#     ax.set_title(f"{dataset_name} Data: Mean & Median with Error Bars")
#     ax.set_xticks(x_pos)
#     ax.set_xticklabels(all_age_groups, rotation=15)

#     # Create Legend for Age Groups
#     age_group_patches = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(all_age_groups))]
#     legend_labels = [f"{age}" for age in all_age_groups]

#     # First Legend (Age Groups)
#     legend1 = ax.legend(age_group_patches, legend_labels, title="Age Groups", loc="upper left", bbox_to_anchor=(1, 1))

#     # Second Legend (Mean/Median)
#     legend2 = ax.legend(title="Statistical Measure", loc="upper left", bbox_to_anchor=(1, 0.8))
#     ax.add_artist(legend1)

#     # Save plot
#     plt.savefig(f"plot/{dataset_name.lower()}_age_group_mean_median_error_plot.png")
#     print(f"\n✅ Plot saved as 'plot/{dataset_name.lower()}_age_group_mean_median_error_plot.png'")

#     plt.show()


def plot_mean_median_grouped(df, categorical_var, target_variable, dataset_name, age_groups_display_map):
    """
    Plots separate bar charts for Mean & Median in a single plot.
    - Mean bars on the left, Median bars on the right.
    - Ensures bars do NOT overlap.
    - Separate plots for Original & Perceived Data.
    - Each bar has a label for clarity.
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

    # Rename age group labels for consistency
    summary_stats = summary_stats.rename(index=age_groups_display_map)

    # Ensure consistent age group order
    all_age_groups = list(age_groups_display_map.values())

    # Align data (fill missing values with NaN, then replace with 0)
    summary_stats = summary_stats.reindex(all_age_groups).fillna(0)

    # Extract values
    mean_values = summary_stats["mean"].tolist()
    median_values = summary_stats["median"].tolist()

    # Compute error bars
    mean_errors = summary_stats["se"].tolist()  # SE for Mean
    median_errors = summary_stats["iqr"].tolist()  # IQR for Median

    # Define bar positions
    num_groups = len(all_age_groups)
    x_indices = np.arange(num_groups * 2)  # Create positions for each bar
    width = 0.3  # Set bar width
    spacing = 0.3  # Space between groups

    mean_x = x_indices[:num_groups] * spacing  # Spread out Mean bars
    median_x = x_indices[num_groups:] * spacing + spacing  # Spread out Median bars

    # Define bar labels for clarity
    mean_labels = [f"Mean - {age}" for age in all_age_groups]
    median_labels = [f"Median - {age}" for age in all_age_groups]
    all_labels = mean_labels + median_labels

    # Define unique colors for each age group
    colors = ["#3498db", "#e74c3c", "#2ecc71"]  # Unique colors

    fig, ax = plt.subplots(figsize=(12, 6))

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
    ax.set_xlabel("Statistic")
    ax.set_ylabel(target_variable)
    ax.set_title(f"{dataset_name} Data: Mean & Median with Error Bars")
    ax.set_xticks(np.concatenate((mean_x, median_x)))  # Merge x positions
    ax.set_xticklabels(all_labels, rotation=20)

    # Create Legend for Age Groups
    age_group_patches = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(num_groups)]
    legend_labels = [f"{age}" for age in all_age_groups]

    # First Legend (Age Groups)
    legend1 = ax.legend(age_group_patches, legend_labels, title="Age Groups", loc="upper left", bbox_to_anchor=(1, 1))

    # Second Legend (Mean/Median)
    # legend2 = ax.legend(title="Statistical Measure", loc="upper left", bbox_to_anchor=(1, 0.8))
    # ax.add_artist(legend1)

    # Save plot
    plt.savefig(f"plot/{dataset_name.lower()}_age_group_mean_median_error_plot.png")
    print(f"\n✅ Plot saved as 'plot/{dataset_name.lower()}_age_group_mean_median_error_plot.png'")

    plt.show()


# Define consistent age group labels
age_groups_original = {"18 to 30": "18 to 30", "30 to 50": "30 to 50"}
age_groups_perceived = {"18 to 30 years": "18 to 30", "30 to 50 years": "30 to 50", "> 50 years": "> 50"}

# Generate Mean & Median Plots with Error Bars for Original Data and Perceived Data
plot_mean_median_grouped(df_original, categorical_variable, target_variable, "Original", age_groups_original)
plot_mean_median_grouped(df_perceived, categorical_variable, target_variable, "Perceived", age_groups_perceived)
