
import seaborn as sns
import matplotlib.pyplot as plt
from utils import load_data, check_reliability, check_normality,calculate_acceptance_score, save_updated_data
from parametric_tests import one_way_anova, two_way_mixed_anova, ind_t_test
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

if is_normal_original:
    ind_t_test(df_original, categorical_variable,target_variable, "Original")
else:
    mann_whitney_u_test(df_original, categorical_variable, target_variable, "Original")

if is_normal_perceived:
    one_way_anova(df_perceived,categorical_variable,  target_variable, "Perceived")
else:
    kruskal_wallis(df_perceived, categorical_variable,  target_variable, "Perceived")

# step 6 : now comparing original and percieved data by effect of age

# Check if Two-Way Mixed ANOVA assumptions hold before running
# if is_normal_original and is_normal_perceived:
#     if df_original[categorical_variable].nunique() >= 2 and df_perceived[categorical_variable].nunique() >= 2:
#         try:
#             two_way_mixed_anova(df_original, df_perceived, categorical_variable, target_variable)
#         except Exception as e:
#             print(f"\n❌ Two-Way Mixed ANOVA failed due to error: {e}")
#             print("Attempting Non-Parametric Test: Wilcoxon Signed-Rank Test")
#             wilcoxon_test(df_original, df_perceived, target_variable)

#     else:
#         print("\nSkipping Two-Way Mixed ANOVA: Not enough unique groups in categorical variable.")
# else:
#     print("\nSkipping Two-Way Mixed ANOVA: Data is not normally distributed.")
#     wilcoxon_test(df_original, df_perceived, target_variable)


# visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.boxplot(x=categorical_variable, y=target_variable, data=df_original, ax=axes[0])
axes[0].set_title(f"Original Data: {target_variable} by Age")

sns.boxplot(x=categorical_variable, y=target_variable, data=df_perceived, ax=axes[1])
axes[1].set_title(f"Perceived Data: {target_variable} by Age")

plt.tight_layout()

plt.savefig("plot/age_effect_plot.png")
print("\n✅ Plot saved as 'plot/age_effect_plot.png'")