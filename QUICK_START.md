# 🚀 Quick Start Guide

## เริ่มใช้งานภายใน 5 นาที!

### ขั้นตอนที่ 1: ติดตั้ง Dependencies (ครั้งเดียว)

```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
pip install -r requirements.txt
```

### ขั้นตอนที่ 2: Start Database

```bash
# ใช้ Docker (แนะนำ)
docker-compose up -d

# รอ database พร้อม (~10 วินาที)
```

### ขั้นตอนที่ 3: Import Sample Data

```bash
cd database
python import_sample_data.py
```

### ขั้นตอนที่ 4: Setup Environment

```bash
# Backend
cd ../backend
copy .env.example .env

# Frontend  
cd ../frontend
copy .env.example .env
```

### ขั้นตอนที่ 5: Start Services

เปิด 2 terminals:

**Terminal 1 - Backend:**
```bash
cd backend
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### ขั้นตอนที่ 6: เปิด Browser

ไปที่: **http://localhost:3000**

---

## 🎯 คุณจะเห็น:

- 🗺️ Satellite map ของ Bangkok
- 🏢 100 sample buildings (สีต่างๆ ตาม confidence)
- 📊 Buildings Data panel (แสดงจำนวน buildings)
- 🎨 Confidence Level legend

## 🖱️ การใช้งาน:

1. **Zoom/Pan** - เลื่อนดู map
2. **Click building** - ดูรายละเอียดและ solar potential
3. **Solar Analysis** - คำนวณอัตโนมัติ:
   - System size (kW)
   - Annual production (kWh)
   - Installation cost (THB)
   - Payback period (years)
   - CO₂ reduction (kg/year)

## 📈 ใช้ Full Dataset (1.88M buildings)

1. ดาวน์โหลดจาก: https://sites.research.google/open-buildings/
2. เลือก Thailand → Bangkok
3. รัน import script:
```bash
python import_full_data.py --file path/to/file.csv
```

## ❓ มีปัญหา?

### Database ไม่เชื่อมต่อ
```bash
# ตรวจสอบ Docker
docker ps

# Restart database
docker-compose restart postgres
```

### Frontend ไม่แสดง buildings
```bash
# ตรวจสอบ Backend API
curl http://localhost:8001/stats

# ตรวจสอบ database
docker exec -it nabha-solar-db psql -U postgres -d nabha_solar -c "SELECT COUNT(*) FROM buildings;"
```

### Port ถูกใช้งานแล้ว
- Frontend (3000): แก้ใน `package.json` → `"start": "PORT=3001 react-scripts start"`
- Backend (8001): แก้ใน `api.py` → `uvicorn.run(app, host="127.0.0.1", port=8002)`
- Database (5432): แก้ใน `docker-compose.yml` → `ports: - "5433:5432"`

---

## 🎉 เสร็จแล้ว!

ตอนนี้คุณมี Buildings Map พร้อม Solar Potential Calculator ที่ทำงานได้แล้ว!
