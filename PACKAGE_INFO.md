# 📦 Nabha Solar Buildings Map - Package Information

## 🎯 สิ่งที่อยู่ใน Package นี้

### 1. Frontend (React Application)
- **Path:** `frontend/`
- **Tech:** React 18, Leaflet, Lucide Icons
- **Features:**
  - Interactive satellite map
  - Building footprints visualization
  - Solar potential calculator
  - Confidence level indicators

### 2. Backend (FastAPI)
- **Path:** `backend/`
- **Tech:** Python 3.9+, FastAPI, PostgreSQL
- **Endpoints:**
  - `/stats` - Database statistics
  - `/buildings/bbox` - Get buildings in bounding box
  - `/buildings/nearby` - Get buildings near a point
  - `/buildings/{id}` - Get building details

### 3. Database (PostgreSQL + PostGIS)
- **Setup:** Docker Compose
- **Schema:** Buildings table with spatial indexes
- **Data:** Sample data (100 buildings) included

### 4. Documentation
- `README.md` - Full documentation
- `QUICK_START.md` - 5-minute setup guide
- `DATA_GUIDE.md` - Data options and import guide
- `PACKAGE_INFO.md` - This file

### 5. Scripts
- `start-all.bat` - Start all services (Windows)
- `database/import_sample_data.py` - Import sample data
- `docker-compose.yml` - Database setup

---

## 📋 System Requirements

### Minimum
- **OS:** Windows 10/11, macOS, Linux
- **RAM:** 4 GB
- **Disk:** 2 GB free space
- **Software:**
  - Node.js 16+
  - Python 3.9+
  - Docker Desktop

### Recommended
- **RAM:** 8 GB+
- **Disk:** 10 GB+ (for full dataset)
- **Internet:** For downloading full dataset

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

### Step 2: Start Database & Import Data
```bash
docker-compose up -d
cd database && python import_sample_data.py
```

### Step 3: Start Services
```bash
# Windows
start-all.bat

# Or manually:
cd backend && python api.py
cd frontend && npm start
```

**Open:** http://localhost:3000

---

## 📊 Data Options

### Option 1: Sample Data (Included) ✅
- 100 buildings
- Ready to use
- Perfect for demo

### Option 2: Full Dataset (Download Required)
- 1.88M buildings
- Real data from Google Open Buildings
- See `DATA_GUIDE.md` for instructions

---

## 🎨 Features

### Map Features
- ✅ Satellite imagery (Esri World Imagery)
- ✅ Building footprints with colors by confidence
- ✅ Interactive zoom/pan
- ✅ Click buildings for details

### Solar Calculator
- ✅ Usable roof area calculation
- ✅ System size estimation (kW)
- ✅ Annual energy production (kWh)
- ✅ Installation cost (THB)
- ✅ Payback period (years)
- ✅ CO₂ reduction (kg/year)

### Data Display
- ✅ Buildings count in view
- ✅ Confidence level legend
- ✅ Building properties (area, confidence, location)

---

## 🔧 Configuration

### Environment Variables

**Backend** (`backend/.env`):
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=nabha_solar_2024
DB_NAME=nabha_solar
```

**Frontend** (`frontend/.env`):
```
REACT_APP_BUILDINGS_API_URL=http://localhost:8001
```

### Ports
- Frontend: 3000
- Backend: 8001
- Database: 5432
- pgAdmin: 5050 (optional)

---

## 📁 File Structure

```
sushi/
├── README.md                    # Full documentation
├── QUICK_START.md               # Quick setup guide
├── DATA_GUIDE.md                # Data import guide
├── PACKAGE_INFO.md              # This file
├── docker-compose.yml           # Database setup
├── start-all.bat                # Windows start script
│
├── frontend/                    # React application
│   ├── src/
│   │   ├── components/
│   │   │   └── BuildingsMap.jsx
│   │   └── services/
│   │       └── buildingsAPI.js
│   ├── package.json
│   └── .env.example
│
├── backend/                     # FastAPI application
│   ├── api.py
│   ├── requirements.txt
│   └── .env.example
│
└── database/                    # Database scripts
    ├── init.sql
    └── import_sample_data.py
```

---

## 🐛 Troubleshooting

### Database won't start
```bash
docker-compose down
docker-compose up -d
```

### Frontend shows no buildings
1. Check Backend is running: http://localhost:8001/stats
2. Check database has data: `docker exec -it nabha-solar-db psql -U postgres -d nabha_solar -c "SELECT COUNT(*) FROM buildings;"`
3. Check browser console for errors

### Port already in use
- Change ports in `docker-compose.yml` and `.env` files

---

## 📝 License

MIT License - Free to use for any purpose

---

## 🎉 Ready to Share!

This package contains everything needed to run the Buildings Map:
- ✅ Complete source code
- ✅ Sample data (100 buildings)
- ✅ Documentation
- ✅ Setup scripts
- ✅ Docker configuration

**Recipients can:**
1. Extract the package
2. Follow QUICK_START.md
3. Have a working system in 5 minutes!

**For full dataset (1.88M buildings):**
- Follow instructions in DATA_GUIDE.md
- Download from Google Open Buildings
- Import using provided scripts

---

## 📞 Support

For issues or questions:
1. Check README.md
2. Check QUICK_START.md
3. Check DATA_GUIDE.md
4. Review error logs in terminal

---

**Package Version:** 1.0.0  
**Last Updated:** March 2026  
**Tested On:** Windows 11, Node.js 18, Python 3.11
