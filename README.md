# 🏢 Nabha Solar Dashboard - Buildings Map

แดชบอร์ดแสดงข้อมูล building footprints จาก Google Open Buildings พร้อมคำนวณ solar potential

## 📋 ความต้องการระบบ

- **Node.js** 16+ (สำหรับ Frontend)
- **Python** 3.9+ (สำหรับ Backend API)
- **PostgreSQL** 14+ with PostGIS (สำหรับ Database)
- **Docker Desktop** (แนะนำ - สำหรับรัน database ง่ายๆ)

## 🚀 วิธีติดตั้งและรัน

### ขั้นตอนที่ 1: ติดตั้ง Dependencies

#### Frontend
```bash
cd frontend
npm install
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
```

### ขั้นตอนที่ 2: Setup Database

#### ใช้ Docker (แนะนำ)
```bash
docker-compose up -d
```

#### หรือติดตั้ง PostgreSQL เอง
1. ติดตั้ง PostgreSQL 14+
2. ติดตั้ง PostGIS extension
3. สร้าง database:
```sql
CREATE DATABASE nabha_solar;
\c nabha_solar
CREATE EXTENSION postgis;
```

### ขั้นตอนที่ 3: Import ข้อมูล Buildings

#### ตัวเลือก A: ใช้ Sample Data (100 buildings)
```bash
cd database
python import_sample_data.py
```

#### ตัวเลือก B: Download Full Dataset (1.88M buildings)
1. ดาวน์โหลดจาก Google Open Buildings: https://sites.research.google/open-buildings/
2. เลือกพื้นที่ Thailand
3. รัน import script:
```bash
python import_full_data.py --file path/to/downloaded/file.csv
```

### ขั้นตอนที่ 4: รัน Services

#### Terminal 1: Start Backend API
```bash
cd backend
python api.py
```
API จะรันที่: http://localhost:8001

#### Terminal 2: Start Frontend
```bash
cd frontend
npm start
```
Frontend จะรันที่: http://localhost:3000

### ขั้นตอนที่ 5: เปิด Browser

ไปที่ http://localhost:3000 เพื่อดู Buildings Map

## 📊 Features

- ✅ แสดง building footprints บน satellite map
- ✅ สี buildings ตาม confidence level
- ✅ คำนวณ solar potential สำหรับแต่ละ building
- ✅ แสดงข้อมูล area, confidence, location
- ✅ ประมาณการค่าติดตั้ง solar panels
- ✅ คำนวณ payback period

## 🗂️ โครงสร้างโปรเจค

```
sushi/
├── frontend/           # React application
│   ├── src/
│   │   ├── components/
│   │   │   └── BuildingsMap.jsx
│   │   └── services/
│   │       └── buildingsAPI.js
│   └── package.json
├── backend/            # FastAPI application
│   ├── api.py
│   └── requirements.txt
├── database/           # Database scripts
│   ├── init.sql
│   ├── import_sample_data.py
│   └── sample_data.csv
├── docker-compose.yml  # Docker setup
└── README.md
```

## 🔧 Configuration

### Environment Variables

สร้างไฟล์ `.env` ใน `frontend/`:
```
REACT_APP_BUILDINGS_API_URL=http://localhost:8001
```

สร้างไฟล์ `.env` ใน `backend/`:
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=nabha_solar_2024
DB_NAME=nabha_solar
```

## 📈 ข้อมูล

### Sample Data (รวมอยู่ในโปรเจค)
- 100 buildings ในพื้นที่ Bangkok
- พร้อมใช้งานทันที
- เหมาะสำหรับ demo และทดสอบ

### Full Dataset (ต้องดาวน์โหลดเอง)
- 1.88M buildings ในพื้นที่ Bangkok Metropolitan
- ขนาดไฟล์: ~275 MB (Parquet format)
- ดาวน์โหลดจาก: https://sites.research.google/open-buildings/

## 🐛 Troubleshooting

### Database connection error
- ตรวจสอบว่า PostgreSQL รันอยู่
- ตรวจสอบ username/password ใน `.env`
- ตรวจสอบว่าติดตั้ง PostGIS extension แล้ว

### Frontend ไม่แสดง buildings
- ตรวจสอบว่า Backend API รันอยู่ที่ port 8001
- เปิด Browser Console ดู error messages
- ตรวจสอบว่า import ข้อมูลเข้า database แล้ว

### API ช้า
- ลด `limit` parameter ใน API calls
- เพิ่ม indexes ใน database
- ใช้ sample data แทน full dataset

## 📝 License

MIT License - ใช้งานได้อย่างอิสระ

## 👥 Support

หากมีปัญหาหรือคำถาม:
1. ตรวจสอบ Troubleshooting section
2. ดู logs ใน terminal
3. ติดต่อทีมพัฒนา

## 🎉 เริ่มต้นใช้งาน

```bash
# Quick Start (ใช้ Docker)
docker-compose up -d
cd backend && python api.py &
cd frontend && npm start
```

เปิด browser ที่ http://localhost:3000 และเริ่มใช้งาน!
