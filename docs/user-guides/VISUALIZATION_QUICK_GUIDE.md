# Visualization Quick Guide

## 🚀 Quick Start

### View Visualizations
1. Open http://localhost:5174
2. Click **"Visualizations"** in sidebar
3. Browse categories:
   - **Heatmaps** - State and district activity patterns
   - **Lifecycle** - Time-based patterns and trends
   - **Trends** - Growth and comparative analysis

### Full-Screen View
- Click any visualization thumbnail
- View in high resolution
- Press ESC or click outside to close

## 📊 What's Available

### Heatmaps (5)
| Visualization | Description |
|--------------|-------------|
| **Biometric State-Month** | Activity across all states over time |
| **Enrollment State-Month** | Enrollment patterns by state |
| **Demographic State-Month** | Demographic updates distribution |
| **Age Distribution** | Age group patterns monthly |
| **Top Districts** | Top 20 districts activity |

### Lifecycle Charts (3)
| Visualization | Description |
|--------------|-------------|
| **Biometric Lifecycle** | Day/Week/Month patterns + Age groups |
| **Enrollment Lifecycle** | Monthly trends + Gender distribution |
| **Demographic Lifecycle** | Monthly updates + Top states |

### Trends (3)
| Visualization | Description |
|--------------|-------------|
| **Combined Trends** | All 3 datasets side-by-side |
| **State-wise Trends** | Top 5 states comparison |
| **Growth Rates** | Month-over-month % changes |

## 🔄 Regenerate Visualizations

When you have new data:
```bash
cd "c:\Users\Shakil Ahmad\OneDrive\Desktop\UIDAI\Adhar Analysis"
python generate_visuals.py
```

This will:
- ✅ Load latest data (3.6M+ records)
- ✅ Generate 11 visualizations
- ✅ Save to 04_visuals/ folder
- ✅ Takes ~30-60 seconds

## 📁 File Locations

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
└── trends/
    ├── combined_trends.png
    ├── state_wise_trends.png
    └── growth_rate_trends.png
```

## 🎨 Visual Features

### Color Schemes
- **Biometric**: Red/Orange tones
- **Enrollment**: Blue tones
- **Demographic**: Green tones
- **Combined**: Multi-color

### Resolution
- All images: 300 DPI
- Print-ready quality
- High-resolution PNG format

## 💡 Use Cases

### 📈 Trend Analysis
Use lifecycle and trend charts to identify:
- Seasonal patterns
- Growth trajectories
- Peak periods

### 🗺️ Geographic Insights
Use heatmaps to discover:
- High-activity states
- Regional variations
- District comparisons

### 📊 Comparative Analysis
Use state-wise trends to:
- Compare performance
- Benchmark states
- Identify outliers

### 📑 Reporting
Download visualizations for:
- Executive summaries
- Monthly reports
- Presentations
- Documentation

## 🔧 Technical Details

### Backend Endpoints
```
GET /api/visuals/list
Returns: JSON with all visualization metadata

GET /api/visuals/{category}/{filename}
Returns: PNG image file
```

### Frontend Route
```
/visualizations
```

### Navigation
Sidebar → Visualizations (Image icon)

## ❓ Troubleshooting

**No visualizations showing?**
→ Run `python generate_visuals.py` first

**Backend error?**
→ Ensure backend running on port 8002

**Images not loading?**
→ Check browser console for errors

**Want to update visuals?**
→ Re-run generation script after data updates

## 📖 Full Documentation
See **VISUALIZATION_SYSTEM.md** for comprehensive details

---

**Quick Access**: http://localhost:5174/visualizations
