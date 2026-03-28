# 📊 Data Guide - คู่มือข้อมูล Buildings

## 🎯 ตัวเลือกข้อมูล

### Option 1: Sample Data (รวมอยู่ในโปรเจค) ✅ แนะนำสำหรับเริ่มต้น

**ข้อมูล:**
- 100 buildings สุ่มในพื้นที่ Bangkok
- Generate อัตโนมัติด้วย Python script
- พร้อมใช้งานทันที

**วิธีใช้:**
```bash
cd database
python import_sample_data.py
```

**ข้อดี:**
- ✅ ไม่ต้องดาวน์โหลดอะไร
- ✅ รันได้ทันที
- ✅ เหมาะสำหรับ demo และทดสอบ
- ✅ ขนาดเล็ก รันเร็ว

**ข้อเสีย:**
- ❌ ข้อมูลไม่ใช่ของจริง
- ❌ จำนวนน้อย (100 buildings)

---

### Option 2: Full Dataset (ต้องดาวน์โหลด) 🚀 แนะนำสำหรับ Production

**ข้อมูล:**
- 1.88M buildings จริงในพื้นที่ Bangkok Metropolitan
- จาก Google Open Buildings V3
- ข้อมูล ML-detected building footprints

**ขนาดไฟล์:**
- Raw CSV: ~2-3 GB
- Processed Parquet: ~275 MB
- Database: ~500 MB

**วิธีดาวน์โหลด:**

#### ขั้นตอนที่ 1: ไปที่เว็บไซต์
https://sites.research.google/open-buildings/

#### ขั้นตอนที่ 2: เลือกพื้นที่
1. คลิก "Download"
2. เลือก Region: **Thailand**
3. เลือก Area: **Bangkok Metropolitan Region**
4. Format: **CSV** หรือ **Parquet** (แนะนำ Parquet - เล็กกว่า)

#### ขั้นตอนที่ 3: ดาวน์โหลด
- ไฟล์จะมีชื่อประมาณ: `thailand_bangkok_buildings.csv.gz`
- แตกไฟล์ (unzip)

#### ขั้นตอนที่ 4: Import เข้า Database

**วิธีที่ 1: ใช้ Script (แนะนำ)**
```bash
cd database
python import_full_data.py --file path/to/downloaded/file.csv
```

**วิธีที่ 2: ใช้ Google Colab (ถ้าเครื่องช้า)**
1. Upload ไฟล์ไปยัง Google Drive
2. เปิด Colab notebook: `database/import_colab.ipynb`
3. รัน cells ทั้งหมด
4. Export เป็น Parquet
5. Download กลับมา
6. Import เข้า local database

**ข้อดี:**
- ✅ ข้อมูลจริง 1.88M buildings
- ✅ Confidence scores จาก ML model
- ✅ Geometry ละเอียด
- ✅ เหมาะสำหรับ production

**ข้อเสีย:**
- ❌ ต้องดาวน์โหลด (~2-3 GB)
- ❌ Import ใช้เวลา (~30-60 นาที)
- ❌ ต้องการ RAM มาก (8GB+)

---

## 📋 โครงสร้างข้อมูล

### Buildings Table Schema

```sql
CREATE TABLE buildings (
    id                  SERIAL PRIMARY KEY,
    open_buildings_id   VARCHAR(50) UNIQUE,  -- ID จาก Google
    latitude            DOUBLE PRECISION,     -- ละติจูด
    longitude           DOUBLE PRECISION,     -- ลองจิจูด
    area_m2             DOUBLE PRECISION,     -- พื้นที่ (ตารางเมตร)
    confidence          DOUBLE PRECISION,     -- ความมั่นใจ (0-1)
    geometry            GEOMETRY(POLYGON),    -- รูปร่าง building
    centroid            GEOMETRY(POINT),      -- จุดกึ่งกลาง
    created_at          TIMESTAMP             -- วันที่สร้าง
);
```

### ตัวอย่างข้อมูล

```json
{
  "id": 1,
  "open_buildings_id": "OB_13.7563_100.7018",
  "latitude": 13.7563,
  "longitude": 100.7018,
  "area_m2": 245.5,
  "confidence": 0.89,
  "geometry": "POLYGON((...))",
  "centroid": "POINT(100.7018 13.7563)"
}
```

---

## 🔄 การ Update ข้อมูล

### เพิ่มข้อมูลใหม่
```bash
python import_full_data.py --file new_data.csv --append
```

### ลบข้อมูลเก่า
```sql
TRUNCATE TABLE buildings;
```

### Backup ข้อมูล
```bash
docker exec nabha-solar-db pg_dump -U postgres nabha_solar > backup.sql
```

### Restore ข้อมูล
```bash
docker exec -i nabha-solar-db psql -U postgres nabha_solar < backup.sql
```

---

## 📈 Performance Tips

### สำหรับ Sample Data (100 buildings)
- ไม่ต้องทำอะไร ใช้งานได้เลย

### สำหรับ Full Dataset (1.88M buildings)

**1. เพิ่ม Indexes**
```sql
CREATE INDEX idx_buildings_spatial ON buildings USING GIST(geometry);
CREATE INDEX idx_buildings_lat_lon ON buildings(latitude, longitude);
```

**2. ปรับ PostgreSQL Config**
```
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB
```

**3. ใช้ Connection Pooling**
- ติดตั้ง pgBouncer
- หรือใช้ SQLAlchemy pool

**4. Limit Results**
- ใช้ `LIMIT` ใน queries
- แสดงแค่ buildings ในพื้นที่ที่มองเห็น
- Default limit: 1000 buildings

---

## 🌍 ข้อมูลพื้นที่อื่นๆ

Google Open Buildings มีข้อมูลครอบคลุม:
- ทั่วประเทศไทย
- เอเชียตะวันออกเฉียงใต้
- แอฟริกา
- ละตินอเมริกา

**วิธีใช้พื้นที่อื่น:**
1. ดาวน์โหลดข้อมูลพื้นที่ที่ต้องการ
2. Import ด้วย script เดียวกัน
3. ปรับ map center ใน `BuildingsMap.jsx`

---

## ❓ FAQ

**Q: ข้อมูลมาจากไหน?**
A: Google Open Buildings - ML-detected building footprints จาก satellite imagery

**Q: ข้อมูลอัพเดทเมื่อไหร่?**
A: Google อัพเดทปีละ 1-2 ครั้ง ตรวจสอบที่เว็บไซต์

**Q: ความแม่นยำเท่าไหร่?**
A: Confidence score 65-98% (เฉลี่ย 80%) ขึ้นอยู่กับคุณภาพภาพถ่าย

**Q: ใช้เชิงพาณิชย์ได้ไหม?**
A: ได้ - ข้อมูลเป็น Open Data (CC BY 4.0 License)

**Q: ต้องใช้ API key ไหม?**
A: ไม่ต้อง - ดาวน์โหลดฟรี ไม่มี rate limit

---

## 📞 Support

หากมีปัญหาเรื่องข้อมูล:
1. ตรวจสอบ error logs
2. ดู Troubleshooting ใน README.md
3. ตรวจสอบ database connection
4. ลองใช้ sample data ก่อน

---

**สรุป:** เริ่มต้นด้วย Sample Data (100 buildings) แล้วค่อยเปลี่ยนเป็น Full Dataset (1.88M) ทีหลังเมื่อพร้อม!
