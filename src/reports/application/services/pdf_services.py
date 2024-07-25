import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, Image, SimpleDocTemplate
from io import BytesIO

def create_pdf(report):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=18, alignment=1, spaceAfter=20, textColor=colors.darkblue)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Heading2'], fontSize=14, spaceAfter=10, textColor=colors.darkblue)
    body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=12, spaceAfter=6)
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=1)

    # Ruta del logo
    base_dir = os.path.dirname(__file__)
    logo_path = os.path.join(base_dir, '..', 'images', 'logo.png')

    # Verifica si la imagen existe
    if os.path.isfile(logo_path):
        header = [
            [Paragraph("Reporte de Incidente Ambiental", title_style), Image(logo_path, width=100, height=50)]
        ]
    else:
        header = [
            [Paragraph("Reporte de Incidente Ambiental", title_style), Paragraph("Logo no disponible", body_style)]
        ]

    header_table = Table(header, colWidths=[400, 100])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (0, 0))
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # Add report details
    elements.append(Paragraph(f"Título del Reporte: {report.titulo_reporte}", subtitle_style))
    elements.append(Paragraph(f"Tipo de Reporte: {report.tipo_reporte}", subtitle_style))
    elements.append(Spacer(1, 12))

    data = [
        ["Descripción:", Paragraph(report.descripcion, body_style)],
        ["Colonia:", report.colonia],
        ["Código Postal:", report.codigo_postal],
        ["Nombres:", report.nombres],
        ["Apellidos:", report.apellidos],
        ["Teléfono:", report.telefono],
        ["Correo:", report.correo],
        ["Fecha de Creación:", str(report.fecha_creacion)],
    ]

    table = Table(data, colWidths=[120, 350])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Add image if available
    if report.imagen_url:
        try:
            img = Image(report.imagen_url, width=200, height=200)
            elements.append(img)
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar imagen: {str(e)}", body_style))

    # Add footer
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Generado por Eco-Reporte", footer_style))

    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()

    filename = f"{report.titulo_reporte}{report.fecha_creacion}.pdf".replace(" ", "")

    return pdf, filename