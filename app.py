"""
World Happiness Report 2015 - Interactive Analytics Dashboard
A modern, responsive Streamlit web application for exploring global happiness metrics.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. Page Configuration & Theme
# ==========================================
st.set_page_config(
    page_title="World Happiness Report 2015 | Global Insights",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.3);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.6);
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .metric-subtitle {
        color: #6366F1;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Header Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        margin-right: 0.5rem;
    }
    .badge-year {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    /* Callout & Highlights */
    .insight-box {
        background: rgba(30, 41, 59, 0.5);
        border-left: 4px solid #6366F1;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. Dataset Loading & Caching
# ==========================================
@st.cache_data
def load_data():
    file_path = "2015.csv"
    if not os.path.exists(file_path):
        st.error(f"Dataset `{file_path}` not found in the current directory.")
        st.stop()
    df = pd.read_csv(file_path)
    return df

df_raw = load_data()

# Factor columns definition
FACTOR_COLS = [
    "Economy (GDP per Capita)",
    "Family",
    "Health (Life Expectancy)",
    "Freedom",
    "Trust (Government Corruption)",
    "Generosity"
]

NUMERIC_COLS = [
    "Happiness Rank",
    "Happiness Score",
    "Standard Error",
    *FACTOR_COLS,
    "Dystopia Residual"
]


# ==========================================
# 3. Sidebar Controls & Filtering
# ==========================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&q=80", use_container_width=True)
    st.title("🌐 Happiness Explorer")
    st.markdown("Interactive analysis of the **UN World Happiness Report** dataset.")
    
    st.markdown("---")
    st.subheader("🔍 Filters & Search")
    
    # Country Search
    search_query = st.text_input("Find Country", placeholder="e.g. Switzerland, India...")
    
    # Region Multi-Select
    all_regions = sorted(df_raw["Region"].unique().tolist())
    select_all_regions = st.checkbox("Select All Regions", value=True)
    
    if select_all_regions:
        selected_regions = st.multiselect("Select Regions", options=all_regions, default=all_regions)
    else:
        selected_regions = st.multiselect("Select Regions", options=all_regions, default=["Western Europe", "North America", "Latin America and Caribbean"])
    
    # Score Range Filter
    min_score = float(df_raw["Happiness Score"].min())
    max_score = float(df_raw["Happiness Score"].max())
    score_range = st.slider(
        "Happiness Score Range",
        min_value=round(min_score, 2),
        max_value=round(max_score, 2),
        value=(round(min_score, 2), round(max_score, 2)),
        step=0.1
    )
    
    st.markdown("---")
    st.markdown("### 📊 About Dataset")
    st.markdown(f"""
    - **Total Records:** {len(df_raw)} Countries
    - **Global Survey Year:** 2015
    - **Core Drivers:** 6 Key Metrics
    """)
    st.markdown("---")
    st.caption("🚀 Built for Streamlit Community Cloud & GitHub")

# Apply Filters
filtered_df = df_raw[
    (df_raw["Region"].isin(selected_regions)) &
    (df_raw["Happiness Score"] >= score_range[0]) &
    (df_raw["Happiness Score"] <= score_range[1])
]

if search_query:
    filtered_df = filtered_df[filtered_df["Country"].str.contains(search_query, case=False, na=False)]


# ==========================================
# 4. Hero Section & KPI Metric Cards
# ==========================================
st.markdown("""
<div>
    <span class="badge badge-year">2015 EDITION</span>
    <span class="badge">158 NATIONS</span>
    <span class="badge">GALLUP WORLD POLL</span>
</div>
<h1 style="margin-top: 0.5rem; margin-bottom: 0.25rem;">World Happiness Report Explorer</h1>
<p style="color: #94A3B8; font-size: 1.05rem; margin-bottom: 1.5rem;">
    Explore global well-being, factor weights, regional trends, and simulate future happiness scores.
