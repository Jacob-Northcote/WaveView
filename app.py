from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import openai
import json
import os
from datetime import datetime
from typing import Dict, Any, List
import uvicorn
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="WaveView", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
try:
    from config import OPENAI_API_KEY, SURF_API_KEY
except ImportError:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
    SURF_API_KEY = os.getenv("SURF_API_KEY", "your-surf-api-key-here")

# OpenAI client will be initialized when needed

# Surf locations database
SURF_LOCATIONS = {
    "malibu": {
        "name": "Malibu",
        "lat": 34.0370,
        "lon": -118.6770,
        "description": "Famous point break in Southern California"
    },
    "pipeline": {
        "name": "Pipeline", 
        "lat": 21.6644,
        "lon": -158.0533,
        "description": "World-famous reef break on North Shore"
    },
    "teahupoo": {
        "name": "Teahupoo",
        "lat": -17.8444,
        "lon": -149.2672,
        "description": "Heavy reef break known for massive barrels"
    },
    "waimea": {
        "name": "Waimea Bay",
        "lat": 21.6389,
        "lon": -158.0667,
        "description": "Big wave spot on North Shore"
    },
    "jaws": {
        "name": "Jaws (Peahi)",
        "lat": 20.9333,
        "lon": -156.3000,
        "description": "Epic big wave spot on Maui"
    }
}

class SurfData(BaseModel):
    location: str
    wave_height: float
    wave_period: float
    wave_direction: str
    wind_speed: float
    wind_direction: str
    temperature: float
    tide_height: float
    swell_height: float
    swell_period: float
    swell_direction: str

