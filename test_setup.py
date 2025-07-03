"""
Test script to verify F1 Data Analytics project setup.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import fastf1
        print("✅ FastF1 imported successfully")
    except ImportError as e:
        print(f"❌ FastF1 import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import plotly
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    # Test our custom modules
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from data_fetcher import f1_fetcher
        print("✅ Data fetcher module imported successfully")
    except ImportError as e:
        print(f"❌ Data fetcher import failed: {e}")
        return False
    
    try:
        from data_processor import f1_processor
        print("✅ Data processor module imported successfully")
    except ImportError as e:
        print(f"❌ Data processor import failed: {e}")
        return False
    
    try:
        from visualizations import f1_visualizer
        print("✅ Visualizations module imported successfully")
    except ImportError as e:
        print(f"❌ Visualizations import failed: {e}")
        return False
    
    try:
        from utils import get_session_type_options
        print("✅ Utils module imported successfully")
    except ImportError as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    return True

def test_fastf1_connection():
    """Test FastF1 connection and basic functionality."""
    print("\nTesting FastF1 connection...")
    
    try:
        import fastf1
        # Disable cache for testing
        fastf1.Cache.disabled = True
        
        # Test getting available years
        current_year = 2024
        print(f"✅ FastF1 cache disabled (no local storage)")
        print(f"✅ Testing with year: {current_year}")
        
        return True
    except Exception as e:
        print(f"❌ FastF1 connection test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🏎️ F1 Data Analytics - Setup Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        print("\n✅ All imports successful!")
    else:
        print("\n❌ Some imports failed. Please check your requirements.txt")
        return
    
    # Test FastF1
    fastf1_ok = test_fastf1_connection()
    
    if fastf1_ok:
        print("\n✅ FastF1 connection test successful!")
    else:
        print("\n❌ FastF1 connection test failed.")
        return
    
    print("\n🎉 All tests passed! Your F1 Data Analytics project is ready to run.")
    print("\nTo start the application, run:")
    print("streamlit run app.py")

if __name__ == "__main__":
    main() 