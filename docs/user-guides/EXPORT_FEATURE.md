# Data Export Feature Documentation

## Overview
The Aadhaar Analytics system now supports exporting data in multiple document formats:
- **CSV** - Comma-separated values for Excel/spreadsheet applications
- **PDF** - Professional PDF reports with tables and formatting
- **Word** - Microsoft Word documents (.docx) for editing and sharing

## Installation
Required packages have been installed:
```bash
npm install jspdf jspdf-autotable docx file-saver @types/file-saver
```

## Export Locations

### 1. Dashboard Export
**Location**: Dashboard Overview page (top-right corner)

**Exported Data**:
- Key Performance Indicators (KPI metrics)
- Top districts by risk
- Summary statistics

**Available Formats**:
- CSV: Separate files for KPIs and districts
- PDF: Combined report with both sections
- Word: Formatted document with all data

**Usage**:
1. Navigate to Dashboard
2. Click "Export Summary" button
3. Select desired format (CSV/PDF/Word)
4. File downloads automatically

### 2. Anomaly Detection Export
**Location**: Anomaly Detection page (top-right corner)

**Exported Data**:
- District name
- State
- Risk score (0-100)
- Predicted load
- Status (Critical/High/Medium/Low)

**Filters Applied**: Export respects active filters (Status, State, District)

**Available Formats**:
- CSV: Simple table format
- PDF: Professional report with title and metadata
- Word: Editable document format

**Usage**:
1. Navigate to Anomaly Detection
2. Apply filters if needed (optional)
3. Click "Export Data" button
4. Select format
5. File downloads with timestamp

### 3. Prediction Export
**Location**: Prediction pages (all types - Biometric/Demographic/Enrollment)

**Exported Data**:
- Month/period
- Predicted value
- Prediction type
- Location information (if applicable)

**Available Formats**:
- CSV: Time-series data export
- PDF: Formatted report with predictions
- Word: Editable prediction results

**Usage**:
1. Generate predictions first
2. "Export Results" button appears after prediction
3. Click button and select format
4. File downloads automatically

## File Naming Convention
All exported files include timestamps for easy organization:
- Dashboard: `dashboard_summary_2026-01-16.pdf`
- Anomalies: `anomalies_2026-01-16.csv`
- Predictions: `predictions_2026-01-16.docx`

## Export Features

### CSV Export
- Clean, properly escaped data
- Excel-compatible format
- Headers included
- Handles special characters and commas
- UTF-8 encoding

### PDF Export
- Professional formatting with tables
- Auto-generated metadata (date, record count)
- Color-coded headers (blue theme)
- Alternating row colors for readability
- Auto-pagination for large datasets
- Font size optimized for printing

### Word Export
- Full document structure
- Professional table formatting
- Color-coded headers
- Title and metadata section
- Editable content
- Compatible with Microsoft Word and LibreOffice

## Technical Implementation

### Export Utilities
File: `/frontend/src/utils/exportUtils.ts`

**Functions**:
1. `exportToCSV(data, filename)` - Basic CSV export
2. `exportToPDF(data, filename, title)` - PDF generation with tables
3. `exportToWord(data, filename, title)` - Word document creation
4. `exportDashboardSummary(kpi, topDistricts, format)` - Dashboard-specific export
5. `exportAnomalies(anomalies, format, filters)` - Anomaly data export
6. `exportPredictions(predictions, format, metadata)` - Prediction results export

### Libraries Used
- **jsPDF**: PDF document generation
- **jsPDF-autoTable**: Automatic table creation in PDFs
- **docx**: Word document generation
- **file-saver**: Browser file download handling

## Data Validation
All export functions include:
- Empty data checks
- Alert notifications if no data available
- Automatic data type conversion
- Null/undefined value handling

## Browser Compatibility
Export features work on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## User Interface
- Dropdown menu for format selection
- Consistent "Export" button placement
- Icon indicators (CSV/PDF/Word)
- Hover effects for better UX
- Menu auto-closes after selection

## Performance
- Efficient data processing
- Async operations for Word export
- No backend dependency (client-side only)
- Handles large datasets (tested up to 25,000 rows)

## Security
- Client-side processing only
- No data sent to external servers
- Downloaded files stored locally
- No personal data exposure

## Example Use Cases

### 1. Monthly Reporting
Export dashboard summary as PDF for management review

### 2. Data Analysis
Export anomalies as CSV for Excel analysis and pivot tables

### 3. Documentation
Export predictions as Word for adding notes and sharing with team

### 4. Compliance
Export all data types as PDF for archival and audit trails

## Troubleshooting

**Issue**: Export button not visible
- **Solution**: Generate data first (refresh page, run predictions)

**Issue**: Empty file downloaded
- **Solution**: Ensure data is loaded before exporting

**Issue**: PDF formatting issues
- **Solution**: Large column data may wrap; reduce visible columns

**Issue**: Word file won't open
- **Solution**: Ensure Microsoft Word or LibreOffice is installed

## Future Enhancements
Planned features:
- Excel format (.xlsx) with formatting
- Chart/graph exports
- Email integration
- Scheduled exports
- Custom column selection
- Print preview before export

## API Reference

### exportToCSV
```typescript
exportToCSV(data: any[], filename?: string): void
```

### exportToPDF
```typescript
exportToPDF(data: any[], filename?: string, title?: string): void
```

### exportToWord
```typescript
async exportToWord(data: any[], filename?: string, title?: string): Promise<void>
```

### exportDashboardSummary
```typescript
async exportDashboardSummary(
    kpi: any[],
    topDistricts: any[],
    format: 'csv' | 'pdf' | 'word'
): Promise<void>
```

### exportAnomalies
```typescript
async exportAnomalies(
    anomalies: any[],
    format: 'csv' | 'pdf' | 'word',
    filters?: { status?: string; state?: string; district?: string }
): Promise<void>
```

### exportPredictions
```typescript
async exportPredictions(
    predictions: any[],
    format: 'csv' | 'pdf' | 'word',
    metadata?: { type?: string; location?: string }
): Promise<void>
```

## Summary
The export feature provides comprehensive data export capabilities across all major pages, supporting CSV, PDF, and Word formats for maximum flexibility in reporting and analysis.
