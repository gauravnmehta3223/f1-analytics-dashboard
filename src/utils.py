"""
F1 Data Analysis Utilities Module

This module contains utility functions and helper methods for the F1 data analysis application.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import streamlit as st
from datetime import datetime


def format_lap_time(seconds: float) -> str:
    """
    Format lap time from seconds to MM:SS.mmm format.
    
    Args:
        seconds: Lap time in seconds
        
    Returns:
        Formatted lap time string
    """
    if pd.isna(seconds) or seconds is None:
        return "N/A"
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:06.3f}"


def format_duration(seconds: float) -> str:
    """
    Format duration from seconds to HH:MM:SS format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if pd.isna(seconds) or seconds is None:
        return "N/A"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
    else:
        return f"{minutes:02d}:{remaining_seconds:02d}"


def get_session_type_display_name(session_type: str) -> str:
    """
    Convert session type code to display name.
    
    Args:
        session_type: Session type code ('R', 'S', 'Q', 'FP1', 'FP2', 'FP3')
        
    Returns:
        Display name for the session type
    """
    session_names = {
        'R': 'Race',
        'S': 'Sprint Race',
        'Q': 'Qualifying',
        'FP1': 'Practice 1',
        'FP2': 'Practice 2',
        'FP3': 'Practice 3'
    }
    
    return session_names.get(session_type, session_type)


def get_session_type_options() -> List[Tuple[str, str]]:
    """
    Get list of available session types with display names.
    
    Returns:
        List of tuples (code, display_name)
    """
    return [
        ('R', 'Race'),
        ('S', 'Sprint Race'),
        ('Q', 'Qualifying'),
        ('FP1', 'Practice 1'),
        ('FP2', 'Practice 2'),
        ('FP3', 'Practice 3')
    ]


def validate_session_data(session_data: Dict) -> bool:
    """
    Validate that session data contains required information.
    
    Args:
        session_data: Dictionary containing session data
        
    Returns:
        True if valid, False otherwise
    """
    if not session_data:
        return False
    
    required_keys = ['laps']
    return all(key in session_data for key in required_keys)


def get_driver_display_name(driver_code: str, driver_info: pd.DataFrame = None) -> str:
    """
    Get display name for a driver code.
    
    Args:
        driver_code: Driver code/number
        driver_info: DataFrame with driver information
        
    Returns:
        Display name for the driver
    """
    if driver_info is not None and not driver_info.empty:
        driver_row = driver_info[driver_info['DriverNumber'] == driver_code]
        if not driver_row.empty:
            return driver_row.iloc[0]['BroadcastName']
    
    return f"Driver {driver_code}"


def calculate_driver_stats(laps_df: pd.DataFrame, driver: str) -> Dict:
    """
    Calculate comprehensive statistics for a specific driver.
    
    Args:
        laps_df: Cleaned lap data
        driver: Driver code/number
        
    Returns:
        Dictionary with driver statistics
    """
    if laps_df is None or laps_df.empty:
        return {}
    
    driver_laps = laps_df[laps_df['Driver'] == driver]
    
    if driver_laps.empty:
        return {}
    
    stats = {
        'total_laps': len(driver_laps),
        'best_lap_time': driver_laps['LapTimeSeconds'].min(),
        'average_lap_time': driver_laps['LapTimeSeconds'].mean(),
        'lap_time_std': driver_laps['LapTimeSeconds'].std(),
        'fastest_lap_number': driver_laps.loc[driver_laps['LapTimeSeconds'].idxmin(), 'LapNumber'] if 'LapNumber' in driver_laps.columns else None,
        'final_position': driver_laps['Position'].iloc[-1] if 'Position' in driver_laps.columns else None,
        'starting_position': driver_laps['Position'].iloc[0] if 'Position' in driver_laps.columns else None
    }
    
    # Add sector times if available
    for sector in ['Sector1TimeSeconds', 'Sector2TimeSeconds', 'Sector3TimeSeconds']:
        if sector in driver_laps.columns:
            stats[f'best_{sector.lower()}'] = driver_laps[sector].min()
            stats[f'avg_{sector.lower()}'] = driver_laps[sector].mean()
    
    # Add consistency metrics
    if 'LapTimeVariance' in driver_laps.columns:
        stats['consistency_score'] = 1 / (1 + driver_laps['LapTimeVariance'].mean())
    
    # Add position change metrics
    if 'PositionGained' in driver_laps.columns:
        stats['positions_gained'] = driver_laps['PositionGained'].sum()
    if 'PositionLost' in driver_laps.columns:
        stats['positions_lost'] = driver_laps['PositionLost'].sum()
    
    return stats


