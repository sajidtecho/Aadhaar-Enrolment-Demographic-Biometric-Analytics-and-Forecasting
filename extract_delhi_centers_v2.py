import pandas as pd

file_path = r"c:\Users\Shakil Ahmad\OneDrive\Desktop\UIDAI\Adhar_biometric\01_data\raw\Aadhar Seva Kendra List.xlsx"

try:
    df = pd.read_excel(file_path)
    # Forward fill the District column to handle merged cells structure
    df['District'] = df['District'].fillna(method='ffill')
    
    # Filter for Delhi related entries
    # Check if District contains 'Delhi' or specific Delhi districts
    delhi_districts = ['Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 
                       'North East Delhi', 'North West Delhi', 'Shahdara', 
                       'South Delhi', 'South East Delhi', 'South West Delhi', 'West Delhi']
    
    # Normalize for matching
    df['District_Clean'] = df['District'].astype(str).str.strip()
    
    # Filter
    delhi_df = df[df['District_Clean'].isin(delhi_districts)]
    
    # If that returns nothing, try searching "Delhi" in district
    if delhi_df.empty:
        print("No exact match for districts, searching 'Delhi' in District column...")
        delhi_df = df[df['District'].astype(str).str.contains('Delhi', case=False, na=False)]
    
    print(f"Found {len(delhi_df)} centers in Delhi.")
    
    # Print them in a format I can copy-paste easily to TypeScript
    print("\n--- TYPESCRIPT DATA ---")
    results = []
    for index, row in delhi_df.iterrows():
        center_info = str(row['Center Name / Address']).replace('\n', ' ').strip()
        clean_address = center_info.replace("\"", "'")
        district = row['District'] # Use original
        if pd.isna(district): district = "Delhi"
        
        print(f"{{ id: 'DL-{index}', name: 'Aadhar Seva Kendra - {district}', address: \"{clean_address}\", district: '{district}', state: 'Delhi', lat: 28.61, lng: 77.23 }},") # Default lat/long for now

except Exception as e:
    print(f"Error: {e}")
