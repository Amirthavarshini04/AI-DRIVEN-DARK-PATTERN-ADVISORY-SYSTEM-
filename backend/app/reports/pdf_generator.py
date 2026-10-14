import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from typing import Dict, Any

def generate_scan_pdf(scan_data: Dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e1b4b'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#312e81'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1e293b')
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("AI Dark Pattern & Compliance Audit Report", title_style))
    elements.append(Paragraph("Framework: Central Consumer Protection Authority (CCPA) Guidelines for Dark Patterns, 2023", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#4f46e5'), spaceAfter=15))

    # Scan Summary Table
    risk_score = scan_data.get("risk_score", 0.0)
    risk_cat = scan_data.get("risk_category", "Low Risk")
    
    summary_data = [
        [Paragraph("<b>Scan ID:</b>", body_style), Paragraph(str(scan_data.get("id")), body_style)],
        [Paragraph("<b>Target URL / Text:</b>", body_style), Paragraph(str(scan_data.get("url") or "Pasted Text Snippet"), body_style)],
        [Paragraph("<b>Language Analyzed:</b>", body_style), Paragraph(str(scan_data.get("language", "auto")).upper(), body_style)],
        [Paragraph("<b>Overall Compliance Risk:</b>", body_style), Paragraph(f"<b>{risk_score} / 100 ({risk_cat})</b>", body_style)],
        [Paragraph("<b>Total Findings Detected:</b>", body_style), Paragraph(str(len(scan_data.get("findings", []))), body_style)]
    ]

    t_summary = Table(summary_data, colWidths=[150, 390])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    elements.append(t_summary)
    elements.append(Spacer(1, 15))

    # Findings Section
    elements.append(Paragraph("Detected Dark Pattern Findings", h2_style))

    findings = scan_data.get("findings", [])
    if not findings:
        elements.append(Paragraph("No deceptive patterns were detected during this scan.", body_style))
    else:
        for idx, f in enumerate(findings, 1):
            sev_color = "#dc2626" if f.get("severity") in ("High", "Critical") else "#d97706"
            
            f_table_data = [
                [
                    Paragraph(f"<b>#{idx}. {f.get('category')}</b>", ParagraphStyle('FHead', parent=body_style, textColor=colors.HexColor('#1e1b4b'), fontSize=10)),
                    Paragraph(f"Severity: <b><font color='{sev_color}'>{f.get('severity')}</font></b> | Confidence: {int(f.get('confidence', 0.85)*100)}%", body_style)
                ],
                [
                    Paragraph("<b>Relevant Text Snippet:</b>", body_style),
                    Paragraph(f"<i>\"{f.get('text_snippet')}\"</i>", body_style)
                ],
                [
                    Paragraph("<b>CCPA 2023 Clause:</b>", body_style),
                    Paragraph(f"{f.get('ccpa_clause')} ({f.get('ccpa_category')})", body_style)
                ],
                [
                    Paragraph("<b>Consumer Impact:</b>", body_style),
                    Paragraph(f.get("consumer_impact", ""), body_style)
                ],
                [
                    Paragraph("<b>Compliant Recommendation:</b>", body_style),
                    Paragraph(f.get("recommendation", ""), body_style)
                ]
            ]
            
            t_f = Table(f_table_data, colWidths=[140, 400])
            t_f.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eeef2')),
                ('PADDING', (0,0), (-1,-1), 5),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ]))
            elements.append(t_f)
            elements.append(Spacer(1, 10))

    # Disclaimer Footer
    elements.append(Spacer(1, 15))
    disclaimer_text = "<b>Academic Project Disclaimer:</b> This report is generated by an automated decision-support system for educational purposes under major engineering project evaluation. It does not constitute formal legal certification or professional advice."
    elements.append(Paragraph(disclaimer_text, ParagraphStyle('Disc', parent=body_style, fontSize=8, textColor=colors.HexColor('#64748b'))))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
