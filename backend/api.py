"""
Buildings API - Google Open Buildings Integration
Provides access to 1.88M building footprints in Bangkok
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Nabha Solar Buildings API")

# CORS - Allow all origins including AWS CloudFront
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins for production
        "https://d21iw00krs7100.cloudfront.net",  # AWS CloudFront
        "https://nabha-solar-dashboard-frontend.s3-website-us-east-1.amazonaws.com",  # S3 direct
        "http://localhost:3000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
# Use DATABASE_URL from environment (for Railway/Supabase) or fallback to local config
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Production mode (Railway/Supabase) - use connection string
    DB_CONFIG = DATABASE_URL
else:
    # Development mode (local) - use config dict
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'nabha_solar_2024'),
        'database': os.getenv('DB_NAME', 'nabha_solar')
    }

def get_db_connection():
    """Create database connection"""
    if isinstance(DB_CONFIG, str):
        # Production: Use connection string
        return psycopg2.connect(DB_CONFIG, cursor_factory=RealDictCursor)
    else:
        # Development: Use config dict
        return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# Models
class Building(BaseModel):
    id: int
    open_buildings_id: str
    latitude: float
    longitude: float
    area_m2: float
    confidence: float
    geometry: Optional[str] = None

class BuildingsResponse(BaseModel):
    total: int
    buildings: List[Building]

class BoundingBox(BaseModel):
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float

# Endpoints

@app.get("/")
def root():
    """API info"""
    return {
        "name": "Nabha Solar Buildings API",
        "version": "1.0.0",
        "buildings": "1.88M in Bangkok",
        "endpoints": {
            "/buildings/bbox": "Get buildings in bounding box",
            "/buildings/nearby": "Get buildings near a point",
            "/buildings/{id}": "Get building details",
            "/stats": "Get database statistics"
        }
    }

@app.get("/stats")
def get_stats():
    """Get database statistics (cached)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Single query for all stats (faster)
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(confidence) as avg_confidence,
                MIN(confidence) as min_confidence,
                MAX(confidence) as max_confidence,
                AVG(area_m2) as avg_area,
                MIN(area_m2) as min_area,
                MAX(area_m2) as max_area,
                MIN(latitude) as min_lat,
                MAX(latitude) as max_lat,
                MIN(longitude) as min_lon,
                MAX(longitude) as max_lon
            FROM buildings;
        """)
        stats = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return {
            "total_buildings": stats['total'],
            "confidence": {
                "average": round(stats['avg_confidence'], 3),
                "min": round(stats['min_confidence'], 3),
                "max": round(stats['max_confidence'], 3)
            },
            "area_m2": {
                "average": round(stats['avg_area'], 1),
                "min": round(stats['min_area'], 1),
                "max": round(stats['max_area'], 1)
            },
            "extent": {
                "latitude": [stats['min_lat'], stats['max_lat']],
                "longitude": [stats['min_lon'], stats['max_lon']]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/buildings/bbox", response_model=BuildingsResponse)
def get_buildings_in_bbox(
    min_lat: float = Query(..., description="Minimum latitude"),
    max_lat: float = Query(..., description="Maximum latitude"),
    min_lon: float = Query(..., description="Minimum longitude"),
    max_lon: float = Query(..., description="Maximum longitude"),
    limit: int = Query(1000, le=5000, description="Max results"),
    min_confidence: float = Query(0.7, description="Minimum confidence")
):
    """Get buildings within bounding box"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT 
                id,
                open_buildings_id,
                latitude,
                longitude,
                area_m2,
                confidence,
                ST_AsGeoJSON(geometry) as geometry
            FROM buildings
            WHERE 
                latitude BETWEEN %s AND %s
                AND longitude BETWEEN %s AND %s
                AND confidence >= %s
            ORDER BY area_m2 DESC
            LIMIT %s;
        """
        
        cur.execute(query, (min_lat, max_lat, min_lon, max_lon, min_confidence, limit))
        buildings = cur.fetchall()
        
        # Count total
        count_query = """
            SELECT COUNT(*) as total
            FROM buildings
            WHERE 
                latitude BETWEEN %s AND %s
                AND longitude BETWEEN %s AND %s
                AND confidence >= %s;
        """
        cur.execute(count_query, (min_lat, max_lat, min_lon, max_lon, min_confidence))
        total = cur.fetchone()['total']
        
        cur.close()
        conn.close()
        
        return {
            "total": total,
            "buildings": buildings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/buildings/nearby", response_model=BuildingsResponse)
def get_buildings_nearby(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius_m: float = Query(500, description="Radius in meters"),
    limit: int = Query(100, le=1000),
    min_confidence: float = Query(0.7)
):
    """Get buildings near a point"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT 
                id,
                open_buildings_id,
                latitude,
                longitude,
                area_m2,
                confidence,
                ST_AsGeoJSON(geometry) as geometry,
                ST_Distance(
                    centroid::geography,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
                ) as distance_m
            FROM buildings
            WHERE 
                ST_DWithin(
                    centroid::geography,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                    %s
                )
                AND confidence >= %s
            ORDER BY distance_m
            LIMIT %s;
        """
        
        cur.execute(query, (lon, lat, lon, lat, radius_m, min_confidence, limit))
        buildings = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return {
            "total": len(buildings),
            "buildings": buildings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/buildings/{building_id}")
def get_building_detail(building_id: int):
    """Get detailed building information"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT 
                id,
                open_buildings_id,
                latitude,
                longitude,
                area_m2,
                confidence,
                ST_AsGeoJSON(geometry) as geometry,
                ST_AsGeoJSON(centroid) as centroid,
                created_at
            FROM buildings
            WHERE id = %s;
        """
        
        cur.execute(query, (building_id,))
        building = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
        
        return building
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/buildings/search/address")
def search_by_address(
    address: str = Query(..., description="Address to search"),
    limit: int = Query(10, le=100)
):
    """Search buildings by address (placeholder - requires geocoding)"""
    return {
        "message": "Address search requires geocoding service",
        "suggestion": "Use /buildings/nearby with coordinates instead"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
