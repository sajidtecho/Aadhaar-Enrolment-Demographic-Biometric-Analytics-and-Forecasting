/**
 * Export Utilities for Dashboard Data
 * Supports CSV, PDF, and Word document exports
 */

import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { Document, Packer, Paragraph, Table, TableCell, TableRow, TextRun, AlignmentType, WidthType } from 'docx';
import { saveAs } from 'file-saver';

// Export data to CSV
export const exportToCSV = (data: any[], filename: string = 'export.csv') => {
    if (!data || data.length === 0) {
        alert('No data to export');
        return;
    }

    // Get headers from first object
    const headers = Object.keys(data[0]);
    
    // Create CSV content
    const csvContent = [
        headers.join(','), // Header row
        ...data.map(row => 
            headers.map(header => {
                const value = row[header];
                // Handle values with commas or quotes
                if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                    return `"${value.replace(/"/g, '""')}"`;
                }
                return value;
            }).join(',')
        )
    ].join('\n');

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
};

// Export data to PDF
export const exportToPDF = (data: any[], filename: string = 'export.pdf', title: string = 'Data Export') => {
    if (!data || data.length === 0) {
        alert('No data to export');
        return;
    }

    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(16);
    doc.text(title, 14, 15);
    
    // Add metadata
    doc.setFontSize(10);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 22);
    doc.text(`Total Records: ${data.length}`, 14, 27);
    
    // Get headers and prepare data
    const headers = Object.keys(data[0]);
    const tableData = data.map(row => headers.map(header => String(row[header] || '')));
    
    // Add table
    autoTable(doc, {
        head: [headers],
        body: tableData,
        startY: 32,
        styles: { fontSize: 8, cellPadding: 2 },
        headStyles: { fillColor: [59, 130, 246], textColor: 255 },
        alternateRowStyles: { fillColor: [248, 250, 252] },
        margin: { top: 32, left: 10, right: 10 },
    });
    
    doc.save(filename);
};

// Export data to Word Document
export const exportToWord = async (data: any[], filename: string = 'export.docx', title: string = 'Data Export') => {
    if (!data || data.length === 0) {
        alert('No data to export');
        return;
    }

    const headers = Object.keys(data[0]);
    
    // Create header row
    const headerRow = new TableRow({
        children: headers.map(header => 
            new TableCell({
                children: [new Paragraph({
                    children: [new TextRun({
                        text: header.toUpperCase(),
                        bold: true,
                        color: "FFFFFF"
                    })],
                    alignment: AlignmentType.CENTER
                })],
                shading: { fill: "3B82F6" },
                width: { size: 100 / headers.length, type: WidthType.PERCENTAGE }
            })
        )
    });
    
    // Create data rows
    const dataRows = data.map(row => 
        new TableRow({
            children: headers.map(header => 
                new TableCell({
                    children: [new Paragraph({
                        text: String(row[header] || ''),
                        alignment: AlignmentType.LEFT
                    })],
                    width: { size: 100 / headers.length, type: WidthType.PERCENTAGE }
                })
            )
        })
    );
    
    // Create table
    const table = new Table({
        rows: [headerRow, ...dataRows],
        width: { size: 100, type: WidthType.PERCENTAGE }
    });
    
    // Create document
    const doc = new Document({
        sections: [{
            properties: {},
            children: [
                new Paragraph({
                    children: [new TextRun({
                        text: title,
                        bold: true,
                        size: 32,
                        color: "1E293B"
                    })],
                    spacing: { after: 200 }
                }),
                new Paragraph({
                    children: [
                        new TextRun({
                            text: `Generated: ${new Date().toLocaleString()}`,
                            size: 20,
                            color: "64748B"
                        })
                    ],
                    spacing: { after: 100 }
                }),
                new Paragraph({
                    children: [
                        new TextRun({
                            text: `Total Records: ${data.length}`,
                            size: 20,
                            color: "64748B"
                        })
                    ],
                    spacing: { after: 300 }
                }),
                table
            ]
        }]
    });
    
    // Generate and save
    const blob = await Packer.toBlob(doc);
    saveAs(blob, filename);
};

