"""
FastF1 Data Fetcher Module

This module handles all data retrieval operations from FastF1 library
for different session types (Race, Sprint, Qualifying, Practice).
"""

import fastf1
import pandas as pd
from typing import Dict, List, Optional, Tuple
import streamlit as st


class F1DataFetcher:
    """Handles data fetching from FastF1 library for different session types."""
    
    def __init__(self):
        """Initialize the data fetcher with FastF1 configuration."""
        # Disable cache since we don't want to store data locally
        # This ensures fresh data every time and no local storage
        fastf1.Cache.disabled = True
        
    def get_available_years(self) -> List[int]:
        """Get list of available years with F1 data."""
        try:
            # Get years from 2018 onwards (when FastF1 data is more reliable)
            current_year = pd.Timestamp.now().year
            return list(range(2018, current_year + 1))
        except Exception as e:
            st.error(f"Error fetching available years: {e}")
            return []
    
    def get_events_for_year(self, year: int) -> List[Dict]:
        """Get all events for a specific year."""
        try:
            schedule = fastf1.get_event_schedule(year)
            events = []
            
            for _, event in schedule.iterrows():
                events.append({
                    'name': event['EventName'],
                    'country': event['Country'],
                    'date': event['EventDate'],
                    'round': event['RoundNumber']
                })
            
            return events
        except Exception as e:
            st.error(f"Error fetching events for year {year}: {e}")
            return []
    
    def get_session_data(self, year: int, event_name: str, session_type: str) -> Optional[pd.DataFrame]:
        """
        Fetch session data for a specific event and session type.
        
        Args:
            year: Year of the event
            event_name: Name of the event/race
            session_type: Type of session ('R', 'S', 'Q', 'FP1', 'FP2', 'FP3')
            
        Returns:
            DataFrame with session data or None if error
        """
        try:
            with st.spinner(f"Fetching {session_type} data for {event_name} {year}..."):
                # Load the session
                session = fastf1.get_session(year, event_name, session_type)
                session.load()
                
                # Get lap data
                laps = session.laps
                
                # Get telemetry data for detailed analysis
                # telemetry = session.get_telemetry()
                
                # Get driver info
                drivers = session.drivers
                
                # Get weather data if available
                weather = session.weather_data if hasattr(session, 'weather_data') else None
                
                return {
                    'laps': laps,
                    # 'telemetry': telemetry,
                    'drivers': drivers,
                    'weather': weather,
                    'session': session
                }
                
        except Exception as e:
            st.error(f"Error fetching session data: {e}")
            return None
    
    def get_driver_info(self, year: int, event_name: str, session_type: str) -> Optional[pd.DataFrame]:
        """Get detailed driver information for a session."""
        try:
            session = fastf1.get_session(year, event_name, session_type)
            session.load()
            
            driver_info = []
            for driver in session.drivers:
                driver_data = session.get_driver(driver)
                driver_info.append({
                    'DriverNumber': driver,
                    'BroadcastName': driver_data['BroadcastName'],
                    'FullName': driver_data['FullName'],
                    'TeamName': driver_data['TeamName'],
                    'CountryCode': driver_data['CountryCode']
                })
            
            return pd.DataFrame(driver_info)
            
        except Exception as e:
            st.error(f"Error fetching driver info: {e}")
            return None
    
    def get_tire_data(self, year: int, event_name: str, session_type: str) -> Optional[pd.DataFrame]:
        """Get tire strategy data for a session."""
        try:
            session = fastf1.get_session(year, event_name, session_type)
            session.load()
            
            laps = session.laps
            tire_data = laps[['Driver', 'LapNumber', 'Compound', 'TyreLife', 'FreshTyre']].copy()
            
            return tire_data.dropna()
            
        except Exception as e:
            st.error(f"Error fetching tire data: {e}")
            return None
    
    def get_sector_times(self, year: int, event_name: str, session_type: str) -> Optional[pd.DataFrame]:
        """Get sector times for all drivers in a session."""
        try:
            session = fastf1.get_session(year, event_name, session_type)
            session.load()
            
            laps = session.laps
            sector_times = laps[['Driver', 'LapNumber', 'Sector1Time', 'Sector2Time', 'Sector3Time']].copy()
            
            return sector_times.dropna()
            
        except Exception as e:
            st.error(f"Error fetching sector times: {e}")
            return None


# Global instance
f1_fetcher = F1DataFetcher() 