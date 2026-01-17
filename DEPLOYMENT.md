# Deployment Guide

## 1. Frontend (Vercel) - Recommended

Since your project uses Vite + React, Vercel is the perfect host for the frontend.

1. **Push your code to GitHub** (You've already done this).
2. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New Project"**.
3. Import your GitHub repository: `Adhar-Analysis` (or whatever you named it).
4. **Configure Project**:
   - **Framework Preset**: Vite
   - **Root Directory**: Click `Edit` and select `frontend`.
   - **Environment Variables**:
     - `VITE_API_BASE_URL`: The URL of your deployed backend (see Section 2). 
     - *For now, you can leave it empty, but the app will try to connect to localhost until you set it.*

5. Click **Deploy**.

## 2. Backend (Render.com / Railway) - Recommended for ML

Your backend uses heavy ML libraries (`pandas`, `scikit-learn`, `xgboost`) and loads model files. **Vercel Serverless Functions have a 250MB size limit**, which your backend likely exceeds. 

**Recommended: Deploy to Render.com**

1. Create a `render.yaml` or connect your repo manually.
2. Select **Web Service**.
3. **Root Directory**: `.` (root) or `backend` (if you adjust paths).
   - If deploying from root:
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   - `PYTHON_VERSION`: `3.10.11` (or match your local version).
5. Once deployed, Render will give you a URL (e.g., `https://adhar-backend.onrender.com`).
6. **Go back to Vercel** -> Settings -> Environment Variables.
   - Set `VITE_API_BASE_URL` to `https://adhar-backend.onrender.com/api`
   - Redeploy Frontend.

## 3. Alternative: Full Docker Deployment

Since you have a `docker-compose.yml`, you can deploy to any VPS (AWS EC2, DigitalOcean, Azure VM):

1. SSH into your server.
2. Clone repo.
3. Run `docker compose up -d --build`.