// Export dashboard summary
export const exportDashboardSummary = async (
    kpi: any[],
    topDistricts: any[],
    format: 'csv' | 'pdf' | 'word' = 'pdf'
) => {
    const timestamp = new Date().toISOString().split('T')[0];
    
    if (format === 'csv') {
        // Export KPIs
        exportToCSV(
            kpi.map(k => ({
                Metric: k.label,
                Value: k.value,
                Change: `${k.change}%`,
                Trend: k.trend
            })),
            `dashboard_kpi_${timestamp}.csv`
        );
        
        // Export top districts
        exportToCSV(topDistricts, `dashboard_districts_${timestamp}.csv`);
    } else if (format === 'pdf') {
        const doc = new jsPDF();
        
        // Title
        doc.setFontSize(18);
        doc.text('Aadhaar Analytics Dashboard Summary', 14, 15);
        
        // Metadata
        doc.setFontSize(10);
        doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 23);
        
        // KPI Section
        doc.setFontSize(14);
        doc.text('Key Performance Indicators', 14, 35);
        
        autoTable(doc, {
            head: [['Metric', 'Value', 'Change (%)', 'Trend']],
            body: kpi.map(k => [k.label, k.value, k.change, k.trend]),
            startY: 40,
            styles: { fontSize: 9 },
            headStyles: { fillColor: [59, 130, 246] }
        });
        
        // Top Districts Section
        const finalY = (doc as any).lastAutoTable.finalY + 10;
        doc.setFontSize(14);
        doc.text('Top Districts by Risk', 14, finalY);
        
        autoTable(doc, {
            head: [['District', 'State', 'Risk Score', 'Prediction', 'Status']],
            body: topDistricts.map(d => [d.district, d.state, d.riskScore, d.prediction, d.status]),
            startY: finalY + 5,
            styles: { fontSize: 9 },
            headStyles: { fillColor: [59, 130, 246] }
        });
        
        doc.save(`dashboard_summary_${timestamp}.pdf`);
    } else if (format === 'word') {
        const sections = [
            new Paragraph({
                children: [new TextRun({
                    text: 'Aadhaar Analytics Dashboard Summary',
                    bold: true,
                    size: 32
                })],
                spacing: { after: 200 }
            }),
            new Paragraph({
                text: `Generated: ${new Date().toLocaleString()}`,
                spacing: { after: 300 }
            }),
            new Paragraph({
                children: [new TextRun({
                    text: 'Key Performance Indicators',
                    bold: true,
                    size: 24
                })],
                spacing: { after: 200 }
            })
        ];
        
        const doc = new Document({
            sections: [{ properties: {}, children: sections }]
        });
        
        const blob = await Packer.toBlob(doc);
        saveAs(blob, `dashboard_summary_${timestamp}.docx`);
    }
};

// Export anomaly detection results
export const exportAnomalies = async (
    anomalies: any[],
    format: 'csv' | 'pdf' | 'word' = 'csv',
    filters?: { status?: string; state?: string; district?: string }
) => {
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `anomalies_${timestamp}`;
    
    // Prepare data
    const exportData = anomalies.map(a => ({
        District: a.district,
        State: a.state,
        'Risk Score': a.riskScore,
        'Predicted Load': a.prediction,
        Status: a.status
    }));
    
    if (format === 'csv') {
        exportToCSV(exportData, `${filename}.csv`);
    } else if (format === 'pdf') {
        exportToPDF(exportData, `${filename}.pdf`, 'Anomaly Detection Report');
    } else if (format === 'word') {
        await exportToWord(exportData, `${filename}.docx`, 'Anomaly Detection Report');
    }
};

// Export prediction results
export const exportPredictions = async (
    predictions: any[],
    format: 'csv' | 'pdf' | 'word' = 'csv',
    metadata?: { type?: string; location?: string }
) => {
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `predictions_${timestamp}`;
    
    if (format === 'csv') {
        exportToCSV(predictions, `${filename}.csv`);
    } else if (format === 'pdf') {
        exportToPDF(predictions, `${filename}.pdf`, 'Prediction Results');
    } else if (format === 'word') {
        await exportToWord(predictions, `${filename}.docx`, 'Prediction Results');
    }
};
