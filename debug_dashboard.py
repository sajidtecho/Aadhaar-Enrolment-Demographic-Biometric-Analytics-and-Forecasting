from backend.model_service import model_service
from backend.dashboard_service import dashboard_service
import pandas as pd

try:
    print("Loading resources...")
    # Force reload to ensure we have latest code/data state
    model_service.load_resources()
    
    print("Data loaded. Shape:", model_service.data.shape if model_service.data is not None else "None")
    
    print("Testing get_dashboard_data()...")
    data = dashboard_service.get_dashboard_data()
    print("Success!")
    print(data)
except Exception as e:
    print("Refused/Error:")
    print(e)
    import traceback
    traceback.print_exc()
