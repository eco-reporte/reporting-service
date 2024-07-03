from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.utils import ImageReader

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
    
    # Agregar imagen al PDF
    if report.imagen_url:
        try:
            image = ImageReader(report.imagen_url)
            p.drawImage(image, 100, 400, width=200, height=200)
        except Exception as e:
            p.drawString(100, 630, f"Error al cargar imagen: {str(e)}")
    
    p.showPage()
    p.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
