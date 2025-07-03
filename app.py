"""
F1 Data Analytics Dashboard

Main Streamlit application for F1 data analysis using FastF1 library.
Provides interactive analysis of F1 sessions including Race, Sprint, Qualifying, and Practice sessions.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import our custom modules
from data_fetcher import f1_fetcher
from data_processor import f1_processor
from visualizations import f1_visualizer
from utils import (
    get_session_type_options, get_session_type_display_name,
    format_lap_time, create_summary_metrics, display_no_data_message,
    validate_year_selection, get_available_years_range
)

# Page configuration
st.set_page_config(
    page_title="F1 Data Analytics Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load custom CSS styles."""
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Initialize session state
if 'session_data' not in st.session_state:
    st.session_state.session_data = None
if 'insights' not in st.session_state:
    st.session_state.insights = None
if 'selected_drivers' not in st.session_state:
    st.session_state.selected_drivers = []

def main():
    """Main application function."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏎️ F1 Data Analytics Dashboard</h1>
        <p>Comprehensive Formula 1 session analysis powered by FastF1</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("### 📊 Session Selection")
        
        # Session type selection
        session_options = get_session_type_options()
        session_type = st.selectbox(
            "Select Session Type",
            options=[opt[0] for opt in session_options],
            format_func=lambda x: get_session_type_display_name(x),
            help="Choose the type of F1 session to analyze"
        )
        
        # Year selection
        start_year, end_year = get_available_years_range()
        selected_year = st.selectbox(
            "Select Year",
            options=list(range(start_year, end_year + 1)),
            index=len(list(range(start_year, end_year + 1))) - 1,  # Default to current year
            help="Select the year for the F1 season"
        )
        
        # Event selection
        if selected_year:
            events = f1_fetcher.get_events_for_year(selected_year)
            if events:
                event_names = [event['name'] for event in events]
                selected_event = st.selectbox(
                    "Select Event",
                    options=event_names,
                    help="Choose the specific F1 event/race"
                )
            else:
                st.error("No events found for the selected year")
                return
        else:
            st.error("Please select a year")
            return
        
        # Load data button
        if st.button("🚀 Load Session Data", type="primary"):
            load_session_data(selected_year, selected_event, session_type)
        
        # Driver selection (if data is loaded)
        if st.session_state.session_data and st.session_state.session_data.get('laps') is not None:
            st.markdown("### 👥 Driver Selection")
            laps_data = st.session_state.session_data['laps']
            if not laps_data.empty:
                available_drivers = sorted(laps_data['Driver'].unique())
                selected_drivers = st.multiselect(
                    "Select Drivers for Analysis",
                    options=available_drivers,
                    default=available_drivers[:5] if len(available_drivers) > 5 else available_drivers,
                    help="Choose specific drivers to focus on in the analysis"
                )
                st.session_state.selected_drivers = selected_drivers
    
    # Main content area
    if st.session_state.session_data is None:
        display_welcome_screen()
    else:
        display_dashboard()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            <p>🏎️ F1 Data Analytics Dashboard | Powered by FastF1 | Data provided by Formula 1</p>
            <p>Built with ❤️ using Streamlit and Python</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_welcome_screen():
    """Display welcome screen with instructions."""
    st.markdown("""
    ## 🎯 Welcome to F1 Data Analytics Dashboard
    
    This application provides comprehensive analysis of Formula 1 sessions using official F1 data.
    
    ### 📋 How to Use:
    1. **Select Session Type**: Choose from Race, Sprint Race, Qualifying, or Practice sessions
    2. **Choose Year**: Select the F1 season year (2018 onwards)
    3. **Pick Event**: Select the specific race/event from the dropdown
    4. **Load Data**: Click the "Load Session Data" button to fetch and analyze data
    
    ### 📊 Available Analysis:
    - **Lap Time Analysis**: Compare lap times across drivers and sessions
    - **Driver Performance**: Detailed driver statistics and consistency metrics
    - **Position Changes**: Track position changes throughout the session
    - **Sector Analysis**: Break down performance by track sectors
    - **Tire Strategy**: Analyze tire compound usage and stint lengths
    - **Speed Analysis**: Visualize speed patterns on track maps
    
    ### 🚀 Features:
    - **Real-time Data**: No local caching required - fresh data every time
    - **Interactive Charts**: Zoom, pan, and hover for detailed insights
    - **Comprehensive Metrics**: Advanced analytics and feature engineering
    - **User-friendly Interface**: Intuitive controls and beautiful visualizations
    
    ---
    
    **Ready to start?** Use the sidebar to select your session and click "Load Session Data"!
    """)

def load_session_data(year: int, event_name: str, session_type: str):
    """Load session data from FastF1."""
    try:
        with st.spinner(f"Fetching {get_session_type_display_name(session_type)} data for {event_name} {year}..."):
            # Fetch session data
            session_data = f1_fetcher.get_session_data(year, event_name, session_type)
            
            if session_data and session_data.get('laps') is not None and not session_data['laps'].empty:
                # Fetch additional data
                tire_data = f1_fetcher.get_tire_data(year, event_name, session_type)
                driver_info = f1_fetcher.get_driver_info(year, event_name, session_type)
                
                # Add additional data to session_data
                session_data['tire_data'] = tire_data
                session_data['driver_info'] = driver_info
                
                # Store session info for dashboard header
                session_data['session_type'] = session_type
                session_data['event_name'] = event_name
                session_data['year'] = year
                
                # Process data and create insights
                insights = f1_processor.create_session_insights(session_data)
                
                # Store in session state
                st.session_state.session_data = session_data
                st.session_state.insights = insights
                
                st.success(f"✅ Successfully loaded {get_session_type_display_name(session_type)} data!")
                st.rerun()
            else:
                display_no_data_message(session_type, event_name, year)
                
    except Exception as e:
        st.error(f"❌ Error loading session data: {str(e)}")
        st.info("💡 Tip: Make sure you have a stable internet connection and the selected session exists.")

def display_dashboard():
    """Display the main dashboard with all visualizations."""
    
    # Get session data and insights
    session_data = st.session_state.session_data
    insights = st.session_state.insights
    
    if not session_data or not insights:
        st.error("No session data available. Please load data first.")
        return
    
    # Session info header
    session_type = session_data.get('session_type', 'Unknown')
    event_name = session_data.get('event_name', 'Unknown')
    year = session_data.get('year', 'Unknown')
    
    st.markdown(f"""
    <h2>📊 {get_session_type_display_name(session_type)} Analysis - {event_name} {year}</h2>
    """, unsafe_allow_html=True)
    
    # Summary metrics
    display_summary_metrics(insights)
    
    # Main visualizations
    display_main_visualizations(session_data, insights)
    
    # Detailed analysis tabs
    display_detailed_analysis(session_data, insights)

def display_summary_metrics(insights: dict):
    """Display summary metrics at the top of the dashboard."""
    st.markdown("### 📈 Session Overview")
    
    summary = create_summary_metrics(insights)
    
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{summary.get('fastest_lap', 'N/A')}</div>
                <div class="metric-label">Fastest Lap</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{summary.get('average_lap', 'N/A')}</div>
                <div class="metric-label">Average Lap</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_drivers', 'N/A')}</div>
                <div class="metric-label">Total Drivers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{summary.get('lap_time_std', 'N/A')}</div>
                <div class="metric-label">Lap Time Std</div>
            </div>
            """, unsafe_allow_html=True)

