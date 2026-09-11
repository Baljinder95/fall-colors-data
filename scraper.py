#!/usr/bin/env python3
"""
Ontario Parks Fall Colours Web Scraper
Extracts park data from https://www.ontarioparks.ca/fallcolour
Updates parks_data.json with real-time fall colour information
"""

import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

# Park coordinates (lat, lng, distance from Brampton in minutes)
PARK_COORDS = {
    "Algonquin": {"lat": 45.90, "lng": -78.50, "distance": 45},
    "Arrowhead": {"lat": 45.15, "lng": -79.35, "distance": 60},
    "Awenda": {"lat": 44.95, "lng": -79.60, "distance": 80},
    "Balsam Lake": {"lat": 44.40, "lng": -79.25, "distance": 70},
    "Bass Lake": {"lat": 46.40, "lng": -87.90, "distance": 160},
    "Batchawana Bay": {"lat": 46.80, "lng": -84.50, "distance": 200},
    "Bon Echo": {"lat": 44.90, "lng": -77.10, "distance": 85},
    "Bonnechere": {"lat": 45.45, "lng": -77.80, "distance": 95},
    "Bronte Creek": {"lat": 43.30, "lng": -79.70, "distance": 25},
    "Caliper Lake": {"lat": 45.05, "lng": -78.30, "distance": 65},
    "Charleston Lake": {"lat": 44.70, "lng": -76.30, "distance": 110},
    "Craigleith": {"lat": 44.20, "lng": -80.25, "distance": 90},
    "Darlington": {"lat": 43.85, "lng": -79.05, "distance": 35},
    "Earl Rowe": {"lat": 44.60, "lng": -80.20, "distance": 85},
    "Finlayson Point": {"lat": 46.80, "lng": -81.30, "distance": 140},
    "Forks of the Credit": {"lat": 43.80, "lng": -80.20, "distance": 35},
    "French River": {"lat": 45.70, "lng": -80.80, "distance": 115},
    "Frontenac": {"lat": 44.90, "lng": -76.35, "distance": 130},
    "Grundy Lake": {"lat": 45.25, "lng": -80.35, "distance": 105},
    "Halfway Lake": {"lat": 46.50, "lng": -81.50, "distance": 120},
    "Inverhuron": {"lat": 44.00, "lng": -81.45, "distance": 110},
    "Kakabeka Falls": {"lat": 48.40, "lng": -89.60, "distance": 200},
    "Kap-Kig-Iwan": {"lat": 46.70, "lng": -81.70, "distance": 130},
    "Kawartha Highlands": {"lat": 44.85, "lng": -78.70, "distance": 75},
    "Kettle Lakes": {"lat": 48.20, "lng": -87.00, "distance": 240},
    "Killarney": {"lat": 46.10, "lng": -81.30, "distance": 90},
    "Killbear": {"lat": 45.20, "lng": -80.40, "distance": 95},
    "Komoka": {"lat": 42.95, "lng": -81.30, "distance": 95},
    "Lake on the Mountain": {"lat": 43.90, "lng": -77.80, "distance": 125},
    "Lake St. Peter": {"lat": 44.55, "lng": -77.65, "distance": 115},
    "Lake Superior - North": {"lat": 47.80, "lng": -87.50, "distance": 180},
    "Lake Superior - South": {"lat": 47.30, "lng": -85.00, "distance": 200},
    "Long Point": {"lat": 42.55, "lng": -80.35, "distance": 105},
    "MacGregor Point": {"lat": 44.70, "lng": -81.20, "distance": 115},
    "Mark S. Burnham": {"lat": 43.65, "lng": -79.50, "distance": 50},
    "Marten River": {"lat": 46.50, "lng": -81.00, "distance": 130},
    "Mikisew": {"lat": 46.30, "lng": -81.90, "distance": 140},
    "Misery Bay": {"lat": 45.50, "lng": -81.70, "distance": 125},
    "Missinaibi": {"lat": 48.60, "lng": -86.30, "distance": 240},
    "Mississagi": {"lat": 46.50, "lng": -84.00, "distance": 180},
    "Mono Cliffs": {"lat": 43.95, "lng": -80.05, "distance": 50},
    "Murphys Point": {"lat": 44.90, "lng": -76.35, "distance": 135},
    "Neys": {"lat": 48.20, "lng": -87.30, "distance": 250},
    "Oastler Lake": {"lat": 45.90, "lng": -81.50, "distance": 115},
    "Oxtongue River - Ragged Falls": {"lat": 45.60, "lng": -78.70, "distance": 60},
    "Pancake Bay": {"lat": 47.50, "lng": -85.50, "distance": 220},
    "Petroglyphs": {"lat": 44.80, "lng": -77.50, "distance": 120},
    "Pigeon River": {"lat": 47.85, "lng": -87.70, "distance": 290},
    "Pinery": {"lat": 43.20, "lng": -81.75, "distance": 125},
    "Point Farms": {"lat": 44.00, "lng": -81.90, "distance": 120},
    "Port Burwell": {"lat": 42.65, "lng": -80.60, "distance": 100},
    "Port Bruce": {"lat": 42.70, "lng": -80.80, "distance": 100},
    "Presqu'ile": {"lat": 43.85, "lng": -77.70, "distance": 130},
    "Quetico": {"lat": 49.50, "lng": -90.70, "distance": 370},
    "Rainbow Falls": {"lat": 47.80, "lng": -87.70, "distance": 185},
    "Restoule": {"lat": 45.60, "lng": -79.30, "distance": 95},
    "Rideau River": {"lat": 45.25, "lng": -76.00, "distance": 150},
    "Rock Point": {"lat": 42.85, "lng": -80.25, "distance": 100},
    "Rondeau": {"lat": 42.30, "lng": -81.85, "distance": 155},
    "Rushing River": {"lat": 49.75, "lng": -93.70, "distance": 380},
    "Samuel de Champlain": {"lat": 45.65, "lng": -75.70, "distance": 140},
    "Sandbanks": {"lat": 43.80, "lng": -77.55, "distance": 135},
    "Sauble Falls": {"lat": 44.50, "lng": -80.75, "distance": 110},
    "Selkirk": {"lat": 43.70, "lng": -80.40, "distance": 65},
    "Sharbot Lake": {"lat": 44.65, "lng": -76.70, "distance": 125},
    "Sibbald Point": {"lat": 44.20, "lng": -79.40, "distance": 55},
    "Silent Lake": {"lat": 44.70, "lng": -78.00, "distance": 75},
    "Silver Lake": {"lat": 46.20, "lng": -81.40, "distance": 120},
    "Sioux Narrows": {"lat": 49.80, "lng": -93.60, "distance": 380},
    "Six Mile Lake": {"lat": 45.10, "lng": -79.50, "distance": 80},
    "Sleeping Giant": {"lat": 48.35, "lng": -89.25, "distance": 210},
    "Sturgeon Bay": {"lat": 45.50, "lng": -81.00, "distance": 120},
    "Sturgeon River": {"lat": 47.60, "lng": -81.50, "distance": 145},
    "The Massasauga": {"lat": 45.30, "lng": -80.30, "distance": 100},
    "Turkey Point": {"lat": 42.70, "lng": -80.35, "distance": 100},
    "Uxbridge Urban": {"lat": 44.10, "lng": -79.15, "distance": 50},
    "Voyageur": {"lat": 45.40, "lng": -75.70, "distance": 145},
    "Wabakimi": {"lat": 49.60, "lng": -87.60, "distance": 300},
    "Wasaga Beach": {"lat": 44.50, "lng": -80.65, "distance": 100},
    "Wheatley": {"lat": 42.10, "lng": -82.40, "distance": 165},
    "White Lake": {"lat": 45.80, "lng": -78.30, "distance": 75},
}

