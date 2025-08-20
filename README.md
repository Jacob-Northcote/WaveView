# 🏄‍♂️ WaveView - Professional Surf Analysis & Wave Visualization

A full-stack Python application that provides real-time surf analysis using AI, featuring wave visualization and surf spot rankings.

## 🌟 Features

- **Real-time Surf Data**: Fetches current conditions from surf APIs
- **AI-Powered Analysis**: Uses GPT to analyze surf conditions and provide insights
- **Wave Visualization**: ASCII art wave representations that match actual conditions
- **Surf Spot Rankings**: Algorithm-based ranking of surf spots by current conditions
- **Professional UI**: Modern, responsive web interface with glassmorphism design
- **CS Fundamentals**: Demonstrates sorting algorithms, data structures, and API integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (for the batch script)

### Easy Setup (Windows)
1. **Download the project** to your computer
2. **Double-click `start.bat`** to run the application
3. **Open your browser** and go to `http://localhost:8000`

The batch script will automatically:
- Check Python installation
- Install required dependencies
- Start the server

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Then open `http://localhost:8000` in your browser.

## 🔧 Configuration

### API Keys (Optional)
The app works with mock data by default, but you can add real API keys for enhanced functionality:

1. **OpenAI API Key** (for GPT analysis):
   - Get a free key from [OpenAI](https://platform.openai.com/)
   - Set environment variable: `OPENAI_API_KEY=your-key-here`

2. **Stormglass API Key** (for real surf data):
   - Get a free key from [Stormglass](https://stormglass.io/)
   - Set environment variable: `SURF_API_KEY=your-key-here`

## 🏄‍♂️ How It Works

### 1. Surf Data Collection
- Fetches real-time wave data from surf APIs
- Includes wave height, period, direction, wind, temperature, and tide
- Falls back to realistic mock data if APIs are unavailable

### 2. AI Analysis
- Sends surf conditions to GPT API
- Receives detailed surf analysis including:
  - Wave quality assessment
  - Difficulty level
  - Safety considerations
  - Best surfing times
  - ASCII wave visualization

### 3. Wave Visualization
- GPT generates ASCII art waves proportional to actual conditions
- 3-foot waves appear smaller than 6-foot waves
- Wave labels show exact heights (e.g., "6-5 feet")
- Uses keyboard characters to create realistic wave shapes

### 4. Surf Spot Rankings
- Implements bubble sort algorithm to rank spots by conditions
- Calculates quality scores based on multiple factors:
  - Wave height (optimal: 3-8 feet)
  - Wave period (optimal: 10-16 seconds)
  - Wind speed (lower is better)
  - Swell consistency

## 🏗️ Technical Architecture

### Backend (Python/FastAPI)
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server for high performance
- **OpenAI API**: GPT integration for surf analysis
- **Requests**: HTTP client for surf data APIs
- **Pydantic**: Data validation and serialization

### Frontend (HTML/CSS/JavaScript)
- **Vanilla JavaScript**: No frameworks, pure ES6+
- **CSS Grid & Flexbox**: Modern responsive layout
- **Glassmorphism Design**: Beautiful UI with backdrop blur effects
- **Async/Await**: Modern JavaScript for API calls

### Algorithms & CS Concepts
- **Bubble Sort**: Used for surf spot rankings
- **Quality Scoring Algorithm**: Multi-factor wave quality calculation
- **Data Structures**: Dictionaries, lists, and custom classes
- **API Integration**: RESTful API design and consumption
- **Error Handling**: Comprehensive error management

## 📊 API Endpoints

- `GET /` - Main application page
- `GET /api/health` - Server health check
- `GET /api/locations` - Available surf locations
- `GET /api/surf-data/{location_id}` - Current surf conditions
- `GET /api/analysis/{location_id}` - AI analysis of conditions
- `GET /api/rankings` - Surf spot rankings by conditions

## 🎯 Surf Locations

The app includes famous surf spots:
- **Malibu, California** - Famous point break
- **Pipeline, Hawaii** - World-famous reef break
- **Teahupoo, Tahiti** - Heavy barrel waves
- **Waimea Bay, Hawaii** - Big wave spot
- **Jaws (Peahi), Maui** - Epic big wave location

## 🎨 Wave Visualization Examples

The app generates ASCII wave art that matches real conditions:

**Small Wave (3 feet):**
```
  ~~~
 ~~~ ~~~
~~~~~ ~~~~~
```

**Large Wave (6+ feet):**
```
      ~~~~~
    ~~~~~ ~~~~~
  ~~~~~ ~~~~~ ~~~~~
~~~~~ ~~~~~ ~~~~~ ~~~~~
```

## 🔍 For Recruiters

This project demonstrates:

### **Technical Skills**
- **Full-Stack Development**: Python backend + JavaScript frontend
- **API Integration**: Multiple external APIs (OpenAI, surf data)
- **Algorithm Implementation**: Sorting algorithms and quality scoring
- **Modern Web Technologies**: FastAPI, ES6+, CSS Grid
- **Error Handling**: Comprehensive error management and fallbacks

### **Software Engineering**
- **Clean Code**: Well-structured, documented code
- **Modular Design**: Separated concerns and reusable components
- **Responsive Design**: Mobile-friendly interface
- **Performance**: Optimized API calls and efficient algorithms

### **Problem Solving**
- **Real-world Application**: Practical surf analysis tool
- **Data Processing**: Complex surf condition analysis
- **User Experience**: Intuitive interface for surfers
- **Scalability**: Easy to add new locations and features

## 🛠️ Development

### Project Structure
```
SurfWave/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── start.bat          # Windows startup script
├── README.md          # This file
└── static/            # Frontend files
    ├── index.html     # Main HTML page
    ├── style.css      # CSS styling
    └── app.js         # JavaScript functionality
```

### Adding New Features
1. **New Surf Spots**: Add to `SURF_LOCATIONS` in `app.py`
2. **New Analysis Types**: Extend GPT prompts in `analyze_surf_conditions_with_gpt()`
3. **UI Enhancements**: Modify CSS in `static/style.css`
4. **Additional Algorithms**: Add new functions in `app.py`

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to contribute by:
- Adding new surf locations
- Improving wave visualization algorithms
- Enhancing the UI/UX
- Adding new analysis features

---

**🏄‍♂️ Happy Surfing!** 🌊 