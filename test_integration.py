"""
Integration Test Script for Frontend-Backend-ML System
Tests all components and their integration
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8002/api"
FRONTEND_URL = "http://localhost:5173"

def test_backend_health():
    """Test if backend is running and models are loaded"""
    print("\n" + "="*50)
    print("1. Testing Backend Health...")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Backend Status: {data['status']}")
            print(f"✓ Model Loaded: {data['model_loaded']}")
            print(f"✓ Records Loaded: {data['records_loaded']}")
            return True
        else:
            print(f"✗ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Backend is NOT running on port 8002")
        print("  Please start backend with: .\\start_backend.bat")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_ml_prediction():
    """Test ML model prediction endpoint"""
    print("\n" + "="*50)
    print("2. Testing ML Model Prediction...")
    print("="*50)
    
    test_payload = {
        "state": "Delhi",
        "district": "Central Delhi",
        "year": 2024,
        "month": 6,
        "bio_age_5_17": 50000,
        "bio_age_17_": 100000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Prediction successful!")
            print(f"  Predicted Demand: {data.get('prediction', 'N/A')}")
            print(f"  Confidence: {data.get('confidence', 'N/A')}")
            return True
        else:
            print(f"✗ Prediction failed with status: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_biometric_prediction():
    """Test Biometric ML model"""
    print("\n" + "="*50)
    print("3. Testing Biometric Model...")
    print("="*50)
    
    test_payload = {
        "age_0_5": 25000,
        "age_5_17": 50000,
        "age_18_greater": 100000,
        "month": 6,
        "year": 2024
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict/biometric", json=test_payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Biometric prediction successful!")
            print(f"  Total Biometric Demand: {data.get('total_biometric_demand', 'N/A')}")
            return True
        else:
            print(f"✗ Biometric prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_dashboard_endpoint():
    """Test dashboard data endpoint"""
    print("\n" + "="*50)
    print("4. Testing Dashboard Endpoint...")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Dashboard data retrieved!")
            print(f"  KPIs: {len(data.get('kpi', []))} metrics")
            print(f"  Trend data points: {len(data.get('trend', []))}")
            print(f"  Districts: {len(data.get('districts', []))}")
            return True
        else:
            print(f"✗ Dashboard failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_anomaly_endpoint():
    """Test anomaly detection endpoint"""
    print("\n" + "="*50)
    print("5a. Testing Anomaly Endpoint...")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/anomalies", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Anomaly data retrieved!")
            print(f"  Total Anomalies: {len(data)}")
            if len(data) > 0:
                print(f"  Sample: {data[0]['district']} - {data[0]['status']}")
            return True
        else:
            print(f"✗ Anomaly check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_bulk_prediction():
    """Test bulk prediction endpoint"""
    print("\n" + "="*50)
    print("5. Testing Bulk Prediction...")
    print("="*50)
    
    test_payload = {
        "items": [
            {
                "state": "Delhi",
                "district": "Central Delhi",
                "year": 2024,
                "month": 6,
                "bio_age_5_17": 50000,
                "bio_age_17_": 100000
            },
            {
                "state": "Maharashtra",
                "district": "Mumbai",
                "year": 2024,
                "month": 6,
                "bio_age_5_17": 75000,
                "bio_age_17_": 150000
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict-bulk", json=test_payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Bulk prediction successful!")
            print(f"  Predictions returned: {len(data.get('results', []))}")
            return True
        else:
            print(f"✗ Bulk prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    print("\n" + "="*50)
    print("6. Testing Frontend...")
    print("="*50)
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print(f"✓ Frontend is running on {FRONTEND_URL}")
            return True
        else:
            print(f"✗ Frontend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Frontend is NOT running on {FRONTEND_URL}")
        print("  Please start frontend with: .\\start_frontend.bat")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("UIDAI System Integration Test")
    print("="*60)
    
    results = {
        "Backend Health": test_backend_health(),
        "ML Prediction": test_ml_prediction(),
        "Biometric Model": test_biometric_prediction(),
        "Dashboard API": test_dashboard_endpoint(),
        "Anomaly Endpoint": test_anomaly_endpoint(),
        "Bulk Prediction": test_bulk_prediction(),
        "Frontend": test_frontend()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All systems integrated and working properly!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
