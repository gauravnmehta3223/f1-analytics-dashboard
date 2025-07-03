"""
F1 Data Processor Module

This module handles data cleaning and feature engineering for F1 data
retrieved from FastF1 library.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import streamlit as st


class F1DataProcessor:
    """Handles data cleaning and feature engineering for F1 data."""
    
    def __init__(self):
        """Initialize the data processor."""
        pass
    
    def clean_lap_data(self, laps_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare lap data for analysis.
        
        Args:
            laps_df: Raw lap data from FastF1
            
        Returns:
            Cleaned lap data
        """
        if laps_df is None or laps_df.empty:
            return pd.DataFrame()
        
        try:
            # Create a copy to avoid modifying original data
            cleaned_laps = laps_df.copy()
            
            # Remove rows with missing critical data
            cleaned_laps = cleaned_laps.dropna(subset=['LapTime', 'Driver'])
            
            # Convert lap time to seconds for easier analysis
            if 'LapTime' in cleaned_laps.columns:
                cleaned_laps['LapTimeSeconds'] = cleaned_laps['LapTime'].dt.total_seconds()
            
            # Convert sector times to seconds
            for sector in ['Sector1Time', 'Sector2Time', 'Sector3Time']:
                if sector in cleaned_laps.columns:
                    cleaned_laps[f'{sector}Seconds'] = cleaned_laps[sector].dt.total_seconds()
            
            # Add lap consistency metrics
            cleaned_laps = self._add_consistency_metrics(cleaned_laps)
            
            # Add position change metrics
            cleaned_laps = self._add_position_metrics(cleaned_laps)
            
            return cleaned_laps
            
        except Exception as e:
            st.error(f"Error cleaning lap data: {e}")
            return pd.DataFrame()
    
    def _add_consistency_metrics(self, laps_df: pd.DataFrame) -> pd.DataFrame:
        """Add consistency metrics to lap data."""
        try:
            # Calculate rolling average lap times
            laps_df['RollingAvgLapTime'] = laps_df.groupby('Driver')['LapTimeSeconds'].rolling(
                window=5, min_periods=1
            ).mean().reset_index(0, drop=True)
            
            # Calculate lap time variance
            laps_df['LapTimeVariance'] = laps_df.groupby('Driver')['LapTimeSeconds'].rolling(
                window=10, min_periods=1
            ).var().reset_index(0, drop=True)
            
            # Calculate best lap time for each driver
            best_laps = laps_df.groupby('Driver')['LapTimeSeconds'].min()
            laps_df['BestLapTime'] = laps_df['Driver'].map(best_laps)
            laps_df['GapToBest'] = laps_df['LapTimeSeconds'] - laps_df['BestLapTime']
            
            return laps_df
            
        except Exception as e:
            st.warning(f"Could not add consistency metrics: {e}")
            return laps_df
    
    def _add_position_metrics(self, laps_df: pd.DataFrame) -> pd.DataFrame:
        """Add position change metrics to lap data."""
        try:
            # Calculate position changes
            laps_df['PositionChange'] = laps_df.groupby('Driver')['Position'].diff()
            
            # Calculate cumulative position changes
            laps_df['CumulativePositionChange'] = laps_df.groupby('Driver')['PositionChange'].cumsum()
            
            # Calculate position gain/loss
            laps_df['PositionGained'] = laps_df['PositionChange'].apply(
                lambda x: abs(x) if x < 0 else 0
            )
            laps_df['PositionLost'] = laps_df['PositionChange'].apply(
                lambda x: x if x > 0 else 0
            )
            
            return laps_df
            
        except Exception as e:
            st.warning(f"Could not add position metrics: {e}")
            return laps_df
    
    def process_telemetry_data(self, telemetry_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process and clean telemetry data.
        
        Args:
            telemetry_df: Raw telemetry data from FastF1
            
        Returns:
            Processed telemetry data
        """
        if telemetry_df is None or telemetry_df.empty:
            return pd.DataFrame()
        
        try:
            # Create a copy
            processed_telemetry = telemetry_df.copy()
            
            # Remove outliers in speed data
            if 'Speed' in processed_telemetry.columns:
                Q1 = processed_telemetry['Speed'].quantile(0.01)
                Q3 = processed_telemetry['Speed'].quantile(0.99)
                processed_telemetry = processed_telemetry[
                    (processed_telemetry['Speed'] >= Q1) & 
                    (processed_telemetry['Speed'] <= Q3)
                ]
            
            # Calculate acceleration from speed
            if 'Speed' in processed_telemetry.columns:
                processed_telemetry['Acceleration'] = processed_telemetry.groupby('Driver')['Speed'].diff()
            
            # Calculate cornering metrics
            if 'Speed' in processed_telemetry.columns and 'X' in processed_telemetry.columns:
                processed_telemetry['CorneringSpeed'] = processed_telemetry['Speed'].rolling(
                    window=10, min_periods=1
                ).mean()
            
            return processed_telemetry
            
        except Exception as e:
            st.error(f"Error processing telemetry data: {e}")
            return pd.DataFrame()
    
    def create_driver_summary(self, laps_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a summary of driver performance.
        
        Args:
            laps_df: Cleaned lap data
            
        Returns:
            Driver summary DataFrame
        """
        if laps_df is None or laps_df.empty:
            return pd.DataFrame()
        
        try:
            summary = []
            max_lap = laps_df['LapNumber'].max() if 'LapNumber' in laps_df.columns else None
            
            for driver in laps_df['Driver'].unique():
                driver_laps = laps_df[laps_df['Driver'] == driver]
                last_lap = driver_laps['LapNumber'].max() if 'LapNumber' in driver_laps.columns else None
                dnf = (last_lap is not None and max_lap is not None and last_lap < max_lap)
                
                driver_summary = {
                    'Driver': driver,
                    'TotalLaps': len(driver_laps),
                    'BestLapTime': driver_laps['LapTimeSeconds'].min(),
                    'AverageLapTime': driver_laps['LapTimeSeconds'].mean(),
                    'LapTimeStd': driver_laps['LapTimeSeconds'].std(),
                    'BestSector1': driver_laps['Sector1TimeSeconds'].min() if 'Sector1TimeSeconds' in driver_laps.columns else None,
                    'BestSector2': driver_laps['Sector2TimeSeconds'].min() if 'Sector2TimeSeconds' in driver_laps.columns else None,
                    'BestSector3': driver_laps['Sector3TimeSeconds'].min() if 'Sector3TimeSeconds' in driver_laps.columns else None,
                    'FinalPosition': driver_laps['Position'].iloc[-1] if 'Position' in driver_laps.columns else None,
                    'StartingPosition': driver_laps['Position'].iloc[0] if 'Position' in driver_laps.columns else None,
                    'PositionGained': driver_laps['PositionGained'].sum() if 'PositionGained' in driver_laps.columns else 0,
                    'PositionLost': driver_laps['PositionLost'].sum() if 'PositionLost' in driver_laps.columns else 0,
                    'ConsistencyScore': 1 / (1 + driver_laps['LapTimeVariance'].mean()) if 'LapTimeVariance' in driver_laps.columns else None,
                    'DNF': dnf
                }
                
                summary.append(driver_summary)
            
            return pd.DataFrame(summary)
            
        except Exception as e:
            st.error(f"Error creating driver summary: {e}")
            return pd.DataFrame()
    
    def process_tire_data(self, tire_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process tire strategy data.
        
        Args:
            tire_df: Raw tire data
            
        Returns:
            Processed tire data
        """
        if tire_df is None or tire_df.empty:
            return pd.DataFrame()
        
        try:
            processed_tires = tire_df.copy()
            
            # Calculate stint lengths
            processed_tires['StintLength'] = processed_tires.groupby(['Driver', 'Compound'])['LapNumber'].transform(
                lambda x: x.max() - x.min() + 1
            )
            
            # Calculate tire degradation
            processed_tires['TireDegradation'] = processed_tires.groupby(['Driver', 'Compound'])['TyreLife'].diff()
            
            # Add tire compound performance metrics
            compound_performance = processed_tires.groupby('Compound').agg({
                'TyreLife': ['mean', 'max'],
                'StintLength': 'mean'
            }).round(2)
            
            return processed_tires, compound_performance
            
        except Exception as e:
            st.error(f"Error processing tire data: {e}")
            return pd.DataFrame(), pd.DataFrame()
    
    def create_session_insights(self, session_data: Dict) -> Dict:
        """
        Create comprehensive insights from session data.
        
        Args:
            session_data: Dictionary containing all session data
            
        Returns:
            Dictionary with insights
        """
        insights = {}
        
        try:
            if 'laps' in session_data and session_data['laps'] is not None:
                cleaned_laps = self.clean_lap_data(session_data['laps'])
                
                if not cleaned_laps.empty:
                    # Driver performance insights
                    insights['driver_summary'] = self.create_driver_summary(cleaned_laps)
                    
                    # Lap time distribution
                    insights['lap_time_stats'] = {
                        'fastest_lap': cleaned_laps['LapTimeSeconds'].min(),
                        'slowest_lap': cleaned_laps['LapTimeSeconds'].max(),
                        'average_lap': cleaned_laps['LapTimeSeconds'].mean(),
                        'lap_time_std': cleaned_laps['LapTimeSeconds'].std()
                    }
                    
                    # Consistency analysis
                    insights['consistency_analysis'] = cleaned_laps.groupby('Driver')['LapTimeVariance'].mean().sort_values()
                    
                    # Position changes
                    if 'PositionChange' in cleaned_laps.columns:
                        insights['position_changes'] = cleaned_laps.groupby('Driver')['PositionChange'].sum().sort_values()
            
            # Tire strategy insights
            if 'tire_data' in session_data and session_data['tire_data'] is not None:
                processed_tires, compound_performance = self.process_tire_data(session_data['tire_data'])
                insights['tire_analysis'] = {
                    'processed_tires': processed_tires,
                    'compound_performance': compound_performance
                }
            
            return insights
            
        except Exception as e:
            st.error(f"Error creating session insights: {e}")
            return {}


# Global instance
f1_processor = F1DataProcessor() 