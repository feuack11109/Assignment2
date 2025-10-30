import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Global Crime Statistics Dashboard",
                   layout="wide")


# Load data with caching

@st.cache_data
def load_data():
    """Load all CSV datasets"""
    data_path = Path(__file__).parent / "data"

    offences = pd.read_csv(data_path / "offences_subset_cleaned.csv")
    victims = pd.read_csv(data_path / "victims_subset_cleaned.csv")
    trafficking = pd.read_csv(data_path / "cleaned_offences_of_trafficking_in_persons.csv")
    convicted = pd.read_csv(data_path / "convicted_focus_rape_trafficking.csv")
    personnel = pd.read_csv(data_path / "criminal_justice_personnel_cleaned.csv")
    prosecuted = pd.read_csv(data_path / "prosecuted_focus_rape_trafficking.csv")
    sdg_safety = pd.read_csv(data_path / "sdg_dataset_perception_of_safety_clean.csv")

    return offences, victims, trafficking, convicted, personnel, prosecuted, sdg_safety


offences_df, victims_df, trafficking_df, convicted_df, personnel_df, prosecuted_df, sdg_safety_df = load_data()

st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: white;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .main-header h1 {
        color: #2d3748;
        margin: 0 0 10px 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #718096;
        margin: 0;
        font-size: 1.1rem;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 60px 40px;
        margin-bottom: 40px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin: 0 0 20px 0;
        line-height: 1.2;
        color: white;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin: 0 0 40px 0;
        opacity: 0.9;
        line-height: 1.6;
        color: white;
    }
    
    /* Stat cards */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        height: 100%;
    }
    
    /* Chart wrapper class for Overview tab */
    .chart-wrapper {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Column spacing for proper card separation */
    [data-testid="column"] {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }
    
    [data-testid="column"]:first-child {
        padding-left: 0 !important;
        padding-right: 0.75rem !important;
    }
    
    [data-testid="column"]:last-child {
        padding-left: 0.75rem !important;
        padding-right: 0 !important;
    }
    
    /* Make Streamlit chart containers blend with white cards */
    [data-testid="stPlotlyChart"] {
        background-color: white !important;
        padding: 10px 25px 25px 25px !important;
        margin-top: 0px !important;
        border-radius: 0 0 12px 12px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        overflow: hidden !important;
    }
    
    [data-testid="stPlotlyChart"] > div {
        background-color: white !important;
    }
    
    /* Style title divs to connect with charts */
    div[style*="border-radius: 12px"] {
        margin-bottom: 0 !important;
        padding-bottom: 15px !important;
        border-radius: 12px 12px 0 0 !important;
        box-shadow: none !important;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0;
    }
    
    .stat-label {
        color: #718096;
        font-size: 1rem;
        margin: 5px 0 0 0;
    }
    
    .stat-change {
        font-size: 0.9rem;
        margin-top: 8px;
        font-weight: 600;
    }
    
    .stat-change.positive {
        color: #e53e3e;
    }
    
    .stat-change.negative {
        color: #38a169;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 3px solid #667eea;
        height: 100%;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-color: #764ba2;
    }
    
    /* Custom tab styling */
    .custom-tabs {
        display: flex;
        gap: 8px;
        background: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 25px;
        padding-bottom: 0;
    }
    
    .custom-tabs > div {
        flex: 1;
        min-width: 0;
    }
    
    .custom-tabs button {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-bottom: none !important;
        border-radius: 8px 8px 0 0 !important;
        color: rgba(255, 255, 255, 0.7) !important;
        padding: 10px 8px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        height: 45px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    .custom-tabs button:hover {
        color: white !important;
        background: rgba(0, 0, 0, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a202c !important;
        margin: 0 0 15px 0;
    }
    
    .feature-description {
        color: #2d3748;
        line-height: 1.6;
        margin: 0 0 20px 0;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 20px;
    }
    
    /* Insight items */
    .insight-item {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        height: 100%;
    }
    
    .insight-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .insight-heading {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 15px 0;
    }
    
    .insight-text {
        color: #4a5568;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Insights wrapper */
    .insights-wrapper {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    
    .insights-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 24px;
    }
    
    @media (max-width: 900px) {
        .insights-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    
    @media (max-width: 600px) {
        .insights-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Hero stats */
    .hero-stat {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        text-align: center;
    }
    
    .hero-stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 5px 0;
        color: white;
    }
    
    .hero-stat-label {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
        color: white;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 10px 0;
        text-align: center;
    }
    
    .chart-explanation {
        font-size: 0.9rem;
        color: #718096;
        line-height: 1.5;
        margin: 0 0 20px 0;
        text-align: center;
        font-style: italic;
    }
    
    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2d3748;
        text-align: center;
        margin: 40px 0;
    }
    
    .methodology-section {
        background: white;
        border-radius: 12px;
        padding: 40px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    
    .methodology-item h4 {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 15px 0;
    }
    
    .methodology-item p {
        color: #4a5568;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Factor cards */
    .factor-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-top: 4px solid #e53e3e;
        height: 100%;
    }
    
    .factor-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 15px 0;
    }
    
    .factor-description {
        color: #4a5568;
        line-height: 1.6;
        margin: 0 0 15px 0;
    }
    
    .factor-stats {
        background: #f7fafc;
        border-radius: 6px;
        padding: 10px;
        font-size: 0.9rem;
        color: #2d3748;
    }
    
    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .insight-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 10px 0;
    }
    
    /* Controls */
    .controls {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        padding: 12px 24px;
        color: #4a5568;
    }
    
    .stTabs [aria-selected="true"] {
        background: #667eea;
        color: white !important;
    }
    
    /* Remove default padding that causes spacing issues */
    .element-container {
        padding: 0 !important;
    }
    
    /* Target the block containing the region selectbox - using position */
    .main .block-container > div:nth-of-type(3) {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Style controls wrapper */
    .controls-wrapper {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Target controls in Overview tab using sibling selector */
    .tab2-controls-start + div[data-testid="column"] {
        background: white !important;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Target the parent of tab2 controls */
    .tab2-controls-start ~ div[data-testid="stHorizontalBlock"] {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Style the filter controls container directly */
    .filter-controls-box {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .filter-controls-box h3 {
        margin: 0 0 15px 0 !important;
    }
</style>
""",
            unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>Global Crime Statistics Dashboard</h1>
    <p>Comprehensive analysis of crime data trends and patterns worldwide</p>
</div>
""",
            unsafe_allow_html=True)

# Region Filter - white background applied via CSS
col1, col2, col3 = st.columns([2, 2, 6])
with col1:
    all_regions = sorted(offences_df['Region'].unique().tolist())
    region_options = ['All Regions'] + all_regions
    selected_region = st.selectbox("🌍 Select Region",
                                   region_options,
                                   key="global_region_filter")

# Filter data based on selected region
if selected_region == 'All Regions':
    filtered_offences = offences_df.copy()
    filtered_convicted = convicted_df.copy()
    filtered_prosecuted = prosecuted_df.copy()
    filtered_trafficking = trafficking_df.copy()
    filtered_victims = victims_df.copy()
    filtered_personnel = personnel_df.copy()
else:
    filtered_offences = offences_df[offences_df['Region'] ==
                                    selected_region].copy()
    filtered_convicted = convicted_df[convicted_df['Region'] ==
                                      selected_region].copy()
    filtered_prosecuted = prosecuted_df[prosecuted_df['Region'] ==
                                        selected_region].copy()
    filtered_trafficking = trafficking_df[trafficking_df['Region'] ==
                                          selected_region].copy()
    filtered_victims = victims_df[victims_df['Region'] ==
                                  selected_region].copy()
    filtered_personnel = personnel_df[personnel_df['Region'] ==
                                      selected_region].copy()

# Calculate key statistics from real data
total_countries = len(filtered_offences['Country'].unique())
total_convicted = int(filtered_convicted['VALUE'].sum()
                      ) if 'VALUE' in filtered_convicted.columns and len(
                          filtered_convicted) > 0 else 0
total_trafficking_victims = len(filtered_trafficking[
    filtered_trafficking['Indicator'] == 'Detected trafficking victims'])

# Display selected region
region_display = selected_region if selected_region != 'All Regions' else 'Worldwide'

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# Create custom tab navigation
st.markdown('<div class="custom-tabs">', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.current_page = "🏠 Home"
        st.rerun()
with col2:
    if st.button("📈 Overview", key="nav_overview", use_container_width=True):
        st.session_state.current_page = "📈 Overview"
        st.rerun()
with col3:
    if st.button("👥 Gender", key="nav_gender", use_container_width=True):
        st.session_state.current_page = "👥 Gender Analysis"
        st.rerun()
with col4:
    if st.button("🔍 Trafficking", key="nav_trafficking", use_container_width=True):
        st.session_state.current_page = "🔍 Trafficking Analysis"
        st.rerun()
with col5:
    if st.button("⚖️ Conviction", key="nav_conviction", use_container_width=True):
        st.session_state.current_page = "⚖️ Conviction Outcomes"
        st.rerun()
with col6:
    if st.button("🏛️ Justice", key="nav_justice", use_container_width=True):
        st.session_state.current_page = "🏛️ Justice System Capacity"
        st.rerun()
with col7:
    if st.button("🛡️ Safety & SDG", key="nav_safety", use_container_width=True):
        st.session_state.current_page = "🛡️ Safety & SDG Indicators"
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Add active tab highlighting via JavaScript
st.markdown(f"""
<script>
const currentPage = "{st.session_state.current_page}";
const buttons = document.querySelectorAll('.custom-tabs button');
buttons.forEach(btn => {{
    if (btn.textContent.includes(currentPage)) {{
        btn.classList.add('active');
    }}
}});
</script>
""", unsafe_allow_html=True)

if st.session_state.current_page == "🏠 Home":
    st.markdown(f"""
    <div class="hero-section">
        <h2 class="hero-title">Crime Data Reporting Coverage - {region_display}</h2>
        <p class="hero-subtitle">Analysis of crime data availability and reporting patterns from government databases. Metrics show data coverage, not incident counts.</p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown(f"""
        <div class="hero-stat">
            <div class="hero-stat-number">{total_trafficking_victims:,}</div>
            <div class="hero-stat-label">Trafficking Data Records</div>
        </div>
        """,
                    unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="hero-stat">
            <div class="hero-stat-number">{total_countries}</div>
            <div class="hero-stat-label">Countries Reporting</div>
        </div>
        """,
                    unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="hero-stat">
            <div class="hero-stat-number">{total_convicted:,}</div>
            <div class="hero-stat-label">Total Convictions</div>
        </div>
        """,
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards with navigation
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3 class="feature-title">Data Coverage Overview</h3>
            <p class="feature-description">Explore which countries and regions report crime data, tracking reporting patterns and data availability across categories</p>
            <div class="feature-highlight">Multi-year coverage trends</div>
        </div>
        """,
                    unsafe_allow_html=True)
        if st.button("📈", key="overview_card", use_container_width=True, help="Click to view Overview"):
            st.session_state.current_page = "📈 Overview"
            st.rerun()
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3 class="feature-title">Gender Data Patterns</h3>
            <p class="feature-description">Analysis of gender-disaggregated data availability in victimization reporting across countries and regions</p>
            <div class="feature-highlight">Demographic reporting</div>
        </div>
        """,
                    unsafe_allow_html=True)
        if st.button("👥", key="gender_card", use_container_width=True, help="Click to view Gender Analysis"):
            st.session_state.current_page = "👥 Gender Analysis"
            st.rerun()

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3 class="feature-title">Trafficking Data Coverage</h3>
            <p class="feature-description">Examine patterns in trafficking data reporting and detection across different regions and countries</p>
            <div class="feature-highlight">Detection reporting</div>
        </div>
        """,
                    unsafe_allow_html=True)
        if st.button("🔍", key="trafficking_card", use_container_width=True, help="Click to view Trafficking Analysis"):
            st.session_state.current_page = "🔍 Trafficking Analysis"
            st.rerun()
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚠️</div>
            <h3 class="feature-title">Conviction Statistics</h3>
            <p class="feature-description">Actual conviction counts from justice systems, showing quantitative outcomes for prosecution efforts</p>
            <div class="feature-highlight">Quantitative data</div>
        </div>
        """,
                    unsafe_allow_html=True)
        if st.button("⚖️", key="conviction_card", use_container_width=True, help="Click to view Conviction Outcomes"):
            st.session_state.current_page = "⚖️ Conviction Outcomes"
            st.rerun()

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏛️</div>
            <h3 class="feature-title">Justice System Reporting</h3>
            <p class="feature-description">Coverage of criminal justice personnel data and prosecution reporting across countries</p>
            <div class="feature-highlight">System capacity data</div>
        </div>
        """,
                    unsafe_allow_html=True)
        if st.button("🏛️", key="justice_card", use_container_width=True, help="Click to view Justice System Capacity"):
            st.session_state.current_page = "🏛️ Justice System Capacity"
            st.rerun()
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3 class="feature-title">Safety & SDG Indicators</h3>
            <p class="feature-description">Analysis of safety perception, violence prevalence, and SDG indicators for peace and justice</p>
            <div class="feature-highlight">Global safety metrics</div>
        </div>
        """,
                    unsafe_allow_html=True)
        if st.button("🛡️", key="safety_card", use_container_width=True, help="Click to view Safety & SDG Indicators"):
            st.session_state.current_page = "🛡️ Safety & SDG Indicators"
            st.rerun()

    # Key Insights with real data
    st.markdown('<h2 class="section-title">Key Insights & Findings</h2>',
                unsafe_allow_html=True)

    # Calculate insights from data
    countries_count = len(filtered_offences['Country'].unique())
    years_covered = sorted(filtered_offences['Year'].unique())
    year_range = f"{min(years_covered)}-{max(years_covered)}" if len(
        years_covered) > 0 else "Multiple years"
    trafficking_countries = len(filtered_trafficking['Country'].unique())

    st.markdown(f"""
    <div class="insights-wrapper">
        <div class="insights-grid">
            <div class="insight-item">
                <div class="insight-icon">🌏</div>
                <h4 class="insight-heading">Geographic Coverage</h4>
                <p class="insight-text">Data reporting from {countries_count} countries in {region_display} spanning {year_range}, showing which locations submit crime data to international databases.</p>
            </div>
            <div class="insight-item">
                <div class="insight-icon">📊</div>
                <h4 class="insight-heading">Trafficking Reporting</h4>
                <p class="insight-text">{trafficking_countries} countries report trafficking data, indicating breadth of detection and reporting infrastructure in {region_display}.</p>
            </div>
            <div class="insight-item">
                <div class="insight-icon">⚖️</div>
                <h4 class="insight-heading">Conviction Counts</h4>
                <p class="insight-text">{total_convicted:,} total convictions recorded (actual quantitative data), representing judicial outcomes across reporting countries.</p>
            </div>
            <div class="insight-item">
                <div class="insight-icon">🔍</div>
                <h4 class="insight-heading">Data Structure</h4>
                <p class="insight-text">Multi-dimensional records tracking crime types, demographics, and temporal patterns. Most metrics show reporting coverage, not incident totals.</p>
            </div>
        </div>
    </div>
    """,
                unsafe_allow_html=True)

    st.markdown("""
    <div class="methodology-section">
        <h2 class="section-title" style="color: #2d3748;">Data Sources & Understanding the Metrics</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 30px;">
            <div class="methodology-item">
                <h4>📊 Data Coverage vs Counts</h4>
                <p>Most visualizations show data <strong>reporting patterns</strong> (which countries/years/categories have records) rather than incident magnitudes. Only conviction data contains actual quantitative counts.</p>
            </div>
            <div class="methodology-item">
                <h4>🔍 Analysis Interpretation</h4>
                <p>Charts reveal geographic and temporal coverage of crime reporting infrastructure, helping identify gaps in data collection systems.</p>
            </div>
            <div class="methodology-item">
                <h4>✅ Data Limitations</h4>
                <p>Source datasets primarily contain categorical records. Trends reflect changes in reporting coverage over time, not necessarily changes in actual crime rates.</p>
            </div>
        </div>
    </div>
    """,
                unsafe_allow_html=True)

elif st.session_state.current_page == "📈 Overview":
    #  Overview narrative with white background
    st.markdown("""
    <div style="background: white; border-radius: 12px 12px 0 0; padding: 25px 25px 15px 25px; margin-bottom: 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <p style="color: #4a5568; font-size: 1rem; line-height: 1.6; margin: 0;">
            Explore crime category reporting patterns from the offences dataset. Filter by year, subregion, and crime type to analyze which countries submit data across different offense categories, and track reporting trends over time through interactive visualizations.
        </p>
    </div>
    <div style="background: white; border-radius: 0 0 12px 12px; padding: 0 25px 25px 25px; margin-bottom: 20px; margin-top: 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        years_available = sorted(filtered_offences['Year'].unique())
        selected_year = st.selectbox(
            "Year",
            years_available if len(years_available) > 0 else [2020],
            key="year")

    with col2:
        subregions = ['All Subregions'] + sorted(
            filtered_offences['Subregion'].unique().tolist())
        selected_subregion = st.selectbox("Subregion",
                                          subregions,
                                          key="subregion")

    with col3:
        categories = ['All Categories'] + sorted(
            filtered_offences['Category'].unique().tolist())
        selected_category = st.selectbox("Crime Type",
                                         categories,
                                         key="crime_type")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Filter data
    filtered_data = filtered_offences.copy()
    if selected_subregion != 'All Subregions':
        filtered_data = filtered_data[filtered_data['Subregion'] ==
                                      selected_subregion]
    if selected_category != 'All Categories':
        filtered_data = filtered_data[filtered_data['Category'] ==
                                      selected_category]

    # Statistics cards
    col1, col2, col3, col4 = st.columns(4, gap="large")

    current_year_data = filtered_data[filtered_data['Year'] == selected_year]
    prev_year_data = filtered_data[filtered_data['Year'] == selected_year - 1]

    total_records = len(current_year_data)
    countries_reporting = len(current_year_data['Country'].unique())

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_records:,}</div>
            <div class="stat-label">Data Records</div>
            <div class="stat-change negative">Year {selected_year}</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{countries_reporting}</div>
            <div class="stat-label">Countries Reporting</div>
            <div class="stat-change negative">Submitting data</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        subregion_count = len(filtered_data['Subregion'].unique())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{subregion_count}</div>
            <div class="stat-label">Subregions</div>
            <div class="stat-change negative">With data coverage</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col4:
        crime_types = len(filtered_data['Category'].unique())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{crime_types}</div>
            <div class="stat-label">Categories Tracked</div>
            <div class="stat-change negative">Crime types</div>
        </div>
        """,
                    unsafe_allow_html=True)
    
    # Add spacing between stats and charts
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Data Reporting Trends</h3>
            <p style="color: #718096; font-size: 0.9rem; font-style: italic; margin: 0 0 15px 0; text-align: center;">
                Tracks how many crime category records are submitted to databases each year. Rising trends indicate improved data collection, while dips may signal gaps in reporting infrastructure.
            </p>
        """, unsafe_allow_html=True)

        # Time series data
        yearly_counts = filtered_data.groupby('Year').size().reset_index(
            name='count')

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=yearly_counts['Year'],
                       y=yearly_counts['count'],
                       mode='lines+markers',
                       name='Incidents',
                       line=dict(color='#667eea', width=3),
                       marker=dict(size=10, color='#667eea')))
        fig.update_layout(height=300,
                          margin=dict(l=40, r=20, t=10, b=40),
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          yaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True, key="chart1")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Top Countries by Data Records</h3>
            <p style="color: #718096; font-size: 0.9rem; font-style: italic; margin: 0 0 15px 0; text-align: center;">
                Identifies which countries contribute the most crime category records to the database. Higher counts indicate more comprehensive data reporting systems for the selected year.
            </p>
        """, unsafe_allow_html=True)

        # Top countries
        country_counts = current_year_data.groupby(
            'Country').size().reset_index(name='count')
        country_counts = country_counts.sort_values('count',
                                                    ascending=False).head(10)

        fig = go.Figure()
        fig.add_trace(
            go.Bar(y=country_counts['Country'],
                   x=country_counts['count'],
                   orientation='h',
                   marker=dict(color='#764ba2')))
        fig.update_layout(height=300,
                          margin=dict(l=200, r=20, t=10, b=40),
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          yaxis=dict(tickfont=dict(color='#2d3748')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True, key="chart2")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Subregion breakdown
    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Distribution by Subregion</h3>
            <p style="color: #718096; font-size: 0.9rem; font-style: italic; margin: 0 0 15px 0; text-align: center;">
                Shows the geographic distribution of crime data reporting across different subregions. Each segment represents the proportion of records contributed by that area.
            </p>
        """, unsafe_allow_html=True)

        subregion_counts = current_year_data.groupby(
            'Subregion').size().reset_index(name='count')

        # Custom cyan/light blue palette without white
        cyan_palette = ['#06b6d4', '#22d3ee', '#67e8f9', '#a5f3fc', '#0891b2', '#0e7490', '#155e75', '#164e63', '#14b8a6', '#2dd4bf', '#5eead4', '#99f6e4']
        fig = px.pie(subregion_counts,
                     values='count',
                     names='Subregion',
                     color_discrete_sequence=cyan_palette)
        fig.update_traces(textfont=dict(color='#2d3748', size=11))
        fig.update_layout(height=300,
                          margin=dict(l=5, r=5, t=0, b=60),
                          paper_bgcolor='white',
                          font=dict(color='#2d3748', size=10),
                          legend=dict(
                              orientation='h',
                              yanchor='top',
                              y=-0.15,
                              xanchor='center',
                              x=0.5,
                              font=dict(color='#2d3748', size=8)),
                          showlegend=True)
        st.plotly_chart(fig, use_container_width=True, key="chart3")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Crime Categories</h3>
            <p style="color: #718096; font-size: 0.9rem; font-style: italic; margin: 0 0 15px 0; text-align: center;">
                Displays the most frequently reported crime categories in the database. Categories with more records indicate areas with stronger data collection and reporting mechanisms.
            </p>
        """, unsafe_allow_html=True)

        category_counts = current_year_data.groupby(
            'Category').size().reset_index(name='count')
        category_counts = category_counts.sort_values('count',
                                                      ascending=True).tail(10)

        fig = go.Figure()
        fig.add_trace(
            go.Bar(y=category_counts['Category'],
                   x=category_counts['count'],
                   orientation='h',
                   marker=dict(color='#667eea')))
        fig.update_layout(height=300,
                          margin=dict(l=150, r=20, t=10, b=40),
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          yaxis=dict(tickfont=dict(color='#2d3748')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True, key="chart4")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "👥 Gender Analysis":
    st.markdown("""
    <div class="insight-card">
        <h4 class="insight-title">👥 Gender-Disaggregated Data Coverage</h4>
        <p class="insight-text">
            Availability of gender-disaggregated victimization data, showing which countries report victim demographics by sex and perpetrator relationship.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        years_victims = ['All Years'] + sorted(filtered_victims['Year'].unique().tolist())
        selected_year_gender = st.selectbox(
            "Year",
            years_victims,
            key="year_gender")
    with col2:
        categories_victims = ['All'] + sorted(
            filtered_victims['Category'].unique().tolist())
        selected_category_gender = st.selectbox("Relationship Category",
                                                categories_victims,
                                                key="category_gender")

    # Filter victim data
    if selected_year_gender != 'All Years':
        filtered_victims = filtered_victims[filtered_victims['Year'] ==
                                            selected_year_gender]
    if selected_category_gender != 'All':
        filtered_victims = filtered_victims[filtered_victims['Category'] ==
                                            selected_category_gender]

    # Gender statistics
    col1, col2, col3, col4 = st.columns(4, gap="large")

    male_victims = len(filtered_victims[filtered_victims['Sex'] == 'Male'])
    female_victims = len(filtered_victims[filtered_victims['Sex'] == 'Female'])
    total_victims_count = len(filtered_victims)
    countries_reporting_victims = len(filtered_victims['Country'].unique())

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{male_victims:,}</div>
            <div class="stat-label">Male Victim Records</div>
            <div class="stat-change negative">Data records</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{female_victims:,}</div>
            <div class="stat-label">Female Victim Records</div>
            <div class="stat-change negative">Data records</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_victims_count:,}</div>
            <div class="stat-label">Total Records</div>
            <div class="stat-change negative">{selected_year_gender}</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{countries_reporting_victims}</div>
            <div class="stat-label">Reporting Countries</div>
            <div class="stat-change negative">{selected_year_gender}</div>
        </div>
        """,
                    unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # Countries list section
    reporting_countries = sorted(filtered_victims['Country'].unique())
    countries_badges = ''.join([f'<span style="display: inline-block; background: #f3f4f6; color: #374151; padding: 6px 12px; margin: 4px; border-radius: 6px; font-size: 0.85rem; font-weight: 500;">{country}</span>' for country in reporting_countries])
    
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #000000; font-size: 1rem; font-weight: 600; margin: 0 0 12px 0;">Countries Reporting Gender-Disaggregated Victim Data</h4>
        <div style="max-height: 150px; overflow-y: auto; padding: 5px;">
            {countries_badges}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add spacing between countries and charts
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    # Charts in one connected container
    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Victims by Sex</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Shows the gender breakdown of reported crime victims. This visualization displays the proportion of male and female victims in the database, helping identify gender-specific patterns in victimization.
            </p>
        """, unsafe_allow_html=True)

        sex_counts = filtered_victims.groupby('Sex').size().reset_index(
            name='count')
        
        # Sort to ensure consistent ordering: Female first, Male second
        sex_counts = sex_counts.sort_values('Sex')

        # Create color list: Pink for Female, Cyan for Male
        colors = []
        for sex in sex_counts['Sex']:
            if sex == 'Female':
                colors.append('#ec4899')  # Pink
            else:
                colors.append('#06b6d4')  # Cyan
        
        fig = px.pie(sex_counts,
                     values='count',
                     names='Sex')
        fig.update_traces(marker=dict(colors=colors),
                         textfont=dict(color='#2d3748', size=11))
        fig.update_layout(height=300, 
                          margin=dict(l=5, r=5, t=0, b=60),
                          paper_bgcolor='white',
                          font=dict(color='#2d3748', size=10),
                          legend=dict(
                              orientation='h',
                              yanchor='top',
                              y=-0.15,
                              xanchor='center',
                              x=0.5,
                              font=dict(color='#2d3748', size=8)))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Relationship to Perpetrator</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Displays the relationship categories between victims and perpetrators. This chart reveals whether crimes involve intimate partners, family members, or other known/unknown individuals.
            </p>
        """, unsafe_allow_html=True)

        relationship_counts = filtered_victims.groupby(
            'Category').size().reset_index(name='count')

        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=relationship_counts['Category'],
                   y=relationship_counts['count'],
                   marker=dict(color='#667eea')))
        fig.update_layout(height=300,
                          margin=dict(l=40, r=20, t=10, b=60),
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748'), tickangle=-45),
                          yaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Gender comparison across relationship categories - more insightful analysis
    st.markdown("""
    <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Gender Patterns Across Perpetrator Relationships</h3>
        <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
            Compares male and female victimization patterns across different perpetrator relationship categories. This reveals which types of relationships show the strongest gender disparities in crime victimization.
        </p>
    """, unsafe_allow_html=True)

    # Group by category and sex to see gender patterns across relationship types
    gender_category = filtered_victims.groupby(
        ['Category', 'Sex']).size().reset_index(name='count')

    fig = px.bar(gender_category,
                 x='Category',
                 y='count',
                 color='Sex',
                 barmode='group',
                 color_discrete_map={
                     'Male': '#06b6d4',
                     'Female': '#ec4899'
                 })
    fig.update_layout(height=300,
                      margin=dict(l=40, r=20, t=10, b=120),
                      plot_bgcolor='white',
                      paper_bgcolor='white',
                      xaxis=dict(gridcolor='#cbd5e0', 
                                tickfont=dict(color='#2d3748'),
                                tickangle=-45,
                                title=dict(text='Perpetrator Relationship', font=dict(color='#2d3748'))),
                      yaxis=dict(gridcolor='#cbd5e0', 
                                tickfont=dict(color='#2d3748'),
                                title=dict(text='Number of Records', font=dict(color='#2d3748'))),
                      legend=dict(
                          orientation='h',
                          yanchor='top',
                          y=-0.45,
                          xanchor='center',
                          x=0.5,
                          font=dict(color='#2d3748', size=8),
                          title=dict(text='Gender', font=dict(color='#2d3748', size=8))))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "🔍 Trafficking Analysis":
    st.markdown("""
    <div class="insight-card">
        <h4 class="insight-title">🔍 Trafficking Data Reporting Patterns</h4>
        <p class="insight-text">
            Coverage of trafficking data in international databases, showing which countries report detection and offence data.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        trafficking_years = ['All Years'] + sorted(filtered_trafficking['Year'].unique().tolist())
        selected_year_trafficking = st.selectbox(
            "Year",
            trafficking_years,
            key="year_trafficking")
    with col2:
        indicators = ['All Indicators'] + sorted(
            filtered_trafficking['Indicator'].unique().tolist())
        selected_indicator = st.selectbox("Indicator",
                                          indicators,
                                          key="indicator")

    # Filter trafficking data
    if selected_year_trafficking != 'All Years':
        filtered_trafficking = filtered_trafficking[filtered_trafficking['Year'] ==
                                                    selected_year_trafficking]
    if selected_indicator != 'All Indicators':
        filtered_trafficking = filtered_trafficking[
            filtered_trafficking['Indicator'] == selected_indicator]

    # Statistics
    col1, col2, col3, col4 = st.columns(4, gap="large")

    detected_victims = len(filtered_trafficking[
        filtered_trafficking['Indicator'] == 'Detected trafficking victims'])
    offences_count = len(
        filtered_trafficking[filtered_trafficking['Indicator'] ==
                             'Offences of trafficking in persons'])
    countries_affected = len(filtered_trafficking['Country'].unique())

    with col1:
        year_display = selected_year_trafficking if selected_year_trafficking != 'All Years' else 'All Years'
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{detected_victims:,}</div>
            <div class="stat-label">Detection Records</div>
            <div class="stat-change negative">{year_display}</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{offences_count:,}</div>
            <div class="stat-label">Offence Records</div>
            <div class="stat-change negative">Data records</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{countries_affected}</div>
            <div class="stat-label">Countries Affected</div>
            <div class="stat-change negative">In dataset</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col4:
        dimensions = len(filtered_trafficking['Dimension'].unique())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{dimensions}</div>
            <div class="stat-label">Data Dimensions</div>
            <div class="stat-change negative">Analysis areas</div>
        </div>
        """,
                    unsafe_allow_html=True)
    
    # Add spacing between stats and charts
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # Charts in one connected container
    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Trafficking by Indicator Type</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Shows the distribution of trafficking data across different indicator categories. This reveals which aspects of human trafficking (detection, prosecution, conviction, offences) have the most comprehensive data reporting.
            </p>
        """, unsafe_allow_html=True)

        indicator_counts = filtered_trafficking.groupby(
            'Indicator').size().reset_index(name='count')

        fig = go.Figure()
        fig.add_trace(
            go.Bar(y=indicator_counts['Indicator'],
                   x=indicator_counts['count'],
                   orientation='h',
                   marker=dict(color='#667eea')))
        fig.update_layout(height=300,
                          margin=dict(l=150, r=20, t=10, b=40),
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          yaxis=dict(tickfont=dict(color='#2d3748')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Top Affected Countries</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Identifies countries with the highest number of trafficking-related data records. Higher record counts indicate more active reporting and data collection efforts in combating human trafficking.
            </p>
        """, unsafe_allow_html=True)

        country_trafficking = filtered_trafficking.groupby(
            'Country').size().reset_index(name='count')
        country_trafficking = country_trafficking.sort_values(
            'count', ascending=False).head(10)

        fig = go.Figure()
        fig.add_trace(
            go.Bar(y=country_trafficking['Country'],
                   x=country_trafficking['count'],
                   orientation='h',
                   marker=dict(color='#764ba2')))
        fig.update_layout(height=300,
                          margin=dict(l=200, r=20, t=10, b=40),
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          yaxis=dict(tickfont=dict(color='#2d3748')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Additional analysis charts
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Trafficking by Dimension</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Shows how trafficking data is categorized by different analytical dimensions such as age, sex, citizenship, and exploitation form. This reveals which demographic and contextual factors are most frequently tracked.
            </p>
        """, unsafe_allow_html=True)
        
        dimension_counts = filtered_trafficking.groupby(
            'Dimension').size().reset_index(name='count')
        dimension_counts = dimension_counts.sort_values('count', ascending=True).tail(10)
        
        fig = go.Figure()
        fig.add_trace(
            go.Bar(y=dimension_counts['Dimension'],
                   x=dimension_counts['count'],
                   orientation='h',
                   marker=dict(color='#06b6d4')))
        fig.update_layout(height=300,
                          margin=dict(l=150, r=20, t=10, b=40),
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          yaxis=dict(tickfont=dict(color='#2d3748')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Regional Distribution</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Displays the geographic distribution of trafficking data reporting across world subregions. This highlights which areas have more comprehensive data collection and which may need enhanced monitoring efforts.
            </p>
        """, unsafe_allow_html=True)
        
        subregion_counts = filtered_trafficking.groupby(
            'Subregion').size().reset_index(name='count')
        subregion_counts = subregion_counts.sort_values('count', ascending=False).head(10)
        
        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=subregion_counts['Subregion'],
                   y=subregion_counts['count'],
                   marker=dict(color='#ec4899')))
        fig.update_layout(height=300,
                          margin=dict(l=40, r=20, t=10, b=100),
                          plot_bgcolor='white',
                          paper_bgcolor='white',
                          xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748'), tickangle=-45),
                          yaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "⚖️ Conviction Outcomes":
    st.markdown("""
    <div class="insight-card">
        <h4 class="insight-title">⚖️ Conviction Outcomes: Justice System Results</h4>
        <p class="insight-text">
            Quantitative analysis of actual conviction counts for serious crimes (rape and trafficking). Unlike other tabs showing reporting coverage, these metrics represent real judicial outcomes with verified conviction numbers.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        conviction_years = ['All Years'] + sorted(filtered_convicted['Year'].unique().tolist())
        selected_year_conviction = st.selectbox(
            "Year",
            conviction_years,
            key="year_conviction")
    with col2:
        crime_categories = ['All Categories'] + sorted(
            filtered_convicted['Category'].unique().tolist())
        selected_crime_cat = st.selectbox("Crime Category",
                                          crime_categories,
                                          key="crime_cat")
    with col3:
        subregions_conv = ['All Subregions'] + sorted(
            filtered_convicted['Subregion'].unique().tolist())
        selected_subregion_conv = st.selectbox("Subregion",
                                               subregions_conv,
                                               key="subregion_conv")

    # Filter conviction data
    if selected_year_conviction != 'All Years':
        filtered_convicted = filtered_convicted[filtered_convicted['Year'] ==
                                                selected_year_conviction]
    if selected_crime_cat != 'All Categories':
        filtered_convicted = filtered_convicted[filtered_convicted['Category']
                                                == selected_crime_cat]
    if selected_subregion_conv != 'All Subregions':
        filtered_convicted = filtered_convicted[filtered_convicted['Subregion']
                                                == selected_subregion_conv]

    # Statistics
    col1, col2, col3, col4 = st.columns(4, gap="large")

    total_convictions = int(filtered_convicted['VALUE'].sum()
                            ) if 'VALUE' in filtered_convicted.columns else 0
    countries_conv = len(filtered_convicted['Country'].unique())
    year_display = selected_year_conviction if selected_year_conviction != 'All Years' else 'All Years'

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_convictions:,}</div>
            <div class="stat-label">Total Convictions</div>
            <div class="stat-change negative">{year_display}</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{countries_conv}</div>
            <div class="stat-label">Countries Reporting</div>
            <div class="stat-change negative">With conviction data</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        avg_convictions = int(filtered_convicted['VALUE'].mean(
        )) if 'VALUE' in filtered_convicted.columns and len(
            filtered_convicted) > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{avg_convictions}</div>
            <div class="stat-label">Average per Record</div>
            <div class="stat-change negative">Mean convictions</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col4:
        max_convictions = int(filtered_convicted['VALUE'].max(
        )) if 'VALUE' in filtered_convicted.columns and len(
            filtered_convicted) > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{max_convictions:,}</div>
            <div class="stat-label">Highest Single Record</div>
            <div class="stat-change negative">Maximum value</div>
        </div>
        """,
                    unsafe_allow_html=True)
    
    # Add spacing between stats and charts
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # Charts in connected white containers
    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Convictions by Crime Category Over Time</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Compares conviction trends between rape and trafficking cases across years. This reveals how judicial efforts against these serious crimes have evolved and identifies which crime type sees more successful prosecutions.
            </p>
        """, unsafe_allow_html=True)

        if 'VALUE' in filtered_convicted.columns:
            category_yearly = filtered_convicted.groupby(
                ['Year', 'Category'])['VALUE'].sum().reset_index()

            fig = px.bar(category_yearly,
                         x='Year',
                         y='VALUE',
                         color='Category',
                         barmode='group',
                         color_discrete_map={
                             'Rape': '#667eea',
                             'Drug trafficking': '#ec4899'
                         })
            fig.update_layout(height=300,
                              margin=dict(l=40, r=20, t=10, b=100),
                              plot_bgcolor='white',
                              paper_bgcolor='white',
                              xaxis=dict(gridcolor='#cbd5e0', 
                                        tickfont=dict(color='#2d3748'),
                                        title=dict(text='Year', font=dict(color='#2d3748'))),
                              yaxis=dict(gridcolor='#cbd5e0', 
                                        tickfont=dict(color='#2d3748'),
                                        title=dict(text='Total Convictions', font=dict(color='#2d3748'))),
                              legend=dict(
                                  orientation='h',
                                  yanchor='top',
                                  y=-0.35,
                                  xanchor='center',
                                  x=0.5,
                                  font=dict(color='#2d3748', size=8),
                                  title=dict(text='Crime Type', font=dict(color='#2d3748', size=8))))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Top 10 Countries by Convictions</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Ranks countries by total conviction counts, showing which nations have the highest judicial activity for serious crimes. Higher conviction numbers indicate both active enforcement and robust criminal justice systems.
            </p>
        """, unsafe_allow_html=True)

        if 'VALUE' in filtered_convicted.columns:
            country_conv = filtered_convicted.groupby(
                'Country')['VALUE'].sum().reset_index()
            country_conv = country_conv.sort_values('VALUE',
                                                    ascending=False).head(10)

            fig = go.Figure()
            fig.add_trace(
                go.Bar(y=country_conv['Country'],
                       x=country_conv['VALUE'],
                       orientation='h',
                       marker=dict(color='#764ba2')))
            fig.update_layout(height=300,
                              margin=dict(l=150, r=20, t=10, b=40),
                              plot_bgcolor='white',
                              paper_bgcolor='white',
                              xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                              yaxis=dict(tickfont=dict(color='#2d3748')),
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Second row of charts
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Regional Conviction Distribution</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Shows the geographic distribution of convictions across world subregions. This highlights where judicial systems are most actively prosecuting these crimes and where enforcement may be stronger or better documented.
            </p>
        """, unsafe_allow_html=True)

        if 'VALUE' in filtered_convicted.columns:
            subregion_conv = filtered_convicted.groupby(
                'Subregion')['VALUE'].sum().reset_index()
            subregion_conv = subregion_conv.sort_values('VALUE', ascending=True).tail(10)

            fig = go.Figure()
            fig.add_trace(
                go.Bar(y=subregion_conv['Subregion'],
                       x=subregion_conv['VALUE'],
                       orientation='h',
                       marker=dict(color='#06b6d4')))
            fig.update_layout(height=300,
                              margin=dict(l=150, r=20, t=10, b=40),
                              plot_bgcolor='white',
                              paper_bgcolor='white',
                              xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                              yaxis=dict(tickfont=dict(color='#2d3748')),
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Category Breakdown</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Displays the proportion of convictions between rape and trafficking cases. This pie chart reveals which crime category receives more judicial attention and successful prosecution outcomes in the selected timeframe.
            </p>
        """, unsafe_allow_html=True)

        if 'VALUE' in filtered_convicted.columns:
            category_breakdown = filtered_convicted.groupby(
                'Category')['VALUE'].sum().reset_index()

            fig = px.pie(category_breakdown,
                         values='VALUE',
                         names='Category',
                         color_discrete_map={
                             'Rape': '#667eea',
                             'Drug trafficking': '#ec4899'
                         })
            fig.update_traces(textfont=dict(color='#2d3748', size=12))
            fig.update_layout(height=300,
                              margin=dict(l=20, r=20, t=10, b=60),
                              paper_bgcolor='white',
                              font=dict(color='#2d3748', size=11),
                              legend=dict(
                                  orientation='h',
                                  yanchor='top',
                                  y=-0.15,
                                  xanchor='center',
                                  x=0.5,
                                  font=dict(color='#2d3748', size=8)))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "🏛️ Justice System Capacity":
    st.markdown("""
    <div class="insight-card">
        <h4 class="insight-title">🏛️ Justice System Capacity: Personnel & Prosecutions</h4>
        <p class="insight-text">
            Analysis of criminal justice infrastructure including personnel deployment and prosecution activity for serious crimes. This page shows the operational capacity and responsiveness of justice systems worldwide.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if len(filtered_prosecuted) > 0:
            prosecution_years = ['All Years'] + sorted(filtered_prosecuted['Year'].unique().tolist())
            selected_year_prosecution = st.selectbox(
                "Year",
                prosecution_years,
                key="year_prosecution")
        else:
            selected_year_prosecution = 'All Years'
    with col2:
        if len(filtered_prosecuted) > 0:
            crime_cats_pros = ['All Categories'] + sorted(
                filtered_prosecuted['Category'].unique().tolist())
            selected_crime_prosecution = st.selectbox("Crime Category",
                                                      crime_cats_pros,
                                                      key="crime_prosecution")
        else:
            selected_crime_prosecution = 'All Categories'
    with col3:
        if len(filtered_personnel) > 0:
            groups = ['All Personnel Types'] + sorted(
                filtered_personnel['Group'].unique().tolist())
            selected_group = st.selectbox("Personnel Type",
                                          groups,
                                          key="group")
        else:
            selected_group = 'All Personnel Types'
    with col4:
        if len(filtered_prosecuted) > 0:
            subregions_pros = ['All Subregions'] + sorted(
                filtered_prosecuted['Subregion'].unique().tolist())
            selected_subregion_pros = st.selectbox("Subregion",
                                                   subregions_pros,
                                                   key="subregion_pros")
        else:
            selected_subregion_pros = 'All Subregions'

    # Apply filters
    if len(filtered_prosecuted) > 0:
        if selected_year_prosecution != 'All Years':
            filtered_prosecuted = filtered_prosecuted[
                filtered_prosecuted['Year'] == selected_year_prosecution]
        if selected_crime_prosecution != 'All Categories':
            filtered_prosecuted = filtered_prosecuted[
                filtered_prosecuted['Category'] == selected_crime_prosecution]
        if selected_subregion_pros != 'All Subregions':
            filtered_prosecuted = filtered_prosecuted[
                filtered_prosecuted['Subregion'] == selected_subregion_pros]
    
    if len(filtered_personnel) > 0 and selected_group != 'All Personnel Types':
        filtered_personnel = filtered_personnel[
            filtered_personnel['Group'] == selected_group]

    # Statistics
    col1, col2, col3, col4 = st.columns(4, gap="large")

    prosecuted_count = len(filtered_prosecuted) if len(filtered_prosecuted) > 0 else 0
    personnel_count = len(filtered_personnel) if len(filtered_personnel) > 0 else 0
    countries_prosecuting = len(filtered_prosecuted['Country'].unique()
                                ) if len(filtered_prosecuted) > 0 else 0
    year_display = selected_year_prosecution if selected_year_prosecution != 'All Years' else 'All Years'

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{prosecuted_count:,}</div>
            <div class="stat-label">Prosecution Records</div>
            <div class="stat-change negative">{year_display}</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{countries_prosecuting}</div>
            <div class="stat-label">Countries Prosecuting</div>
            <div class="stat-change negative">With prosecution data</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{personnel_count:,}</div>
            <div class="stat-label">Personnel Records</div>
            <div class="stat-change negative">In database</div>
        </div>
        """,
                    unsafe_allow_html=True)

    with col4:
        personnel_countries = len(filtered_personnel['Country'].unique()
                                  ) if len(filtered_personnel) > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{personnel_countries}</div>
            <div class="stat-label">Personnel Countries</div>
            <div class="stat-change negative">Reporting data</div>
        </div>
        """,
                    unsafe_allow_html=True)
    
    # Add spacing between stats and charts
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # Charts in connected white containers
    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Prosecutions by Crime Category Over Time</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Compares prosecution activity between rape and trafficking cases across years. This reveals how justice systems are allocating resources and which crime types are receiving more prosecutorial attention over time.
            </p>
        """, unsafe_allow_html=True)

        if len(filtered_prosecuted) > 0:
            category_yearly_pros = filtered_prosecuted.groupby(
                ['Year', 'Category']).size().reset_index(name='count')

            fig = px.bar(category_yearly_pros,
                         x='Year',
                         y='count',
                         color='Category',
                         barmode='group',
                         color_discrete_map={
                             'Rape': '#667eea',
                             'Trafficking in persons': '#ec4899'
                         })
            fig.update_layout(height=300,
                              margin=dict(l=40, r=20, t=10, b=100),
                              plot_bgcolor='white',
                              paper_bgcolor='white',
                              xaxis=dict(gridcolor='#cbd5e0', 
                                        tickfont=dict(color='#2d3748'),
                                        title=dict(text='Year', font=dict(color='#2d3748'))),
                              yaxis=dict(gridcolor='#cbd5e0', 
                                        tickfont=dict(color='#2d3748'),
                                        title=dict(text='Prosecution Records', font=dict(color='#2d3748'))),
                              legend=dict(
                                  orientation='h',
                                  yanchor='top',
                                  y=-0.35,
                                  xanchor='center',
                                  x=0.5,
                                  font=dict(color='#2d3748', size=8),
                                  title=dict(text='Crime Type', font=dict(color='#2d3748', size=8))))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Top 10 Countries by Prosecutions</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Ranks countries by total prosecution records, identifying nations with the most active prosecution efforts. Higher numbers indicate robust judicial systems actively pursuing serious crime cases.
            </p>
        """, unsafe_allow_html=True)

        if len(filtered_prosecuted) > 0:
            country_prosecution = filtered_prosecuted.groupby(
                'Country').size().reset_index(name='count')
            country_prosecution = country_prosecution.sort_values(
                'count', ascending=False).head(10)

            fig = go.Figure()
            fig.add_trace(
                go.Bar(y=country_prosecution['Country'],
                       x=country_prosecution['count'],
                       orientation='h',
                       marker=dict(color='#764ba2')))
            fig.update_layout(height=300,
                              margin=dict(l=150, r=20, t=10, b=40),
                              plot_bgcolor='white',
                              paper_bgcolor='white',
                              xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                              yaxis=dict(tickfont=dict(color='#2d3748')),
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Second row of charts
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Personnel Distribution by Type</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Shows the distribution of criminal justice personnel across different roles (Police, Judges, Prosecutors, etc.). This reveals the composition and structure of justice system workforce globally.
            </p>
        """, unsafe_allow_html=True)

        if len(filtered_personnel) > 0:
            group_counts = filtered_personnel.groupby(
                'Group').size().reset_index(name='count')
            group_counts = group_counts.sort_values('count', ascending=True)

            fig = go.Figure()
            fig.add_trace(
                go.Bar(y=group_counts['Group'],
                       x=group_counts['count'],
                       orientation='h',
                       marker=dict(color='#06b6d4')))
            fig.update_layout(height=300,
                              margin=dict(l=150, r=20, t=10, b=40),
                              plot_bgcolor='white',
                              paper_bgcolor='white',
                              xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                              yaxis=dict(tickfont=dict(color='#2d3748')),
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Regional Prosecution Distribution</h3>
            <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                Displays prosecution activity across world subregions. This geographic breakdown helps identify areas with strong judicial enforcement and regions where prosecution systems may be less developed or documented.
            </p>
        """, unsafe_allow_html=True)

        if len(filtered_prosecuted) > 0:
            subregion_pros = filtered_prosecuted.groupby(
                'Subregion').size().reset_index(name='count')
            subregion_pros = subregion_pros.sort_values('count', ascending=False).head(10)

            fig = go.Figure()
            fig.add_trace(
                go.Bar(x=subregion_pros['Subregion'],
                       y=subregion_pros['count'],
                       marker=dict(color='#ec4899')))
            fig.update_layout(height=300,
                              margin=dict(l=40, r=20, t=10, b=100),
                              plot_bgcolor='white',
                              paper_bgcolor='white',
                              xaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748'), tickangle=-45),
                              yaxis=dict(gridcolor='#cbd5e0', tickfont=dict(color='#2d3748')),
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # World map visualization - full width
    st.markdown("""
    <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h3 style="color: #000000; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Global Prosecution Activity Map</h3>
        <p style="color: #000000; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
            Interactive world map showing prosecution records by country. Darker colors indicate higher prosecution activity. Hover over countries to see specific data. This visualization reveals the global distribution of justice system enforcement efforts.
        </p>
    """, unsafe_allow_html=True)

    if len(filtered_prosecuted) > 0:
        country_map_data = filtered_prosecuted.groupby(
            'Country').size().reset_index(name='Prosecution Records')

        fig = px.choropleth(country_map_data,
                           locations='Country',
                           locationmode='country names',
                           color='Prosecution Records',
                           color_continuous_scale=[[0, '#a78bfa'], [0.5, '#7c3aed'], [1, '#4c1d95']],
                           labels={'Prosecution Records': 'Records'})
        fig.update_layout(height=500,
                          margin=dict(l=0, r=0, t=0, b=80),
                          paper_bgcolor='white',
                          geo=dict(showframe=False,
                                  showcoastlines=True,
                                  projection_type='natural earth',
                                  bgcolor='white'),
                          coloraxis_colorbar=dict(
                              orientation='h',
                              yanchor='top',
                              y=-0.15,
                              xanchor='center',
                              x=0.5,
                              thickness=15,
                              len=0.5,
                              tickfont=dict(color='#000000', size=10),
                              title=dict(text='Records', font=dict(color='#000000', size=10))))
        fig.update_traces(hovertemplate='<b>%{location}</b><br>Prosecution Records: %{z}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "🛡️ Safety & SDG Indicators":
    st.markdown("""
    <div style="background: white; border-radius: 12px !important; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 30px; overflow: hidden; border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;">
        <h2 style="color: #2d3748; font-size: 1.5rem; font-weight: 700; margin: 0 0 15px 0; text-align: center;">🛡️ Safety Perception & SDG Indicators</h2>
        <p style="color: #4a5568; font-size: 0.95rem; margin: 0; text-align: center; line-height: 1.6;">
            Explore UN Sustainable Development Goal indicators through interactive controls. Select an indicator, filter by year and gender, and dive deep into specific countries to analyze safety and crime data.
        </p>
    </div>
    """,
                unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)

    # Map SDG regions to our filter regions
    def map_sdg_region(sdg_region):
        """Map SDG regions to our standard region filter"""
        region_mapping = {
            'Sub-saharan Africa': 'Africa',
            'Northern Africa And Western Asia': 'Africa',
            'Latin America And The Caribbean': 'Americas',
            'Central And Southern Asia': 'Asia',
            'Eastern And South-eastern Asia': 'Asia',
            'Europe And Northern America': 'Europe',
            'Oceania': 'Oceania'
        }
        return region_mapping.get(sdg_region, None)

    # Add mapped region column
    sdg_safety_df['MappedRegion'] = sdg_safety_df['Region'].apply(
        map_sdg_region)

    # Filter SDG data by selected region
    if selected_region == 'All Regions':
        filtered_sdg = sdg_safety_df.copy()
    else:
        filtered_sdg = sdg_safety_df[sdg_safety_df['MappedRegion'] ==
                                     selected_region].copy()

    # INTERACTIVE CONTROLS SECTION
    col1, col2, col3 = st.columns(3)

    with col1:
        # SDG Indicator Selector
        indicator_options = {
            '📊 Intentional Homicide': 'intentional homicide',
            '🚨 Human Trafficking': 'trafficking',
            '🌃 Safety Perception': 'feel safe walking',
            '⚠️ Violence Prevalence': 'Prevalence rate',
            '👮 Police Reporting': 'Police reporting rate',
            '⚖️ Prison & Bribery': 'unsentenced|bribery'
        }
        selected_indicator = st.selectbox("Select SDG Indicator",
                                          options=list(
                                              indicator_options.keys()),
                                          key="sdg_indicator")

    with col2:
        # Year Range Filter
        if len(filtered_sdg) > 0:
            min_year = int(filtered_sdg['Year'].min())
            max_year = int(filtered_sdg['Year'].max())
            year_range = st.slider("Year Range",
                                   min_value=min_year,
                                   max_value=max_year,
                                   value=(min_year, max_year),
                                   key="sdg_year_range")
        else:
            year_range = (2000, 2023)

    with col3:
        # Gender Filter
        gender_options = ['All Genders', 'Male', 'Female', 'Both']
        selected_gender = st.selectbox("Gender Filter",
                                       options=gender_options,
                                       key="sdg_gender")

    # Additional filters row
    col1, col2 = st.columns(2)

    with col1:
        # Country selector
        if len(filtered_sdg) > 0:
            countries = ['All Countries'] + sorted(
                filtered_sdg['Geo'].unique().tolist())
            selected_country = st.selectbox(
                "Select Country (for detailed view)",
                options=countries,
                key="sdg_country")
        else:
            selected_country = 'All Countries'

    with col2:
        # Subregion selector
        if len(filtered_sdg) > 0:
            subregions = ['All Subregions'] + sorted([
                sr for sr in filtered_sdg['Subregion'].unique() if pd.notna(sr)
            ])
            selected_subregion = st.selectbox("Select Subregion",
                                              options=subregions,
                                              key="sdg_subregion")
        else:
            selected_subregion = 'All Subregions'

    # Apply all filters
    indicator_pattern = indicator_options[selected_indicator]
    analysis_data = filtered_sdg[filtered_sdg['Series'].str.contains(
        indicator_pattern, case=False, na=False, regex=True)].copy()

    # Apply year filter
    analysis_data = analysis_data[(analysis_data['Year'] >= year_range[0])
                                  & (analysis_data['Year'] <= year_range[1])]

    # Apply gender filter
    if selected_gender != 'All Genders':
        analysis_data = analysis_data[analysis_data['Sex'] == selected_gender]

    # Apply country filter
    if selected_country != 'All Countries':
        analysis_data = analysis_data[analysis_data['Geo'] == selected_country]

    # Apply subregion filter
    if selected_subregion != 'All Subregions':
        analysis_data = analysis_data[analysis_data['Subregion'] ==
                                      selected_subregion]

    # Display filtered statistics
    st.markdown("""
    <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
        <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 15px 0; text-align: center;">📊 Filtered Data Summary</h3>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 0 10px;">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-number">{len(analysis_data):,}</p>
            <p class="stat-label">Records Found</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        unique_years = len(
            analysis_data['Year'].unique()) if len(analysis_data) > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-number">{unique_years}</p>
            <p class="stat-label">Years Covered</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        unique_countries = len(
            analysis_data['Geo'].unique()) if len(analysis_data) > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-number">{unique_countries}</p>
            <p class="stat-label">Countries</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col4:
        unique_series = len(
            analysis_data['Series'].unique()) if len(analysis_data) > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-number">{unique_series}</p>
            <p class="stat-label">Indicators</p>
        </div>
        """,
                    unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close padding div
    st.markdown('</div>', unsafe_allow_html=True)  # Close statistics container

    # Show visualizations if data available
    if len(analysis_data) == 0:
        st.warning(
            "⚠️ No data available for the selected filters. Try adjusting your filter selections."
        )
    else:
        # Dynamic visualizations based on selected indicator

        # Intentional Homicide visualizations
        if selected_indicator == "📊 Intentional Homicide":
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.3rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">📊 Intentional Homicide Rates Analysis</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 20px 0; text-align: center;">
                    Tracking homicide victimization rates to monitor SDG 16.1 (reduce violence and death rates)
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="large")

            with col1:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Trend Over Time by Gender</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                        <strong>What it shows:</strong> This line chart displays how homicide data reporting varies by gender (Male, Female, Both) across years.<br>
                        <strong>Purpose:</strong> Helps identify reporting patterns, gender gaps in data collection, and changes in data availability over time to assess the completeness of gender-disaggregated statistics.
                    </p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    yearly_gender = analysis_data.groupby(
                        ['Year', 'Sex']).size().reset_index(name='Records')
                    fig = px.line(yearly_gender,
                                  x='Year',
                                  y='Records',
                                  color='Sex',
                                  color_discrete_map={
                                      'Male': '#10b981',
                                      'Female': '#ef4444',
                                      'Both': '#f59e0b'
                                  },
                                  markers=True)
                    fig.update_traces(line=dict(width=3), marker=dict(size=8))
                    fig.update_layout(height=300,
                                      margin=dict(l=30, r=30, t=20, b=80),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      yaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      xaxis=dict(title=dict(text='Year', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Top 10 Countries</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                        <strong>What it shows:</strong> Horizontal bar chart ranking the top 10 countries by number of homicide data records submitted.<br>
                        <strong>Purpose:</strong> Identifies which countries are most active in reporting homicide statistics, indicating strong data collection systems and transparency in crime reporting.
                    </p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    country_counts = analysis_data.groupby(
                        'Geo').size().reset_index(name='Records')
                    country_counts = country_counts.sort_values(
                        'Records', ascending=False).head(10)
                    fig = go.Figure()
                    fig.add_trace(
                        go.Bar(y=country_counts['Geo'][::-1],
                               x=country_counts['Records'][::-1],
                               orientation='h',
                               marker=dict(color='#553c9a')))
                    fig.update_layout(height=300,
                                      margin=dict(l=10, r=30, t=0, b=0),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      xaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      yaxis=dict(title=dict(text='Country', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Regional Comparison</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                    <strong>What it shows:</strong> Gradient bar chart comparing homicide data records across global regions (Europe, Americas, Africa, Asia, Oceania).<br>
                    <strong>Purpose:</strong> Reveals regional disparities in data reporting capacity and helps identify areas that may need support in strengthening their crime statistics infrastructure.
                </p>
            """, unsafe_allow_html=True)

            if len(analysis_data) > 0:
                regional_data = analysis_data.groupby(
                    'Region').size().reset_index(name='Records')
                regional_data = regional_data.sort_values('Records',
                                                          ascending=True)
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(y=regional_data['Region'],
                           x=regional_data['Records'],
                           orientation='h',
                           marker=dict(color=regional_data['Records'],
                                      colorscale=[[0, '#764ba2'], [0.5, '#667eea'], [1, '#4c51bf']],
                                      showscale=False)))
                fig.update_layout(height=300,
                                  margin=dict(l=30, r=30, t=20, b=80),
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  showlegend=False,
                                  xaxis=dict(gridcolor='#e2e8f0',
                                            title=dict(text='Data Records', font=dict(color='#000000')),
                                            tickfont=dict(color='#000000')),
                                  yaxis=dict(title=dict(text='Region', font=dict(color='#000000')),
                                            tickfont=dict(color='#000000')))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No regional data available")
            st.markdown('</div>', unsafe_allow_html=True)

        # Human Trafficking visualizations
        elif selected_indicator == "🚨 Human Trafficking":
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.3rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">🚨 Human Trafficking Victims Analysis</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 20px 0; text-align: center;">
                    Monitoring trafficking victim rates to support SDG 16.2 (end trafficking and exploitation)
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="large")

            with col1:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Yearly Trends</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                        <strong>What it shows:</strong> Area chart showing the volume of trafficking victim data reports submitted each year.<br>
                        <strong>Purpose:</strong> Tracks improvements in trafficking detection and reporting systems over time, helping assess whether countries are enhancing their anti-trafficking efforts.
                    </p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    yearly_data = analysis_data.groupby(
                        'Year').size().reset_index(name='Records')
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(x=yearly_data['Year'],
                                   y=yearly_data['Records'],
                                   mode='lines+markers',
                                   fill='tozeroy',
                                   line=dict(color='#c53030', width=3),
                                   marker=dict(size=8, color='#c53030'),
                                   fillcolor='rgba(197, 48, 48, 0.2)'))
                    fig.update_layout(height=280,
                                      margin=dict(l=40, r=60, t=10, b=10),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      yaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      xaxis=dict(title=dict(text='Year', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')),
                                      showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Gender Breakdown</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                        <strong>What it shows:</strong> Pie chart displaying the proportion of trafficking data records by gender category (Male, Female, Both).<br>
                        <strong>Purpose:</strong> Reveals gender dimensions in trafficking reporting and helps identify which populations are most represented in trafficking victim data.
                    </p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    gender_data = analysis_data.groupby(
                        'Sex').size().reset_index(name='Records')
                    fig = px.pie(
                        gender_data,
                        values='Records',
                        names='Sex',
                        color_discrete_sequence=px.colors.sequential.Purples_r)
                    fig.update_layout(height=280,
                                      margin=dict(l=40, r=100, t=20, b=80),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      font=dict(color='#000000'),
                                      legend=dict(
                                          orientation='h',
                                          yanchor='top',
                                          y=-0.15,
                                          xanchor='center',
                                          x=0.5,
                                          font=dict(color='#000000', size=8)))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Country Comparison</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                    <strong>What it shows:</strong> Vertical bar chart ranking the top 15 countries by volume of trafficking victim data reports.<br>
                    <strong>Purpose:</strong> Identifies which nations have the most comprehensive trafficking data collection, potentially indicating strong detection systems or high trafficking prevalence.
                </p>
            """, unsafe_allow_html=True)

            if len(analysis_data) > 0:
                country_data = analysis_data.groupby('Geo').size().reset_index(
                    name='Records')
                country_data = country_data.sort_values(
                    'Records', ascending=False).head(15)
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(x=country_data['Geo'],
                           y=country_data['Records'],
                           marker=dict(color='#4c51bf')))
                fig.update_layout(height=300,
                                  margin=dict(l=20, r=50, t=0, b=0),
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  yaxis=dict(gridcolor='#e2e8f0',
                                             title=dict(text='Data Records', font=dict(color='#000000')),
                                             tickfont=dict(color='#000000')),
                                  xaxis=dict(tickangle=-45,
                                            title=dict(text='Country', font=dict(color='#000000')),
                                            tickfont=dict(color='#000000')))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No country data available")
            st.markdown('</div>', unsafe_allow_html=True)

        # Safety Perception visualizations
        elif selected_indicator == "🌃 Safety Perception":
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.3rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">🌃 Perception of Safety Analysis</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 20px 0; text-align: center;">
                    Proportion of population feeling safe walking alone, supporting SDG 11.7 (safe, inclusive public spaces)
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="large")

            with col1:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Trends Over Years</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                        <strong>What it shows:</strong> Bar chart showing how many countries reported safety perception data each year.<br>
                        <strong>Purpose:</strong> Monitors the growth in data collection on public safety perceptions, crucial for measuring SDG 11.7 progress on safe and inclusive public spaces.
                    </p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    yearly_data = analysis_data.groupby(
                        'Year').size().reset_index(name='Records')
                    fig = px.bar(yearly_data,
                                 x='Year',
                                 y='Records',
                                 color_discrete_sequence=['#4c51bf'])
                    fig.update_layout(height=280,
                                      margin=dict(l=40, r=60, t=10, b=10),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      yaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      xaxis=dict(title=dict(text='Year', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Gender Comparison</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                        <strong>What it shows:</strong> Bar chart comparing the number of safety perception data records by gender category.<br>
                        <strong>Purpose:</strong> Examines whether safety perception data adequately captures both male and female perspectives, essential for understanding gender differences in feeling safe.
                    </p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    gender_data = analysis_data.groupby(
                        'Sex').size().reset_index(name='Records')
                    fig = px.bar(gender_data,
                                 x='Sex',
                                 y='Records',
                                 color='Sex',
                                 color_discrete_map={
                                     'Male': '#4c51bf',
                                     'Female': '#c53030',
                                     'Both': '#553c9a'
                                 })
                    fig.update_layout(height=280,
                                      margin=dict(l=40, r=60, t=10, b=10),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      yaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      xaxis=dict(title=dict(text='Gender', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')),
                                      showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Country Rankings</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                    <strong>What it shows:</strong> Horizontal gradient bar chart ranking the top 15 countries by safety perception data volume.<br>
                    <strong>Purpose:</strong> Highlights countries leading in measuring public safety perceptions, providing benchmark data for SDG 11.7 on creating safe, inclusive, and accessible public spaces.
                </p>
            """, unsafe_allow_html=True)

            if len(analysis_data) > 0:
                country_data = analysis_data.groupby('Geo').size().reset_index(
                    name='Records')
                country_data = country_data.sort_values(
                    'Records', ascending=True).tail(15)
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(y=country_data['Geo'],
                           x=country_data['Records'],
                           orientation='h',
                           marker=dict(color=country_data['Records'],
                                       colorscale=[[0, '#764ba2'], [0.5, '#667eea'], [1, '#4c51bf']],
                                       showscale=False)))
                fig.update_layout(height=400,
                                  margin=dict(l=30, r=30, t=20, b=80),
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  xaxis=dict(gridcolor='#e2e8f0',
                                             title=dict(text='Data Records', font=dict(color='#000000')),
                                             tickfont=dict(color='#000000')),
                                  yaxis=dict(title=dict(text='Country', font=dict(color='#000000')),
                                            tickfont=dict(color='#000000')))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No country data available")
            st.markdown('</div>', unsafe_allow_html=True)

        # Violence Prevalence visualizations
        elif selected_indicator == "⚠️ Violence Prevalence":
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.3rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">⚠️ Violence and Harassment Prevalence</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 20px 0; text-align: center;">
                    Tracking different types of violence to support SDG 16.1 and 11.7 (reduce violence, ensure safe spaces)
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if len(analysis_data) > 0:
                violence_types = [
                    'physical assault', 'sexual assault', 'sexual violence',
                    'psychological violence', 'harassment', 'robbery'
                ]

                def extract_violence_type(series_name):
                    for vtype in violence_types:
                        if vtype in series_name.lower():
                            return vtype.title()
                    return 'Other'

                analysis_data_copy = analysis_data.copy()
                analysis_data_copy['ViolenceType'] = analysis_data_copy[
                    'Series'].apply(extract_violence_type)

            col1, col2 = st.columns(2, gap="large")

            with col1:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Violence Types Comparison</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                        Distribution of data across different violence categories
                    </p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    type_data = analysis_data_copy.groupby(
                        'ViolenceType').size().reset_index(name='Records')
                    type_data = type_data.sort_values('Records',
                                                      ascending=True)
                    fig = px.bar(type_data,
                                 x='Records',
                                 y='ViolenceType',
                                 orientation='h',
                                 color='Records',
                                 color_continuous_scale=[[0, '#764ba2'], [0.5, '#667eea'], [1, '#4c51bf']])
                    fig.update_layout(height=350,
                                      margin=dict(l=30, r=30, t=20, b=100),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      xaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      yaxis=dict(title=dict(text='Violence Type', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')),
                                      coloraxis_colorbar=dict(
                                          orientation='h',
                                          yanchor='top',
                                          y=-0.3,
                                          xanchor='center',
                                          x=0.5,
                                          thickness=15,
                                          len=0.5,
                                          title=dict(text='Records', font=dict(color='#000000', size=10)),
                                          tickfont=dict(color='#000000', size=10)),
                                      showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Trends by Violence Type</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                        How reporting for different violence types has evolved over time
                    </p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    yearly_type = analysis_data_copy.groupby(
                        ['Year',
                         'ViolenceType']).size().reset_index(name='Records')
                    fig = px.line(
                        yearly_type,
                        x='Year',
                        y='Records',
                        color='ViolenceType',
                        markers=True,
                        color_discrete_sequence=['#c53030', '#4c51bf', '#d69e2e', '#38a169', '#805ad5', '#dd6b20'])
                    fig.update_traces(line=dict(width=3), marker=dict(size=8))
                    fig.update_layout(height=350,
                                      margin=dict(l=0, r=120, t=0, b=80),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      yaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      xaxis=dict(title=dict(text='Year', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')),
                                      legend=dict(
                                          orientation='h',
                                          yanchor='top',
                                          y=-0.25,
                                          xanchor='center',
                                          x=0.5,
                                          font=dict(color='#000000', size=8),
                                          title=dict(font=dict(color='#000000', size=8))))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Gender Breakdown by Type</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 15px 0; text-align: center;">
                    Gender-specific distribution across different types of violence
                </p>
            """, unsafe_allow_html=True)

            if len(analysis_data) > 0:
                gender_type = analysis_data_copy.groupby(
                    ['ViolenceType', 'Sex']).size().reset_index(name='Records')
                fig = px.bar(gender_type,
                             x='ViolenceType',
                             y='Records',
                             color='Sex',
                             barmode='group',
                             color_discrete_map={
                                 'Male': '#4c51bf',
                                 'Female': '#c53030',
                                 'Both': '#553c9a'
                             })
                fig.update_layout(height=300,
                                  margin=dict(l=30, r=30, t=20, b=120),
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  yaxis=dict(gridcolor='#e2e8f0',
                                             title=dict(text='Data Records', font=dict(color='#000000')),
                                             tickfont=dict(color='#000000')),
                                  xaxis=dict(tickangle=-45,
                                            title=dict(text='Violence Type', font=dict(color='#000000')),
                                            tickfont=dict(color='#000000')),
                                  legend=dict(
                                      orientation='h',
                                      yanchor='top',
                                      y=-0.45,
                                      xanchor='center',
                                      x=0.5,
                                      font=dict(color='#000000', size=8),
                                      title=dict(font=dict(color='#000000', size=8))))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for this view")
            st.markdown('</div>', unsafe_allow_html=True)

        # Police Reporting visualizations
        elif selected_indicator == "👮 Police Reporting":
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.3rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">👮 Police Reporting Rates Analysis</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 20px 0; text-align: center;">
                    Percentage of crime victims who report incidents, indicating trust in law enforcement
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if len(analysis_data) > 0:

                def extract_crime_type(series_name):
                    if 'physical assault' in series_name.lower():
                        return 'Physical Assault'
                    elif 'sexual assault' in series_name.lower():
                        return 'Sexual Assault'
                    elif 'sexual violence' in series_name.lower():
                        return 'Sexual Violence'
                    elif 'physical violence' in series_name.lower():
                        return 'Physical Violence'
                    elif 'robbery' in series_name.lower():
                        return 'Robbery'
                    return 'Other'

                analysis_data_copy = analysis_data.copy()
                analysis_data_copy['CrimeType'] = analysis_data_copy[
                    'Series'].apply(extract_crime_type)

            col1, col2 = st.columns(2, gap="large")

            with col1:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Reporting Rates by Crime Type</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 8px 0; text-align: center;">
                        Distribution of police reporting data across different crime types
                    </p>
                    <p style="color: #4a5568; font-size: 0.85rem; margin: 0 0 5px 0;"><strong>What it shows:</strong> The proportion of data available for each crime category in police reporting statistics.</p>
                    <p style="color: #4a5568; font-size: 0.85rem; margin: 0;"><strong>Purpose:</strong> Identifies which crimes have the most comprehensive reporting data and helps understand data coverage gaps across different crime types.</p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    crime_data = analysis_data_copy.groupby(
                        'CrimeType').size().reset_index(name='Records')
                    crime_data = crime_data.sort_values('Records',
                                                        ascending=False)
                    fig = px.pie(
                        crime_data,
                        values='Records',
                        names='CrimeType',
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        hole=0.4)
                    fig.update_layout(height=350,
                                      margin=dict(l=30, r=30, t=20, b=80),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      font=dict(color='#000000'),
                                      legend=dict(
                                          orientation='h',
                                          yanchor='top',
                                          y=-0.25,
                                          xanchor='center',
                                          x=0.5,
                                          font=dict(color='#000000', size=8),
                                          title=dict(font=dict(color='#000000', size=8))))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Gender Comparison</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 8px 0; text-align: center;">
                        Police reporting data by crime type and gender
                    </p>
                    <p style="color: #4a5568; font-size: 0.85rem; margin: 0 0 5px 0;"><strong>What it shows:</strong> Comparison of police reporting data between male and female victims across different crime categories.</p>
                    <p style="color: #4a5568; font-size: 0.85rem; margin: 0;"><strong>Purpose:</strong> Reveals gender-specific patterns in crime reporting and helps identify which crimes disproportionately affect different genders.</p>
                """, unsafe_allow_html=True)

                if len(analysis_data) > 0:
                    gender_crime = analysis_data_copy.groupby(
                        ['CrimeType',
                         'Sex']).size().reset_index(name='Records')
                    fig = px.bar(gender_crime,
                                 x='CrimeType',
                                 y='Records',
                                 color='Sex',
                                 barmode='group',
                                 color_discrete_map={
                                     'Male': '#4c51bf',
                                     'Female': '#c53030',
                                     'Both': '#553c9a'
                                 })
                    fig.update_layout(height=350,
                                      margin=dict(l=30, r=30, t=20, b=120),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      yaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      xaxis=dict(tickangle=-45,
                                                title=dict(text='Crime Type', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')),
                                      legend=dict(
                                          orientation='h',
                                          yanchor='top',
                                          y=-0.45,
                                          xanchor='center',
                                          x=0.5,
                                          font=dict(color='#000000', size=8),
                                          title=dict(font=dict(color='#000000', size=8))))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for this view")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Trends Over Time</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 8px 0; text-align: center;">
                    How police reporting data has evolved over time by crime type
                </p>
                <p style="color: #4a5568; font-size: 0.85rem; margin: 0 0 5px 0;"><strong>What it shows:</strong> Yearly trends in the volume of police reporting data for each crime category from past years to present.</p>
                <p style="color: #4a5568; font-size: 0.85rem; margin: 0 0 15px 0;"><strong>Purpose:</strong> Tracks how data collection efforts have changed over time and identifies emerging or declining trends in crime reporting for different categories.</p>
            """, unsafe_allow_html=True)

            if len(analysis_data) > 0:
                yearly_crime = analysis_data_copy.groupby(
                    ['Year', 'CrimeType']).size().reset_index(name='Records')
                fig = px.line(
                    yearly_crime,
                    x='Year',
                    y='Records',
                    color='CrimeType',
                    markers=True,
                    color_discrete_sequence=['#c53030', '#4c51bf', '#d69e2e', '#38a169', '#805ad5', '#dd6b20'])
                fig.update_traces(line=dict(width=3), marker=dict(size=8))
                fig.update_layout(height=300,
                                  margin=dict(l=30, r=30, t=20, b=80),
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  yaxis=dict(gridcolor='#e2e8f0',
                                             title=dict(text='Data Records', font=dict(color='#000000')),
                                             tickfont=dict(color='#000000')),
                                  xaxis=dict(title=dict(text='Year', font=dict(color='#000000')),
                                            tickfont=dict(color='#000000')),
                                  legend=dict(
                                      orientation='h',
                                      yanchor='top',
                                      y=-0.2,
                                      xanchor='center',
                                      x=0.5,
                                      font=dict(color='#000000', size=8),
                                      title=dict(font=dict(color='#000000', size=8))))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for this view")
            st.markdown('</div>', unsafe_allow_html=True)

        # Prison & Bribery visualizations
        elif selected_indicator == "⚖️ Prison & Bribery":
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.3rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">⚖️ Prison Statistics & Bribery Prevalence</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 20px 0; text-align: center;">
                    Unsentenced prisoner rates and bribery prevalence, supporting SDG 16 (peaceful and inclusive societies)
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="large")

            with col1:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Prison Data Trends</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 8px 0; text-align: center;">
                        Unsentenced prisoner data reporting trends over time
                    </p>
                    <p style="color: #4a5568; font-size: 0.85rem; margin: 0 0 5px 0;"><strong>What it shows:</strong> The number of data records about unsentenced prisoners collected each year.</p>
                    <p style="color: #4a5568; font-size: 0.85rem; margin: 0;"><strong>Purpose:</strong> Tracks transparency and data availability about pretrial detention, a key indicator of justice system efficiency and human rights.</p>
                """, unsafe_allow_html=True)

                prison_data = analysis_data[
                    analysis_data['Series'].str.contains('unsentenced',
                                                         case=False,
                                                         na=False)]
                if len(prison_data) > 0:
                    yearly_prison = prison_data.groupby(
                        'Year').size().reset_index(name='Records')
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(x=yearly_prison['Year'],
                                   y=yearly_prison['Records'],
                                   mode='lines+markers',
                                   line=dict(color='#4c51bf', width=3),
                                   marker=dict(size=10, color='#553c9a')))
                    fig.update_layout(height=300,
                                      margin=dict(l=30, r=30, t=20, b=30),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      yaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      xaxis=dict(title=dict(text='Year', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')),
                                      showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No prison data available")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                    <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Bribery Prevalence</h3>
                    <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 8px 0; text-align: center;">
                        Bribery data reporting trends across years
                    </p>
                    <p style="color: #4a5568; font-size: 0.85rem; margin: 0 0 5px 0;"><strong>What it shows:</strong> Annual volume of data records about bribery incidents and prevalence.</p>
                    <p style="color: #4a5568; font-size: 0.85rem; margin: 0;"><strong>Purpose:</strong> Monitors corruption transparency and anti-corruption data collection efforts, supporting SDG 16 goals for accountable institutions.</p>
                """, unsafe_allow_html=True)

                bribery_data = analysis_data[
                    analysis_data['Series'].str.contains('bribery',
                                                         case=False,
                                                         na=False)]
                if len(bribery_data) > 0:
                    yearly_bribery = bribery_data.groupby(
                        'Year').size().reset_index(name='Records')
                    fig = px.area(yearly_bribery,
                                  x='Year',
                                  y='Records',
                                  color_discrete_sequence=['#c53030'])
                    fig.update_layout(height=300,
                                      margin=dict(l=30, r=30, t=20, b=30),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      yaxis=dict(gridcolor='#e2e8f0',
                                                 title=dict(text='Data Records', font=dict(color='#000000')),
                                                 tickfont=dict(color='#000000')),
                                      xaxis=dict(title=dict(text='Year', font=dict(color='#000000')),
                                                tickfont=dict(color='#000000')))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No bribery data available")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden;">
                <h3 style="color: #2d3748; font-size: 1.2rem; font-weight: 600; margin: 0 0 10px 0; text-align: center;">Regional Comparison</h3>
                <p style="color: #4a5568; font-size: 0.9rem; margin: 0 0 8px 0; text-align: center;">
                    Distribution of prison and bribery data across different regions
                </p>
                <p style="color: #4a5568; font-size: 0.85rem; margin: 0 0 5px 0;"><strong>What it shows:</strong> The volume of prison and bribery data reported from different geographic regions worldwide.</p>
                <p style="color: #4a5568; font-size: 0.85rem; margin: 0 0 15px 0;"><strong>Purpose:</strong> Identifies which regions have better data transparency about justice systems and corruption, revealing global patterns in governance monitoring.</p>
            """, unsafe_allow_html=True)

            if len(analysis_data) > 0:
                regional_data = analysis_data.groupby(
                    'Region').size().reset_index(name='Records')
                regional_data = regional_data.sort_values('Records',
                                                          ascending=True)
                fig = px.bar(regional_data,
                             x='Records',
                             y='Region',
                             orientation='h',
                             color='Records',
                             color_continuous_scale=[[0, '#764ba2'], [0.5, '#667eea'], [1, '#4c51bf']])
                fig.update_layout(height=300,
                                  margin=dict(l=30, r=30, t=20, b=100),
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  xaxis=dict(gridcolor='#e2e8f0',
                                             title=dict(text='Data Records', font=dict(color='#000000')),
                                             tickfont=dict(color='#000000')),
                                  yaxis=dict(title=dict(text='Region', font=dict(color='#000000')),
                                            tickfont=dict(color='#000000')),
                                  coloraxis_colorbar=dict(
                                      orientation='h',
                                      yanchor='top',
                                      y=-0.35,
                                      xanchor='center',
                                      x=0.5,
                                      thickness=15,
                                      len=0.5,
                                      title=dict(text='Records', font=dict(color='#000000', size=10)),
                                      tickfont=dict(color='#000000', size=10)),
                                  showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No regional data available")
            st.markdown('</div>', unsafe_allow_html=True)

        # Summary insights card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-top: 30px;">
            <h4 style="color: white; font-size: 1.2rem; font-weight: 600; margin-bottom: 15px;">📋 Key Insights About {selected_indicator}</h4>
            <p style="color: white; line-height: 1.8; font-size: 0.95rem; margin: 0;">
                The visualizations above show data reporting patterns for the selected indicator across different dimensions.
                Use the filters to explore specific countries, time periods, and demographic breakdowns to better understand
                reporting coverage and trends in your area of interest.
            </p>
        </div>
        """,
                    unsafe_allow_html=True)