def get_surf_data_from_api(location_id: str) -> Dict[str, Any]:
    """
    Fetch surf data from a free surf API
    Using Stormglass API (free tier available)
    """
    try:
        location = SURF_LOCATIONS.get(location_id)
        if not location:
            raise ValueError(f"Location {location_id} not found")
        
        # Stormglass API endpoint
        url = "https://api.stormglass.io/v2/weather/point"
        params = {
            'lat': location['lat'],
            'lng': location['lon'],
            'params': 'waveHeight,wavePeriod,waveDirection,windSpeed,windDirection,airTemperature,waterTemperature',
            'start': datetime.now().strftime('%Y-%m-%d'),
            'end': datetime.now().strftime('%Y-%m-%d')
        }
        
        headers = {'Authorization': SURF_API_KEY}
        
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract current conditions
            current = data['data'][0] if data['data'] else {}
            
            return {
                'location_name': location['name'],
                'wave_height': current.get('waveHeight', {}).get('noaa', 3.0),
                'wave_period': current.get('wavePeriod', {}).get('noaa', 10.0),
                'wave_direction': current.get('waveDirection', {}).get('noaa', 'SW'),
                'wind_speed': current.get('windSpeed', {}).get('noaa', 10.0),
                'wind_direction': current.get('windDirection', {}).get('noaa', 'NW'),
                'temperature': current.get('airTemperature', {}).get('noaa', 20.0),
                'swell_height': current.get('waveHeight', {}).get('noaa', 3.0),
                'swell_period': current.get('wavePeriod', {}).get('noaa', 10.0),
                'swell_direction': current.get('waveDirection', {}).get('noaa', 'SW'),
                'tide_height': 0.5,  # Mock tide data
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Fallback to mock data if API fails
            return generate_mock_surf_data(location)
            
    except Exception as e:
        print(f"API Error: {e}")
        # Return mock data as fallback
        return generate_mock_surf_data(SURF_LOCATIONS.get(location_id, SURF_LOCATIONS['malibu']))

def generate_mock_surf_data(location: Dict[str, Any]) -> Dict[str, Any]:
    """Generate realistic mock surf data"""
    import random
    
    wave_height = round(random.uniform(2.0, 12.0), 1)
    wave_period = round(random.uniform(8.0, 18.0), 1)
    
    return {
        'location_name': location['name'],
        'wave_height': wave_height,
        'wave_period': wave_period,
        'wave_direction': random.choice(['SW', 'W', 'NW', 'N', 'NE', 'E', 'SE', 'S']),
        'wind_speed': round(random.uniform(5.0, 25.0), 1),
        'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
        'temperature': round(random.uniform(15.0, 30.0), 1),
        'swell_height': wave_height,
        'swell_period': wave_period,
        'swell_direction': random.choice(['SW', 'W', 'NW', 'N', 'NE', 'E', 'SE', 'S']),
        'tide_height': round(random.uniform(-0.5, 2.5), 2),
        'timestamp': datetime.now().isoformat()
    }

def analyze_surf_conditions_with_gpt(surf_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use GPT API to analyze surf conditions and generate wave visualization
    """
    try:
        # Create detailed prompt for GPT
        prompt = f"""
        You are a professional surf analyst and ASCII artist. Analyze these surf conditions and create a detailed report:

        Location: {surf_data['location_name']}
        Wave Height: {surf_data['wave_height']} feet
        Wave Period: {surf_data['wave_period']} seconds
        Wave Direction: {surf_data['wave_direction']}
        Wind Speed: {surf_data['wind_speed']} mph
        Wind Direction: {surf_data['wind_direction']}
        Temperature: {surf_data['temperature']}°C
        Swell Height: {surf_data['swell_height']} feet
        Swell Period: {surf_data['swell_period']} seconds
        Swell Direction: {surf_data['swell_direction']}
        Tide: {surf_data['tide_height']} feet

        Please provide the analysis in this EXACT format:

        **WAVE VISUALIZATION:**
        [Create an ASCII wave using this style:
        
         _.====.._
      ,:._       ~-_
          `\        ~-_
            | _  _  |  `.
          ,/ /_)/ | |    ~-_
 -..__..-''  \_ \_\ `_      ~~--..__]

        **SURF ANALYSIS:**
        - Wave Quality: [analysis]
        - Difficulty Level: [analysis] 
        - Conditions: [analysis]
        - Key Insights: [recommendations]
        - Safety: [considerations]
        - Best Time: [when to surf]
        """

        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional surf analyst and ASCII artist. Provide detailed, accurate surf analysis and create proportional ASCII wave visualizations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return {
            'analysis': response.choices[0].message.content,
            'surf_data': surf_data,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"GPT API Error: {e}")
        return {
            'analysis': f"Error analyzing conditions: {str(e)}",
            'surf_data': surf_data,
            'timestamp': datetime.now().isoformat()
        }

def calculate_wave_quality(surf_data: Dict[str, Any]) -> float:
    """
    Algorithm: Calculate wave quality score using multiple factors
    This demonstrates algorithmic thinking for recruiters
    """
    score = 0.0
    
    # Wave height factor (optimal range: 3-8 feet)
    wave_height = surf_data['wave_height']
    if 3.0 <= wave_height <= 8.0:
        score += 30
    elif 2.0 <= wave_height <= 10.0:
        score += 20
    else:
        score += 10
    
    # Wave period factor (optimal range: 10-16 seconds)
    wave_period = surf_data['wave_period']
    if 10.0 <= wave_period <= 16.0:
        score += 25
    elif 8.0 <= wave_period <= 18.0:
        score += 15
    else:
        score += 5
    
    # Wind factor (lower is better for most spots)
    wind_speed = surf_data['wind_speed']
    if wind_speed <= 10.0:
        score += 25
    elif wind_speed <= 15.0:
        score += 15
    else:
        score += 5
    
    # Swell consistency factor
    swell_height = surf_data['swell_height']
    swell_period = surf_data['swell_period']
    if swell_height >= 3.0 and swell_period >= 10.0:
        score += 20
    else:
        score += 10
    
    return min(score, 100.0)  # Cap at 100

def sort_surf_spots_by_conditions() -> List[Dict[str, Any]]:
    """
    Algorithm: Sort surf spots by current conditions
    Demonstrates sorting algorithm implementation
    """
    spots_data = []
    
    for location_id in SURF_LOCATIONS.keys():
        try:
            surf_data = get_surf_data_from_api(location_id)
            quality_score = calculate_wave_quality(surf_data)
            
            spots_data.append({
                'location_id': location_id,
                'location_name': surf_data['location_name'],
                'wave_height': surf_data['wave_height'],
                'quality_score': quality_score,
                'surf_data': surf_data
            })
        except Exception as e:
            print(f"Error getting data for {location_id}: {e}")
    
    # Sort by quality score (bubble sort for demonstration)
    n = len(spots_data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if spots_data[j]['quality_score'] < spots_data[j + 1]['quality_score']:
                spots_data[j], spots_data[j + 1] = spots_data[j + 1], spots_data[j]
    
    return spots_data

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.get("/api/locations")
async def get_locations():
    """Get all available surf locations"""
    return {
        "locations": list(SURF_LOCATIONS.keys()),
        "location_data": SURF_LOCATIONS
    }

@app.get("/api/surf-data/{location_id}")
async def get_surf_data(location_id: str):
    """Get surf data for a specific location"""
    try:
        surf_data = get_surf_data_from_api(location_id)
        return surf_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/{location_id}")
async def get_surf_analysis(location_id: str):
    """Get GPT analysis for surf conditions"""
    try:
        surf_data = get_surf_data_from_api(location_id)
        analysis = analyze_surf_conditions_with_gpt(surf_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rankings")
async def get_surf_rankings():
    """Get surf spots ranked by current conditions"""
    try:
        rankings = sort_surf_spots_by_conditions()
        return {
            "rankings": rankings,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
