# reports/infraestructure/controllers/report_controller.py

from flask import request, jsonify, send_file
from reports.application.services.report_service import ReportService
from reports.application.services.pdf_services import create_pdf
import io
import os
from zipfile import ZipFile

class ReportController:
    def __init__(self, report_service: ReportService):
        self.report_service = report_service

    def create_report(self):
        report_data = request.form.to_dict()
        image_file = request.files['image']
        new_report = self.report_service.create_report(report_data, image_file)
        pdf, filename = create_pdf(new_report)
        return send_file(
            io.BytesIO(pdf),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    def get_all_reports(self):
        reports = self.report_service.get_all_reports()
        return jsonify([report.to_dict() for report in reports])

    def get_report(self, report_id):
        report = self.report_service.get_report_by_id(report_id)
        if report:
            return jsonify(report.to_dict())
        return jsonify({'message': 'Report not found'}), 404

    def update_report(self, report_id):
        report_data = request.json
        updated_report = self.report_service.update_report(report_id, report_data)
        if updated_report:
            return jsonify(updated_report.to_dict())
        return jsonify({'message': 'Report not found'}), 404

    def patch_report(self, report_id):
        report_data = request.json
        updated_report = self.report_service.update_report(report_id, report_data)
        if updated_report:
            return jsonify(updated_report.to_dict())
        return jsonify({'message': 'Report not found'}), 404

    def delete_report(self, report_id):
        deleted = self.report_service.delete_report(report_id)
        if deleted:
            return jsonify({'message': 'Report deleted successfully'})
        return jsonify({'message': 'Report not found'}), 404

    def get_report_pdf(self, report_id):
        report = self.report_service.get_report_by_id(report_id)
        if report and report.pdf_url:
            return send_file(report.pdf_url, 
                             mimetype='application/pdf',
                             as_attachment=True,
                             download_name=f"report_{report_id}.pdf")
        return jsonify({'message': 'PDF not found'}), 404

    def get_all_pdfs(self):
        pdfs = self.report_service.get_all_pdfs()
        return jsonify(pdfs)

    def download_all_pdfs(self):
        reports = self.report_service.get_all_reports()
        pdf_files = [report.pdf_url for report in reports if report.pdf_url and os.path.exists(report.pdf_url)]
        
        if not pdf_files:
            return jsonify({'message': 'No PDFs found'}), 404
        
        memory_file = io.BytesIO()
        with ZipFile(memory_file, 'w') as zf:
            for pdf_file in pdf_files:
                zf.write(pdf_file, os.path.basename(pdf_file))
        
        memory_file.seek(0)
        return send_file(memory_file,
                         mimetype='application/zip',
                         as_attachment=True,
                         download_name='all_reports.zip')