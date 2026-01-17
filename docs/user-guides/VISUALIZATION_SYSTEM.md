# Visualization System Documentation

## Overview
The Aadhaar Analytics system now includes comprehensive data visualizations generated from all three datasets (Biometric, Enrollment, Demographic). Visualizations are automatically generated and served through the web interface.

## Generated Visualizations

### 📊 Heatmaps (5 visualizations)
1. **Biometric State-Month Heatmap**
   - Shows biometric updates across states and months
   - Color intensity represents activity volume
   - File: `biometric_state_month_heatmap.png`

2. **Enrollment State-Month Heatmap**
   - Shows enrollment patterns across states and months
   - Blue color scheme
   - File: `enrollment_state_month_heatmap.png`

3. **Demographic State-Month Heatmap**
   - Shows demographic update patterns
   - Green color scheme
   - File: `demographic_state_month_heatmap.png`

4. **Biometric Age Distribution Heatmap**
   - Monthly age group distribution (5-17 years, 17+ years)
   - Viridis color scheme
   - File: `biometric_age_distribution_heatmap.png`

5. **Top Districts Activity Heatmap**
   - Top 20 districts by activity volume
   - Monthly patterns
   - File: `top_districts_activity_heatmap.png`

### 🔄 Lifecycle Charts (3 visualizations)
1. **Biometric Lifecycle**
   - Day of week pattern
   - Monthly lifecycle trend
   - Age group lifecycle
   - File: `biometric_lifecycle.png`

2. **Enrollment Lifecycle**
   - Monthly enrollment pattern
   - Gender distribution lifecycle (if available)
   - File: `enrollment_lifecycle.png`

3. **Demographic Lifecycle**
   - Monthly demographic updates
   - Top 5 states lifecycle
   - File: `demographic_lifecycle.png`

### 📈 Trends (3 visualizations)
1. **Combined Trends**
   - Biometric, Enrollment, and Demographic trends
   - All three datasets on separate charts
   - Time series with fill areas
   - File: `combined_trends.png`

2. **State-wise Trends**
   - Top 5 states for each dataset
   - Comparative state analysis
   - File: `state_wise_trends.png`

3. **Growth Rate Trends**
   - Month-over-month growth percentages
   - All three datasets compared
   - Zero baseline indicator
   - File: `growth_rate_trends.png`

## File Structure
```
04_visuals/
├── heatmaps/
│   ├── biometric_state_month_heatmap.png
│   ├── enrollment_state_month_heatmap.png
│   ├── demographic_state_month_heatmap.png
│   ├── biometric_age_distribution_heatmap.png
│   └── top_districts_activity_heatmap.png
├── lifecycle/
│   ├── biometric_lifecycle.png
│   ├── enrollment_lifecycle.png
│   └── demographic_lifecycle.png
├── trends/
│   ├── combined_trends.png
│   ├── state_wise_trends.png
│   └── growth_rate_trends.png
└── anomalies/
    (Reserved for future anomaly visualizations)
```

## Generation Script

### Script: `generate_visuals.py`
**Location**: Root directory  
**Purpose**: Generate all visualizations from the three datasets

**Usage**:
```bash
python generate_visuals.py
```

**Features**:
- Loads all three datasets (1.86M + 983K + 1.6M records)
- Generates 11 visualizations automatically
- Saves in organized folder structure
- High-resolution output (300 DPI)
- Professional styling with seaborn

**Output**:
```
================================================================================
VISUALIZATION GENERATION COMPLETE
================================================================================

📊 Total visualizations generated: 11

📁 Output directories:
   • Heatmaps:  04_visuals/heatmaps  (5 files)
   • Lifecycle: 04_visuals/lifecycle (3 files)
   • Trends:    04_visuals/trends    (3 files)

✓ All visualizations saved successfully!
```

## Backend API

### Endpoints

#### GET /api/visuals/list
Returns list of all available visualizations

**Response**:
```json
{
  "heatmaps": [
    {
      "name": "biometric_state_month_heatmap.png",
      "path": "visuals/heatmaps/biometric_state_month_heatmap.png",
      "category": "heatmaps",
      "title": "Biometric State Month Heatmap"
    },
    ...
  ],
  "lifecycle": [...],
  "trends": [...],
  "anomalies": [...]
}
```

#### GET /api/visuals/{category}/{filename}
Serves visualization image file

**Parameters**:
- `category`: heatmaps | lifecycle | trends | anomalies
- `filename`: PNG filename

**Response**: Image file (image/png)

**Example**:
```
GET /api/visuals/heatmaps/biometric_state_month_heatmap.png
```

## Frontend Interface

### Page: Visualizations
**Route**: `/visualizations`  
**Component**: `src/pages/Visualizations.tsx`

