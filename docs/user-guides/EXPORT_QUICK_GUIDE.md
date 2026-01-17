# Quick Export Guide

## 🚀 Quick Start

### Export Dashboard Summary
1. Go to **Dashboard** page
2. Click **"Export Summary"** (top-right)
3. Choose format:
   - **CSV** - KPIs and districts in separate files
   - **PDF** - Combined professional report
   - **Word** - Editable document

### Export Anomaly Data
1. Go to **Anomaly Detection** page
2. (Optional) Apply filters for specific data
3. Click **"Export Data"** (top-right)
4. Choose format (CSV/PDF/Word)

### Export Predictions
1. Go to **Prediction** page (Biometric/Demographic/Enrollment)
2. Run a prediction first
3. Click **"Export Results"** (appears after prediction)
4. Choose format (CSV/PDF/Word)

## 📁 File Formats

### CSV - Best For:
- ✅ Opening in Excel/Google Sheets
- ✅ Data analysis and pivot tables
- ✅ Importing into other systems
- ✅ Quick data sharing

### PDF - Best For:
- ✅ Professional reports
- ✅ Printing and archiving
- ✅ Presentations to management
- ✅ Email attachments
- ✅ Read-only distribution

### Word - Best For:
- ✅ Adding notes and comments
- ✅ Collaborative editing
- ✅ Custom formatting
- ✅ Merging with other documents
- ✅ Creating custom reports

## 📊 What Gets Exported

### Dashboard Export
```
KPI Metrics:
- Biometric Updates
- Total Enrollments
- Adult Enrollments
- High Demand Districts

Top Districts:
- District name
- State
- Risk score
- Prediction
- Status
```

### Anomaly Export
```
For each district:
- District name
- State
- Risk score (0-100)
- Predicted load
- Status (Critical/High/Medium/Low)
```

### Prediction Export
```
For each time period:
- Month/Date
- Predicted value
- Prediction type
- Location (if applicable)
```

## 💡 Pro Tips

1. **Filter Before Exporting**
   - Apply filters in Anomaly Detection
   - Export only what you need

2. **File Names**
   - Auto-timestamped: `anomalies_2026-01-16.csv`
   - No need to rename

3. **Multiple Formats**
   - Export same data in different formats
   - Use CSV for analysis, PDF for reports

4. **Large Datasets**
   - System handles up to 25,000+ rows
   - PDF auto-paginates
   - CSV works with all sizes

5. **Share Securely**
   - Files saved to your Downloads folder
   - No data sent to external servers
   - Client-side processing only

## 🔧 Troubleshooting

**Q: Export button not visible?**
A: Make sure data is loaded (refresh page)

**Q: Empty file downloaded?**
A: Wait for data to load before exporting

**Q: PDF looks compressed?**
A: Many columns - try CSV instead

**Q: Word file won't open?**
A: Install Microsoft Word or LibreOffice

## 📱 Browser Support
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

## 🎯 Use Cases

### Weekly Reports
Export Dashboard as PDF every Monday

### Data Analysis
Export Anomalies as CSV for Excel analysis

### Team Collaboration
Export Predictions as Word for team review

### Compliance
Export all data as PDF for audit trails

---

**Need Help?** See full documentation in `EXPORT_FEATURE.md`