def create_summary_metrics(insights: Dict) -> Dict:
    """
    Create summary metrics for display in the dashboard.
    
    Args:
        insights: Dictionary containing session insights
        
    Returns:
        Dictionary with summary metrics
    """
    summary = {}
    
    try:
        if 'lap_time_stats' in insights:
            stats = insights['lap_time_stats']
            summary['fastest_lap'] = format_lap_time(stats.get('fastest_lap'))
            summary['average_lap'] = format_lap_time(stats.get('average_lap'))
            summary['lap_time_std'] = f"{stats.get('lap_time_std', 0):.3f}s"
        
        if 'driver_summary' in insights and not insights['driver_summary'].empty:
            driver_summary = insights['driver_summary']
            summary['total_drivers'] = len(driver_summary)
            summary['best_driver'] = driver_summary.loc[driver_summary['BestLapTime'].idxmin(), 'Driver'] if 'BestLapTime' in driver_summary.columns else None
            summary['most_consistent'] = driver_summary.loc[driver_summary['ConsistencyScore'].idxmax(), 'Driver'] if 'ConsistencyScore' in driver_summary.columns else None
        
        return summary
        
    except Exception as e:
        st.error(f"Error creating summary metrics: {e}")
        return {}


def get_tire_compound_colors() -> Dict[str, str]:
    """
    Get color mapping for tire compounds.
    
    Returns:
        Dictionary mapping compound names to colors
    """
    return {
        'SOFT': '#FF0000',      # Red
        'MEDIUM': '#FFFF00',    # Yellow
        'HARD': '#FFFFFF',      # White
        'INTERMEDIATE': '#00FF00',  # Green
        'WET': '#0000FF'        # Blue
    }


def format_tire_compound(compound: str) -> str:
    """
    Format tire compound name for display.
    
    Args:
        compound: Raw compound name
        
    Returns:
        Formatted compound name
    """
    if pd.isna(compound):
        return "Unknown"
    
    compound_map = {
        'SOFT': 'Soft',
        'MEDIUM': 'Medium',
        'HARD': 'Hard',
        'INTERMEDIATE': 'Intermediate',
        'WET': 'Wet'
    }
    
    return compound_map.get(compound.upper(), compound)


def create_download_dataframe(df: pd.DataFrame, filename: str) -> bytes:
    """
    Create downloadable CSV data from DataFrame.
    
    Args:
        df: DataFrame to convert
        filename: Name for the file
        
    Returns:
        CSV data as bytes
    """
    if df is None or df.empty:
        return b""
    
    return df.to_csv(index=False).encode('utf-8')


def get_available_years_range() -> Tuple[int, int]:
    """
    Get the range of available years for F1 data.
    
    Returns:
        Tuple of (start_year, end_year)
    """
    current_year = datetime.now().year
    return (2018, current_year)


def validate_year_selection(year: int) -> bool:
    """
    Validate if the selected year is within the available range.
    
    Args:
        year: Selected year
        
    Returns:
        True if valid, False otherwise
    """
    start_year, end_year = get_available_years_range()
    return start_year <= year <= end_year


def create_error_message(error: Exception, context: str = "") -> str:
    """
    Create a user-friendly error message.
    
    Args:
        error: Exception that occurred
        context: Additional context about the error
        
    Returns:
        Formatted error message
    """
    base_message = f"An error occurred: {str(error)}"
    
    if context:
        return f"{context} - {base_message}"
    
    return base_message


def display_loading_message(message: str = "Loading data..."):
    """
    Display a loading message with spinner.
    
    Args:
        message: Message to display
    """
    with st.spinner(message):
        st.info("Please wait while we fetch the latest F1 data...")


def display_no_data_message(session_type: str, event_name: str, year: int):
    """
    Display a message when no data is available.
    
    Args:
        session_type: Type of session
        event_name: Name of the event
        year: Year of the event
    """
    st.warning(
        f"No data available for {get_session_type_display_name(session_type)} "
        f"session at {event_name} {year}. "
        "This might be due to session cancellation or data availability issues."
    ) 