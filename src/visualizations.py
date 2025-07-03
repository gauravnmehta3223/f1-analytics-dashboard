"""
F1 Data Visualizations Module

This module handles all chart and graph generation for F1 data analysis
using Plotly for interactive visualizations.
"""

import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import streamlit as st


class F1Visualizer:
    """Handles creation of interactive visualizations for F1 data."""
    
    def __init__(self):
        """Initialize the visualizer with default color schemes."""
        self.color_scheme = px.colors.qualitative.Set3
        self.driver_colors = {}
    
    def create_lap_time_comparison(self, laps_df: pd.DataFrame, drivers: List[str] = None) -> go.Figure:
        """
        Create lap time comparison chart for selected drivers.
        
        Args:
            laps_df: Cleaned lap data
            drivers: List of drivers to include (None for all)
            
        Returns:
            Plotly figure object
        """
        if laps_df is None or laps_df.empty:
            return go.Figure()
        
        try:
            if drivers:
                filtered_laps = laps_df[laps_df['Driver'].isin(drivers)]
            else:
                filtered_laps = laps_df
            
            fig = px.line(
                filtered_laps,
                x='LapNumber',
                y='LapTimeSeconds',
                color='Driver',
                title='Lap Time Comparison',
                labels={'LapTimeSeconds': 'Lap Time (seconds)', 'LapNumber': 'Lap Number'},
                hover_data=['Driver', 'LapTimeSeconds', 'Position']
            )
            
            fig.update_layout(
                xaxis_title="Lap Number",
                yaxis_title="Lap Time (seconds)",
                hovermode='x unified',
                height=500
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating lap time comparison: {e}")
            return go.Figure()
    
    def create_driver_performance_summary(self, driver_summary: pd.DataFrame) -> go.Figure:
        """
        Create driver performance summary chart.
        
        Args:
            driver_summary: Driver summary DataFrame
            
        Returns:
            Plotly figure object
        """
        if driver_summary is None or driver_summary.empty:
            return go.Figure()
        
        try:
            # Create subplots
            fig = sp.make_subplots(
                rows=2, cols=2,
                subplot_titles=('Best Lap Times', 'Average Lap Times', 'Total Laps', 'Consistency Score'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Best lap times
            fig.add_trace(
                go.Bar(
                    x=driver_summary['Driver'],
                    y=driver_summary['BestLapTime'],
                    name='Best Lap Time',
                    marker_color='lightblue'
                ),
                row=1, col=1
            )
            
            # Average lap times
            fig.add_trace(
                go.Bar(
                    x=driver_summary['Driver'],
                    y=driver_summary['AverageLapTime'],
                    name='Average Lap Time',
                    marker_color='lightcoral'
                ),
                row=1, col=2
            )
            
            # Total laps
            fig.add_trace(
                go.Bar(
                    x=driver_summary['Driver'],
                    y=driver_summary['TotalLaps'],
                    name='Total Laps',
                    marker_color='lightgreen'
                ),
                row=2, col=1
            )
            
            # Consistency score
            if 'ConsistencyScore' in driver_summary.columns:
                fig.add_trace(
                    go.Bar(
                        x=driver_summary['Driver'],
                        y=driver_summary['ConsistencyScore'],
                        name='Consistency Score',
                        marker_color='lightyellow'
                    ),
                    row=2, col=2
                )
            
            fig.update_layout(
                title='Driver Performance Summary',
                height=600,
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating driver performance summary: {e}")
            return go.Figure()
    
    def create_position_changes(self, laps_df: pd.DataFrame, drivers: List[str] = None) -> go.Figure:
        """
        Create position changes throughout the session.
        
        Args:
            laps_df: Cleaned lap data
            drivers: List of drivers to include (None for all)
            
        Returns:
            Plotly figure object
        """
        if laps_df is None or laps_df.empty or 'Position' not in laps_df.columns:
            return go.Figure()
        
        try:
            if drivers:
                filtered_laps = laps_df[laps_df['Driver'].isin(drivers)]
            else:
                filtered_laps = laps_df
            
            fig = px.line(
                filtered_laps,
                x='LapNumber',
                y='Position',
                color='Driver',
                title='Position Changes Throughout Session',
                labels={'Position': 'Position', 'LapNumber': 'Lap Number'},
                hover_data=['Driver', 'Position', 'LapTimeSeconds']
            )
            
            # Reverse y-axis so P1 is at the top
            fig.update_layout(
                yaxis=dict(autorange="reversed"),
                xaxis_title="Lap Number",
                yaxis_title="Position",
                height=500
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating position changes chart: {e}")
            return go.Figure()
    
    def create_sector_analysis(self, laps_df: pd.DataFrame, drivers: List[str] = None) -> go.Figure:
        """
        Create sector time analysis chart.
        
        Args:
            laps_df: Cleaned lap data
            drivers: List of drivers to include (None for all)
            
        Returns:
            Plotly figure object
        """
        if laps_df is None or laps_df.empty:
            return go.Figure()
        
        try:
            sector_cols = ['Sector1TimeSeconds', 'Sector2TimeSeconds', 'Sector3TimeSeconds']
            available_sectors = [col for col in sector_cols if col in laps_df.columns]
            
            if not available_sectors:
                return go.Figure()
            
            if drivers:
                filtered_laps = laps_df[laps_df['Driver'].isin(drivers)]
            else:
                filtered_laps = laps_df
            
            # Create subplots for each sector
            fig = sp.make_subplots(
                rows=1, cols=len(available_sectors),
                subplot_titles=[f'Sector {i+1}' for i in range(len(available_sectors))],
                specs=[[{"secondary_y": False}] * len(available_sectors)]
            )
            
            for i, sector_col in enumerate(available_sectors):
                fig.add_trace(
                    go.Box(
                        y=filtered_laps[sector_col],
                        x=filtered_laps['Driver'],
                        name=f'Sector {i+1}',
                        marker_color=self.color_scheme[i]
                    ),
                    row=1, col=i+1
                )
            
            fig.update_layout(
                title='Sector Time Analysis',
                height=400,
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating sector analysis: {e}")
            return go.Figure()
    
    def create_tire_strategy(self, tire_df: pd.DataFrame, drivers: List[str] = None) -> go.Figure:
        """
        Create tire strategy visualization.
        
        Args:
            tire_df: Processed tire data
            drivers: List of drivers to include (None for all)
            
        Returns:
            Plotly figure object
        """
        if tire_df is None or tire_df.empty:
            return go.Figure()
        
        try:
            if drivers:
                filtered_tires = tire_df[tire_df['Driver'].isin(drivers)]
            else:
                filtered_tires = tire_df
            
            # Create tire compound timeline
            fig = px.scatter(
                filtered_tires,
                x='LapNumber',
                y='Driver',
                color='Compound',
                size='TyreLife',
                title='Tire Strategy Timeline',
                labels={'LapNumber': 'Lap Number', 'Driver': 'Driver'},
                hover_data=['Compound', 'TyreLife', 'FreshTyre']
            )
            
            fig.update_layout(
                xaxis_title="Lap Number",
                yaxis_title="Driver",
                height=500
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating tire strategy chart: {e}")
            return go.Figure()
    
    def create_speed_analysis(self, telemetry_df: pd.DataFrame, drivers: List[str] = None) -> go.Figure:
        """
        Create speed analysis from telemetry data.
        
        Args:
            telemetry_df: Processed telemetry data
            drivers: List of drivers to include (None for all)
            
        Returns:
            Plotly figure object
        """
        if telemetry_df is None or telemetry_df.empty or 'Speed' not in telemetry_df.columns:
            return go.Figure()
        
        try:
            if drivers:
                filtered_telemetry = telemetry_df[telemetry_df['Driver'].isin(drivers)]
            else:
                filtered_telemetry = telemetry_df
            
            # Sample data to avoid overwhelming the chart
            if len(filtered_telemetry) > 10000:
                filtered_telemetry = filtered_telemetry.sample(n=10000, random_state=42)
            
            fig = px.scatter(
                filtered_telemetry,
                x='X',
                y='Y',
                color='Speed',
                title='Speed Analysis - Track Map',
                labels={'X': 'X Position', 'Y': 'Y Position', 'Speed': 'Speed (km/h)'},
                color_continuous_scale='viridis'
            )
            
            fig.update_layout(
                height=500,
                coloraxis_colorbar=dict(title="Speed (km/h)")
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating speed analysis: {e}")
            return go.Figure()
    
    def create_consistency_heatmap(self, laps_df: pd.DataFrame) -> go.Figure:
        """
        Create consistency heatmap showing lap time variance.
        
        Args:
            laps_df: Cleaned lap data
            
        Returns:
            Plotly figure object
        """
        if laps_df is None or laps_df.empty or 'LapTimeVariance' not in laps_df.columns:
            return go.Figure()
        
        try:
            # Create pivot table for heatmap
            heatmap_data = laps_df.pivot_table(
                values='LapTimeVariance',
                index='Driver',
                columns='LapNumber',
                aggfunc='mean'
            )
            
            fig = px.imshow(
                heatmap_data,
                title='Lap Time Consistency Heatmap',
                labels=dict(x="Lap Number", y="Driver", color="Lap Time Variance"),
                color_continuous_scale='RdYlGn_r'
            )
            
            fig.update_layout(height=400)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating consistency heatmap: {e}")
            return go.Figure()
    
    def create_session_overview_dashboard(self, session_data: Dict, insights: Dict) -> List[go.Figure]:
        """
        Create a comprehensive dashboard with multiple visualizations.
        
        Args:
            session_data: Dictionary containing all session data
            insights: Dictionary containing processed insights
            
        Returns:
            List of Plotly figures
        """
        figures = []
        
        try:
            # Get cleaned lap data
            if 'laps' in session_data and session_data['laps'] is not None:
                cleaned_laps = session_data['laps']
                
                # 1. Lap time comparison
                if not cleaned_laps.empty:
                    figures.append(self.create_lap_time_comparison(cleaned_laps))
                
                # 2. Position changes
                if 'Position' in cleaned_laps.columns:
                    figures.append(self.create_position_changes(cleaned_laps))
                
                # 3. Sector analysis
                figures.append(self.create_sector_analysis(cleaned_laps))
                
                # 4. Consistency heatmap
                figures.append(self.create_consistency_heatmap(cleaned_laps))
            
            # 5. Driver performance summary
            if 'driver_summary' in insights and not insights['driver_summary'].empty:
                figures.append(self.create_driver_performance_summary(insights['driver_summary']))
            
            # 6. Tire strategy
            if 'tire_analysis' in insights and 'processed_tires' in insights['tire_analysis']:
                figures.append(self.create_tire_strategy(insights['tire_analysis']['processed_tires']))
            
            # 7. Speed analysis
            if 'telemetry' in session_data and session_data['telemetry'] is not None:
                figures.append(self.create_speed_analysis(session_data['telemetry']))
            
            return figures
            
        except Exception as e:
            st.error(f"Error creating session overview dashboard: {e}")
            return []


# Global instance
f1_visualizer = F1Visualizer() 