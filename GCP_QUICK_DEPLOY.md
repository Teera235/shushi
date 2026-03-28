# 🚀 GCP Quick Deploy - 5 นาที!

## ✅ Prerequisites (ทำแล้ว)
- [x] ข้อมูลอัพโหลดไปยัง Cloud Storage แล้ว
- [x] Cloud SQL instance สร้างแล้ว
- [x] ข้อมูล import เข้า Cloud SQL แล้ว

## 🎯 ขั้นตอนถัดไป: Deploy Backend + Frontend

### ขั้นตอนที่ 1: เตรียม GCP Project

```powershell
# Login (ถ้ายังไม่ได้ login)
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### ขั้นตอนที่ 2: Deploy Backend API

```powershell
cd sushi

# Run deployment script
.\deploy-to-gcp.ps1 `
  -ProjectId "YOUR_PROJECT_ID" `
  -CloudSqlInstance "nabha-solar-db" `
  -DbPassword "YOUR_DB_PASSWORD" `
  -Region "asia-southeast1"
```

**Script จะทำอัตโนมัติ:**
1. ✅ Build Docker image
2. ✅ Push to Container Registry
3. ✅ Deploy to Cloud Run
4. ✅ Connect to Cloud SQL
5. ✅ Test API
6. ✅ Build Frontend
7. ✅ Deploy to Firebase (ถ้า setup แล้ว)

### ขั้นตอนที่ 3: Deploy Frontend (Manual)

#### Option A: Firebase Hosting (แนะนำ)

```powershell
cd frontend

# Install Firebase CLI (ถ้ายังไม่มี)
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init hosting
# - Select: Use existing project
# - Public directory: build
# - Single-page app: Yes
# - GitHub deploys: No

# Deploy
firebase deploy --only hosting
```

#### Option B: Cloud Storage + Cloud CDN

```powershell
# Create bucket
gsutil mb -l asia-southeast1 gs://nabha-solar-frontend

# Enable website hosting
gsutil web set -m index.html -e index.html gs://nabha-solar-frontend

# Upload build files
gsutil -m cp -r build/* gs://nabha-solar-frontend/

# Make public
gsutil iam ch allUsers:objectViewer gs://nabha-solar-frontend

# Get URL
echo "https://storage.googleapis.com/nabha-solar-frontend/index.html"
```

---

## 🧪 ทดสอบ

### Test Backend API

```powershell
# Get API URL
$ApiUrl = gcloud run services describe buildings-api --region asia-southeast1 --format 'value(status.url)'

# Test stats
Invoke-WebRequest -Uri "$ApiUrl/stats" | Select-Object -ExpandProperty Content

# Test bbox
Invoke-WebRequest -Uri "$ApiUrl/buildings/bbox?min_lat=13.7&max_lat=13.8&min_lon=100.5&max_lon=100.6&limit=10" | Select-Object -ExpandProperty Content
```

### Test Frontend

เปิด browser ไปที่:
- Firebase: `https://YOUR_PROJECT.web.app`
- Cloud Storage: `https://storage.googleapis.com/nabha-solar-frontend/index.html`

---

## 📊 ตรวจสอบ Logs

### Backend Logs
```powershell
# View logs
gcloud run services logs read buildings-api --region asia-southeast1 --limit 50

# Follow logs (real-time)
gcloud run services logs tail buildings-api --region asia-southeast1
```

### Cloud SQL Logs
```powershell
# View logs
gcloud sql operations list --instance nabha-solar-db

# Connect to database
gcloud sql connect nabha-solar-db --user=postgres
```

---

## 🔧 Troubleshooting

### Backend ไม่ทำงาน

```powershell
# Check service status
gcloud run services describe buildings-api --region asia-southeast1

# Check logs
gcloud run services logs read buildings-api --region asia-southeast1 --limit 100

# Test Cloud SQL connection
gcloud sql connect nabha-solar-db --user=postgres
# Then: SELECT COUNT(*) FROM buildings;
```

### Frontend ไม่แสดงข้อมูล

1. ตรวจสอบ API URL ใน `.env`:
```powershell
cat frontend/.env
```

2. ตรวจสอบ CORS settings ใน backend
3. เปิด Browser Console ดู errors

### Deployment ล้มเหลว

```powershell
# Check Cloud Build logs
gcloud builds list --limit 5

# Check permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID
```

---

## 💰 ประมาณการค่าใช้จ่าย

**ตามที่ Deploy:**
- Cloud Run (2 vCPU, 2GB RAM): ~$10-20/month
- Cloud SQL (ตาม tier ที่เลือก): ~$10-100/month
- Cloud Storage: ~$1-2/month
- Firebase Hosting: ฟรี (10GB/month)

**Total: ~$21-122/month** (ขึ้นกับ traffic และ Cloud SQL tier)

---

## 🎉 เสร็จแล้ว!

ตอนนี้คุณมี:
- ✅ Backend API บน Cloud Run (auto-scale)
- ✅ Frontend บน Firebase/Cloud Storage
- ✅ Database บน Cloud SQL (1.88M buildings)
- ✅ Production-ready system

**URLs:**
- API: `https://buildings-api-xxx.run.app`
- Frontend: `https://your-project.web.app`

---

## 📝 Commands สำหรับจัดการ

```powershell
# Update backend
cd backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/buildings-api
gcloud run deploy buildings-api --image gcr.io/YOUR_PROJECT_ID/buildings-api --region asia-southeast1

# Update frontend
cd frontend
npm run build
firebase deploy --only hosting

# View all resources
gcloud run services list
gcloud sql instances list
firebase hosting:sites:list

# Delete resources (cleanup)
gcloud run services delete buildings-api --region asia-southeast1
gcloud sql instances delete nabha-solar-db
gsutil rm -r gs://nabha-solar-frontend
```

---

**ต้องการความช่วยเหลือ?**
- ดู logs: `gcloud run services logs read buildings-api --region asia-southeast1`
- ตรวจสอบ status: `gcloud run services describe buildings-api --region asia-southeast1`
- Connect to DB: `gcloud sql connect nabha-solar-db --user=postgres`
