# 🌍 World Happiness Report 2015 - Interactive Web App & Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/visualizations-Plotly%20%7C%20Seaborn-orange)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An interactive data analytics web application and exploratory data analysis of the **2015 UN World Happiness Report** dataset (`2015.csv`). Explore how national factors like GDP, Family support, Life Expectancy, Freedom, and Government Trust determine life satisfaction worldwide.

---

### 🎥 Video Demonstration
🔗 **Video Walkthrough:** [Watch Google Drive Demo](https://drive.google.com/file/d/1WuKIhkcrFSNLyFtjrTyS175vYUC9ttOl/view?usp=sharing)

---

## 🌟 Web Application Features (`app.py`)

The Streamlit web application transforms the static data science script into a reactive dashboard:

1. **🗺️ Interactive Global Choropleth Map**:
   - High-resolution world map colored by Happiness Score.
   - Interactive hover cards revealing national rankings, GDP, health, and freedom.
2. **🏆 Dynamic Leaderboards & Regional Breakdown**:
   - Configurable Top N and Bottom N country rankings with customizable sliders.
   - Regional average happiness bar chart comparing Western Europe, North America, Sub-Saharan Africa, etc.
3. **📊 Correlation Matrix & Dynamic Scatter Explorer**:
   - Full interactive correlation heatmap between all numeric metrics.
   - Dynamic bivariate scatter plot where you select custom X and Y axes, complete with linear regression trendline and $R^2$ fit calculation.
   - Score distribution histograms and regional box plots.
4. **⚖️ Multi-Country Radar Comparison**:
   - Select 2 to 5 countries side-by-side.
   - Normalized 6-factor spider/radar charts displaying relative national strengths.
   - Highlighting comparison data table with delta insights.
5. **🧮 What-If Happiness Simulator**:
   - Interactive metric sliders to configure a hypothetical nation.
   - Real-time Multiple Linear Regression model calculating the predicted Happiness Score.
   - Real-world benchmark indicator showing which existing country matches the simulated score.
6. **📁 Filterable Data Explorer & CSV Export**:
   - Searchable, sortable table with instant CSV export of filtered datasets.
   - Complete descriptive statistics table (`describe()`).

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit Web App
```bash
streamlit run app.py
```
*(Or use `python -m streamlit run app.py`)*

The dashboard will open automatically in your default browser at `http://localhost:8501`.

---

## ☁️ How to Deploy to Streamlit Community Cloud (Free)

Follow these simple steps to deploy your live web app on the internet:

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add interactive Streamlit dashboard"
   git push origin main
   ```
2. **Open Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. **Deploy New App**:
   - Click **"Create app"** (or **"New app"**).
   - Select your GitHub repository: `<your-username>/<your-repo-name>`.
   - Set **Branch**: `main`.
   - Set **Main file path**: `app.py`.
   - Click **"Deploy!"**.
4. **Done!** Your live application URL will be generated and hosted worldwide for free!

---

## 📊 Dataset Schema (`2015.csv`)

The dataset contains records for 158 countries across 12 distinct attributes:

| Column Name | Description |
| :--- | :--- |
| **Country** | Name of the nation |
| **Region** | Geographic region |
| **Happiness Rank** | National rank based on Happiness Score (1 = Highest) |
| **Happiness Score** | Metric rating on a 0 to 10 Cantril Ladder scale |
| **Standard Error** | The standard error of the survey score |
| **Economy (GDP per Capita)** | Contribution of economic productivity to the score |
| **Family** | Contribution of social support and relationships |
| **Health (Life Expectancy)** | Contribution of healthy life expectancy |
| **Freedom** | Contribution of perceived freedom to make life choices |
| **Trust (Government Corruption)** | Perception of absence of corruption in government/business |
| **Generosity** | Generosity based on recent charitable donations |
| **Dystopia Residual** | Baseline hypothetical minimum benchmark score |

---

## 🔬 Standalone Analysis Script (`fp.py`)

If you want to generate static visualization image files locally into the `images/` directory:

```bash
python fp.py
```

### Analytical Breakdown:
- **Correlation Heatmap**: GDP (0.78), Family (0.74), and Health (0.72) have the highest positive correlations with Happiness.
- **Top 10 Leaders**: Switzerland, Iceland, Denmark, Norway, and Canada lead the rankings.
- **Bivariate Scatter Plots**: Evaluates GDP, Family, Health, Freedom, and Corruption against national happiness.
- **Score Distribution**: Centered around a global mean of ~5.38.
- **Regression Fit**: Confirms strong statistically significant positive trends across economic and liberty drivers.

---

## 🛠️ Project Structure

```text
.
├── .streamlit/
│   └── config.toml          # Custom dark modern UI theme
├── images/                  # Static image exports from fp.py
│   ├── correlation_heatmap.png
│   ├── happiest_countries.png
│   ├── gdp_vs_happiness.png
│   ├── ...
├── 2015.csv                 # Raw dataset
├── app.py                   # Main Streamlit web application
├── fp.py                    # Standalone data analysis script
├── fp.ipynb                 # Jupyter notebook
├── requirements.txt         # Pinned dependencies for Streamlit Cloud
└── README.md                # Project documentation
```

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
