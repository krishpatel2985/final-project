# ==========================================
# World Happiness Report 2015 - Data Analysis
# ==========================================

# 1. Library Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory to save visualization outputs
os.makedirs("images", exist_ok=True)

# 2. Dataset Loading and Inspection
# Read the 2015 world happiness dataset and inspect its structure and check for missing values.
df = pd.read_csv("2015.csv")
df.head()

df.columns

df.info()

df.isnull().sum()

# 3. Correlation Heatmap
# Calculate pairwise Pearson correlation between all numerical columns and plot a heatmap.
corr = df.select_dtypes(include='number').corr()
plt.figure(figsize=(12,8))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("images/correlation_heatmap.png", bbox_inches='tight', dpi=150)
plt.show()

# 4. Happiest Countries Bar Plot
# Select and plot the top 10 happiest countries sorted by Happiness Score.
top10 = df.sort_values("Happiness Score", ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(data=top10, x = "Happiness Score", y="Country")
plt.title("Happiest Countries")
plt.savefig("images/happiest_countries.png", bbox_inches='tight', dpi=150)
plt.show()

# 5. Bivariate Scatter Plots
# Scatter plots mapping the overall Happiness Score against individual metrics.

# GDP vs Happiness Score
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df,
    x="Economy (GDP per Capita)",
    y="Happiness Score"
)
plt.title("GDP vs Happiness score")
plt.savefig("images/gdp_vs_happiness.png", bbox_inches='tight', dpi=150)
plt.show()

# Family vs Happiness Score
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df,
    x="Family",
    y="Happiness Score"
)
plt.title("Family vs Happiness Score")
plt.savefig("images/family_vs_happiness.png", bbox_inches='tight', dpi=150)
plt.show()

# Health (Life Expectancy) vs Happiness Score
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df,
    x="Health (Life Expectancy)",
    y="Happiness Score"
)
plt.title("Health VS Happiness score")
plt.savefig("images/health_vs_happiness.png", bbox_inches='tight', dpi=150)
plt.show()

# Freedom vs Happiness Score
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df,
    x="Freedom",
    y="Happiness Score"
)
plt.title("Freedom vs Happiness score")
plt.savefig("images/freedom_vs_happiness.png", bbox_inches='tight', dpi=150)
plt.show()

# Trust (Government Corruption) vs Happiness Score
plt.figure(figsize=(8,6))
sns.scatterplot(
    data=df,
    x="Trust (Government Corruption)",
    y="Happiness Score"
)
plt.title("Government Trust vs Happiness Score")
plt.savefig("images/trust_vs_happiness.png", bbox_inches='tight', dpi=150)
plt.show()

# 6. Distribution of Happiness Scores
# Plot a histogram with a Kernel Density Estimate (KDE) line to show overall score frequency.
plt.figure(figsize=(10,6))
sns.histplot(df["Happiness Score"], bins=20, kde=True)
plt.title("Distribution of Happiness Scores")
plt.savefig("images/happiness_distribution.png", bbox_inches='tight', dpi=150)
plt.show()

# 7. Pairplot Matrix
# Generate pairplots to explore pairwise relationships between selected variables.
columns = [
    "Happiness Score",
    "Economy (GDP per Capita)",
    "Family",
    "Health (Life Expectancy)",
    "Freedom"
]
sns.pairplot(df[columns])
plt.savefig("images/pairplot.png", bbox_inches='tight', dpi=150)
plt.show()

# 8. Top 20 Countries by GDP per Capita
# Sort countries by Economy (GDP per Capita) and plot the top 20.
top_gdp = df.sort_values("Economy (GDP per Capita)", ascending=False).head(20)

plt.figure(figsize=(12,6))
sns.barplot(data=top_gdp,
            x="Economy (GDP per Capita)",
            y="Country",
            palette="viridis")

plt.title("Top 20 Countries by GDP per Capita")
plt.savefig("images/top_20_gdp.png", bbox_inches='tight', dpi=150)
plt.show()

# 9. Freedom vs. Happiness Score Regression Plot
# Create a regression plot illustrating correlation and line of best fit for Freedom.
plt.figure(figsize=(10,6))

sns.regplot(
    data=df,
    x="Freedom",
    y="Happiness Score",
    scatter_kws={"alpha":0.7}
)

plt.title("Freedom vs Happiness Score")
plt.savefig("images/freedom_regression.png", bbox_inches='tight', dpi=150)
plt.show()

# 10. GDP per Capita Boxplot
# Render a boxplot to outline the distribution and statistics of the GDP feature.
plt.figure(figsize=(6,6))

sns.boxplot(
    y=df["Economy (GDP per Capita)"],
    color="orange"
)

plt.title("Boxplot of GDP per Capita")
plt.savefig("images/gdp_boxplot.1png", bbox_inches='tight', dpi=150)
plt.show()