def display_main_visualizations(session_data: dict, insights: dict):
    """Display main visualization charts."""
    st.markdown("### 📊 Performance Analysis")
    
    # Get selected drivers for filtering
    selected_drivers = st.session_state.selected_drivers
    
    # Clean lap data before plotting
    cleaned_laps = f1_processor.clean_lap_data(session_data['laps']) if session_data.get('laps') is not None else None
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["🏁 Lap Times", "📈 Positions", "⚡ Sectors", "🔄 Consistency"])
    
    with tab1:
        if cleaned_laps is not None and not cleaned_laps.empty:
            fig = f1_visualizer.create_lap_time_comparison(
                cleaned_laps, 
                selected_drivers if selected_drivers else None
            )
            st.plotly_chart(fig, use_container_width=True, key="lap_times_chart")
    
    with tab2:
        if cleaned_laps is not None and not cleaned_laps.empty:
            fig = f1_visualizer.create_position_changes(
                cleaned_laps,
                selected_drivers if selected_drivers else None
            )
            st.plotly_chart(fig, use_container_width=True, key="positions_chart")
    
    with tab3:
        if cleaned_laps is not None and not cleaned_laps.empty:
            fig = f1_visualizer.create_sector_analysis(
                cleaned_laps,
                selected_drivers if selected_drivers else None
            )
            st.plotly_chart(fig, use_container_width=True, key="sectors_chart")
    
    with tab4:
        if cleaned_laps is not None and not cleaned_laps.empty:
            fig = f1_visualizer.create_consistency_heatmap(cleaned_laps)
            st.plotly_chart(fig, use_container_width=True, key="consistency_chart")

def display_detailed_analysis(session_data: dict, insights: dict):
    """Display detailed analysis in tabs."""
    st.markdown("### 🔍 Detailed Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Driver Performance", "🛞 Tire Strategy", "📊 Speed Analysis", "📥 Data Export"])
    
    with tab1:
        display_driver_performance(insights)
    
    with tab2:
        display_tire_strategy(session_data, insights)
    
    with tab3:
        display_speed_analysis(session_data)
    
    with tab4:
        display_data_export(session_data, insights)

