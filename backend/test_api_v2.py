import requests
import sys
import json
import time

BASE_URL = "http://127.0.0.1:8002"

def run_checks():
    print(f"🔍 Checking System Integrity on {BASE_URL}...\n")
    
    # 1. Health Check
    try:
        print("[HEALTH] Connecting...")
        resp = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            model_status = "✅ Loaded" if data['model_loaded'] else "❌ Not Loaded"
            print(f"[HEALTH] Status: {data['status']} | Model: {model_status} | Records: {data.get('records_loaded', 'N/A')}")
            if not data['model_loaded']:
                print("   ⚠️ CRITICAL: Model not loaded. Backend is running but ML is inactive.")
        else:
            print(f"[HEALTH] ❌ Failed: {resp.status_code}")
    except Exception as e:
        print(f"[HEALTH] ❌ Connection Failed. Is uvicorn running on port 8002? Error: {e}")
        return # Cannot proceed

    # 2. Dashboard Data (Real vs Mock)
    try:
        resp = requests.get(f"{BASE_URL}/api/dashboard", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            
            districts = data['districts']
            print(f"[DASHBOARD] Retrieved {len(districts)} districts.")
            
            if len(districts) > 0:
                sample = districts[0]
                print(f"   Sample District: {sample['district']} (Score: {sample['riskScore']})")
            
            # Check specific field types
            if 'trend' in data and len(data['trend']) > 0:
                print(f"   Trend Data Points: {len(data['trend'])}")
                print("   ✅ Real-time aggregation functional.")
        else:
             print(f"[DASHBOARD] ❌ Failed: {resp.status_code}")
            
    except Exception as e:
        print(f"[DASHBOARD] ❌ Failed: {e}")

    # 3. Prediction (ML Inference)
    print("\n[INFERENCE] Testing ML Model (GradientBoosting)...")
    payload = {
        "state": "Maharashtra",
        "district": "Pune",
        "year": 2026,
        "month": 4,
        "bio_age_5_17": 12500,
        "bio_age_17_": 45000,
        "lag_1m_bio": 57000,
        "lag_2m_bio": 56000,
        "lag_3m_bio": 55000
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/api/predict", json=payload, timeout=5)
        if resp.status_code == 200:
            res = resp.json()
            print("✅ Prediction Successful!")
            print(f"   Prediction: {res['prediction']}")
            print(f"   Risk Score: {res['risk_score']}")
            print(f"   Status: {res['status']}")
            print(f"   Insight: {res['insight']}")
            
            # Verify Response Structure matches Schema
            required_keys = ['prediction', 'risk_score', 'status', 'operationalMetrics']
            if all(k in res for k in required_keys):
                print("   ✅ Schema Validation Passed")
            else:
                 print("   ❌ Schema Validation Failed")
                
        else:
            print(f"❌ Prediction Failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"[INFERENCE] ❌ Error: {e}")

if __name__ == "__main__":
    run_checks()
