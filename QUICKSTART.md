# 🚀 Quick Start Guide - F1 Data Analytics Dashboard

Get your F1 Data Analytics dashboard up and running in minutes!

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for downloading F1 data)

## ⚡ Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test Your Setup

```bash
python test_setup.py
```

This will verify that all required packages are installed correctly.

### 3. Launch the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🎯 How to Use

### Step 1: Select Session Type
- Choose from: **Race**, **Sprint Race**, **Qualifying**, **Practice 1**, **Practice 2**, **Practice 3**

### Step 2: Choose Year
- Select any year from 2018 onwards (when FastF1 data is most reliable)

### Step 3: Pick Event
- Select the specific F1 race/event from the dropdown menu

### Step 4: Load Data
- Click the **"Load Session Data"** button
- Wait for the data to be fetched and processed

### Step 5: Explore Analytics
- **Lap Time Analysis**: Compare lap times across drivers
- **Position Changes**: Track position changes throughout the session
- **Sector Analysis**: Break down performance by track sectors
- **Driver Performance**: Detailed driver statistics
- **Tire Strategy**: Analyze tire compound usage
- **Speed Analysis**: Visualize speed patterns on track maps

## 🔧 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade
```

**2. FastF1 Connection Issues**
- Ensure you have a stable internet connection
- FastF1 requires internet access to fetch F1 data

**3. No Data Available**
- Some sessions may not have data available
- Try different years or events
- Sprint races are only available from 2021 onwards

**4. Slow Loading**
- First-time data loading may take longer
- Subsequent loads will be faster due to caching

### Getting Help

If you encounter issues:

1. Run the test script: `python test_setup.py`
2. Check your internet connection
3. Try a different session/event combination
4. Ensure you're using Python 3.8+

## 📊 Features Overview

### Real-time Data Analysis
- No local storage required
- Fresh data every time
- Official F1 data via FastF1

### Interactive Visualizations
- Zoom and pan charts
- Hover for detailed information
- Filter by specific drivers

### Comprehensive Metrics
- Lap time consistency analysis
- Position change tracking
- Tire strategy insights
- Speed and acceleration analysis

### Data Export
- Download analysis results as CSV
- Export lap data, driver summaries, tire data
- Share insights with others

## 🎨 Customization

### Styling
- Custom CSS in `assets/styles.css`
- F1-themed color scheme
- Responsive design

### Adding Features
- Extend modules in the `src/` directory
- Add new visualizations in `visualizations.py`
- Create additional data processors in `data_processor.py`

## 📈 Example Use Cases

1. **Race Analysis**: Compare driver performance throughout a race
2. **Qualifying Insights**: Analyze qualifying pace and consistency
3. **Tire Strategy**: Understand tire compound performance
4. **Driver Comparison**: Compare specific drivers head-to-head
5. **Season Trends**: Track performance across multiple events

## 🏁 Ready to Go!

Your F1 Data Analytics dashboard is now ready! Start exploring F1 data like never before.

For more detailed information, check out the main [README.md](README.md) file. 