from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf(report):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Añadir contenido al PDF
    p.drawString(100, 750, f"Título: {report.titulo_reporte}")
    p.drawString(100, 730, f"Tipo: {report.tipo_reporte}")
    p.drawString(100, 710, f"Descripción: {report.descripcion}")
    p.drawString(100, 690, f"Colonia: {report.colonia}")
    p.drawString(100, 670, f"Código Postal: {report.codigo_postal}")
    p.drawString(100, 650, f"Fecha de Creación: {report.fecha_creacion}")
    
    p.showPage()
    p.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf