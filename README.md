# 🏎️ F1 Data Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![FastF1](https://img.shields.io/badge/FastF1-3.4+-orange.svg)](https://github.com/theOehrly/Fast-F1)

A comprehensive **Formula 1 data analytics dashboard** built with Streamlit and FastF1 library. Analyze F1 sessions in real-time with interactive visualizations and advanced analytics.

## 📊 Features

### 🎯 Session Analysis
- **Race Sessions**: Complete race analysis with position changes and lap times
- **Sprint Races**: Sprint race performance analysis (2021 onwards)
- **Qualifying**: Q1, Q2, Q3 session breakdowns
- **Practice Sessions**: FP1, FP2, FP3 detailed analysis

### 📈 Interactive Visualizations
- **Lap Time Comparisons**: Real-time lap time analysis across drivers
- **Position Changes**: Track position evolution throughout sessions
- **Sector Analysis**: Break down performance by track sectors
- **Consistency Heatmaps**: Driver consistency visualization
- **Tire Strategy**: Tire compound usage and stint analysis
- **Speed Analysis**: Track map speed visualization

### 🔍 Advanced Analytics
- **DNF Detection**: Automatic detection of drivers who didn't finish
- **Driver Performance**: Comprehensive driver statistics and metrics
- **Feature Engineering**: Advanced lap time and consistency calculations
- **Real-time Data**: No local caching - fresh data every session

### 📱 User Experience
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Controls**: Easy session and driver selection
- **Data Export**: Download analysis results as CSV files
- **Modern UI**: Beautiful F1-themed interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection (for F1 data access)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gauravnmehta3223/f1-analytics-dashboard.git
   cd f1-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test your setup**
   ```bash
   python test_setup.py
   ```

4. **Launch the application**
   ```bash
   streamlit run app.py
   ```

The dashboard will open in your browser at `http://localhost:8501`

## 📖 How to Use

### 1. Select Session Type
Choose from the available session types:
- 🏁 **Race**: Full race analysis
- ⚡ **Sprint Race**: Sprint race analysis (2021+)
- 🏆 **Qualifying**: Qualifying session analysis
- 🏃 **Practice 1/2/3**: Practice session analysis

### 2. Choose Year and Event
- Select any year from **2018 onwards** (when FastF1 data is most reliable)
- Pick the specific F1 event from the dropdown menu

### 3. Load and Analyze
- Click **"Load Session Data"** to fetch fresh data
- Explore different analysis tabs
- Filter by specific drivers
- Export results as needed

## 🏗️ Project Structure

```
F1 Data Analysis/
├── 📄 app.py                 # Main Streamlit application
├── 📄 requirements.txt       # Python dependencies
├── 📄 README.md             # Project documentation
├── 📄 QUICKSTART.md         # Quick start guide
├── 📄 test_setup.py         # Setup verification script
├── 📄 .gitignore            # Git ignore rules
├── 📁 assets/
│   └── 📄 styles.css        # Custom CSS styling
└── 📁 src/
    ├── 📄 __init__.py
    ├── 📄 data_fetcher.py   # FastF1 data retrieval
    ├── 📄 data_processor.py # Data cleaning & feature engineering
    └── 📄 visualizations.py # Plotly chart generation
```

## 🔧 Technical Details

### Data Sources
- **FastF1 Library**: Official Formula 1 data access
- **Real-time Fetching**: No local storage required
- **Comprehensive Coverage**: All F1 sessions and events

### Key Technologies
- **Streamlit**: Web application framework
- **FastF1**: F1 data access library
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Performance Features
- **No Local Caching**: Fresh data every session
- **Efficient Processing**: Optimized data cleaning and feature engineering
- **Responsive UI**: Fast loading and smooth interactions

## 📊 Analysis Capabilities

### Lap Time Analysis
- Best lap time identification
- Average lap time calculations
- Lap time consistency metrics
- Rolling average analysis

### Driver Performance
- Individual driver statistics
- Position change tracking
- Sector time breakdowns
- Consistency scoring

### Race Strategy
- Tire compound analysis
- Stint length calculations
- Pit stop strategy insights
- DNF detection and analysis

### Comparative Analysis
- Driver-to-driver comparisons
- Session-to-session analysis
- Year-over-year trends
- Team performance analysis

## 🎨 Customization

### Styling
The dashboard uses custom CSS for F1-themed styling:
- F1 red color scheme (`#e10600`)
- Responsive design elements
- Custom animations and transitions
- Professional data visualization styling

### Adding Features
- Extend modules in the `src/` directory
- Add new visualizations in `visualizations.py`
- Create additional data processors in `data_processor.py`
- Modify the UI in `app.py`

## 🔍 Troubleshooting

### Common Issues

**Import Errors**
```bash
pip install -r requirements.txt --upgrade
```

**FastF1 Connection Issues**
- Ensure stable internet connection
- Check firewall/proxy settings
- Try different session/event combinations

**No Data Available**
- Some sessions may not have data
- Try different years or events
- Sprint races only available from 2021

**Slow Loading**
- Each load downloads the session again, because local caching is turned off
- Large race sessions can take a minute or more
- Check internet connection speed

### Getting Help
1. Run the test script: `python test_setup.py`
2. Check your internet connection
3. Try different session combinations
4. Ensure Python 3.8+ is installed

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- **FastF1 Team**: For providing excellent F1 data access
- **Streamlit Team**: For the amazing web app framework
- **Formula 1**: For providing the official data
- **Plotly**: For interactive visualization capabilities

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the quick start guide

---

**Built with ❤️ for the F1 community**

*This project is not affiliated with Formula 1 or any official F1 entities.*

