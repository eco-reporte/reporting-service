from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, Image
from io import BytesIO
from reportlab.lib.utils import ImageReader

def create_pdf(report):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = styles['Heading2']
    body_style = styles['BodyText']
    body_style.alignment = 1  # Center-align text

    # Title and subtitles
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height-50, "Reporte de Incidente Ambiental")

    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height-80, f"Título del Reporte: {report.titulo_reporte}")
    p.drawCentredString(width/2, height-100, f"Tipo de Reporte: {report.tipo_reporte}")

    # Divider line
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(50, height-120, width-50, height-120)

    # Report details
    data = [
        ["Descripción:", report.descripcion],
        ["Colonia:", report.colonia],
        ["Código Postal:", report.codigo_postal],
        ["Nombres:", report.nombres],
        ["Apellidos:", report.apellidos],
        ["Teléfono:", report.telefono],
        ["Correo:", report.correo],
        ["Fecha de Creación:", str(report.fecha_creacion)],
    ]

    table = Table(data, colWidths=[120, width-170])
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

    table.wrapOn(p, width, height)
    table.drawOn(p, 50, height-350)

    # Image
    if report.imagen_url:
        try:
            img = Image(report.imagen_url, width=200, height=200)
            img.drawOn(p, width/2 - 100, height-580)
        except Exception as e:
            p.drawString(50, height-400, f"Error al cargar imagen: {str(e)}")

    # Footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawCentredString(width/2, 30, "Generado por Eco-Reporte")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    filename = f"{report.titulo_reporte}_{report.fecha_creacion}.pdf".replace(" ", "_")

    return pdf, filename