def scrape_ontario_parks():
    """Scrape fall colours data from Ontario Parks website"""
    url = "https://www.ontarioparks.ca/fallcolour"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        parks_data = {}
        
        # Parse each park entry (they appear to be separated by <hr> tags)
        # Look for patterns like "Park Name - Report Date: ..."
        text_content = soup.get_text()
        
        # Split by park entries
        lines = text_content.split('\n')
        
        current_park = None
        park_info = {}
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for park name and report date
            if ' - ' in line and 'Report Date' in line:
                # Save previous park if exists
                if current_park and current_park in PARK_COORDS:
                    parks_data[current_park] = park_info
                
                # Parse new park entry
                parts = line.split(' - ')
                current_park = parts[0].strip()
                
                park_info = {
                    "name": current_park,
                    "colorChange": 0,
                    "leafFall": 0,
                    "dominantColour": "Green",
                    "reportDate": "",
                    "bestViewing": ""
                }
                
                # Extract report date
                date_match = re.search(r'Report Date\s*:\s*(\w+\s+\d+,\s+\d+)', line)
                if date_match:
                    park_info["reportDate"] = date_match.group(1)
            
            # Look for Dominant Colour
            if 'Dominant Colour' in line and ':' in line:
                colour = line.split(':')[-1].strip()
                if current_park:
                    park_info["dominantColour"] = colour
            
            # Look for Colour Change and Leaf Fall
            if 'Colour Change' in line and 'Leaf Fall' in line:
                # Extract percentages
                change_match = re.search(r'Colour Change\s*:\s*(\d+)', line)
                fall_match = re.search(r'Leaf Fall\s*:\s*(\d+)', line)
                
                if change_match and current_park:
                    park_info["colorChange"] = int(change_match.group(1))
                if fall_match and current_park:
                    park_info["leafFall"] = int(fall_match.group(1))
            
            # Look for Best viewing
            if 'Best viewing' in line and ':' in line:
                viewing = line.split(':', 1)[-1].strip()
                if current_park and viewing:
                    park_info["bestViewing"] = viewing[:200]  # Limit length
        
        # Save last park
        if current_park and current_park in PARK_COORDS:
            parks_data[current_park] = park_info
        
        # Add coordinates to parks that have data
        for park_name in list(parks_data.keys()):
            if park_name in PARK_COORDS:
                parks_data[park_name].update(PARK_COORDS[park_name])
        
        return parks_data
    
    except Exception as e:
        print(f"Error scraping Ontario Parks: {e}")
        return {}

def save_parks_data(parks_data):
    """Save parks data to JSON file"""
    output = {
        "parks": parks_data,
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "totalParks": len(parks_data),
        "source": "https://www.ontarioparks.ca/fallcolour"
    }
    
    with open("parks_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Updated parks_data.json with {len(parks_data)} parks")
    print(f"Last updated: {output['lastUpdated']}")

if __name__ == "__main__":
    print("Starting scraper...")
    parks_data = scrape_ontario_parks()
    
    if parks_data:
        save_parks_data(parks_data)
        print(f"Success! Scraped {len(parks_data)} parks")
    else:
        print("No parks data found")
