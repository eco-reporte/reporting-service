from fpdf import FPDF

class PDFGenerator:
    def __init__(self, title):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.title = title

    def add_title(self):
        self.pdf.set_font("Arial", 'B', size=16)
        self.pdf.cell(200, 10, txt=self.title, ln=True, align='C')
        self.pdf.ln(10)  # Line break

    def add_paragraph(self, text):
        self.pdf.set_font("Arial", size=12)
        self.pdf.multi_cell(0, 10, text)
        self.pdf.ln()

    def save_pdf(self, filename):
        self.pdf.output(filename)

# Ejemplo de uso
if __name__ == "__main__":
    pdf_gen = PDFGenerator("Reporte de Ejemplo")
    pdf_gen.add_title()
    pdf_gen.add_paragraph("Este es un ejemplo de un párrafo en el PDF.")
    pdf_gen.save_pdf("reporte_ejemplo.pdf")