**Features**:
1. **Category Tabs**
   - Heatmaps (red theme)
   - Lifecycle (green theme)
   - Trends (blue theme)
   - Anomalies (gray theme)
   - Shows count per category

2. **Grid Layout**
   - Responsive grid (1/2/3 columns)
   - Thumbnail previews
   - Hover effects
   - Click to enlarge

3. **Full-Screen Modal**
   - Click any visualization to view full-size
   - High-resolution display
   - Dark overlay
   - Title and category info
   - Click outside to close

4. **Data Statistics**
   - Shows record counts for all datasets
   - Visual indicators for data sources

### Navigation
**Sidebar**: "Visualizations" menu item with Image icon

## Technical Details

### Libraries Used
**Python**:
- `pandas` - Data processing
- `matplotlib` - Plotting
- `seaborn` - Statistical visualizations
- `numpy` - Numerical operations

**Frontend**:
- `axios` - API requests
- `lucide-react` - Icons
- React components

### Image Specifications
- **Format**: PNG
- **Resolution**: 300 DPI
- **Color**: RGB
- **Sizes**:
  - Heatmaps: 16×12 inches
  - Lifecycle: 14×10/12 inches
  - Trends: 14-18 inches width

### Color Schemes
- **Biometric**: Red/Orange (`YlOrRd`)
- **Enrollment**: Blue (`Blues`)
- **Demographic**: Green (`Greens`)
- **Age Groups**: Viridis
- **Districts**: Red-Yellow-Green (`RdYlGn`)

## Regenerating Visualizations

### When to Regenerate
- After data updates
- When new records are added
- To refresh analysis
- After model retraining

### Steps
1. Ensure all datasets are current in `01_data/processed/`
2. Run generation script:
   ```bash
   python generate_visuals.py
   ```
3. Refresh frontend page to see updated visualizations

### Automatic Updates
The system doesn't auto-regenerate. Manual execution required for updates.

## Use Cases

### 1. Executive Reporting
Export heatmaps for state-wise performance reports

### 2. Trend Analysis
Use lifecycle charts to identify seasonal patterns

### 3. Capacity Planning
Growth rate trends for forecasting infrastructure needs

### 4. State Comparisons
State-wise trends for regional analysis

### 5. Presentations
Full-screen modal for presentations and demos

## Error Handling

### No Visualizations Available
If no visualizations found, shows helpful message:
```
Run python generate_visuals.py to create visualizations
```

### Backend Not Running
Shows error with retry button if API unavailable

### Image Load Failures
Graceful fallback with placeholder SVG

## Performance

### Load Times
- List API: < 100ms
- Image serving: < 50ms per image
- Grid render: Instant (client-side)

### Caching
- Browser caches images automatically
- No server-side caching needed
- Images are static files

## Future Enhancements

### Planned Features
1. **Real-time Generation**
   - Generate on-demand through UI
   - Background job processing

2. **Interactive Visualizations**
   - D3.js integration
   - Zoom and pan capabilities
   - Tooltips and hover data

3. **Custom Filters**
   - Date range selection
   - State/district filtering
   - Custom color schemes

4. **Export Options**
   - Download individual images
   - Export reports with multiple charts
   - PDF compilation

5. **Comparison Tools**
   - Side-by-side comparisons
   - Difference highlighting
   - Trend overlays

## Troubleshooting

### Script Errors
**Issue**: Column not found error  
**Solution**: Check dataset column names match script expectations

**Issue**: Memory error  
**Solution**: Process datasets in chunks or reduce data size

### API Errors
**Issue**: 404 Not Found  
**Solution**: Run `python generate_visuals.py` first

**Issue**: CORS error  
**Solution**: Ensure backend CORS allows frontend origin

### Frontend Issues
**Issue**: Images not displaying  
**Solution**: Check browser console, verify API URLs

**Issue**: Modal not working  
**Solution**: Check click event handlers, verify state management

## Maintenance

### Regular Tasks
1. **Weekly**: Review visualization quality
2. **Monthly**: Regenerate with latest data
3. **Quarterly**: Update color schemes if needed
4. **Annually**: Archive old visualizations

### File Management
- Keep only latest 3 generations
- Archive older versions
- Maintain 04_visuals/ structure

## Integration Points

### With Export Feature
Visualizations can be exported using the export feature:
- Dashboard exports include visualization links
- Anomaly reports can reference visual insights

### With Predictions
Prediction pages can link to relevant trend visualizations

### With Dashboard
Dashboard can embed thumbnail previews of key visualizations

## Summary
The visualization system provides comprehensive visual analytics across all three datasets, with 11 professional visualizations organized into heatmaps, lifecycle charts, and trends. The system is fully integrated with the backend API and frontend interface, providing an intuitive browsing experience with full-screen viewing capabilities.
