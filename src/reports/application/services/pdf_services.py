from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from io import BytesIO
from reportlab.lib.utils import ImageReader

def create_pdf(report):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Estilos de texto
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = styles['Heading2']
    body_style = styles['BodyText']

    # Añadir título y subtítulos
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 750, "Reporte de Incidente Ambiental")

    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Título del Reporte: {report.titulo_reporte}")
    p.drawString(100, 710, f"Tipo de Reporte: {report.tipo_reporte}")

    # Línea divisoria
    p.setStrokeColor(colors.black)
    p.setLineWidth(0.5)
    p.line(50, 700, 550, 700)

    # Detalles del reporte
    p.setFont("Helvetica", 10)
    text = [
        f"Descripción: {report.descripcion}",
        f"Colonia: {report.colonia}",
        f"Código Postal: {report.codigo_postal}",
        f"Nombres: {report.nombres}",
        f"Apellidos: {report.apellidos}",
        f"Teléfono: {report.telefono}",
        f"Correo: {report.correo}",
        f"Fecha de Creación: {report.fecha_creacion}",
    ]

    y_position = 680
    for line in text:
        p.drawString(100, y_position, line)
        y_position -= 20

    # Agregar imagen al PDF
    if report.imagen_url:
        try:
            image = ImageReader(report.imagen_url)
            p.drawImage(image, 100, 400, width=200, height=200)
        except Exception as e:
            p.drawString(100, y_position, f"Error al cargar imagen: {str(e)}")
    
    # Pie de página
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(100, 50, "Generado por Eco-Reporte")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    # Crear el nombre del archivo usando el título y la fecha de creación
    filename = f"{report.titulo_reporte}_{report.fecha_creacion}.pdf".replace(" ", "_")

    return pdf, filename
