/**
 * Buildings API Service
 * Access to 1.88M building footprints from Google Open Buildings
 */

const API_BASE_URL = process.env.REACT_APP_BUILDINGS_API_URL || 'http://localhost:8001';

console.log('🔧 API Configuration:', {
  API_BASE_URL,
  env: process.env.REACT_APP_BUILDINGS_API_URL
});

/**
 * Get API statistics
 */
export const getBuildingsStats = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return await response.json();
  } catch (error) {
    console.error('Error fetching buildings stats:', error);
    throw error;
  }
};

/**
 * Get buildings within bounding box
 * @param {Object} bbox - {minLat, maxLat, minLon, maxLon}
 * @param {Object} options - {limit, minConfidence}
 */
export const getBuildingsInBBox = async (bbox, options = {}) => {
  const {
    limit = 1000,
    minConfidence = 0.7
  } = options;

  try {
    const params = new URLSearchParams({
      min_lat: bbox.minLat,
      max_lat: bbox.maxLat,
      min_lon: bbox.minLon,
      max_lon: bbox.maxLon,
      limit,
      min_confidence: minConfidence
    });

    const url = `${API_BASE_URL}/buildings/bbox?${params}`;
    console.log('🔗 Fetching from:', url);
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors'
    });
    
    if (!response.ok) {
      console.error('❌ API Error:', response.status, response.statusText);
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log('✅ Data received:', data.buildings?.length, 'buildings');
    
    // Parse GeoJSON geometries safely
    if (data.buildings) {
      data.buildings = data.buildings.map(building => {
        try {
          return {
            ...building,
            geometry: typeof building.geometry === 'string' ? 
              JSON.parse(building.geometry) : 
              building.geometry
          };
        } catch (e) {
          console.warn('Failed to parse geometry for building', building.id, e);
          return { ...building, geometry: null };
        }
      });
    }
    
    return data;
  } catch (error) {
    console.error('❌ Error fetching buildings in bbox:', error);
    throw error;
  }
};

/**
 * Get buildings near a point
 * @param {number} lat - Latitude
 * @param {number} lon - Longitude
 * @param {Object} options - {radiusM, limit, minConfidence}
 */
export const getBuildingsNearby = async (lat, lon, options = {}) => {
  const {
    radiusM = 500,
    limit = 100,
    minConfidence = 0.7
  } = options;

  try {
    const params = new URLSearchParams({
      lat,
      lon,
      radius_m: radiusM,
      limit,
      min_confidence: minConfidence
    });

    const response = await fetch(`${API_BASE_URL}/buildings/nearby?${params}`);
    if (!response.ok) throw new Error('Failed to fetch nearby buildings');
    
    const data = await response.json();
    
    // Parse GeoJSON geometries
    data.buildings = data.buildings.map(building => ({
      ...building,
      geometry: building.geometry ? JSON.parse(building.geometry) : null
    }));
    
    return data;
  } catch (error) {
    console.error('Error fetching nearby buildings:', error);
    throw error;
  }
};

/**
 * Get building details by ID
 * @param {number} buildingId - Building ID
 */
export const getBuildingDetail = async (buildingId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/buildings/${buildingId}`);
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Building not found');
      }
      throw new Error('Failed to fetch building details');
    }
    
    const building = await response.json();
    
    // Parse GeoJSON
    if (building.geometry) {
      building.geometry = JSON.parse(building.geometry);
    }
    if (building.centroid) {
      building.centroid = JSON.parse(building.centroid);
    }
    
    return building;
  } catch (error) {
    console.error('Error fetching building detail:', error);
    throw error;
  }
};

/**
 * Convert buildings to GeoJSON FeatureCollection
 * @param {Array} buildings - Array of buildings
 */
export const buildingsToGeoJSON = (buildings) => {
  return {
    type: 'FeatureCollection',
    features: buildings.map(building => ({
      type: 'Feature',
      id: building.id,
      geometry: building.geometry,
      properties: {
        id: building.id,
        open_buildings_id: building.open_buildings_id,
        area_m2: building.area_m2,
        confidence: building.confidence,
        latitude: building.latitude,
        longitude: building.longitude,
        distance_m: building.distance_m
      }
    }))
  };
};

/**
 * Calculate solar potential for a building
 * @param {Object} building - Building object
 * @param {Object} solarData - Solar irradiance data
 */
export const calculateBuildingSolarPotential = (building, solarData = {}) => {
  const {
    area_m2,
    confidence
  } = building;

  // Default solar parameters for Bangkok
  const avgIrradiance = solarData.avgIrradiance || 5.5; // kWh/m²/day
  const systemEfficiency = 0.75; // 75%
  const usableRoofArea = area_m2 * 0.6; // 60% of roof is usable
  const panelEfficiency = 0.20; // 20% panel efficiency

  // Annual energy production (kWh/year)
  const annualProduction = usableRoofArea * avgIrradiance * 365 * systemEfficiency * panelEfficiency;

  // System size (kW)
  const systemSize = usableRoofArea * panelEfficiency;

  // Cost estimation (THB)
  const costPerWatt = 35; // THB/W
  const installationCost = systemSize * 1000 * costPerWatt;

  // Savings (THB/year) - assuming 4 THB/kWh
  const electricityRate = 4;
  const annualSavings = annualProduction * electricityRate;

  // Payback period (years)
  const paybackPeriod = installationCost / annualSavings;

  return {
    usableRoofArea: Math.round(usableRoofArea),
    systemSize: Math.round(systemSize * 10) / 10,
    annualProduction: Math.round(annualProduction),
    installationCost: Math.round(installationCost),
    annualSavings: Math.round(annualSavings),
    paybackPeriod: Math.round(paybackPeriod * 10) / 10,
    confidence: Math.round(confidence * 100),
    co2Reduction: Math.round(annualProduction * 0.5) // kg CO2/year
  };
};

export default {
  getBuildingsStats,
  getBuildingsInBBox,
  getBuildingsNearby,
  getBuildingDetail,
  buildingsToGeoJSON,
  calculateBuildingSolarPotential
};