</p>
""", unsafe_allow_html=True)

if len(filtered_df) == 0:
    st.warning("⚠️ No countries match the selected filters. Please adjust the sidebar settings.")
    st.stop()

# Key metrics
total_filtered = len(filtered_df)
avg_score = filtered_df["Happiness Score"].mean()
top_country_row = filtered_df.sort_values("Happiness Score", ascending=False).iloc[0]
lowest_country_row = filtered_df.sort_values("Happiness Score", ascending=True).iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Nations Analyzed</div>
        <div class="metric-value">{total_filtered} <span style="font-size: 1rem; color: #94A3B8;">/ {len(df_raw)}</span></div>
        <div class="metric-subtitle">Across {len(filtered_df['Region'].unique())} Regions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Score</div>
        <div class="metric-value">{avg_score:.2f} <span style="font-size: 1rem; color: #94A3B8;">/ 10</span></div>
        <div class="metric-subtitle">Global Mean: {df_raw['Happiness Score'].mean():.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Top Country</div>
        <div class="metric-value">{top_country_row['Country']}</div>
        <div class="metric-subtitle">Score: {top_country_row['Happiness Score']:.3f} (Rank #{top_country_row['Happiness Rank']})</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Lowest Country</div>
        <div class="metric-value">{lowest_country_row['Country']}</div>
        <div class="metric-subtitle">Score: {lowest_country_row['Happiness Score']:.3f} (Rank #{lowest_country_row['Happiness Rank']})</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# 5. Interactive Navigation Tabs
# ==========================================
tab_map, tab_rank, tab_corr, tab_radar, tab_sim, tab_data = st.tabs([
    "🗺️ Global Choropleth",
    "🏆 Top & Bottom Rankings",
    "📊 Correlations & Drivers",
    "⚖️ Country Comparison",
    "🧮 What-If Simulator",
    "📁 Dataset & Statistics"
])


# ------------------------------------------
# TAB 1: Global Choropleth Map
# ------------------------------------------
with tab_map:
    st.subheader("Global Distribution of Happiness Scores")
    st.markdown("Hover over any country to inspect detailed factors, ranking, and economic metrics.")
    
    fig_map = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color="Happiness Score",
        hover_name="Country",
        hover_data={
            "Happiness Rank": True,
            "Happiness Score": ":.3f",
            "Region": True,
            "Economy (GDP per Capita)": ":.2f",
            "Health (Life Expectancy)": ":.2f",
            "Freedom": ":.2f"
        },
        color_continuous_scale="Plasma",
        template="plotly_dark",
        height=620
    )
    
    fig_map.update_layout(
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            title="Happiness Score",
            thicknessmode="pixels", thickness=15,
            lenmode="pixels", len=320,
            x=0.98
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <b>💡 Key Observation:</b> Northern and Western Europe, North America, and Australia consistently report scores above 7.0, primarily driven by strong GDP per capita, social safety nets (Family), and high life expectancy.
    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------
# TAB 2: Top & Bottom Rankings
# ------------------------------------------
with tab_rank:
    st.subheader("Leaderboards & Regional Breakdown")
    
    col_ctrl, col_fill = st.columns([1, 3])
    with col_ctrl:
        num_countries = st.slider("Select number of countries to display", min_value=5, max_value=25, value=10, step=1)
    
    col_top, col_bot = st.columns(2)
    
    with col_top:
        st.markdown(f"#### 🌟 Top {num_countries} Happiest Countries")
        top_n = filtered_df.sort_values("Happiness Score", ascending=False).head(num_countries)
        
        fig_top = px.bar(
            top_n,
            x="Happiness Score",
            y="Country",
            orientation="h",
            color="Happiness Score",
            color_continuous_scale="Viridis",
            text="Happiness Score",
            template="plotly_dark",
            height=450
        )
        fig_top.update_traces(texttemplate='%{text:.2f}', textposition='inside')
        fig_top.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis=dict(range=[0, 8.5]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_top, use_container_width=True)
        
    with col_bot:
        st.markdown(f"#### ⚠️ Bottom {num_countries} Countries")
        bot_n = filtered_df.sort_values("Happiness Score", ascending=True).head(num_countries)
        
        fig_bot = px.bar(
            bot_n,
            x="Happiness Score",
            y="Country",
            orientation="h",
            color="Happiness Score",
            color_continuous_scale="Reds_r",
            text="Happiness Score",
            template="plotly_dark",
            height=450
        )
        fig_bot.update_traces(texttemplate='%{text:.2f}', textposition='inside')
        fig_bot.update_layout(
            yaxis={'categoryorder': 'total descending'},
            xaxis=dict(range=[0, 8.5]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bot, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Regional Happiness Comparison")
    region_stats = df_raw.groupby("Region")["Happiness Score"].agg(["mean", "median", "count"]).reset_index()
    region_stats = region_stats.sort_values("mean", ascending=False)
    
    fig_region = px.bar(
        region_stats,
        x="Region",
        y="mean",
        color="mean",
        color_continuous_scale="Tealgrn",
        labels={"mean": "Average Happiness Score"},
        template="plotly_dark",
        text="mean"
    )
    fig_region.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_region.update_layout(
        xaxis_tickangle=-35,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        height=420
    )
    st.plotly_chart(fig_region, use_container_width=True)


# ------------------------------------------
# TAB 3: Correlations & Drivers
# ------------------------------------------
with tab_corr:
    st.subheader("Correlation Matrix & Factor Influences")
    
    col_corr1, col_corr2 = st.columns([1.1, 1.3])
    
    with col_corr1:
        st.markdown("#### Pearson Correlation Heatmap")
        corr_matrix = df_raw[NUMERIC_COLS].corr().round(2)
        
        fig_heat = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            template="plotly_dark",
            zmin=-1, zmax=1
        )
        fig_heat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10),
            height=460
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col_corr2:
        st.markdown("#### Dynamic Scatter Explorer with Trendline")
        
        col_x, col_y = st.columns(2)
        with col_x:
            x_factor = st.selectbox("Select Independent Variable (X-axis)", options=FACTOR_COLS, index=0)
        with col_y:
            y_factor = st.selectbox("Select Dependent Variable (Y-axis)", options=["Happiness Score"] + FACTOR_COLS, index=0)
            
        x_vals = filtered_df[x_factor].values
        y_vals = filtered_df[y_factor].values
        
        # Calculate OLS line manually using numpy for resilience
        slope, intercept = np.polyfit(x_vals, y_vals, 1)
        r_val = np.corrcoef(x_vals, y_vals)[0, 1]
        
        fig_scatter = px.scatter(
            filtered_df,
            x=x_factor,
            y=y_factor,
            color="Region",
            hover_name="Country",
            hover_data=["Happiness Rank", "Happiness Score"],
            template="plotly_dark",
            height=400
        )
        
        # Add regression line
        x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)
        y_trend = slope * x_trend + intercept
        
        fig_scatter.add_trace(go.Scatter(
            x=x_trend,
            y=y_trend,
            mode="lines",
            name="Linear Fit",
            line=dict(color="#6366F1", width=3, dash="dash")
        ))
        
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.info(f"**Statistical Fit:** Equation: `y = {slope:.2f}x + {intercept:.2f}` | **Correlation (r):** `{r_val:.3f}` ($R^2 = {r_val**2:.3f}$)")

    # Distribution of happiness scores
    st.markdown("---")
    st.subheader("Distribution Analysis")
    col_dist1, col_dist2 = st.columns(2)
    
    with col_dist1:
        fig_hist = px.histogram(
            df_raw,
            x="Happiness Score",
            nbins=22,
            marginal="box",
            color_discrete_sequence=["#818CF8"],
            template="plotly_dark",
            title="Distribution & Boxplot of Happiness Scores"
        )
        fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col_dist2:
        fig_box = px.box(
            df_raw,
            x="Region",
            y="Happiness Score",
            color="Region",
            template="plotly_dark",
            title="Regional Variance of Happiness Scores"
        )
        fig_box.update_layout(
            showlegend=False,
            xaxis_tickangle=-35,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_box, use_container_width=True)


# ------------------------------------------
# TAB 4: Country Comparison (Radar)
# ------------------------------------------
with tab_radar:
    st.subheader("Direct Country vs Country Comparison")
    st.markdown("Select 2 to 5 countries to contrast their relative strength across all 6 core components.")
    
    selected_countries = st.multiselect(
        "Select Countries to Compare",
        options=sorted(df_raw["Country"].unique().tolist()),
        default=["Switzerland", "United States", "India", "Brazil"]
    )
    
    if len(selected_countries) < 1:
        st.info("Please select at least 1 country to visualize radar profiles.")
    else:
        # Normalize factors between 0 and 1 for radar plot
        df_radar_norm = df_raw.copy()
        for f in FACTOR_COLS:
            min_f = df_raw[f].min()
            max_f = df_raw[f].max()
            df_radar_norm[f] = (df_raw[f] - min_f) / (max_f - min_f)
            
        fig_radar = go.Figure()
        colors = ["#6366F1", "#10B981", "#F59E0B", "#EC4899", "#3B82F6"]
        
        for idx, country in enumerate(selected_countries):
            row_norm = df_radar_norm[df_radar_norm["Country"] == country].iloc[0]
            values = [row_norm[f] for f in FACTOR_COLS]
            values.append(values[0])  # Close radar loop
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=FACTOR_COLS + [FACTOR_COLS[0]],
                fill='toself',
                name=country,
                line=dict(color=colors[idx % len(colors)], width=2.5)
            ))
            
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], showticklabels=False),
                bgcolor="rgba(15, 23, 42, 0.4)"
            ),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Side-by-side metric comparison table
        st.markdown("#### Detailed Metric Breakdown")
        comp_df = df_raw[df_raw["Country"].isin(selected_countries)][
            ["Country", "Region", "Happiness Rank", "Happiness Score"] + FACTOR_COLS
        ].set_index("Country")
        st.dataframe(comp_df.style.highlight_max(axis=0, color="#3730A3"), use_container_width=True)


# ------------------------------------------
# TAB 5: What-If Happiness Simulator
# ------------------------------------------
with tab_sim:
    st.subheader("🧮 Interactive Happiness Simulator")
    st.markdown("Adjust the core metric sliders to predict a hypothetical nation's happiness score based on a trained Multiple Linear Regression model.")
    
    # Train OLS analytical weights
    X = df_raw[FACTOR_COLS].values
    X_with_const = np.column_stack([np.ones(len(X)), X])
    y = df_raw["Happiness Score"].values
    weights, residuals, rank, s = np.linalg.lstsq(X_with_const, y, rcond=None)
    
    col_sim_ctrl, col_sim_res = st.columns([1.2, 1])
    
    with col_sim_ctrl:
        st.markdown("#### Input Nation Metrics")
        sim_inputs = {}
        for f in FACTOR_COLS:
            f_min = float(df_raw[f].min())
            f_max = float(df_raw[f].max())
            f_mean = float(df_raw[f].mean())
            sim_inputs[f] = st.slider(
                f"{f}",
                min_value=round(f_min, 3),
                max_value=round(f_max, 3),
                value=round(f_mean, 3),
                step=0.01,
                help=f"Observed Range: {f_min:.2f} - {f_max:.2f}"
            )
            
    with col_sim_res:
        st.markdown("#### Prediction Output")
        sim_vector = np.array([1.0] + [sim_inputs[f] for f in FACTOR_COLS])
        predicted_score = float(np.dot(sim_vector, weights))
        
        # Clamp to realistic bounds
        predicted_score = max(0.0, min(10.0, predicted_score))
        
        # Find closest country
        diffs = (df_raw["Happiness Score"] - predicted_score).abs()
        closest_idx = diffs.idxmin()
        closest_country = df_raw.loc[closest_idx, "Country"]
        closest_score = df_raw.loc[closest_idx, "Happiness Score"]
        closest_rank = df_raw.loc[closest_idx, "Happiness Rank"]
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_score,
            title={'text': "Estimated Happiness Score", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#6366F1"},
                'bgcolor': "rgba(30, 41, 59, 0.7)",
                'borderwidth': 2,
                'bordercolor': "#475569",
                'steps': [
                    {'range': [0, 4.5], 'color': 'rgba(239, 68, 68, 0.4)'},
                    {'range': [4.5, 6.5], 'color': 'rgba(234, 179, 8, 0.4)'},
                    {'range': [6.5, 10], 'color': 'rgba(16, 185, 129, 0.4)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': predicted_score
                }
            }
        ))
        fig_gauge.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box">
            <b>📍 Real-World Benchmark:</b><br>
            A country with these parameters would perform closest to <b>{closest_country}</b> 
            (Score: <b>{closest_score:.2f}</b>, Global Rank: <b>#{closest_rank}</b>).
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------
# TAB 6: Dataset & Statistics
# ------------------------------------------
with tab_data:
    st.subheader("Data Explorer & Export")
    
    col_search, col_export = st.columns([3, 1])
    with col_search:
        st.caption(f"Displaying {len(filtered_df)} of {len(df_raw)} records according to current sidebar filters.")
    with col_export:
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_data,
            file_name="world_happiness_2015_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    st.dataframe(filtered_df, use_container_width=True, height=350)
    
    st.markdown("---")
    st.subheader("Descriptive Summary Statistics")
    st.dataframe(filtered_df[NUMERIC_COLS].describe().round(3).T, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 1rem 0;">
    World Happiness Report Analytics • Ready for Streamlit Community Cloud & GitHub Deployment
</div>
""", unsafe_allow_html=True)