def display_driver_performance(insights: dict):
    """Display driver performance analysis."""
    if 'driver_summary' in insights and not insights['driver_summary'].empty:
        driver_summary = insights['driver_summary']
        
        # Driver performance chart
        fig = f1_visualizer.create_driver_performance_summary(driver_summary)
        st.plotly_chart(fig, use_container_width=True, key="driver_performance_chart")
        
        # Driver summary table
        st.markdown("### 📋 Driver Summary Table")
        # Show DNF as Yes/No in the table
        driver_summary_display = driver_summary.copy()
        if 'DNF' in driver_summary_display.columns:
            driver_summary_display['DNF'] = driver_summary_display['DNF'].apply(lambda x: 'Yes' if x else 'No')
        st.dataframe(
            driver_summary_display.round(3),
            use_container_width=True,
            hide_index=True
        )
        
        # Individual driver analysis
        st.markdown("### 🎯 Individual Driver Analysis")
        selected_driver = st.selectbox(
            "Select Driver for Detailed Analysis",
            options=driver_summary['Driver'].tolist()
        )
        
        if selected_driver:
            driver_stats = driver_summary[driver_summary['Driver'] == selected_driver].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                dnf_status = "<span style='color:red;font-weight:bold;'>DNF</span>" if driver_stats.get('DNF', False) else "<span style='color:green;font-weight:bold;'>Finished</span>"
                st.markdown(f"""
                <div class="driver-card">
                    <div class="driver-name">{selected_driver} {dnf_status}</div>
                    <div class="driver-stats">
                        <div><strong>Best Lap:</strong> {format_lap_time(driver_stats.get('BestLapTime', 0))}</div>
                        <div><strong>Avg Lap:</strong> {format_lap_time(driver_stats.get('AverageLapTime', 0))}</div>
                        <div><strong>Total Laps:</strong> {driver_stats.get('TotalLaps', 0)}</div>
                        <div><strong>Final Position:</strong> {driver_stats.get('FinalPosition', 'N/A')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if 'ConsistencyScore' in driver_stats:
                    st.metric("Consistency Score", f"{driver_stats['ConsistencyScore']:.3f}")
                if 'PositionGained' in driver_stats:
                    st.metric("Positions Gained", driver_stats['PositionGained'])
                if 'PositionLost' in driver_stats:
                    st.metric("Positions Lost", driver_stats['PositionLost'])

def display_tire_strategy(session_data: dict, insights: dict):
    """Display tire strategy analysis."""
    if 'tire_analysis' in insights and 'processed_tires' in insights['tire_analysis']:
        tire_data = insights['tire_analysis']['processed_tires']
        compound_performance = insights['tire_analysis']['compound_performance']
        
        # Tire strategy chart
        fig = f1_visualizer.create_tire_strategy(tire_data)
        st.plotly_chart(fig, use_container_width=True, key="tire_strategy_chart")
        
        # Compound performance table
        if not compound_performance.empty:
            st.markdown("### 🛞 Tire Compound Performance")
            st.dataframe(compound_performance, use_container_width=True)
        
        # Tire data table
        st.markdown("### 📊 Tire Strategy Data")
        st.dataframe(tire_data, use_container_width=True)
    else:
        st.info("No tire strategy data available for this session.")

def display_speed_analysis(session_data: dict):
    """Display speed analysis."""
    if session_data.get('telemetry') is not None:
        fig = f1_visualizer.create_speed_analysis(session_data['telemetry'])
        st.plotly_chart(fig, use_container_width=True, key="speed_analysis_chart")
        
        st.markdown("### 📈 Speed Statistics")
        telemetry = session_data['telemetry']
        if 'Speed' in telemetry.columns:
            speed_stats = telemetry['Speed'].describe()
            st.dataframe(speed_stats, use_container_width=True)
    else:
        st.info("No telemetry data available for this session.")

def display_data_export(session_data: dict, insights: dict):
    """Display data export options."""
    st.markdown("### 📥 Export Data")
    
    # Export options
    export_options = []
    
    if session_data.get('laps') is not None:
        export_options.append(('Lap Data', session_data['laps']))
    
    if 'driver_summary' in insights and not insights['driver_summary'].empty:
        export_options.append(('Driver Summary', insights['driver_summary']))
    
    if 'tire_analysis' in insights and 'processed_tires' in insights['tire_analysis']:
        export_options.append(('Tire Data', insights['tire_analysis']['processed_tires']))
    
    if session_data.get('telemetry') is not None:
        export_options.append(('Telemetry Data', session_data['telemetry']))
    
    for option_name, data in export_options:
        if not data.empty:
            csv_data = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {option_name} (CSV)",
                data=csv_data,
                file_name=f"f1_{option_name.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main() 